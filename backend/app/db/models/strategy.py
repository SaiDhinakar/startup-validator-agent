"""Strategy document schema — stores a generated CTO strategy."""

from datetime import datetime

from pydantic import BaseModel, Field
from bson import ObjectId


class StrategyDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    idea: str
    budget: str
    team_size: str
    timeline: str
    planner: dict = {}
    product: dict = {}
    architecture: dict = {}
    engineering: dict = {}
    review: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
