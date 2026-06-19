"""Web search tool using DuckDuckGo (free, no API key)."""

from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web and return results with titles, URLs, and snippets."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [
                {"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")}
                for r in results
            ]
    except Exception:
        return []


def format_search_results(results: list[dict]) -> str:
    """Format search results into compact string for LLM context."""
    if not results:
        return "No search results available."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    {r['snippet'][:150]}")
    return "\n".join(lines)
