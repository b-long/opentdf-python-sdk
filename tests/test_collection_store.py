import unittest

from otdf_python.collection_store import (
    CollectionKey,
    CollectionStoreImpl,
    NoOpCollectionStore,
)


class DummyHeader:
    def __init__(self, value):
        self.value = value

    def to_bytes(self):
        return self.value.encode()


class TestCollectionStore(unittest.TestCase):
    def test_noop_collection_store(self):
        store = NoOpCollectionStore()
        header = DummyHeader("header1")
        key = CollectionKey(b"secret")
        store.store(header, key)
        self.assertIs(store.get_key(header), store.NO_PRIVATE_KEY)

    def test_collection_store_impl(self):
        store = CollectionStoreImpl()
        header1 = DummyHeader("header1")
        header2 = DummyHeader("header2")
        key1 = CollectionKey(b"key1")
        key2 = CollectionKey(b"key2")
        store.store(header1, key1)
        store.store(header2, key2)
        self.assertEqual(store.get_key(header1).key, b"key1")
        self.assertEqual(store.get_key(header2).key, b"key2")
        # Test eviction
        for i in range(store.MAX_SIZE_STORE + 1):
            store.store(DummyHeader(f"h{i}"), CollectionKey(bytes([i % 256])))
        self.assertLessEqual(len(store), store.MAX_SIZE_STORE)


if __name__ == "__main__":
    unittest.main()
