"""Tests for database models and repository."""

from datetime import datetime

from app.db.models.strategy import StrategyDocument


class TestStrategyDocument:
    def test_create_document(self):
        doc = StrategyDocument(
            idea="Test idea",
            budget="₹5L",
            team_size="3",
            timeline="2 months",
        )
        assert doc.idea == "Test idea"
        assert doc.budget == "₹5L"
        assert doc.team_size == "3"
        assert doc.timeline == "2 months"
        assert doc.planner == {}
        assert doc.feasibility_report == {}
        assert doc.market_analysis == {}
        assert doc.growth_strategy == {}
        assert doc.hiring_plan == {}
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.updated_at, datetime)

    def test_document_with_agent_outputs(self):
        doc = StrategyDocument(
            idea="Test",
            budget="₹10L",
            team_size="5",
            timeline="3 months",
            planner={"plan": "test plan"},
            feasibility_report={"report": "feasibility data"},
            market_analysis={"analysis": "market data"},
        )
        assert doc.planner == {"plan": "test plan"}
        assert doc.feasibility_report == {"report": "feasibility data"}
        assert doc.market_analysis == {"analysis": "market data"}

    def test_document_serialization(self):
        doc = StrategyDocument(
            idea="Test",
            budget="₹10L",
            team_size="5",
            timeline="3 months",
        )
        data = doc.model_dump(by_alias=True)
        assert "_id" in data
        assert data["idea"] == "Test"
        assert isinstance(data["created_at"], datetime)
