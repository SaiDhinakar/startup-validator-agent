"""Planner LangGraph definition. START → plan → END."""

from langgraph.graph import END, START, StateGraph

from app.agents.planner.nodes import plan_node
from app.agents.planner.state import PlannerState


def build_planner_graph() -> StateGraph:
    graph = StateGraph(PlannerState)
    graph.add_node("plan", plan_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", END)
    return graph.compile()
