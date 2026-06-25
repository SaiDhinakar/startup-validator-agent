"""Search result caching with validation dates."""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional

# Cache directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
CACHE_EXPIRY_HOURS = 24  # Default cache expiry


def _ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def _get_cache_key(query: str, tool_name: str) -> str:
    """Generate a cache key from query and tool name."""
    key_string = f"{tool_name}:{query}"
    return hashlib.md5(key_string.encode()).hexdigest()


def _get_cache_path(cache_key: str) -> str:
    """Get the file path for a cache key."""
    return os.path.join(CACHE_DIR, f"{cache_key}.json")


def get_cached_results(query: str, tool_name: str) -> Optional[list[dict]]:
    """Retrieve cached search results if they exist and are valid."""
    _ensure_cache_dir()
    cache_key = _get_cache_key(query, tool_name)
    cache_path = _get_cache_path(cache_key)

    if not os.path.exists(cache_path):
        return None

    try:
        with open(cache_path, "r") as f:
            cache_data = json.load(f)

        cached_time = datetime.fromisoformat(cache_data["timestamp"])
        expiry_hours = cache_data.get("expiry_hours", CACHE_EXPIRY_HOURS)

        if datetime.now() - cached_time < timedelta(hours=expiry_hours):
            return cache_data["results"]
        else:
            # Cache expired, remove it
            os.remove(cache_path)
            return None
    except (json.JSONDecodeError, KeyError, ValueError):
        # Invalid cache file, remove it
        if os.path.exists(cache_path):
            os.remove(cache_path)
        return None


def cache_results(query: str, tool_name: str, results: list[dict], expiry_hours: int = CACHE_EXPIRY_HOURS):
    """Cache search results with expiry time."""
    _ensure_cache_dir()
    cache_key = _get_cache_key(query, tool_name)
    cache_path = _get_cache_path(cache_key)

    cache_data = {
        "query": query,
        "tool": tool_name,
        "timestamp": datetime.now().isoformat(),
        "expiry_hours": expiry_hours,
        "results": results,
    }

    with open(cache_path, "w") as f:
        json.dump(cache_data, f, indent=2)


def clear_expired_cache():
    """Remove all expired cache entries."""
    _ensure_cache_dir()

    if not os.path.exists(CACHE_DIR):
        return

    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".json"):
            cache_path = os.path.join(CACHE_DIR, filename)
            try:
                with open(cache_path, "r") as f:
                    cache_data = json.load(f)

                cached_time = datetime.fromisoformat(cache_data["timestamp"])
                expiry_hours = cache_data.get("expiry_hours", CACHE_EXPIRY_HOURS)

                if datetime.now() - cached_time >= timedelta(hours=expiry_hours):
                    os.remove(cache_path)
            except (json.JSONDecodeError, KeyError, ValueError, OSError):
                # Invalid or unreadable cache file, remove it
                if os.path.exists(cache_path):
                    os.remove(cache_path)


def get_cache_stats() -> dict:
    """Get statistics about the cache."""
    _ensure_cache_dir()

    if not os.path.exists(CACHE_DIR):
        return {"total_entries": 0, "valid_entries": 0, "expired_entries": 0}

    total = 0
    valid = 0
    expired = 0

    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".json"):
            total += 1
            cache_path = os.path.join(CACHE_DIR, filename)
            try:
                with open(cache_path, "r") as f:
                    cache_data = json.load(f)

                cached_time = datetime.fromisoformat(cache_data["timestamp"])
                expiry_hours = cache_data.get("expiry_hours", CACHE_EXPIRY_HOURS)

                if datetime.now() - cached_time < timedelta(hours=expiry_hours):
                    valid += 1
                else:
                    expired += 1
            except (json.JSONDecodeError, KeyError, ValueError):
                expired += 1

    return {"total_entries": total, "valid_entries": valid, "expired_entries": expired}