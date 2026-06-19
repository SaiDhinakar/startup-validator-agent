"""Reviewer agent — validates agent outputs for ground truth accuracy."""

from langchain_core.messages import HumanMessage

from app.agents.reviewer.prompts import REVIEWER_SYSTEM, build_review_prompt
from app.core.llm import get_llm


def review_agent_output(
    idea: str,
    agent_name: str,
    agent_output: str,
    context: dict,
) -> dict:
    llm = get_llm(temperature=0.2)
    prompt = build_review_prompt(idea, agent_name, agent_output, context)
    response = llm.invoke([
        {"role": "system", "content": REVIEWER_SYSTEM},
        HumanMessage(content=prompt),
    ])

    text = response.content.strip().upper()
    valid = "VALID" in text and "INVALID" not in text

    reason = ""
    if not valid:
        lines = response.content.strip().split("\n")
        for line in lines:
            if line.strip().startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()
                break
        if not reason:
            reason = "Output does not meet ground truth standards."

    return {"valid": valid, "reason": reason}
