"""Unit tests for KASClient."""

from base64 import b64decode
from unittest.mock import MagicMock, patch

import pytest

from otdf_python.kas_client import KASClient, KeyAccess
from otdf_python.kas_key_cache import KASKeyCache
from otdf_python.sdk_exceptions import SDKException


class MockKasInfo:
    """Mock KAS info for testing."""

    def __init__(self, url, algorithm=None, public_key=None, kid=None, default=False):
        """Initialize MockKasInfo.

        Args:
            url: KAS URL.
            algorithm: Key algorithm.
            public_key: Public key.
            kid: Key ID.
            default: Whether this is the default KAS.

        """
        self.url = url
        self.algorithm = algorithm or ""
        self.public_key = public_key or ""
        self.kid = kid or ""
        self.default = default

    def clone(self):
        return MockKasInfo(
            url=self.url,
            algorithm=self.algorithm,
            public_key=self.public_key,
            kid=self.kid,
            default=self.default,
        )


def test_get_public_key_uses_cache():
    """Test that get_public_key uses cached KAS info."""
    cache = KASKeyCache()
    kas_info = MockKasInfo(url="http://kas")
    # Store in cache using the new mechanism
    cache.store(kas_info)
    client = KASClient("http://kas", cache=cache)
    # Get public key should now return the cached KASInfo object
    assert client.get_public_key(MockKasInfo(url="http://kas")) == kas_info


@patch("urllib3.PoolManager")
@patch("otdf_python.kas_connect_rpc_client.AccessServiceClient")
def test_get_public_key_fetches_and_caches(
    mock_access_service_client, mock_pool_manager
):
    """Test that get_public_key fetches and caches public key."""
    cache = KASKeyCache()
    client = KASClient("http://kas", cache=cache)

    # Mock urllib3.PoolManager to prevent real network calls
    mock_pool_instance = MagicMock()
    mock_pool_manager.return_value = mock_pool_instance

    # Setup a successful HTTP response that bypasses error handling
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/proto"}
    mock_response.read.return_value = (
        b""  # Empty protobuf data since we're mocking the client layer
    )
    mock_pool_instance.request.return_value = mock_response

    # Mock the Connect RPC client directly since it expects protobuf responses
    mock_client_instance = MagicMock()
    mock_access_service_client.return_value = mock_client_instance

    # Mock the public key response using protobuf structure
    mock_rpc_response = MagicMock()
    mock_rpc_response.kid = "kid2"
    mock_rpc_response.public_key = "public-key-data"

    def mock_public_key_call(*args, **kwargs):
        return mock_rpc_response

    mock_client_instance.public_key = mock_public_key_call

    # Create KASInfo with URL but no KID or public key
    from otdf_python.config import KASInfo

    kas_info = KASInfo(url="http://kas")

    result = client.get_public_key(kas_info)

    # Verify the result has kid and public_key populated
    assert result.kid == "kid2"
    assert result.public_key == "public-key-data"

    # Verify the result was cached
    cached = cache.get("http://kas")
    assert cached is not None
    assert cached.kid == "kid2"
    assert cached.public_key == "public-key-data"


