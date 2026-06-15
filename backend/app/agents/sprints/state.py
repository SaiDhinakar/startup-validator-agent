"""Sprints agent state schema."""

from typing import TypedDict


class SprintsState(TypedDict):
    idea: str
    budget: str
    team_size: str
    sprints: list[dict]
    milestones: list[dict]
    total_weeks: int
    reasoning: str
