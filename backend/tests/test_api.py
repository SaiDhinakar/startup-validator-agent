"""Tests for API endpoints."""

from unittest.mock import patch, MagicMock, AsyncMock

from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_strategy_repo
from app.db.models.strategy import StrategyDocument

client = TestClient(app)

MOCK_STRATEGY = StrategyDocument(
    idea="Build an Uber clone",
    budget="₹10L",
    team_size="5",
    timeline="3 months",
)


def _mock_repo():
    repo = MagicMock()
    repo.create = AsyncMock(return_value=MOCK_STRATEGY)
    repo.get_by_id = AsyncMock(return_value=MOCK_STRATEGY)
    repo.list_all = AsyncMock(return_value=[MOCK_STRATEGY])
    repo.update = AsyncMock(return_value=MOCK_STRATEGY)
    repo.delete = AsyncMock(return_value=True)
    return repo


def _setup_mock(func):
    """Decorator that overrides the dependency for the test."""
    def wrapper(self):
        mock = _mock_repo()
        app.dependency_overrides[get_strategy_repo] = lambda: mock
        try:
            func(self, mock)
        finally:
            app.dependency_overrides.clear()
    wrapper.__name__ = func.__name__
    return wrapper


class TestHealthEndpoint:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestRootEndpoint:
    def test_root_returns_message(self):
        response = client.get("/api/v1/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestCreateStrategy:
    @_setup_mock
    def test_create_strategy(self, repo):
        response = client.post("/api/v1/strategies", json={
            "idea": "Build an Uber clone",
            "budget": "₹10L",
            "team_size": "5",
            "timeline": "3 months",
        })
        assert response.status_code == 201
        assert response.json()["idea"] == "Build an Uber clone"

    def test_create_strategy_validation(self):
        response = client.post("/api/v1/strategies", json={
            "idea": "",
            "budget": "₹10L",
            "team_size": "5",
            "timeline": "3 months",
        })
        assert response.status_code == 422


class TestListStrategies:
    @_setup_mock
    def test_list_strategies(self, repo):
        response = client.get("/api/v1/strategies")
        assert response.status_code == 200
        assert len(response.json()["strategies"]) == 1


class TestGetStrategy:
    @_setup_mock
    def test_get_strategy(self, repo):
        response = client.get(f"/api/v1/strategies/{MOCK_STRATEGY.id}")
        assert response.status_code == 200

    def test_get_strategy_not_found(self):
        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=None)
        app.dependency_overrides[get_strategy_repo] = lambda: repo
        try:
            fake_id = "000000000000000000000000"
            response = client.get(f"/api/v1/strategies/{fake_id}")
            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()


class TestDeleteStrategy:
    @_setup_mock
    def test_delete_strategy(self, repo):
        response = client.delete(f"/api/v1/strategies/{MOCK_STRATEGY.id}")
        assert response.status_code == 204

    def test_delete_strategy_not_found(self):
        repo = _mock_repo()
        repo.delete = AsyncMock(return_value=False)
        app.dependency_overrides[get_strategy_repo] = lambda: repo
        try:
            fake_id = "000000000000000000000000"
            response = client.delete(f"/api/v1/strategies/{fake_id}")
            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()


class TestGenerateStrategy:
    @_setup_mock
    def test_generate_all_agents(self, repo):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content='{"result": "ok"}')
        with patch("app.agents.planner.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.product.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.architecture.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.engineering.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.reviewer.nodes.get_llm", return_value=mock_llm):
            response = client.post(f"/api/v1/strategies/{MOCK_STRATEGY.id}/generate")
            assert response.status_code == 200

    @_setup_mock
    def test_generate_specific_agents(self, repo):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content='{"result": "ok"}')
        with patch("app.agents.planner.nodes.get_llm", return_value=mock_llm):
            response = client.post(
                f"/api/v1/strategies/{MOCK_STRATEGY.id}/generate",
                json={"agents": ["planner"]},
            )
            assert response.status_code == 200

    def test_generate_not_found(self):
        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=None)
        app.dependency_overrides[get_strategy_repo] = lambda: repo
        try:
            fake_id = "000000000000000000000000"
            response = client.post(f"/api/v1/strategies/{fake_id}/generate")
            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()
