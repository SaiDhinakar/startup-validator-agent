"""Planner prompts — concise."""

PLANNER_SYSTEM = """Startup Planner. Output HTML.

Use search_web 1-2x to research similar startups and tech stacks.
Cite sources as <a href="URL" target="_blank">[N]</a>.

BEFORE your plan, output one line:
<!-- AGENTS: agent1,agent2 -->

Agents: feasibility, market, growth, hiring
- feasibility: include if budget/timeline/team are tight
- market: always include
- growth: include if B2C or network effects
- hiring: include if team_size > 3 or building from scratch

HTML sections: Problem, Users, Features, Value Prop, Goals, Metrics.

Tags: <h1><h2><h3><p><ul><li><strong><em><table><tr><th><td>"""

PLANNER_USER = """Idea: {idea}
Budget: {budget} | Team: {team_size} | Timeline: {timeline}

Search for similar startups. Create execution plan."""

PLANNER_USER_CTO = """Product: {product_name} ({product_type})
Budget: {budget} | Team: {team_size} | Timeline: {timeline_months}m
Users: {target_users}

Search for similar products. Create execution plan."""

ALL_AGENTS = ["feasibility", "market", "growth", "hiring"]


def parse_selected_agents(plan: str) -> list[str]:
    """Extract selected agents from <!-- AGENTS: ... --> marker."""
    import re
    match = re.search(r"<!--\s*AGENTS:\s*([^>]+)\s*-->", plan)
    if match:
        raw = match.group(1)
        selected = [a.strip() for a in raw.split(",") if a.strip() in ALL_AGENTS]
        if selected:
            return selected
    return ALL_AGENTS
