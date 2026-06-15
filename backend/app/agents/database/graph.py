"""Database LangGraph definition. START → design → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.database.state import DatabaseState
from app.agents.database.nodes import design_node


def build_database_graph() -> StateGraph:
    graph = StateGraph(DatabaseState)
    graph.add_node("design", design_node)
    graph.add_edge(START, "design")
    graph.add_edge("design", END)
    return graph.compile()
