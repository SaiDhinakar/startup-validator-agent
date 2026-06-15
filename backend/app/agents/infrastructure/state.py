"""Infrastructure agent state schema."""

from typing import TypedDict


class InfrastructureState(TypedDict):
    idea: str
    budget: str
    team_size: str
    services: list[dict]
    cost_estimate: dict
    providers: list[str]
    scaling_strategy: str
    reasoning: str
