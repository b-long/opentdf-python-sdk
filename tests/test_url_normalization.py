#!/usr/bin/env python3
"""Test script to verify URL normalization functionality is working correctly.

This script tests the _normalize_kas_url method to ensure it properly respects
the use_plaintext setting when converting URLs.
"""

from src.otdf_python.kas_client import KASClient


def test_url_normalization():
    """Test KAS URL normalization with plaintext settings."""
    print("Testing with use_plaintext=True:")
    client_plaintext = KASClient(use_plaintext=True)

    test_urls = [
        "example.com:8080",
        "example.com",
        "https://example.com:8080/kas",
        "http://example.com:8080/kas",
    ]

    for url in test_urls:
        normalized = client_plaintext._normalize_kas_url(url)
        print(f"  {url} -> {normalized}")
        # With plaintext=True, all URLs should use http://
        assert "http://" in normalized
        assert "https://" not in normalized

    print("\nTesting with use_plaintext=False:")
    client_https = KASClient(use_plaintext=False)

    for url in test_urls:
        normalized = client_https._normalize_kas_url(url)
        print(f"  {url} -> {normalized}")
        # With plaintext=False, all URLs should use https://
        assert "https://" in normalized
        assert "http://" not in normalized

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_url_normalization()
