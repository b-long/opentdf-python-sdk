"""Tests for address_normalizer module."""

import pytest

from otdf_python.address_normalizer import normalize_address
from otdf_python.sdk_exceptions import SDKException


def test_normalize_address_with_scheme():
    """Test normalizing address that already has a scheme."""
    # Test with HTTPS URL
    url = "https://example.com/path"
    normalized = normalize_address(url, False)
    assert normalized == "https://example.com:443"

    # Test with HTTP URL, but requesting HTTPS
    url = "http://example.com/path"
    normalized = normalize_address(url, False)
    assert normalized == "https://example.com:443"

    # Test with HTTP URL, requesting plaintext
    url = "http://example.com/path"
    normalized = normalize_address(url, True)
    assert normalized == "http://example.com:80"


def test_normalize_address_with_port():
    """Test normalizing address with custom port."""
    # With HTTPS and custom port
    url = "https://example.com:8443/path"
    normalized = normalize_address(url, False)
    assert normalized == "https://example.com:8443"

    # With HTTP and custom port
    url = "http://example.com:8080/path"
    normalized = normalize_address(url, True)
    assert normalized == "http://example.com:8080"

    # Forcing HTTP on HTTPS URL with custom port
    url = "https://example.com:8443/path"
    normalized = normalize_address(url, True)
    assert normalized == "http://example.com:8443"


def test_normalize_address_no_scheme():
    """Test normalizing address without a scheme."""
    # Just hostname
    url = "example.com"
    normalized = normalize_address(url, False)
    assert normalized == "https://example.com:443"

    # Hostname with port
    url = "example.com:8080"
    normalized = normalize_address(url, False)
    assert normalized == "https://example.com:8080"

    # Hostname with port, plaintext
    url = "example.com:8080"
    normalized = normalize_address(url, True)
    assert normalized == "http://example.com:8080"


def test_normalize_address_invalid():
    """Test normalizing invalid addresses."""
    # Non-numeric port
    with pytest.raises(SDKException):
        normalize_address("example.com:invalid", False)

    # Very malformed URL
    with pytest.raises(SDKException):
        normalize_address("not a real url with spaces:123:456", False)
