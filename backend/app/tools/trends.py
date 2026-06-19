"""Google Trends search interest validation."""

from ddgs import DDGS


def trends_search(query: str, max_results: int = 3) -> list[dict]:
    """Search for Google Trends data and search interest info."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"Google Trends {query} search interest", max_results=max_results))
            return [
                {"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")}
                for r in results
            ]
    except Exception:
        return []


def format_trends_results(results: list[dict]) -> str:
    """Format trends results for LLM context."""
    if not results:
        return "No trends data found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[T{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    {r['snippet'][:150]}")
    return "\n".join(lines)
