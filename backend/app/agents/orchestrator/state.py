"""Orchestrator agent state schema."""

from typing import TypedDict


class OrchestratorState(TypedDict):
    idea: str
    budget: str
    team_size: str
    architecture: dict
    database: dict
    api: dict
    infrastructure: dict
    sprints: dict
    hiring: dict
    errors: list[str]
