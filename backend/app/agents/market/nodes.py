"""Market agent — LLM decides what to search."""

from typing import Callable

from app.agents.market.prompts import MARKET_SYSTEM, MARKET_USER
from app.agents.market.state import MarketState
from app.core.agent_runner import run_agent
from app.core.llm import get_llm
from app.tools import search_web, search_reddit, search_trends


def market_node(state: MarketState, on_event: Callable | None = None) -> dict:
    idea = state.get("product_name") or state.get("idea", "")
    prompt = MARKET_USER.format(
        idea=idea,
        plan=state.get("plan", "")[:500],
    )
    response = run_agent(
        llm=get_llm(temperature=0.4),
        system_prompt=MARKET_SYSTEM,
        user_prompt=prompt,
        tools=[search_web, search_reddit, search_trends],
        on_event=on_event,
    )
    return {"market_analysis": response}
