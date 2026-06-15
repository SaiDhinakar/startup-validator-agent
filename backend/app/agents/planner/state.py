"""Planner agent state schema."""

from typing import TypedDict


class PlannerState(TypedDict):
    idea: str
    budget: str
    team_size: str
    timeline: str
    product_output: dict
    architecture_output: dict
    engineering_output: dict
    review_output: dict
    errors: list[str]
