"""Strategy CRUD and generation endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from app.api.routes.strategies.schemas import (
    StrategyCreate,
    StrategyResponse,
    StrategyListResponse,
    GenerateRequest,
)
from app.api.deps import get_strategy_repo
from app.db.repositories.strategy import StrategyRepository

router = APIRouter(prefix="/strategies", tags=["strategies"])


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


@router.post("/{strategy_id}/generate", response_model=StrategyResponse)
async def generate_strategy(
    strategy_id: str,
    data: GenerateRequest = GenerateRequest(),
    repo: StrategyRepository = Depends(get_strategy_repo),
):
    doc = await repo.get_by_id(strategy_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Strategy not found")

    agent_input = {
        "idea": doc.idea,
        "budget": doc.budget,
        "team_size": doc.team_size,
        "timeline": doc.timeline,
    }

    updates = {}

    if "planner" in data.agents:
        from app.agents.planner.nodes import plan_node
        result = plan_node({**agent_input, "plan": "", "product_output": {}, "architecture_output": {}, "engineering_output": {}, "review_output": {}, "errors": []})
        updates["planner"] = result

    if "product" in data.agents:
        from app.agents.product.nodes import analyze_node
        result = analyze_node({**agent_input, "target_users": [], "core_features": [], "user_flows": [], "business_rules": [], "mvp_scope": {}, "reasoning": ""})
        updates["product"] = result

    if "architecture" in data.agents:
        from app.agents.architecture.nodes import design_node
        result = design_node({**agent_input, "components": [], "connections": [], "tech_stack": [], "infrastructure": {}, "reasoning": ""})
        updates["architecture"] = result

    if "engineering" in data.agents:
        from app.agents.engineering.nodes import generate_node
        result = generate_node({**agent_input, "database": {}, "api": {}, "sprints": {}, "hiring": {}, "reasoning": ""})
        updates["engineering"] = result

    if "reviewer" in data.agents:
        from app.agents.reviewer.nodes import review_node
        result = review_node({
            **agent_input,
            "architecture_output": updates.get("architecture", {}),
            "engineering_output": updates.get("engineering", {}),
            "feasibility_score": 0,
            "risks": [],
            "recommendations": [],
            "verdict": "",
            "reasoning": "",
        })
        updates["reviewer"] = result

    updated = await repo.update(strategy_id, updates)
    return updated
