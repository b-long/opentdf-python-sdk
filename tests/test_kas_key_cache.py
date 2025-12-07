"""Unit tests for KASKeyCache."""

from dataclasses import dataclass

from otdf_python.kas_key_cache import KASKeyCache


@dataclass
class MockKasInfo:
    """Mock KAS info for testing."""

    url: str
    algorithm: str | None = None
    public_key: str | None = None
    kid: str | None = None
    default: bool = False


def test_kas_key_cache_set_and_get():
    """Test KASKeyCache set and get operations."""
    cache = KASKeyCache()
    # Use the new store/get interface
    kas_info = MockKasInfo(url="http://example.com")
    cache.store(kas_info)
    assert cache.get("http://example.com") == kas_info


def test_kas_key_cache_overwrite():
    """Test KASKeyCache overwriting cached values."""
    cache = KASKeyCache()
    # Test overwriting with new values
    kas_info1 = MockKasInfo(url="http://example.com")
    kas_info2 = MockKasInfo(url="http://example.com", algorithm="RSA")
    cache.store(kas_info1)
    cache.store(kas_info2)
    # Without specifying an algorithm, should return the no-algorithm version
    assert cache.get("http://example.com") == kas_info1
    # With algorithm specified, should return the algorithm-specific version
    assert cache.get("http://example.com", "RSA") == kas_info2


def test_kas_key_cache_clear():
    """Test KASKeyCache clear operation."""
    cache = KASKeyCache()
    cache.set("key1", "value1")
    cache.clear()
    assert cache.get("key1") is None
