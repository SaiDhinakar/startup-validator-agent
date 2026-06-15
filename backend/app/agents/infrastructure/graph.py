"""Infrastructure LangGraph definition. START → estimate → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.infrastructure.state import InfrastructureState
from app.agents.infrastructure.nodes import estimate_node


def build_infrastructure_graph() -> StateGraph:
    graph = StateGraph(InfrastructureState)
    graph.add_node("estimate", estimate_node)
    graph.add_edge(START, "estimate")
    graph.add_edge("estimate", END)
    return graph.compile()
