"""Feasibility agent state schema."""

from typing import TypedDict


class FeasibilityState(TypedDict):
    product_name: str
    product_type: str
    budget: int
    team_size: int
    timeline_months: int
    target_users: str
    plan: str
    feasibility_report: str
