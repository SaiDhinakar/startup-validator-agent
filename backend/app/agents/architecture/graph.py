"""Architecture LangGraph definition. START → design → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.architecture.state import ArchitectureState
from app.agents.architecture.nodes import design_node


def build_architecture_graph() -> StateGraph:
    graph = StateGraph(ArchitectureState)
    graph.add_node("design", design_node)
    graph.add_edge(START, "design")
    graph.add_edge("design", END)
    return graph.compile()
