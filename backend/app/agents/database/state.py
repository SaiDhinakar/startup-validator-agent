"""Database agent state schema."""

from typing import TypedDict


class DatabaseState(TypedDict):
    idea: str
    budget: str
    team_size: str
    tables: list[dict]
    relationships: list[dict]
    indexes: list[dict]
    reasoning: str
