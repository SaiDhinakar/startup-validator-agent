"""Hiring agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.hiring.prompts import HIRING_SYSTEM, HIRING_USER
from app.agents.hiring.state import HiringState


def plan_node(state: HiringState) -> dict:
    llm = get_llm(temperature=0.5)
    prompt = HIRING_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": HIRING_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
