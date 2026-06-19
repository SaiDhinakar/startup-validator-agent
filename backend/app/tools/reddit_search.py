"""Reddit search tool — finds real user pain points and discussions."""

from ddgs import DDGS


def reddit_search(query: str, max_results: int = 5) -> list[dict]:
    """Search Reddit via DuckDuckGo for user discussions."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"site:reddit.com {query}", max_results=max_results))
            return [
                {"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")}
                for r in results
            ]
    except Exception:
        return []


def format_reddit_results(results: list[dict]) -> str:
    """Format Reddit results for LLM context."""
    if not results:
        return "No Reddit discussions found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[R{i}] {r['title']}")
        lines.append(f"    URL: {r['url']}")
        lines.append(f"    {r['snippet'][:150]}")
    return "\n".join(lines)
