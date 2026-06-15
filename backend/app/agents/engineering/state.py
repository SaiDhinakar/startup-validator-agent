"""Engineering agent state schema."""

from typing import TypedDict


class EngineeringState(TypedDict):
    idea: str
    budget: str
    team_size: str
    timeline: str
    database: dict
    api: dict
    sprints: dict
    hiring: dict
    reasoning: str
