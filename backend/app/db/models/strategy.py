"""Strategy document schema — stores a generated CTO strategy."""

from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field


class StrategyDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    idea: str
    budget: str
    team_size: str
    timeline: str
    product_name: str = ""
    product_type: str = ""
    timeline_months: int = 0
    target_users: str = ""
    selected_agents: list[str] = Field(default_factory=lambda: ["feasibility", "market", "growth", "hiring"])
    planner: dict = {}
    feasibility_report: dict = {}
    market_analysis: dict = {}
    growth_strategy: dict = {}
    hiring_plan: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_mongo(cls, data: dict) -> "StrategyDocument":
        if "_id" in data and isinstance(data["_id"], ObjectId):
            data["_id"] = str(data["_id"])
        return cls(**data)

    model_config = {"populate_by_name": True}
