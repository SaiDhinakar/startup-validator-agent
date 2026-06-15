"""Infrastructure agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.infrastructure.prompts import INFRA_SYSTEM, INFRA_USER
from app.agents.infrastructure.state import InfrastructureState


def estimate_node(state: InfrastructureState) -> dict:
    llm = get_llm(temperature=0.4)
    prompt = INFRA_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": INFRA_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
