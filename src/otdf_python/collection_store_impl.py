"""Collection store implementation."""

from collections import OrderedDict
from threading import RLock

MAX_SIZE_STORE = 500


class CollectionStoreImpl(OrderedDict):
    """Thread-safe collection store for caching TDF keys."""

    def __init__(self):
        """Initialize collection store."""
        super().__init__()
        self._lock = RLock()

    def store(self, header, key):
        buf = header.to_bytes()  # Assumes header has a to_bytes() method
        with self._lock:
            self[buf] = key
            if len(self) > MAX_SIZE_STORE:
                self.popitem(last=False)

    def get_key(self, header, no_private_key=None):
        buf = header.to_bytes()
        with self._lock:
            return self.get(buf, no_private_key)
