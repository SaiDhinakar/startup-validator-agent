"""Engineering LangGraph definition. START → generate → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.engineering.state import EngineeringState
from app.agents.engineering.nodes import generate_node


def build_engineering_graph() -> StateGraph:
    graph = StateGraph(EngineeringState)
    graph.add_node("generate", generate_node)
    graph.add_edge(START, "generate")
    graph.add_edge("generate", END)
    return graph.compile()
