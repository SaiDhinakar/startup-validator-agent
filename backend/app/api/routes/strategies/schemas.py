"""Strategy schemas — request/response Pydantic models."""

from datetime import datetime

from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    idea: str = Field(..., min_length=1, max_length=2000)
    budget: str = Field(..., min_length=1, max_length=100)
    team_size: str = Field(..., min_length=1, max_length=10)
    timeline: str = Field(..., min_length=1, max_length=100)


class StrategyResponse(BaseModel):
    id: str
    idea: str
    budget: str
    team_size: str
    timeline: str
    planner: dict = {}
    product: dict = {}
    architecture: dict = {}
    engineering: dict = {}
    review: dict = {}
    created_at: datetime
    updated_at: datetime


class StrategyListResponse(BaseModel):
    strategies: list[StrategyResponse]
    total: int


class GenerateRequest(BaseModel):
    agents: list[str] = Field(
        default=["planner", "product", "architecture", "engineering", "reviewer"],
        description="Which agents to run. Defaults to all.",
    )
