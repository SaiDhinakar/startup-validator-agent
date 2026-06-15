"""Orchestrator LangGraph definition. Single-node graph: START → plan → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.orchestrator.state import OrchestratorState
from app.agents.orchestrator.nodes import plan_node


def build_orchestrator_graph() -> StateGraph:
    graph = StateGraph(OrchestratorState)
    graph.add_node("plan", plan_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", END)
    return graph.compile()
