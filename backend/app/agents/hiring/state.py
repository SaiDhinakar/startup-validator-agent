"""Hiring agent state schema."""

from typing import TypedDict


class HiringState(TypedDict):
    idea: str
    budget: str
    team_size: str
    roles: list[dict]
    salary_ranges: dict
    hiring_phases: list[dict]
    reasoning: str