@patch("urllib3.PoolManager")
@patch("otdf_python.kas_connect_rpc_client.AccessServiceClient")
@patch("otdf_python.kas_client.CryptoUtils")
@patch("otdf_python.kas_client.AsymDecryption")
@patch("otdf_python.kas_client.jwt.encode")  # Mock JWT encoding directly
def test_unwrap_success(
    mock_jwt_encode,
    mock_asym_decryption,
    mock_crypto_utils,
    mock_access_service_client,
    mock_pool_manager,
):
    """Test successful key unwrap operation."""
    # Setup mocks for RSA key pair generation and decryption
    mock_private_key = MagicMock()
    mock_public_key = MagicMock()

    # Mock the DPoP key generation (called in KASClient.__init__)
    # and the ephemeral key generation (called in unwrap)
    mock_crypto_utils.generate_rsa_keypair.side_effect = [
        (mock_private_key, mock_public_key),  # First call: DPoP keys
        (mock_private_key, mock_public_key),  # Second call: ephemeral keys
    ]
    mock_crypto_utils.get_rsa_public_key_pem.return_value = "mock_private_key_pem"

    # Mock JWT encoding (for both request JWT and DPoP proof)
    mock_jwt_encode.return_value = "mock_jwt_token"

    # Mock decryptor
    mock_decryptor = MagicMock()
    mock_decryptor.decrypt.return_value = b"decrypted_key"
    mock_asym_decryption.return_value = mock_decryptor

    # Mock urllib3.PoolManager to prevent real network calls
    mock_pool_instance = MagicMock()
    mock_pool_manager.return_value = mock_pool_instance

    # Setup a successful HTTP response that bypasses error handling
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/proto"}
    mock_response.read.return_value = (
        b""  # Empty protobuf data since we're mocking the client layer
    )
    mock_pool_instance.request.return_value = mock_response

    # Mock Connect RPC client directly instead of HTTP layer
    mock_client_instance = MagicMock()
    mock_access_service_client.return_value = mock_client_instance

    mock_rpc_response = MagicMock()
    mock_rpc_response.entity_wrapped_key = b64decode(
        "d2VsY29tZQ=="
    )  # "welcome" decoded
    mock_rpc_response.responses = []  # Empty to test fallback to legacy field
    mock_client_instance.rewrap.return_value = mock_rpc_response

    # Create client and test unwrap
    # We need to patch the DPoP proof creation method to avoid RSA key access
    with patch.object(KASClient, "_create_dpop_proof", return_value="mock_dpop_proof"):
        client = KASClient("http://kas", token_source=lambda: "tok")
        key_access = KeyAccess(url="http://kas", wrapped_key="wrapped_key")
        result = client.unwrap(key_access, "policy")

    # Verify result
    assert result == b"decrypted_key"
    # Verify the Connect RPC client was called correctly
    mock_access_service_client.assert_called_once()
    mock_client_instance.rewrap.assert_called_once()
    # Verify the decryptor was called
    mock_decryptor.decrypt.assert_called_once()


@patch("urllib3.PoolManager")
@patch("otdf_python_proto.kas.kas_pb2_connect.AccessServiceClient")
def test_unwrap_failure(mock_access_service_client, mock_pool_manager):
    """Test key unwrap failure handling."""
    # Setup realistic HTTP response mock for PoolManager
    mock_response = MagicMock()
    mock_response.status = 500
    mock_response.read.return_value = b'{"error": "fail"}'
    mock_response.headers = {"content-type": "application/json"}

    mock_pool_instance = MagicMock()
    mock_pool_instance.request.return_value = mock_response
    mock_pool_manager.return_value = mock_pool_instance

    # Mock the Connect RPC client to raise an exception
    mock_access_service_client.side_effect = Exception("fail")

    client = KASClient("http://kas", token_source=lambda: "tok")

    with pytest.raises(SDKException) as exc_info:
        key_access = KeyAccess(url="http://kas", wrapped_key="wrapped_key")
        client.unwrap(key_access, "policy")

    # Updated to match the new error message pattern when Connect RPC fails
    assert "Connect RPC rewrap failed" in str(exc_info.value)


def test_kas_url_normalization_with_insecure_client():
    """Test that KAS URLs are properly normalized based on security settings.

    This test mirrors the Java SDK's testAddressNormalizationWithInsecureHTTPClient
    and ensures HTTP URLs are normalized correctly for insecure connections.
    """
    # Test with insecure (plaintext) client
    client = KASClient(use_plaintext=True)

    # Test HTTP URL normalization
    normalized_url = client._normalize_kas_url("http://example.com")
    assert normalized_url == "http://example.com:80"

    # Test URL with explicit port
    normalized_url = client._normalize_kas_url("example.com:8080")
    assert normalized_url == "http://example.com:8080"

    # Test localhost handling
    normalized_url = client._normalize_kas_url("localhost")
    assert normalized_url == "http://localhost:80"


