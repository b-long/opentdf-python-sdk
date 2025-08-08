"""
KASKeyCache: In-memory cache for KAS (Key Access Service) public keys and info.
"""

import threading
from typing import Any


class KASKeyCache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()

    def get(self, url: str, algorithm: str | None = None) -> Any | None:
        """
        Gets a KASInfo object from the cache based on URL and algorithm.

        Args:
            url: The URL of the KAS
            algorithm: Optional algorithm identifier

        Returns:
            The cached KASInfo object, or None if not found
        """
        cache_key = self._make_key(url, algorithm)
        with self._lock:
            return self._cache.get(cache_key)

    def store(self, kas_info) -> None:
        """
        Stores a KASInfo object in the cache.

        Args:
            kas_info: The KASInfo object to store
        """
        cache_key = self._make_key(kas_info.url, getattr(kas_info, "algorithm", None))
        with self._lock:
            self._cache[cache_key] = kas_info

    def set(self, key, value):
        """Store a key-value pair in the cache."""
        with self._lock:
            self._cache[key] = value

    def clear(self):
        """Clears the cache"""
        with self._lock:
            self._cache.clear()

    def _make_key(self, url: str, algorithm: str | None = None) -> str:
        """Creates a cache key from URL and algorithm"""
        return f"{url}:{algorithm or ''}"
