"""LangGraph agent definitions. Each subdirectory is a self-contained agent
with its own state schema, nodes, prompts, and compiled graph.

Agents:
  - planner: analyzes requirements, orchestrates the workflow
  - product: extracts business requirements and core features
  - architecture: designs technical stack and system components
  - engineering: generates DB schemas, APIs, and sprint roadmaps
  - reviewer: evaluates feasibility, scalability, and constraints
"""

from app.agents.planner.graph import build_planner_graph
from app.agents.product.graph import build_product_graph
from app.agents.architecture.graph import build_architecture_graph
from app.agents.engineering.graph import build_engineering_graph
from app.agents.reviewer.graph import build_reviewer_graph
