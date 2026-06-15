"""Engineering agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.engineering.prompts import ENGINEERING_SYSTEM, ENGINEERING_USER
from app.agents.engineering.state import EngineeringState


def generate_node(state: EngineeringState) -> dict:
    llm = get_llm(temperature=0.3)
    prompt = ENGINEERING_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
        timeline=state["timeline"],
    )
    response = llm.invoke([
        {"role": "system", "content": ENGINEERING_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
