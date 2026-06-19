"""Tests for API endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.api.deps import get_strategy_repo
from app.db.models.strategy import StrategyDocument
from app.main import app

client = TestClient(app)

MOCK_STRATEGY = StrategyDocument(
    idea="Build an Uber clone",
    budget="₹10L",
    team_size="5",
    timeline="3 months",
)

MOCK_CTO_STRATEGY = StrategyDocument(
    idea="Build an Uber clone",
    budget="₹10L",
    team_size="5",
    timeline="6 months",
    product_name="Uber Clone",
    product_type="Mobile App",
    timeline_months=6,
    target_users="Urban commuters",
)


def _mock_repo():
    repo = MagicMock()
    repo.create = AsyncMock(return_value=MOCK_STRATEGY)
    repo.get_by_id = AsyncMock(return_value=MOCK_STRATEGY)
    repo.list_all = AsyncMock(return_value=[MOCK_STRATEGY])
    repo.update = AsyncMock(return_value=MOCK_STRATEGY)
    repo.delete = AsyncMock(return_value=True)
    return repo


def _mock_repo_cto():
    repo = MagicMock()
    repo.create = AsyncMock(return_value=MOCK_CTO_STRATEGY)
    repo.get_by_id = AsyncMock(return_value=MOCK_CTO_STRATEGY)
    repo.list_all = AsyncMock(return_value=[MOCK_CTO_STRATEGY])
    repo.update = AsyncMock(return_value=MOCK_CTO_STRATEGY)
    repo.delete = AsyncMock(return_value=True)
    return repo


def _setup_mock(func):
    def wrapper(self):
        mock = _mock_repo()
        app.dependency_overrides[get_strategy_repo] = lambda: mock
        try:
            func(self, mock)
        finally:
            app.dependency_overrides.clear()
    wrapper.__name__ = func.__name__
    return wrapper


def _setup_mock_cto(func):
    def wrapper(self):
        mock = _mock_repo_cto()
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


class TestGenerateCTOStrategy:
    @_setup_mock_cto
    def test_generate_cto_all_agents(self, repo):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="VALID\nREASON: Output is grounded.")
        with patch("app.agents.planner.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.feasibility.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.market.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.growth.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.hiring.nodes.get_llm", return_value=mock_llm), \
             patch("app.agents.reviewer.nodes.get_llm", return_value=mock_llm):
            response = client.post(f"/api/v1/strategies/{MOCK_CTO_STRATEGY.id}/generate-cto")
            assert response.status_code == 200

    def test_generate_cto_not_found(self):
        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=None)
        app.dependency_overrides[get_strategy_repo] = lambda: repo
        try:
            fake_id = "000000000000000000000000"
            response = client.post(f"/api/v1/strategies/{fake_id}/generate-cto")
            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()
