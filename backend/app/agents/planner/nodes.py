"""Planner agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.planner.prompts import PLANNER_SYSTEM, PLANNER_USER
from app.agents.planner.state import PlannerState


def plan_node(state: PlannerState) -> dict:
    llm = get_llm(temperature=0.4)
    prompt = PLANNER_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
        timeline=state["timeline"],
    )
    response = llm.invoke([
        {"role": "system", "content": PLANNER_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"plan": response.content}
