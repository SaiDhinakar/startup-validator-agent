"""Reviewer LangGraph definition. START → review → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.reviewer.state import ReviewerState
from app.agents.reviewer.nodes import review_node


def build_reviewer_graph() -> StateGraph:
    graph = StateGraph(ReviewerState)
    graph.add_node("review", review_node)
    graph.add_edge(START, "review")
    graph.add_edge("review", END)
    return graph.compile()
