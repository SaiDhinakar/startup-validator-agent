"""Hiring agent state schema."""

from typing import TypedDict


class HiringState(TypedDict):
    product_name: str
    product_type: str
    budget: int
    team_size: int
    timeline_months: int
    target_users: str
    plan: str
    hiring_plan: str