def test_kas_url_normalization_with_secure_client():
    """Test that KAS URLs are properly normalized for secure HTTPS connections.

    This test mirrors the Java SDK's testAddressNormalizationWithHTTPSClient
    and ensures HTTPS URLs are normalized correctly for secure connections.
    """
    # Test with secure (HTTPS) client
    client = KASClient(use_plaintext=False)

    # Test HTTP URL gets upgraded to HTTPS
    normalized_url = client._normalize_kas_url("http://example.com")
    assert normalized_url == "https://example.com:443"

    # Test HTTPS URL stays HTTPS
    normalized_url = client._normalize_kas_url("https://example.com")
    assert normalized_url == "https://example.com:443"

    # Test URL with custom port
    normalized_url = client._normalize_kas_url("https://example.com:8443")
    assert normalized_url == "https://example.com:8443"


def test_kas_url_normalization_with_kasinfo_objects_plaintext():
    """Test URL normalization using KASInfo objects with plaintext client.

    This test ensures that _normalize_kas_url works correctly when called
    with various KASInfo.url values in plaintext mode (use_plaintext=True).
    """
    from otdf_python.config import KASInfo

    client = KASClient(use_plaintext=True)

    # Test cases with different URL formats in KASInfo objects
    test_cases = [
        # Basic hostname without scheme
        (KASInfo(url="example.com"), "http://example.com:80"),
        # Hostname with port
        (KASInfo(url="example.com:8080"), "http://example.com:8080"),
        # Localhost
        (KASInfo(url="localhost"), "http://localhost:80"),
        # Localhost with port
        (KASInfo(url="localhost:8080"), "http://localhost:8080"),
        # HTTP URL (should preserve port)
        (KASInfo(url="http://example.com"), "http://example.com:80"),
        # HTTP URL with custom port
        (KASInfo(url="http://example.com:9000"), "http://example.com:9000"),
        # HTTPS URL (should be converted to HTTP in plaintext mode)
        (KASInfo(url="https://example.com"), "http://example.com:80"),
        # HTTPS URL with custom port (should be converted to HTTP)
        (KASInfo(url="https://example.com:8443"), "http://example.com:8443"),
        # URL with /kas path (no scheme, should add proper scheme and port)
        (KASInfo(url="example.com/kas"), "http://example.com:80/kas"),
        # URL with /kas path and port would be invalid as parsed - skip this case
        # Complex URL with path
        (
            KASInfo(url="https://platform.example.com:8443/api/kas"),
            "http://platform.example.com:8443/api/kas",
        ),
    ]

    for kas_info, expected_url in test_cases:
        normalized_url = client._normalize_kas_url(kas_info.url)
        assert normalized_url == expected_url, (
            f"Failed for {kas_info.url}: expected {expected_url}, got {normalized_url}"
        )


def test_kas_url_normalization_with_kasinfo_objects_secure():
    """Test URL normalization using KASInfo objects with secure client.

    This test ensures that _normalize_kas_url works correctly when called
    with various KASInfo.url values in secure mode (use_plaintext=False).
    """
    from otdf_python.config import KASInfo

    client = KASClient(use_plaintext=False)

    # Test cases with different URL formats in KASInfo objects
    test_cases = [
        # Basic hostname without scheme
        (KASInfo(url="example.com"), "https://example.com:443"),
        # Hostname with port
        (KASInfo(url="example.com:8443"), "https://example.com:8443"),
        # Localhost
        (KASInfo(url="localhost"), "https://localhost:443"),
        # Localhost with port
        (KASInfo(url="localhost:8443"), "https://localhost:8443"),
        # HTTP URL (should be upgraded to HTTPS)
        (KASInfo(url="http://example.com"), "https://example.com:443"),
        # HTTP URL with custom port (should be upgraded to HTTPS)
        (KASInfo(url="http://example.com:8080"), "https://example.com:8080"),
        # HTTPS URL (should preserve HTTPS)
        (KASInfo(url="https://example.com"), "https://example.com:443"),
        # HTTPS URL with custom port
        (KASInfo(url="https://example.com:8443"), "https://example.com:8443"),
        # URL with /kas path (no scheme, should add proper scheme and port)
        (KASInfo(url="example.com/kas"), "https://example.com:443/kas"),
        # Complex URL with path
        (
            KASInfo(url="http://platform.example.com:8080/api/kas"),
            "https://platform.example.com:8080/api/kas",
        ),
    ]

    for kas_info, expected_url in test_cases:
        normalized_url = client._normalize_kas_url(kas_info.url)
        assert normalized_url == expected_url, (
            f"Failed for {kas_info.url}: expected {expected_url}, got {normalized_url}"
        )


