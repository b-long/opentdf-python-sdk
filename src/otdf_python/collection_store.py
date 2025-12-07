"""Collection store interface for managing collections."""

from collections import OrderedDict


class CollectionKey:
    """Collection key wrapper for store operations."""

    def __init__(self, key: bytes | None):
        """Initialize collection key."""
        self.key = key


class CollectionStore:
    """Abstract collection store interface for key management."""

    NO_PRIVATE_KEY = CollectionKey(None)

    def store(self, header, key: CollectionKey):
        raise NotImplementedError

    def get_key(self, header) -> CollectionKey:
        raise NotImplementedError


class NoOpCollectionStore(CollectionStore):
    """No-op collection store that discards all keys."""

    def store(self, header, key: CollectionKey):
        """Discard key operation (no-op)."""
        pass

    def get_key(self, header) -> CollectionKey:
        return self.NO_PRIVATE_KEY


class CollectionStoreImpl(OrderedDict, CollectionStore):
    """Collection store implementation with ordered dictionary."""

    MAX_SIZE_STORE = 500

    def __init__(self):
        """Initialize collection store."""
        super().__init__()

    def store(self, header, key: CollectionKey):
        buf = header.to_bytes()
        self[buf] = key
        if len(self) > self.MAX_SIZE_STORE:
            self.popitem(last=False)

    def get_key(self, header) -> CollectionKey:
        buf = header.to_bytes()
        return self.get(buf, self.NO_PRIVATE_KEY)
