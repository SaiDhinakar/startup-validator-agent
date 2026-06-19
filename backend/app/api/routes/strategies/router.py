"""Strategy CRUD and generation endpoints."""

import asyncio
import json
import queue

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.api.deps import get_strategy_repo
from app.api.routes.strategies.schemas import (
    GenerateCTORequest,
    StrategyCreate,
    StrategyListResponse,
    StrategyResponse,
)
from app.db.repositories.strategy import StrategyRepository

router = APIRouter(prefix="/strategies", tags=["strategies"])

MAX_RETRIES = 1

REVIEW_TARGETS = {
    "planner": "plan",
    "feasibility": "feasibility_report",
    "market": "market_analysis",
    "growth": "growth_strategy",
    "hiring": "hiring_plan",
}

SKIP_REASONS = {
    "planner": "Planning output could not be validated. Proceeding with best-effort plan.",
    "feasibility": "Feasibility analysis could not be validated. Very low feasibility in this area.",
    "market": "Market analysis could not be validated. Insufficient or unreliable market data.",
    "growth": "Growth strategy could not be validated. Projections not grounded in realistic assumptions.",
    "hiring": "Hiring plan could not be validated. Requirements may not align with scope or budget.",
}


@router.post("", response_model=StrategyResponse, status_code=201)
async def create_strategy(
    data: StrategyCreate,
    repo: StrategyRepository = Depends(get_strategy_repo),
):
    doc = await repo.create(data.model_dump())
    return doc


