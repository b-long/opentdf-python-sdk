from collections import OrderedDict


class CollectionKey:
    def __init__(self, key: bytes | None):
        self.key = key


class CollectionStore:
    NO_PRIVATE_KEY = CollectionKey(None)

    def store(self, header, key: CollectionKey):
        raise NotImplementedError

    def get_key(self, header) -> CollectionKey:
        raise NotImplementedError


class NoOpCollectionStore(CollectionStore):
    def store(self, header, key: CollectionKey):
        pass

    def get_key(self, header) -> CollectionKey:
        return self.NO_PRIVATE_KEY


class CollectionStoreImpl(OrderedDict, CollectionStore):
    MAX_SIZE_STORE = 500

    def __init__(self):
        super().__init__()

    def store(self, header, key: CollectionKey):
        buf = header.to_bytes()
        self[buf] = key
        if len(self) > self.MAX_SIZE_STORE:
            self.popitem(last=False)

    def get_key(self, header) -> CollectionKey:
        buf = header.to_bytes()
        return self.get(buf, self.NO_PRIVATE_KEY)
