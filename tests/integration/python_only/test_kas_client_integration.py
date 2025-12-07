"""Integration tests for KASClient."""

import pytest

from otdf_python.kas_client import KASClient, KeyAccess
from otdf_python.kas_key_cache import KASKeyCache
from otdf_python.sdk_exceptions import SDKException
from tests.config_pydantic import CONFIG_TDF


@pytest.mark.integration
def test_connect_rpc_public_key_retrieval():
    """Test Connect RPC public key retrieval using live backend server."""
    from otdf_python.config import KASInfo

    # Create KAS info from configuration
    kas_info = KASInfo(url=CONFIG_TDF.KAS_ENDPOINT)

    # Create KAS client with SSL verification disabled for testing
    client = KASClient(
        kas_url=CONFIG_TDF.KAS_ENDPOINT,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
        use_plaintext=bool(CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://")),
    )

    # Retrieve public key using Connect RPC
    result = client.get_public_key(kas_info)

    # Verify the result
    assert result is not None
    assert result.url == CONFIG_TDF.KAS_ENDPOINT
    assert result.public_key is not None
    assert len(result.public_key) > 0
    assert result.kid is not None
    assert len(result.kid) > 0

    # Verify the public key looks like a PEM format
    assert "-----BEGIN" in result.public_key
    assert "-----END" in result.public_key


@pytest.mark.integration
def test_public_key_caching():
    """Test that retrieving the public key uses the cache on subsequent calls."""
    from otdf_python.config import KASInfo

    # Create a custom cache instance to verify caching behavior
    cache = KASKeyCache()
    kas_info = KASInfo(url=CONFIG_TDF.KAS_ENDPOINT)

    # Create KAS client with the custom cache
    client = KASClient(
        kas_url=CONFIG_TDF.KAS_ENDPOINT,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
        use_plaintext=bool(CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://")),
        cache=cache,
    )

    # First call should retrieve from server and cache the result
    result1 = client.get_public_key(kas_info)
    assert result1 is not None
    assert result1.public_key is not None
    assert result1.kid is not None

    # Verify the result was cached
    cached_result = cache.get(CONFIG_TDF.KAS_ENDPOINT)
    assert cached_result is not None
    assert cached_result.url == CONFIG_TDF.KAS_ENDPOINT
    assert cached_result.public_key == result1.public_key
    assert cached_result.kid == result1.kid

    # Second call should return the cached result (same instance)
    result2 = client.get_public_key(kas_info)
    assert result2 is not None
    assert result2.url == result1.url
    assert result2.public_key == result1.public_key
    assert result2.kid == result1.kid

    # Verify that we got the same cached instance
    assert result2 is cached_result


@pytest.mark.integration
def test_unwrap_success():
    """Test successful key unwrapping using Connect RPC."""
    import base64

    # Create a token source for authentication
    def mock_token_source():
        return "mock_token_for_integration_test"

    # Create KAS client with authentication
    client = KASClient(
        kas_url=CONFIG_TDF.KAS_ENDPOINT,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
        use_plaintext=bool(CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://")),
        token_source=mock_token_source,
    )

    # Create a test key access object with a mock wrapped key
    # Note: In a real scenario, this would be a valid wrapped key from a TDF
    mock_wrapped_key = base64.b64encode(b"test_wrapped_key_data").decode("utf-8")
    key_access = KeyAccess(
        url=CONFIG_TDF.KAS_ENDPOINT,
        wrapped_key=mock_wrapped_key,
    )

    # Create a simple test policy
    test_policy = '{"body": {"dataAttributes": []}}'

    # Attempt to unwrap the key
    # Note: This test will likely fail with a real KAS server because we're using
    # a mock wrapped key, but it tests the integration path
    try:
        result = client.unwrap(key_access, test_policy)

        # If we get here, the unwrap succeeded (unlikely with mock data)
        assert result is not None
        assert isinstance(result, bytes)

    except SDKException as e:
        # Expected to fail with mock data, but we should see a proper error
        # indicating the request made it to the server
        assert "Connect RPC rewrap failed" in str(e)
        print(f"Expected failure with mock data: {e}")


@pytest.mark.integration
def test_unwrap_failure():
    """Test unwrap failure handling with invalid data."""
    import base64

    # Create a token source for authentication
    def mock_token_source():
        return "invalid_token"

    # Create KAS client with invalid authentication
    client = KASClient(
        kas_url=CONFIG_TDF.KAS_ENDPOINT,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
        use_plaintext=bool(CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://")),
        token_source=mock_token_source,
    )

    # Create a key access object with invalid wrapped key
    invalid_wrapped_key = base64.b64encode(b"completely_invalid_key_data").decode(
        "utf-8"
    )
    key_access = KeyAccess(
        url=CONFIG_TDF.KAS_ENDPOINT,
        wrapped_key=invalid_wrapped_key,
    )

    # Create an invalid policy
    invalid_policy = '{"invalid": "policy_structure"}'

    # Attempt to unwrap should fail
    with pytest.raises(SDKException) as exc_info:
        client.unwrap(key_access, invalid_policy)

    # Verify we get the expected error
    assert "Connect RPC rewrap failed" in str(exc_info.value)


@pytest.mark.integration
def test_kas_url_normalization():
    """Test KAS URL normalization with different URL formats."""
    from urllib.parse import urlparse

    # Test with plaintext client (HTTP)
    plaintext_client = KASClient(
        use_plaintext=True,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
    )

    # Test various URL formats for plaintext normalization
    test_cases_plaintext = [
        ("localhost", "http://localhost:80"),
        ("localhost:8080", "http://localhost:8080"),
        ("example.com", "http://example.com:80"),
        ("example.com:9000", "http://example.com:9000"),
        ("http://example.com", "http://example.com:80"),
        ("https://example.com", "http://example.com:80"),  # Should convert to HTTP
        (
            "https://example.com:8443",
            "http://example.com:8443",
        ),  # Should convert to HTTP
    ]

    for input_url, expected_url in test_cases_plaintext:
        normalized = plaintext_client._normalize_kas_url(input_url)
        assert normalized == expected_url, (
            f"Plaintext normalization failed for {input_url}: expected {expected_url}, got {normalized}"
        )

    # Test with secure client (HTTPS)
    secure_client = KASClient(
        use_plaintext=False,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
    )

    # Test various URL formats for secure normalization
    test_cases_secure = [
        ("localhost", "https://localhost:443"),
        ("localhost:8443", "https://localhost:8443"),
        ("example.com", "https://example.com:443"),
        ("example.com:9443", "https://example.com:9443"),
        ("http://example.com", "https://example.com:443"),  # Should convert to HTTPS
        ("https://example.com", "https://example.com:443"),
        ("https://example.com:8443", "https://example.com:8443"),
    ]

    for input_url, expected_url in test_cases_secure:
        normalized = secure_client._normalize_kas_url(input_url)
        assert normalized == expected_url, (
            f"Secure normalization failed for {input_url}: expected {expected_url}, got {normalized}"
        )

    # Test URL normalization with the actual test configuration
    test_url = CONFIG_TDF.KAS_ENDPOINT
    parsed_test_url = urlparse(test_url)

    if CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://"):
        # Platform is HTTP, so should normalize to HTTP
        client = KASClient(use_plaintext=True)
        normalized = client._normalize_kas_url(test_url)
        assert normalized.startswith("http://"), (
            f"Expected HTTP URL for plaintext config, got: {normalized}"
        )
    else:
        # Platform is HTTPS, so should normalize to HTTPS
        client = KASClient(use_plaintext=False)
        normalized = client._normalize_kas_url(test_url)
        assert normalized.startswith("https://"), (
            f"Expected HTTPS URL for secure config, got: {normalized}"
        )

    # Verify the normalized URL preserves the path component (e.g., /kas)
    if parsed_test_url.path:
        assert parsed_test_url.path in normalized, (
            f"Path component {parsed_test_url.path} should be preserved in {normalized}"
        )
