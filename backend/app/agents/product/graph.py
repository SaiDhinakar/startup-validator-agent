"""Product LangGraph definition. START → analyze → END."""

from langgraph.graph import StateGraph, START, END

from app.agents.product.state import ProductState
from app.agents.product.nodes import analyze_node


def build_product_graph() -> StateGraph:
    graph = StateGraph(ProductState)
    graph.add_node("analyze", analyze_node)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", END)
    return graph.compile()
