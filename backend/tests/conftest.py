"""Shared test fixtures and mock data."""

from unittest.mock import MagicMock, patch

import pytest

MOCK_INPUT = {
    "idea": "Build an Uber clone for grocery delivery",
    "budget": "₹10,00,000",
    "team_size": "5",
    "timeline": "3 months",
}


class MockLLMResponse:
    def __init__(self, content: str):
        self.content = content
        self.tool_calls = []


@pytest.fixture
def mock_input():
    return MOCK_INPUT.copy()


@pytest.fixture
def mock_llm():
    with patch("app.core.llm.get_llm") as mock:
        llm_instance = MagicMock()
        mock.return_value = llm_instance
        yield llm_instance
