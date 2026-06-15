"""Dependency injection for API endpoints."""

from app.db.repositories.strategy import StrategyRepository


def get_strategy_repo() -> StrategyRepository:
    return StrategyRepository()
