"""Orchestrator agent graph nodes. Each node is a step in the LangGraph workflow."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.orchestrator.prompts import ORCHESTRATOR_SYSTEM, PLAN_USER
from app.agents.orchestrator.state import OrchestratorState


def plan_node(state: OrchestratorState) -> dict:
    llm = get_llm(temperature=0.5)
    prompt = PLAN_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": ORCHESTRATOR_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"plan": response.content}
