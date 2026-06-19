"""Tests for LangGraph graph compilation and execution."""

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
    "plan": "",
    "feasibility_report": "",
    "market_analysis": "",
    "growth_strategy": "",
    "hiring_plan": "",
}


def _make_mock_llm(response_key: str):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MockLLMResponse(MOCK_RESPONSES[response_key])
    return mock_llm


class TestGraphCompilation:
    def test_planner_graph_compiles(self):
        from app.agents.planner.graph import build_planner_graph

        assert build_planner_graph() is not None

    def test_feasibility_graph_compiles(self):
        from app.agents.feasibility.graph import build_feasibility_graph

        assert build_feasibility_graph() is not None

    def test_market_graph_compiles(self):
        from app.agents.market.graph import build_market_graph

        assert build_market_graph() is not None

    def test_growth_graph_compiles(self):
        from app.agents.growth.graph import build_growth_graph

        assert build_growth_graph() is not None

    def test_hiring_graph_compiles(self):
        from app.agents.hiring.graph import build_hiring_graph

        assert build_hiring_graph() is not None


class TestGraphExecution:
    def test_planner_graph_runs(self):
        with patch(
            "app.agents.planner.nodes.get_llm",
            return_value=_make_mock_llm("planner"),
        ):
            from app.agents.planner.graph import build_planner_graph

            graph = build_planner_graph()
            state = {**MOCK_CTO_INPUT, "plan": ""}
            result = graph.invoke(state)
            assert "plan" in result

    def test_feasibility_graph_runs(self):
        with patch(
            "app.agents.feasibility.nodes.get_llm",
            return_value=_make_mock_llm("feasibility"),
        ):
            from app.agents.feasibility.graph import build_feasibility_graph

            graph = build_feasibility_graph()
            result = graph.invoke(MOCK_CTO_INPUT)
            assert "feasibility_report" in result

    def test_market_graph_runs(self):
        with patch(
            "app.agents.market.nodes.get_llm",
            return_value=_make_mock_llm("market"),
        ):
            from app.agents.market.graph import build_market_graph

            graph = build_market_graph()
            result = graph.invoke(MOCK_CTO_INPUT)
            assert "market_analysis" in result

    def test_growth_graph_runs(self):
        with patch(
            "app.agents.growth.nodes.get_llm",
            return_value=_make_mock_llm("growth"),
        ):
            from app.agents.growth.graph import build_growth_graph

            graph = build_growth_graph()
            result = graph.invoke(MOCK_CTO_INPUT)
            assert "growth_strategy" in result

    def test_hiring_graph_runs(self):
        with patch(
            "app.agents.hiring.nodes.get_llm",
            return_value=_make_mock_llm("hiring"),
        ):
            from app.agents.hiring.graph import build_hiring_graph

            graph = build_hiring_graph()
            result = graph.invoke(MOCK_CTO_INPUT)
            assert "hiring_plan" in result
