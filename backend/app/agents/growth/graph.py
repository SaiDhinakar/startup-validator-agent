"""Growth LangGraph definition. START → growth → END."""

from langgraph.graph import END, START, StateGraph

from app.agents.growth.nodes import growth_node
from app.agents.growth.state import GrowthState


def build_growth_graph() -> StateGraph:
    graph = StateGraph(GrowthState)
    graph.add_node("growth", growth_node)
    graph.add_edge(START, "growth")
    graph.add_edge("growth", END)
    return graph.compile()
