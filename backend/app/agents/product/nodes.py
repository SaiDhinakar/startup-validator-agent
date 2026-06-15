"""Product agent graph nodes."""

from langchain_core.messages import HumanMessage

from app.core.llm import get_llm
from app.agents.product.prompts import PRODUCT_SYSTEM, PRODUCT_USER
from app.agents.product.state import ProductState


def analyze_node(state: ProductState) -> dict:
    llm = get_llm(temperature=0.5)
    prompt = PRODUCT_USER.format(
        idea=state["idea"],
        budget=state["budget"],
        team_size=state["team_size"],
        timeline=state["timeline"],
    )
    response = llm.invoke([
        {"role": "system", "content": PRODUCT_SYSTEM},
        HumanMessage(content=prompt),
    ])
    return {"reasoning": response.content}
