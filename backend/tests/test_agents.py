"""Tests for individual agent nodes with mocked LLM."""

from unittest.mock import patch, MagicMock

from tests.mock_data import MOCK_RESPONSES
from tests.conftest import MockLLMResponse


MOCK_INPUT = {
    "idea": "Build an Uber clone for grocery delivery",
    "budget": "₹10,00,000",
    "team_size": "5",
    "timeline": "3 months",
}


def _make_mock_llm(response_key: str):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MockLLMResponse(MOCK_RESPONSES[response_key])
    return mock_llm


class TestPlannerAgent:
    def test_plan_node_returns_plan(self):
        with patch("app.agents.planner.nodes.get_llm", return_value=_make_mock_llm("planner")):
            from app.agents.planner.nodes import plan_node

            result = plan_node({**MOCK_INPUT, "product_output": {}, "architecture_output": {}, "engineering_output": {}, "review_output": {}, "errors": []})
            assert "plan" in result
            assert "domains" in result["plan"]

    def test_plan_node_receives_correct_prompt(self):
        mock_llm = _make_mock_llm("planner")
        with patch("app.agents.planner.nodes.get_llm", return_value=mock_llm):
            from app.agents.planner.nodes import plan_node

            plan_node({**MOCK_INPUT, "product_output": {}, "architecture_output": {}, "engineering_output": {}, "review_output": {}, "errors": []})
            call_args = mock_llm.invoke.call_args[0][0]
            user_msg = [m for m in call_args if hasattr(m, "content") and "Build an Uber clone" in m.content][0]
            assert "Build an Uber clone" in user_msg.content


class TestProductAgent:
    def test_analyze_node_returns_reasoning(self):
        with patch("app.agents.product.nodes.get_llm", return_value=_make_mock_llm("product")):
            from app.agents.product.nodes import analyze_node

            result = analyze_node({**MOCK_INPUT, "target_users": [], "core_features": [], "user_flows": [], "business_rules": [], "mvp_scope": {}, "reasoning": ""})
            assert "reasoning" in result
            assert "target_users" in result["reasoning"]


class TestArchitectureAgent:
    def test_design_node_returns_reasoning(self):
        with patch("app.agents.architecture.nodes.get_llm", return_value=_make_mock_llm("architecture")):
            from app.agents.architecture.nodes import design_node

            result = design_node({**MOCK_INPUT, "components": [], "connections": [], "tech_stack": [], "infrastructure": {}, "reasoning": ""})
            assert "reasoning" in result
            assert "components" in result["reasoning"]


class TestEngineeringAgent:
    def test_generate_node_returns_reasoning(self):
        with patch("app.agents.engineering.nodes.get_llm", return_value=_make_mock_llm("engineering")):
            from app.agents.engineering.nodes import generate_node

            result = generate_node({**MOCK_INPUT, "database": {}, "api": {}, "sprints": {}, "hiring": {}, "reasoning": ""})
            assert "reasoning" in result
            assert "database" in result["reasoning"]


class TestReviewerAgent:
    def test_review_node_returns_reasoning(self):
        with patch("app.agents.reviewer.nodes.get_llm", return_value=_make_mock_llm("reviewer")):
            from app.agents.reviewer.nodes import review_node

            result = review_node({
                **MOCK_INPUT,
                "architecture_output": {},
                "engineering_output": {},
                "feasibility_score": 0,
                "risks": [],
                "recommendations": [],
                "verdict": "",
                "reasoning": "",
            })
            assert "reasoning" in result
            assert "feasibility_score" in result["reasoning"]
