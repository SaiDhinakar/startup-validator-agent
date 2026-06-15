"""Sprints LangGraph definition. START → plan → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.sprints.state import SprintsState
from app.agents.sprints.nodes import plan_node


def build_sprints_graph() -> StateGraph:
    graph = StateGraph(SprintsState)
    graph.add_node("plan", plan_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", END)
    return graph.compile()
