"""Reviewer agent state schema."""

from typing import TypedDict


class ReviewerState(TypedDict):
    idea: str
    agent_name: str
    agent_output: str
    valid: bool
    reason: str
