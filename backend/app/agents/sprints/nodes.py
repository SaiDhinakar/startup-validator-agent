"""Sprints agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.sprints.prompts import SPRINTS_SYSTEM, SPRINTS_USER
from app.agents.sprints.state import SprintsState


def plan_node(state: SprintsState) -> dict:
    llm = get_llm(temperature=0.4)
    prompt = SPRINTS_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": SPRINTS_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
