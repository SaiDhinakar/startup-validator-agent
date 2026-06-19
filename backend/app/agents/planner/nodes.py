"""Planner agent — LLM decides what to search and which agents to run."""

from typing import Callable

from app.agents.planner.prompts import PLANNER_SYSTEM, PLANNER_USER, PLANNER_USER_CTO, parse_selected_agents
from app.agents.planner.state import PlannerState
from app.core.agent_runner import run_agent
from app.core.llm import get_llm
from app.tools import search_web


def plan_node(state: PlannerState, on_event: Callable | None = None) -> dict:
    product_name = state.get("product_name", "")
    idea = product_name or state.get("idea", "")

    if product_name:
        prompt = PLANNER_USER_CTO.format(
            product_name=product_name,
            product_type=state.get("product_type", ""),
            budget=state["budget"],
            team_size=state["team_size"],
            timeline_months=state.get("timeline_months", 0),
            target_users=state.get("target_users", ""),
        )
    else:
        prompt = PLANNER_USER.format(
            idea=state["idea"],
            budget=state["budget"],
            team_size=state["team_size"],
            timeline=state["timeline"],
        )

    response = run_agent(
        llm=get_llm(temperature=0.4),
        system_prompt=PLANNER_SYSTEM,
        user_prompt=prompt,
        tools=[search_web],
        on_event=on_event,
    )

    selected = parse_selected_agents(response)
    return {"plan": response, "selected_agents": selected}
