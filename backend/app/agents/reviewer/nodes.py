"""Reviewer agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.reviewer.prompts import REVIEWER_SYSTEM, REVIEWER_USER
from app.agents.reviewer.state import ReviewerState


def review_node(state: ReviewerState) -> dict:
    llm = get_llm(temperature=0.3)
    prompt = REVIEWER_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
        timeline=state["timeline"],
        architecture_output=state.get("architecture_output", {}),
        engineering_output=state.get("engineering_output", {}),
    )
    response = llm.invoke([
        {"role": "system", "content": REVIEWER_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
