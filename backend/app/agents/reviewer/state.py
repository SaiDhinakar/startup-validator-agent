"""Reviewer agent state schema."""

from typing import TypedDict


class ReviewerState(TypedDict):
    idea: str
    budget: str
    team_size: str
    timeline: str
    architecture_output: dict
    engineering_output: dict
    feasibility_score: int
    risks: list[dict]
    recommendations: list[str]
    verdict: str
    reasoning: str
