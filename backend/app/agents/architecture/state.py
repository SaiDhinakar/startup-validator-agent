"""Architecture agent state schema."""

from typing import TypedDict


class ArchitectureState(TypedDict):
    idea: str
    budget: str
    team_size: str
    components: list[dict]
    connections: list[dict]
    tech_choices: list[dict]
    reasoning: str
