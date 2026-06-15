"""API spec agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.api.prompts import API_SYSTEM, API_USER
from app.agents.api.state import ApiSpecState


def design_node(state: ApiSpecState) -> dict:
    llm = get_llm(temperature=0.3)
    prompt = API_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
    )
    response = llm.invoke([
        {"role": "system", "content": API_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
