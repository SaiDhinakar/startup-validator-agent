"""Growth agent state schema."""

from typing import TypedDict


class GrowthState(TypedDict):
    product_name: str
    product_type: str
    budget: int
    team_size: int
    timeline_months: int
    target_users: str
    plan: str
    market_analysis: str
    growth_strategy: str
