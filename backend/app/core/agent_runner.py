"""Shared agent runner — LLM decides when to call tools, emits events."""

from typing import Callable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool

MAX_TOOL_ROUNDS = 4


def run_agent(
    llm: BaseChatModel,
    system_prompt: str,
    user_prompt: str,
    tools: list[BaseTool],
    on_event: Callable[[str, dict], None] | None = None,
) -> str:
    """Run an agent with tool-calling loop. Returns final HTML response.

    on_event(event_type, data) is called for tool_start/tool_done so the
    caller can stream status updates to the client.
    """
    def emit(event_type: str, data: dict):
        if on_event:
            on_event(event_type, data)

    bound_llm = llm.bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    for _ in range(MAX_TOOL_ROUNDS):
        response: AIMessage = bound_llm.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tc in response.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            query = tool_args.get("query", "")

            emit("tool_start", {"tool": tool_name, "query": query})

            tool_fn = tool_map.get(tool_name)
            if tool_fn:
                result = tool_fn.invoke(tool_args)
            else:
                result = f"Unknown tool: {tool_name}"

            emit("tool_done", {"tool": tool_name})
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))

    return messages[-1].content if messages else ""
