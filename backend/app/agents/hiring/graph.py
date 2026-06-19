"""Hiring LangGraph definition. START → hiring → END."""

from langgraph.graph import END, START, StateGraph

from app.agents.hiring.nodes import hiring_node
from app.agents.hiring.state import HiringState


def build_hiring_graph() -> StateGraph:
    graph = StateGraph(HiringState)
    graph.add_node("hiring", hiring_node)
    graph.add_edge(START, "hiring")
    graph.add_edge("hiring", END)
    return graph.compile()
