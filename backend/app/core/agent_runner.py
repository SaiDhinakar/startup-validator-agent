"""Shared agent runner — LLM decides when to call tools, emits events."""

import logging
from typing import Callable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 4


def run_agent(
    llm: BaseChatModel,
    system_prompt: str,
    user_prompt: str,
    tools: list[BaseTool],
    on_event: Callable[[str, dict], None] | None = None,
    previous_output: str = "",
) -> str:
    """Run an agent with tool-calling loop. Returns final HTML response.

    on_event(event_type, data) is called for tool_start/tool_done so the
    caller can stream status updates to the client.
    previous_output: Output from a previous iteration to build upon.
    """
    def emit(event_type: str, data: dict):
        if on_event:
            on_event(event_type, data)

    bound_llm = llm.bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    messages = [
        SystemMessage(content=system_prompt),
    ]

    # Add previous output context if available
    if previous_output:
        messages.append(HumanMessage(
            content=f"Previous iteration output to build upon:\n\n{previous_output[:1500]}"
        ))

    messages.append(HumanMessage(content=user_prompt))

    for round_num in range(MAX_TOOL_ROUNDS):
        logger.debug("Agent LLM round %d/%d", round_num + 1, MAX_TOOL_ROUNDS)
        response: AIMessage = bound_llm.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            logger.debug("Agent finished after %d rounds (no more tool calls)", round_num + 1)
            return response.content

        for tc in response.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            query = tool_args.get("query", "")

            # Handle malformed tool args - extract query from any string value
            if not query:
                for v in tool_args.values():
                    if isinstance(v, str) and len(v) > 3:
                        query = v
                        break

            logger.info("Tool call: %s(query=%s)", tool_name, query[:100])
            emit("tool_start", {"tool": tool_name, "query": query})

            tool_fn = tool_map.get(tool_name)
            if tool_fn:
                try:
                    result = tool_fn.invoke(tool_args)
                except Exception as e:
                    logger.warning("Tool call failed for %s: %s", tool_name, e)
                    # Retry with extracted query
                    if query:
                        try:
                            result = tool_fn.invoke({"query": query})
                        except Exception:
                            result = f"Tool error: {e}"
                    else:
                        result = f"Tool error: {e}"
            else:
                result = f"Unknown tool: {tool_name}"
                logger.warning("Unknown tool requested: %s", tool_name)

            emit("tool_done", {"tool": tool_name})
            logger.info("Tool done: %s", tool_name)
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))

    return messages[-1].content if messages else ""
