"""LangChain Tool definitions for web search, reddit, and trends."""

import logging
from langchain_core.tools import tool

from app.tools.web_search import web_search as _web_search
from app.tools.reddit_search import reddit_search as _reddit_search
from app.tools.trends import trends_search as _trends_search
from app.tools.search_cache import get_cached_results, cache_results

logger = logging.getLogger(__name__)


@tool
def search_web(query: str) -> str:
    """Search the web for current information about technologies, APIs, costs, competitors, market data, regulations, or any factual topic. Returns titles, URLs, and snippets."""
    # Check cache first
    cached = get_cached_results(query, "web_search")
    if cached is not None:
        logger.info("Using cached results for web search: %s", query[:50])
        results = cached
    else:
        results = _web_search(query, max_results=5)
        if results:
            cache_results(query, "web_search", results)

    if not results:
        return "No results found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    {r['snippet'][:200]}")
    return "\n".join(lines)


@tool
def search_reddit(query: str) -> str:
    """Search Reddit for real user discussions, pain points, complaints, and feedback about a topic. Good for understanding user sentiment and real-world problems."""
    # Check cache first
    cached = get_cached_results(query, "reddit_search")
    if cached is not None:
        logger.info("Using cached results for Reddit search: %s", query[:50])
        results = cached
    else:
        results = _reddit_search(query, max_results=5)
        if results:
            cache_results(query, "reddit_search", results)

    if not results:
        return "No Reddit discussions found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    {r['snippet'][:200]}")
    return "\n".join(lines)


@tool
def search_trends(query: str) -> str:
    """Search for Google Trends data and search interest over time for a topic. Good for validating market demand and timing."""
    # Check cache first
    cached = get_cached_results(query, "trends_search")
    if cached is not None:
        logger.info("Using cached results for trends search: %s", query[:50])
        results = cached
    else:
        results = _trends_search(query, max_results=3)
        if results:
            cache_results(query, "trends_search", results)

    if not results:
        return "No trends data found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    {r['snippet'][:200]}")
    return "\n".join(lines)
