"""Architecture agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.architecture.prompts import ARCHITECTURE_SYSTEM, ARCHITECTURE_USER
from app.agents.architecture.state import ArchitectureState


def design_node(state: ArchitectureState) -> dict:
    llm = get_llm(temperature=0.4)
    prompt = ARCHITECTURE_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": ARCHITECTURE_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
