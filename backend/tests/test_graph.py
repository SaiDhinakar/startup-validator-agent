"""Tests for LangGraph graph compilation and execution."""

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


class TestGraphCompilation:
    def test_planner_graph_compiles(self):
        from app.agents.planner.graph import build_planner_graph
        graph = build_planner_graph()
        assert graph is not None

    def test_product_graph_compiles(self):
        from app.agents.product.graph import build_product_graph
        graph = build_product_graph()
        assert graph is not None

    def test_architecture_graph_compiles(self):
        from app.agents.architecture.graph import build_architecture_graph
        graph = build_architecture_graph()
        assert graph is not None

    def test_engineering_graph_compiles(self):
        from app.agents.engineering.graph import build_engineering_graph
        graph = build_engineering_graph()
        assert graph is not None

    def test_reviewer_graph_compiles(self):
        from app.agents.reviewer.graph import build_reviewer_graph
        graph = build_reviewer_graph()
        assert graph is not None


class TestGraphExecution:
    def test_planner_graph_runs(self):
        with patch("app.agents.planner.nodes.get_llm", return_value=_make_mock_llm("planner")):
            from app.agents.planner.graph import build_planner_graph
            graph = build_planner_graph()
            result = graph.invoke({
                **MOCK_INPUT,
                "plan": "",
                "product_output": {},
                "architecture_output": {},
                "engineering_output": {},
                "review_output": {},
                "errors": [],
            })
            assert "plan" in result

    def test_product_graph_runs(self):
        with patch("app.agents.product.nodes.get_llm", return_value=_make_mock_llm("product")):
            from app.agents.product.graph import build_product_graph
            graph = build_product_graph()
            result = graph.invoke({
                **MOCK_INPUT,
                "target_users": [],
                "core_features": [],
                "user_flows": [],
                "business_rules": [],
                "mvp_scope": {},
                "reasoning": "",
            })
            assert "reasoning" in result

    def test_architecture_graph_runs(self):
        with patch("app.agents.architecture.nodes.get_llm", return_value=_make_mock_llm("architecture")):
            from app.agents.architecture.graph import build_architecture_graph
            graph = build_architecture_graph()
            result = graph.invoke({
                **MOCK_INPUT,
                "components": [],
                "connections": [],
                "tech_stack": [],
                "infrastructure": {},
                "reasoning": "",
            })
            assert "reasoning" in result

    def test_engineering_graph_runs(self):
        with patch("app.agents.engineering.nodes.get_llm", return_value=_make_mock_llm("engineering")):
            from app.agents.engineering.graph import build_engineering_graph
            graph = build_engineering_graph()
            result = graph.invoke({
                **MOCK_INPUT,
                "database": {},
                "api": {},
                "sprints": {},
                "hiring": {},
                "reasoning": "",
            })
            assert "reasoning" in result

    def test_reviewer_graph_runs(self):
        with patch("app.agents.reviewer.nodes.get_llm", return_value=_make_mock_llm("reviewer")):
            from app.agents.reviewer.graph import build_reviewer_graph
            graph = build_reviewer_graph()
            result = graph.invoke({
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
