"""Hiring agent — LLM decides what to search."""

import logging
from typing import Callable

from app.agents.hiring.prompts import HIRING_SYSTEM, HIRING_USER
from app.agents.hiring.state import HiringState
from app.core.agent_runner import run_agent
from app.core.llm import get_llm
from app.tools import search_web

logger = logging.getLogger(__name__)


def hiring_node(state: HiringState, on_event: Callable | None = None) -> dict:
    idea = state.get("product_name") or state.get("idea", "")
    logger.info("Hiring node starting for: %s", idea[:60])
    prompt = HIRING_USER.format(
        idea=idea,
        budget=state.get("budget", "Not specified"),
        team_size=state.get("team_size", "Not specified"),
        timeline_months=state.get("timeline_months", 0),
        plan=state.get("plan", "")[:500],
    )
    previous_output = state.get("hiring_plan", "")
    response = run_agent(
        llm=get_llm(temperature=0.4),
        system_prompt=HIRING_SYSTEM,
        user_prompt=prompt,
        tools=[search_web],
        on_event=on_event,
        previous_output=previous_output,
    )
    logger.info("Hiring node complete for: %s", idea[:60])
    return {"hiring_plan": response}
