"""Tests for the SDKBuilder class."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import respx

from otdf_python.sdk import SDK
from otdf_python.sdk_builder import SDKBuilder
from otdf_python.sdk_exceptions import AutoConfigureException


def test_sdk_builder_init():
    """Test basic initialization of SDKBuilder."""
    builder = SDKBuilder()
    assert builder.platform_endpoint is None
    assert builder.oauth_config is None
    assert builder.use_plaintext is False
    assert builder.ssl_context is None
    assert builder.auth_token is None


def test_sdk_builder_new_builder():
    """Test the static new_builder method."""
    builder = SDKBuilder.new_builder()
    assert isinstance(builder, SDKBuilder)
    assert builder.platform_endpoint is None
    assert builder.oauth_config is None
    assert builder.use_plaintext is False


def test_platform_endpoint():
    """Test setting platform endpoint."""
    builder = SDKBuilder()

    # Test with plain domain
    result = builder.set_platform_endpoint("example.com")
    assert result is builder  # Returns self for chaining
    assert builder.platform_endpoint == "https://example.com"

    # Test with http://
    result = builder.set_platform_endpoint("http://example.org")
    assert builder.platform_endpoint == "http://example.org"

    # Test with https://
    result = builder.set_platform_endpoint("https://secure.example.com")
    assert builder.platform_endpoint == "https://secure.example.com"

    # Test with use_plaintext=True
    builder.use_plaintext = True
    result = builder.set_platform_endpoint("example.net")
    assert builder.platform_endpoint == "http://example.net"


def test_use_insecure_plaintext_connection():
    """Test setting insecure plaintext connection."""
    builder = SDKBuilder()

    # Set endpoint first, then change connection type
    builder.set_platform_endpoint("secure.example.com")
    assert builder.platform_endpoint == "https://secure.example.com"

    result = builder.use_insecure_plaintext_connection(True)
    assert result is builder  # Returns self for chaining
    assert builder.use_plaintext is True
    assert builder.platform_endpoint == "http://secure.example.com"

    # Change back to secure
    result = builder.use_insecure_plaintext_connection(False)
    assert builder.use_plaintext is False
    assert builder.platform_endpoint == "https://secure.example.com"


def test_client_secret():
    """Test setting client credentials."""
    builder = SDKBuilder()
    result = builder.client_secret("client123", "secret456")

    assert result is builder  # Returns self for chaining
    assert builder.oauth_config is not None
    assert builder.oauth_config.client_id == "client123"
    assert builder.oauth_config.client_secret == "secret456"
    assert builder.oauth_config.grant_type == "client_credentials"


def test_bearer_token():
    """Test setting bearer token."""
    builder = SDKBuilder()
    result = builder.bearer_token("my-token-123")

    assert result is builder  # Returns self for chaining
    assert builder.auth_token == "my-token-123"


def test_ssl_context_from_directory():
    """Test setting up SSL context from certificates directory."""
    builder = SDKBuilder()

    # Create temporary directory with cert files
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create dummy cert files
        tmpdir_path = Path(tmpdirname)
        with (
            (tmpdir_path / "cert1.pem").open("w") as f1,
            (tmpdir_path / "cert2.crt").open("w") as f2,
            (tmpdir_path / "not_a_cert.txt").open("w") as f3,
        ):
            f1.write("dummy cert")
            f2.write("dummy cert")
            f3.write("not a cert")

        # Patch ssl context creation and cert loading to avoid real SSL errors
        with patch("ssl.create_default_context") as mock_create_ctx:
            mock_ctx = MagicMock()
            mock_create_ctx.return_value = mock_ctx
            # Patch load_verify_locations to do nothing
            mock_ctx.load_verify_locations.return_value = None

            # Test the builder method
            result = builder.ssl_context_from_directory(tmpdirname)

            assert result is builder  # Returns self for chaining
            assert len(builder.cert_paths) == 2  # Only .pem and .crt files
            assert any("cert1.pem" in path for path in builder.cert_paths)
            assert any("cert2.crt" in path for path in builder.cert_paths)
            assert not any("not_a_cert.txt" in path for path in builder.cert_paths)


@respx.mock
def test_get_token_from_client_credentials():
    """Test getting OAuth token from client credentials."""
    builder = SDKBuilder()
    builder.set_platform_endpoint("example.com")
    builder.set_issuer_endpoint("https://keycloak.example.com")
    builder.client_secret("client123", "secret456")

    # Mock the discovery endpoint (Keycloak format)
    respx.get(
        "https://keycloak.example.com/realms/opentdf/.well-known/openid-configuration"
    ).respond(
        json={"token_endpoint": "https://keycloak.example.com/oauth/token"},
        status_code=200,
    )

    # Mock the token endpoint
    respx.post("https://keycloak.example.com/oauth/token").respond(
        json={"access_token": "test-token-123", "token_type": "Bearer"}, status_code=200
    )

    # Test the method
    token = builder._get_token_from_client_credentials()
    assert token == "test-token-123"


@respx.mock
def test_get_token_failure():
    """Test handling of token acquisition failure."""
    builder = SDKBuilder()
    builder.set_platform_endpoint("example.com")
    builder.set_issuer_endpoint("https://keycloak.example.com")
    builder.client_secret("client123", "secret456")

    # Mock the discovery endpoint (Keycloak format)
    respx.get(
        "https://keycloak.example.com/realms/opentdf/.well-known/openid-configuration"
    ).respond(
        json={"token_endpoint": "https://keycloak.example.com/oauth/token"},
        status_code=200,
    )

    # Mock the token endpoint with error
    respx.post("https://keycloak.example.com/oauth/token").respond(
        json={"error": "invalid_client"}, status_code=401
    )

    # Test the method
    with pytest.raises(AutoConfigureException) as excinfo:
        builder._get_token_from_client_credentials()

    assert "Token request failed: 401" in str(excinfo.value)


def test_build_without_platform_endpoint():
    """Test building SDK without platform endpoint."""
    builder = SDKBuilder()

    with pytest.raises(AutoConfigureException) as excinfo:
        builder.build()

    assert "Platform endpoint is not set" in str(excinfo.value)


def test_build_success():
    """Test successful SDK build."""
    builder = SDKBuilder()
    builder.set_platform_endpoint("example.com")
    builder.bearer_token("test-token")

    # Mock _create_services to avoid actual service creation
    with patch.object(SDKBuilder, "_create_services") as mock_create_services:
        mock_services = MagicMock(spec=SDK.Services)
        mock_create_services.return_value = mock_services

        # Build the SDK
        sdk = builder.build()

        # Verify the SDK was created correctly
        assert isinstance(sdk, SDK)
        assert sdk.platform_url == "https://example.com"
        assert sdk.get_services() is mock_services
