"""Database agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.database.prompts import DATABASE_SYSTEM, DATABASE_USER
from app.agents.database.state import DatabaseState


def design_node(state: DatabaseState) -> dict:
    llm = get_llm(temperature=0.3)
    prompt = DATABASE_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": DATABASE_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
