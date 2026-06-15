"""Architecture agent state schema."""

from typing import TypedDict


class ArchitectureState(TypedDict):
    idea: str
    budget: str
    team_size: str
    timeline: str
    components: list[dict]
    connections: list[dict]
    tech_stack: list[dict]
    infrastructure: dict
    reasoning: str
