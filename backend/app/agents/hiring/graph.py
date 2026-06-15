"""Hiring LangGraph definition. START → plan → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.hiring.state import HiringState
from app.agents.hiring.nodes import plan_node


def build_hiring_graph() -> StateGraph:
    graph = StateGraph(HiringState)
    graph.add_node("plan", plan_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", END)
    return graph.compile()