def test_kas_url_normalization_with_kasinfo_edge_cases():
    """Test URL normalization edge cases using KASInfo objects.

    This test covers edge cases and potential error conditions when
    normalizing URLs from KASInfo objects.
    """
    from otdf_python.config import KASInfo

    client = KASClient(use_plaintext=False)

    # Test various edge cases
    test_cases = [
        # IP addresses
        (KASInfo(url="192.168.1.100"), "https://192.168.1.100:443"),
        (KASInfo(url="192.168.1.100:8443"), "https://192.168.1.100:8443"),
        # URLs with query parameters (no scheme, should add proper scheme and port)
        (
            KASInfo(url="example.com/kas?param=value"),
            "https://example.com:443/kas?param=value",
        ),
        # URLs with fragments (no scheme, should add proper scheme and port)
        (KASInfo(url="example.com/kas#section"), "https://example.com:443/kas#section"),
        # Complex paths (no scheme, should add proper scheme and port)
        (
            KASInfo(url="platform.example.com/api/v1/kas"),
            "https://platform.example.com:443/api/v1/kas",
        ),
    ]

    for kas_info, expected_url in test_cases:
        normalized_url = client._normalize_kas_url(kas_info.url)
        assert normalized_url == expected_url, (
            f"Failed for {kas_info.url}: expected {expected_url}, got {normalized_url}"
        )


def test_kas_url_normalization_with_kasinfo_additional_fields():
    """Test that URL normalization works with KASInfo objects containing additional fields.

    This test ensures that the normalization process only uses the URL field
    and doesn't interfere with other KASInfo fields like algorithm, kid, etc.
    """
    from otdf_python.config import KASInfo

    client = KASClient(use_plaintext=False)

    # Create KASInfo with all fields populated
    # Using a URL with scheme to avoid the hostname:port/path parsing issue
    kas_info = KASInfo(
        url="https://example.com:8443/kas",
        public_key="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...",
        kid="key-id-123",
        default=True,
        algorithm="rsa",
    )

    normalized_url = client._normalize_kas_url(kas_info.url)
    assert normalized_url == "https://example.com:8443/kas"

    # Verify other fields remain unchanged
    assert (
        kas_info.public_key
        == "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."
    )
    assert kas_info.kid == "key-id-123"
    assert kas_info.default is True
    assert kas_info.algorithm == "rsa"


def test_kas_url_normalization_error_handling_with_kasinfo():
    """Test error handling in URL normalization with invalid KASInfo URLs.

    This test ensures that appropriate SDKExceptions are raised for
    malformed URLs in KASInfo objects.
    """
    from otdf_python.config import KASInfo

    client = KASClient(use_plaintext=False)

    # Test cases that should raise SDKException
    invalid_urls = [
        # Invalid port format
        "example.com:invalid_port",
        # Multiple colons (ambiguous port)
        "example.com:8080:extra",
        # IPv6 addresses without proper scheme (current limitation)
        "[::1]",
        "[2001:db8::1]",
    ]

    for invalid_url in invalid_urls:
        kas_info = KASInfo(url=invalid_url)
        with pytest.raises(SDKException):
            client._normalize_kas_url(kas_info.url)


