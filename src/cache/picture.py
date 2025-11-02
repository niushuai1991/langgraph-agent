
from uuid import UUID
from functools import lru_cache

# Although lru_cache is a decorator, we can use a dictionary-based
# approach to simulate the put/get behavior the user requested.
# A simple dictionary is more direct for this use case.

_cache = {}
_maxsize = 128

def put(key: UUID, value: str):
    """
    Caches the SVG content with the given UUID key.
    """
    if len(_cache) >= _maxsize:
        # Simple eviction: remove the first item (FIFO, not true LRU)
        try:
            del _cache[next(iter(_cache))]
        except StopIteration:
            pass  # Cache is empty
    _cache[key] = value

def get(key: UUID) -> str | None:
    """
    Retrieves the SVG content for the given UUID key from the cache.
    """
    return _cache.get(key)
