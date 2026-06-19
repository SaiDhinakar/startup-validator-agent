"""Reviewer prompts — compact, verifies search-backed truth."""

REVIEWER_SYSTEM = """Brutal truth reviewer. Validate agent output against search data (if available).

Check:
1. Are cited URLs real and relevant? (flag fabricated links)
2. Do claims match search evidence?
3. Is advice specific to THIS idea?
4. Are stats/numbers plausible?

Output EXACTLY:
VALID — if grounded in evidence
INVALID — if fabricated/unrelevant
REASON: explanation (required if INVALID)"""


def build_review_prompt(
    idea: str,
    agent_name: str,
    agent_output: str,
    context: dict,
) -> str:
    budget = context.get("budget", "Not specified")
    team_size = context.get("team_size", "Not specified")
    timeline = context.get("timeline_months", "Not specified")

    output_label = {
        "planner": "Plan",
        "feasibility": "Feasibility Report",
        "market": "Market Analysis",
        "growth": "Growth Strategy",
        "hiring": "Hiring Plan",
    }.get(agent_name, "Output")

    return f"""Validate this {output_label} for: {idea}

Budget: {budget} | Team: {team_size} | Timeline: {timeline} months

OUTPUT:
{agent_output[:1500]}

Check: relevance, source credibility, claim accuracy, specificity.
VALID or INVALID + REASON:"""
