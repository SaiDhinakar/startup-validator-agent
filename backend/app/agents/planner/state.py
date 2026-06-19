"""Planner agent state schema."""

from typing import TypedDict


class PlannerState(TypedDict):
    idea: str
    budget: str
    team_size: str
    timeline: str
    product_name: str
    product_type: str
    timeline_months: int
    target_users: str
    plan: str
