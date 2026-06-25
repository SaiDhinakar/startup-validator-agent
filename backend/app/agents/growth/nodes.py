"""Growth agent — LLM decides what to search."""

import logging
from typing import Callable

from app.agents.growth.prompts import GROWTH_SYSTEM, GROWTH_USER
from app.agents.growth.state import GrowthState
from app.core.agent_runner import run_agent
from app.core.llm import get_llm
from app.tools import search_web

logger = logging.getLogger(__name__)


def growth_node(state: GrowthState, on_event: Callable | None = None) -> dict:
    idea = state.get("product_name") or state.get("idea", "")
    logger.info("Growth node starting for: %s", idea[:60])
    prompt = GROWTH_USER.format(
        idea=idea,
        plan=state.get("plan", "")[:500],
        market_analysis=state.get("market_analysis", "")[:500],
    )
    previous_output = state.get("growth_strategy", "")
    response = run_agent(
        llm=get_llm(temperature=0.4),
        system_prompt=GROWTH_SYSTEM,
        user_prompt=prompt,
        tools=[search_web],
        on_event=on_event,
        previous_output=previous_output,
    )
    logger.info("Growth node complete for: %s", idea[:60])
    return {"growth_strategy": response}
