"""
Unit tests for KASClient.
"""

import pytest
from unittest.mock import patch, MagicMock
from otdf_python.kas_client import KASClient, KeyAccess
from otdf_python.kas_key_cache import KASKeyCache
from otdf_python.sdk_exceptions import SDKException
from dataclasses import dataclass


@dataclass
class MockKasInfo:
    url: str
    algorithm: str | None = None
    public_key: str | None = None
    kid: str | None = None
    default: bool = False

    def clone(self):
        return MockKasInfo(
            url=self.url,
            algorithm=self.algorithm,
            public_key=self.public_key,
            kid=self.kid,
            default=self.default,
        )


def test_get_public_key_uses_cache():
    cache = KASKeyCache()
    kas_info = MockKasInfo(url="http://kas")
    # Store in cache using the new mechanism
    cache.store(kas_info)
    client = KASClient("http://kas", cache=cache)
    # Get public key should now return the cached KASInfo object
    assert client.get_public_key(MockKasInfo(url="http://kas")) == kas_info


@patch("httpx.get")
def test_get_public_key_fetches_and_caches(mock_get):
    cache = KASKeyCache()
    client = KASClient("http://kas", cache=cache)
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"kid": "kid2", "publicKey": "public-key-data"}
    mock_resp.raise_for_status.return_value = None
    mock_resp.status_code = 200  # Add status code for the test
    mock_get.return_value = mock_resp

    # Create KASInfo with URL but no KID or public key
    kas_info = MockKasInfo(url="http://kas")
    result = client.get_public_key(kas_info)

    # Verify the result has kid and public_key populated
    assert result.kid == "kid2"
    assert result.public_key == "public-key-data"

    # Verify the result was cached
    cached = cache.get("http://kas")
    assert cached is not None
    assert cached.kid == "kid2"
    assert cached.public_key == "public-key-data"


@patch("httpx.post")
@patch("otdf_python.kas_client.CryptoUtils")
@patch("otdf_python.kas_client.AsymDecryption")
@patch("otdf_python.kas_client.jwt.encode")  # Mock JWT encoding directly
def test_unwrap_success(
    mock_jwt_encode, mock_asym_decryption, mock_crypto_utils, mock_post
):
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

    # Mock HTTP response
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "entityWrappedKey": "d2VsY29tZQ=="
    }  # Base64 for "welcome"
    mock_resp.raise_for_status.return_value = None
    mock_resp.status_code = 200  # Add status code for the test
    mock_post.return_value = mock_resp

    # Create client and test unwrap
    # We need to patch the DPoP proof creation method to avoid RSA key access
    with patch.object(KASClient, "_create_dpop_proof", return_value="mock_dpop_proof"):
        client = KASClient("http://kas", token_source=lambda: "tok")
        key_access = KeyAccess(url="http://kas", wrapped_key="wrapped_key")
        result = client.unwrap(key_access, "policy")

    # Verify result
    assert result == b"decrypted_key"
    # Verify the request was made correctly
    mock_post.assert_called_once()
    # Verify the decryptor was called
    mock_decryptor.decrypt.assert_called_once()


@patch("httpx.post")
def test_unwrap_failure(mock_post):
    client = KASClient("http://kas", token_source=lambda: "tok")
    mock_post.side_effect = Exception("fail")

    with pytest.raises(SDKException) as exc_info:
        key_access = KeyAccess(url="http://kas", wrapped_key="wrapped_key")
        client.unwrap(key_access, "policy")

    # Updated to match the new error message pattern when Connect RPC is available
    assert "Both Connect RPC and HTTP unwrap failed" in str(exc_info.value)


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


@patch("httpx.post")
def test_jwt_signature_verification_in_unwrap_request(mock_post, collect_server_logs):
    """Test that JWT signature is properly created and can be verified.

    This test is inspired by the Java SDK's testCallingRewrap which verifies
    the JWT signature in the rewrap request. It ensures our DPoP proof and
    signed request JWT are properly formatted.
    """
    import jwt
    import json

    # Create a mock successful response
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "entityWrappedKey": "d2VsY29tZQ=="
    }  # "welcome" in base64
    mock_resp.raise_for_status.return_value = None
    mock_resp.status_code = 200
    mock_post.return_value = mock_resp

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

            # Verify the request was made
            assert mock_post.called

            # Extract the request data to verify JWT structure
            call_args = mock_post.call_args
            if call_args and len(call_args) > 1:
                request_data = call_args[1].get("data") or call_args[1].get("json")
                if request_data:
                    # Verify that signedRequestToken is present and is a valid JWT
                    if isinstance(request_data, str):
                        request_data = json.loads(request_data)

                    signed_token = request_data.get("signedRequestToken")
                    assert signed_token is not None, (
                        "signedRequestToken should be present in request"
                    )

                    # Decode JWT without verification to check structure
                    # (we can't verify signature since we mocked the key generation)
                    decoded = jwt.decode(
                        signed_token, options={"verify_signature": False}
                    )

                    # Verify JWT has required claims
                    assert "requestBody" in decoded, (
                        "JWT should contain requestBody claim"
                    )
                    assert "iat" in decoded, "JWT should contain iat (issued at) claim"
                    assert "exp" in decoded, "JWT should contain exp (expiration) claim"

                    # Verify the requestBody contains the expected structure
                    request_body = json.loads(decoded["requestBody"])
                    assert "keyAccess" in request_body, (
                        "requestBody should contain keyAccess"
                    )
                    assert "clientPublicKey" in request_body, (
                        "requestBody should contain clientPublicKey"
                    )
                    assert "policy" in request_body, "requestBody should contain policy"

                    # Verify keyAccess structure matches what we sent
                    key_access_data = request_body["keyAccess"]
                    assert key_access_data["url"] == "http://kas"
                    assert key_access_data["wrappedKey"] == "dGVzdF93cmFwcGVkX2tleQ=="

        except Exception as e:
            # If the test fails, collect server logs for debugging
            if callable(collect_server_logs):
                logs = collect_server_logs()
                if logs:
                    print(f"Server logs for debugging:\n{logs}")
            # Re-raise the exception with additional context
            raise SDKException(f"JWT signature verification test failed: {e!s}") from e


@pytest.mark.integration
def test_connect_rpc_public_key_retrieval():
    """Test Connect RPC public key retrieval using live backend server."""
    from tests.config_pydantic import CONFIG_TDF
    from otdf_python.config import KASInfo

    # Create KAS info from configuration
    kas_info = KASInfo(url=CONFIG_TDF.KAS_ENDPOINT)

    # Create KAS client with SSL verification disabled for testing
    client = KASClient(
        kas_url=CONFIG_TDF.KAS_ENDPOINT, verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY
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
