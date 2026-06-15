"""Product agent state schema."""

from typing import TypedDict


class ProductState(TypedDict):
    idea: str
    budget: str
    team_size: str
    timeline: str
    target_users: list[str]
    core_features: list[dict]
    user_flows: list[dict]
    business_rules: list[str]
    mvp_scope: dict
    reasoning: str
