"""Growth agent — LLM decides what to search."""

from typing import Callable

from app.agents.growth.prompts import GROWTH_SYSTEM, GROWTH_USER
from app.agents.growth.state import GrowthState
from app.core.agent_runner import run_agent
from app.core.llm import get_llm
from app.tools import search_web


def growth_node(state: GrowthState, on_event: Callable | None = None) -> dict:
    idea = state.get("product_name") or state.get("idea", "")
    prompt = GROWTH_USER.format(
        idea=idea,
        plan=state.get("plan", "")[:500],
        market_analysis=state.get("market_analysis", "")[:500],
    )
    response = run_agent(
        llm=get_llm(temperature=0.4),
        system_prompt=GROWTH_SYSTEM,
        user_prompt=prompt,
        tools=[search_web],
        on_event=on_event,
    )
    return {"growth_strategy": response}
