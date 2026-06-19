"""Strategy schemas — request/response Pydantic models."""

from datetime import datetime

from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    idea: str = Field(..., min_length=1, max_length=2000)
    budget: str = Field(default="", max_length=100)
    team_size: str = Field(default="", max_length=50)
    timeline: str = Field(default="", max_length=100)
    product_name: str = Field(default="", max_length=2000)
    product_type: str = Field(default="", max_length=100)
    timeline_months: int = Field(default=0, ge=0)
    target_users: str = Field(default="", max_length=500)


class StrategyResponse(BaseModel):
    id: str
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
    created_at: datetime
    updated_at: datetime


class StrategyListResponse(BaseModel):
    strategies: list[StrategyResponse]
    total: int


class GenerateCTORequest(BaseModel):
    agents: list[str] = Field(
        default=["planner", "feasibility", "market", "growth", "hiring"],
        description="Which CTO agents to run. Defaults to all.",
    )