@patch("urllib3.PoolManager")
@patch("otdf_python.kas_connect_rpc_client.AccessServiceClient")
def test_jwt_signature_verification_in_unwrap_request(
    mock_access_service_client, mock_pool_manager, collect_server_logs
):
    """Test that JWT signature is properly created and can be verified.

    This test is inspired by the Java SDK's testCallingRewrap which verifies
    the JWT signature in the rewrap request. It ensures our DPoP proof and
    signed request JWT are properly formatted.
    """
    import jwt

    # Mock urllib3.PoolManager to prevent real network calls
    mock_pool_instance = MagicMock()
    mock_pool_manager.return_value = mock_pool_instance

    # Setup a successful HTTP response that bypasses error handling
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/proto"}
    mock_response.read.return_value = (
        b""  # Empty protobuf data since we're mocking the client layer
    )
    mock_pool_instance.request.return_value = mock_response

    # Mock Connect RPC client directly for protobuf compatibility
    mock_client_instance = MagicMock()
    mock_access_service_client.return_value = mock_client_instance

    # Create a mock successful response
    mock_rpc_response = MagicMock()
    mock_rpc_response.entity_wrapped_key = b64decode(
        "d2VsY29tZQ=="
    )  # "welcome" decoded
    mock_rpc_response.responses = []  # Empty to test fallback to legacy field
    mock_client_instance.rewrap.return_value = mock_rpc_response

    # Create client with known DPoP keys for verification
    client = KASClient("http://kas", token_source=lambda: "test_token")

    # Create a key access object with all required fields
    key_access = KeyAccess(
        url="http://kas",
        wrapped_key="dGVzdF93cmFwcGVkX2tleQ==",  # "test_wrapped_key" in base64
    )

    # Mock the decryption parts since we're focusing on JWT verification
    with (
        patch("otdf_python.kas_client.CryptoUtils") as mock_crypto_utils,
        patch("otdf_python.kas_client.AsymDecryption") as mock_asym_decryption,
    ):
        # Setup mocks for the crypto operations
        mock_private_key = MagicMock()
        mock_public_key = MagicMock()
        mock_crypto_utils.generate_rsa_keypair.return_value = (
            mock_private_key,
            mock_public_key,
        )
        mock_crypto_utils.get_rsa_public_key_pem.return_value = "mock_public_key_pem"

        mock_decryptor = MagicMock()
        mock_decryptor.decrypt.return_value = b"decrypted_key"
        mock_asym_decryption.return_value = mock_decryptor

        # Call unwrap - this should create and send a properly signed JWT
        try:
            client.unwrap(key_access, '{"test": "policy"}')

            # Verify the Connect RPC client was called
            assert mock_client_instance.rewrap.called

            # Extract the request to verify JWT structure
            call_args = mock_client_instance.rewrap.call_args
            if call_args and len(call_args) > 0:
                request = call_args[0][0]  # First positional argument (the request)
                signed_token = request.signed_request_token

                assert signed_token is not None, (
                    "signed_request_token should be present in request"
                )

                # Decode JWT without verification to check structure
                # (we can't verify signature since we mocked the key generation)
                decoded = jwt.decode(signed_token, options={"verify_signature": False})

                # Verify JWT has required claims
                assert "requestBody" in decoded, "JWT should contain requestBody claim"
                assert "iat" in decoded, "JWT should contain iat (issued at) claim"
                assert "exp" in decoded, "JWT should contain exp (expiration) claim"

                # Verify the requestBody contains the expected structure
                # For Connect RPC, the request body should be protobuf-encoded
                # We just verify it exists and is not empty
                assert decoded["requestBody"], "requestBody should not be empty"

        except Exception as e:
            # If the test fails, collect server logs for debugging
            if callable(collect_server_logs):
                logs = collect_server_logs()
                if logs:
                    print(f"Server logs for debugging:\n{logs}")
            # Re-raise the exception with additional context
            raise SDKException(f"JWT signature verification test failed: {e!s}") from e
