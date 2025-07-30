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
    algorithm: str = None
    public_key: str = None
    kid: str = None
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
def test_unwrap_success(mock_asym_decryption, mock_crypto_utils, mock_post):
    # Setup mocks for RSA key pair generation and decryption
    mock_private_key = MagicMock()
    mock_public_key = MagicMock()
    mock_crypto_utils.generate_rsa_keypair.return_value = (
        mock_private_key,
        mock_public_key,
    )
    mock_crypto_utils.get_rsa_public_key_pem.return_value = "mock_public_key_pem"

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
    mock_post.return_value = mock_resp

    # Create client and test unwrap
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

    assert "Error unwrapping key" in str(exc_info.value)
