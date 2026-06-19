"""Market LangGraph definition. START → market → END."""

from langgraph.graph import END, START, StateGraph

from app.agents.market.nodes import market_node
from app.agents.market.state import MarketState


def build_market_graph() -> StateGraph:
    graph = StateGraph(MarketState)
    graph.add_node("market", market_node)
    graph.add_edge(START, "market")
    graph.add_edge("market", END)
    return graph.compile()
