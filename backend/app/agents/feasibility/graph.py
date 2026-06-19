"""Feasibility LangGraph definition. START → feasibility → END."""

from langgraph.graph import END, START, StateGraph

from app.agents.feasibility.nodes import feasibility_node
from app.agents.feasibility.state import FeasibilityState


def build_feasibility_graph() -> StateGraph:
    graph = StateGraph(FeasibilityState)
    graph.add_node("feasibility", feasibility_node)
    graph.add_edge(START, "feasibility")
    graph.add_edge("feasibility", END)
    return graph.compile()
