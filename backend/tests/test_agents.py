"""Tests for individual agent nodes with mocked LLM."""

from unittest.mock import MagicMock, patch

from tests.conftest import MockLLMResponse
from tests.mock_data import MOCK_RESPONSES

MOCK_CTO_INPUT = {
    "product_name": "Uber Clone",
    "product_type": "Mobile App",
    "budget": 1000000,
    "team_size": 5,
    "timeline_months": 6,
    "target_users": "Urban commuters",
}


def _make_mock_llm(response_key: str):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MockLLMResponse(MOCK_RESPONSES[response_key])
    return mock_llm


class TestPlannerAgent:
    def test_plan_node_returns_plan(self):
        with patch(
            "app.agents.planner.nodes.get_llm",
            return_value=_make_mock_llm("planner"),
        ):
            from app.agents.planner.nodes import plan_node

            state = {**MOCK_CTO_INPUT, "plan": ""}
            result = plan_node(state)
            assert "plan" in result
            assert len(result["plan"]) > 0

    def test_plan_node_receives_correct_prompt(self):
        mock_llm = _make_mock_llm("planner")
        with patch(
            "app.agents.planner.nodes.get_llm", return_value=mock_llm
        ):
            from app.agents.planner.nodes import plan_node

            state = {**MOCK_CTO_INPUT, "plan": ""}
            plan_node(state)
            call_args = mock_llm.invoke.call_args[0][0]
            user_msg = [m for m in call_args if hasattr(m, "content")][0]
            assert "Uber Clone" in user_msg.content


class TestReviewerAgent:
    def test_review_valid_output(self):
        with patch(
            "app.agents.reviewer.nodes.get_llm",
            return_value=_make_mock_llm("reviewer_valid"),
        ):
            from app.agents.reviewer.nodes import review_agent_output

            result = review_agent_output(
                idea="Test idea",
                agent_name="planner",
                agent_output="<h1>Test Plan</h1>",
                context=MOCK_CTO_INPUT,
            )
            assert result["valid"] is True

    def test_review_invalid_output(self):
        with patch(
            "app.agents.reviewer.nodes.get_llm",
            return_value=_make_mock_llm("reviewer_invalid"),
        ):
            from app.agents.reviewer.nodes import review_agent_output

            result = review_agent_output(
                idea="Test idea",
                agent_name="planner",
                agent_output="<h1>Generic content</h1>",
                context=MOCK_CTO_INPUT,
            )
            assert result["valid"] is False
            assert "fabricated" in result["reason"].lower()


class TestFeasibilityAgent:
    def test_feasibility_node_returns_report(self):
        with patch(
            "app.agents.feasibility.nodes.get_llm",
            return_value=_make_mock_llm("feasibility"),
        ):
            from app.agents.feasibility.nodes import feasibility_node

            state = {**MOCK_CTO_INPUT, "plan": "Test plan", "feasibility_report": ""}
            result = feasibility_node(state)
            assert "feasibility_report" in result
            assert len(result["feasibility_report"]) > 0


class TestMarketAgent:
    def test_market_node_returns_analysis(self):
        with patch(
            "app.agents.market.nodes.get_llm",
            return_value=_make_mock_llm("market"),
        ):
            from app.agents.market.nodes import market_node

            state = {**MOCK_CTO_INPUT, "plan": "Test plan", "market_analysis": ""}
            result = market_node(state)
            assert "market_analysis" in result
            assert len(result["market_analysis"]) > 0


class TestGrowthAgent:
    def test_growth_node_returns_strategy(self):
        with patch(
            "app.agents.growth.nodes.get_llm",
            return_value=_make_mock_llm("growth"),
        ):
            from app.agents.growth.nodes import growth_node

            state = {
                **MOCK_CTO_INPUT,
                "plan": "Test plan",
                "market_analysis": "Test market",
                "growth_strategy": "",
            }
            result = growth_node(state)
            assert "growth_strategy" in result
            assert len(result["growth_strategy"]) > 0


class TestHiringAgent:
    def test_hiring_node_returns_plan(self):
        with patch(
            "app.agents.hiring.nodes.get_llm",
            return_value=_make_mock_llm("hiring"),
        ):
            from app.agents.hiring.nodes import hiring_node

            state = {**MOCK_CTO_INPUT, "plan": "Test plan", "hiring_plan": ""}
            result = hiring_node(state)
            assert "hiring_plan" in result
            assert len(result["hiring_plan"]) > 0
