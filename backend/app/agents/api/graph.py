"""API spec LangGraph definition. START → design → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.api.state import ApiSpecState
from app.agents.api.nodes import design_node


def build_api_graph() -> StateGraph:
    graph = StateGraph(ApiSpecState)
    graph.add_node("design", design_node)
    graph.add_edge(START, "design")
    graph.add_edge("design", END)
    return graph.compile()