@router.get("", response_model=StrategyListResponse)
async def list_strategies(
    limit: int = 50,
    skip: int = 0,
    repo: StrategyRepository = Depends(get_strategy_repo),
):
    docs = await repo.list_all(limit=limit, skip=skip)
    strategies = []
    for d in docs:
        data = d.model_dump(by_alias=True)
        data["id"] = str(d.id)
        strategies.append(StrategyResponse(**data))
    return StrategyListResponse(strategies=strategies, total=len(strategies))


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: str,
    repo: StrategyRepository = Depends(get_strategy_repo),
):
    doc = await repo.get_by_id(strategy_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return doc


@router.delete("/{strategy_id}", status_code=204)
async def delete_strategy(
    strategy_id: str,
    repo: StrategyRepository = Depends(get_strategy_repo),
):
    deleted = await repo.delete(strategy_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Strategy not found")


@router.post("/{strategy_id}/generate-cto")
async def generate_cto_strategy(
    strategy_id: str,
    data: GenerateCTORequest = GenerateCTORequest(),
    repo: StrategyRepository = Depends(get_strategy_repo),
):
    doc = await repo.get_by_id(strategy_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Strategy not found")

    async def stream():
        from app.agents.planner.nodes import plan_node
        from app.agents.feasibility.nodes import feasibility_node
        from app.agents.market.nodes import market_node
        from app.agents.growth.nodes import growth_node
        from app.agents.hiring.nodes import hiring_node
        from app.agents.reviewer.nodes import review_agent_output

        state = {
            "product_name": doc.product_name or doc.idea,
            "product_type": doc.product_type,
            "budget": doc.budget,
            "team_size": doc.team_size,
            "timeline_months": doc.timeline_months,
            "target_users": doc.target_users,
            "plan": "",
            "feasibility_report": "",
            "market_analysis": "",
            "growth_strategy": "",
            "hiring_plan": "",
        }

        node_map = {
            "planner": plan_node,
            "feasibility": feasibility_node,
            "market": market_node,
            "growth": growth_node,
            "hiring": hiring_node,
        }

        # Phase 1: Run planner to decide which agents are needed
        yield sse("agent_start", {"agent": "planner"})

        eq: queue.Queue = queue.Queue()

        def on_event(event_type, data, q=eq):
            q.put((event_type, data))

        def run_planner():
            return plan_node(state, on_event=on_event)

        thread = asyncio.get_event_loop().run_in_executor(None, run_planner)

        while not thread.done():
            try:
                evt_type, evt_data = eq.get_nowait()
                yield sse(evt_type, evt_data)
            except queue.Empty:
                pass
            await asyncio.sleep(0.1)

        result = thread.result()
        while not eq.empty():
            evt_type, evt_data = eq.get_nowait()
            yield sse(evt_type, evt_data)

        state.update(result)
        selected_agents = result.get("selected_agents", ["feasibility", "market", "growth", "hiring"])

        yield sse("agents_selected", {"agents": selected_agents})

        # Review planner output
        yield sse("review_start", {"agent": "planner"})
        review = await asyncio.to_thread(
            review_agent_output,
            idea=doc.idea,
            agent_name="planner",
            agent_output=state.get("plan", ""),
            context=state,
        )
        yield sse("review_done", {"agent": "planner", "valid": review["valid"]})

        if not review["valid"]:
            for attempt in range(1, MAX_RETRIES + 1):
                yield sse("agent_retry", {"agent": "planner", "attempt": attempt})
                eq2: queue.Queue = queue.Queue()

                def on_retry(event_type, data, q=eq2):
                    q.put((event_type, data))

                retry_thread = asyncio.get_event_loop().run_in_executor(
                    None, lambda: plan_node(state, on_event=on_retry)
                )
                while not retry_thread.done():
                    try:
                        yield sse(*eq2.get_nowait())
                    except queue.Empty:
                        pass
                    await asyncio.sleep(0.1)

                retry_result = retry_thread.result()
                while not eq2.empty():
                    yield sse(*eq2.get_nowait())

                state.update(retry_result)
                selected_agents = retry_result.get("selected_agents", selected_agents)

                yield sse("review_start", {"agent": "planner"})
                review = await asyncio.to_thread(
                    review_agent_output, idea=doc.idea, agent_name="planner",
                    agent_output=state.get("plan", ""), context=state,
                )
                yield sse("review_done", {"agent": "planner", "valid": review["valid"]})
                if review["valid"]:
                    break

            if not review["valid"]:
                yield sse("agent_skipped", {"agent": "planner", "reason": SKIP_REASONS["planner"]})

        yield sse("agent_done", {"agent": "planner"})

        # Phase 2: Run only selected downstream agents
        for agent_name in selected_agents:
            yield sse("agent_start", {"agent": agent_name})

            node_fn = node_map[agent_name]
            output_key = REVIEW_TARGETS[agent_name]

            eq3: queue.Queue = queue.Queue()

            def on_agent_event(event_type, data, q=eq3):
                q.put((event_type, data))

            def run_agent():
                return node_fn(state, on_event=on_agent_event)

            agent_thread = asyncio.get_event_loop().run_in_executor(None, run_agent)

            while not agent_thread.done():
                try:
                    yield sse(*eq3.get_nowait())
                except queue.Empty:
                    pass
                await asyncio.sleep(0.1)

            agent_result = agent_thread.result()
            while not eq3.empty():
                yield sse(*eq3.get_nowait())

            state.update(agent_result)

            yield sse("review_start", {"agent": agent_name})
            agent_output = agent_result.get(output_key, "")
            review = await asyncio.to_thread(
                review_agent_output, idea=doc.idea, agent_name=agent_name,
                agent_output=agent_output, context=state,
            )
            yield sse("review_done", {"agent": agent_name, "valid": review["valid"]})

            if not review["valid"]:
                for attempt in range(1, MAX_RETRIES + 1):
                    yield sse("agent_retry", {"agent": agent_name, "attempt": attempt})
                    eq4: queue.Queue = queue.Queue()

                    def on_retry_agent(event_type, data, q=eq4):
                        q.put((event_type, data))

                    retry_thread = asyncio.get_event_loop().run_in_executor(
                        None, lambda: node_fn(state, on_event=on_retry_agent)
                    )
                    while not retry_thread.done():
                        try:
                            yield sse(*eq4.get_nowait())
                        except queue.Empty:
                            pass
                        await asyncio.sleep(0.1)

                    retry_result = retry_thread.result()
                    while not eq4.empty():
                        yield sse(*eq4.get_nowait())

                    state.update(retry_result)

                    yield sse("review_start", {"agent": agent_name})
                    agent_output = retry_result.get(output_key, "")
                    review = await asyncio.to_thread(
                        review_agent_output, idea=doc.idea, agent_name=agent_name,
                        agent_output=agent_output, context=state,
                    )
                    yield sse("review_done", {"agent": agent_name, "valid": review["valid"]})
                    if review["valid"]:
                        break

                if not review["valid"]:
                    fail_reason = review.get("reason") or SKIP_REASONS[agent_name]
                    state[output_key] = (
                        f'<div class="agent-failure">'
                        f"<p><strong>Analysis could not be completed</strong></p>"
                        f"<p>{fail_reason}</p>"
                        f"</div>"
                    )
                    yield sse("agent_skipped", {"agent": agent_name, "reason": fail_reason})

            yield sse("agent_done", {"agent": agent_name})

        updates = {
            "selected_agents": selected_agents,
            "planner": {"plan": state["plan"]},
            "feasibility_report": {"report": state["feasibility_report"]},
            "market_analysis": {"analysis": state["market_analysis"]},
            "growth_strategy": {"strategy": state["growth_strategy"]},
            "hiring_plan": {"plan": state["hiring_plan"]},
        }
        updated = await repo.update(strategy_id, updates)

        final = {
            "id": updated.id,
            "idea": updated.idea,
            "budget": updated.budget,
            "team_size": updated.team_size,
            "timeline": updated.timeline,
            "created_at": str(updated.created_at),
            "selected_agents": selected_agents,
            "planner": updated.planner,
            "feasibility_report": updated.feasibility_report,
            "market_analysis": updated.market_analysis,
            "growth_strategy": updated.growth_strategy,
            "hiring_plan": updated.hiring_plan,
        }
        yield sse("done", final)

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


def sse(event: str, data: dict) -> bytes:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n".encode()
