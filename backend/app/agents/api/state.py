"""API spec agent state schema."""

from typing import TypedDict


class ApiSpecState(TypedDict):
    idea: str
    budget: str
    team_size: str
    endpoints: list[dict]
    schemas: list[dict]
    auth_strategy: str
    reasoning: str
