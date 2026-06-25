"""External tool integrations — web search, reddit, trends, etc."""

from app.tools.web_search import web_search as web_search
from app.tools.web_search import format_search_results as format_search_results
from app.tools.reddit_search import reddit_search as reddit_search
from app.tools.reddit_search import format_reddit_results as format_reddit_results
from app.tools.trends import trends_search as trends_search
from app.tools.trends import format_trends_results as format_trends_results
from app.tools.langchain_tools import search_web as search_web
from app.tools.langchain_tools import search_reddit as search_reddit
from app.tools.langchain_tools import search_trends as search_trends
from app.tools.search_cache import get_cached_results, cache_results, clear_expired_cache, get_cache_stats
