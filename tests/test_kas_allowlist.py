"""Tests for the KAS allowlist functionality.

This module tests the KASAllowlist class which provides protection against
SSRF attacks where malicious TDF files could contain attacker-controlled
KAS URLs to steal OIDC credentials.
"""

import logging

import pytest

from otdf_python.kas_allowlist import KASAllowlist
from otdf_python.kas_client import KASClient
from otdf_python.sdk import SDK
from otdf_python.sdk_builder import SDKBuilder


class TestKASAllowlist:
    """Test cases for the KASAllowlist class."""

    def test_empty_allowlist_rejects_all(self):
        """Empty allowlist should reject all URLs."""
        allowlist = KASAllowlist()
        assert not allowlist.is_allowed("https://example.com")
        assert not allowlist.is_allowed("https://evil.com")

    def test_add_and_check_urls(self):
        """Test adding URLs and checking if they are allowed."""
        allowlist = KASAllowlist()
        allowlist.add("https://kas.example.com")

        assert allowlist.is_allowed("https://kas.example.com")
        assert allowlist.is_allowed("https://kas.example.com/kas")
        assert allowlist.is_allowed("https://kas.example.com:443/some/path")
        assert not allowlist.is_allowed("https://evil.com")
        assert not allowlist.is_allowed("https://kas.evil.com")

    def test_constructor_with_urls(self):
        """Test initializing with a list of URLs."""
        allowlist = KASAllowlist(
            ["https://kas1.example.com", "https://kas2.example.com"]
        )

        assert allowlist.is_allowed("https://kas1.example.com")
        assert allowlist.is_allowed("https://kas2.example.com")
        assert not allowlist.is_allowed("https://kas3.example.com")

    def test_allow_all_mode(self):
        """Test allow_all mode allows everything."""
        allowlist = KASAllowlist(allow_all=True)

        assert allowlist.is_allowed("https://any.domain.com")
        assert allowlist.is_allowed("https://evil.com")
        assert allowlist.is_allowed("http://localhost:8080")

    def test_origin_normalization_strips_path(self):
        """Test that paths are stripped when normalizing origins."""
        allowlist = KASAllowlist()
        allowlist.add("https://kas.example.com/some/path")

        # Should allow any path on the same origin
        assert allowlist.is_allowed("https://kas.example.com")
        assert allowlist.is_allowed("https://kas.example.com/different/path")
        assert allowlist.is_allowed("https://kas.example.com/kas")

    def test_origin_normalization_default_ports(self):
        """Test that default ports are normalized correctly."""
        allowlist = KASAllowlist()
        allowlist.add("https://kas.example.com")  # Implies port 443

        # Should match with explicit port 443
        assert allowlist.is_allowed("https://kas.example.com:443")
        assert allowlist.is_allowed("https://kas.example.com:443/kas")

        # Should NOT match different port
        assert not allowlist.is_allowed("https://kas.example.com:8443")

    def test_origin_normalization_http_default_port(self):
        """Test that HTTP default port (80) is normalized correctly."""
        allowlist = KASAllowlist()
        allowlist.add("http://kas.example.com")

        assert allowlist.is_allowed("http://kas.example.com:80")
        assert not allowlist.is_allowed("http://kas.example.com:8080")

    def test_origin_normalization_explicit_port(self):
        """Test that explicit ports are preserved."""
        allowlist = KASAllowlist()
        allowlist.add("https://kas.example.com:8443")

        assert allowlist.is_allowed("https://kas.example.com:8443")
        assert allowlist.is_allowed("https://kas.example.com:8443/kas")
        assert not allowlist.is_allowed("https://kas.example.com:443")
        assert not allowlist.is_allowed("https://kas.example.com")

    def test_origin_normalization_adds_scheme(self):
        """Test that missing schemes default to https."""
        allowlist = KASAllowlist()
        allowlist.add("kas.example.com")

        assert allowlist.is_allowed("https://kas.example.com")
        assert not allowlist.is_allowed("http://kas.example.com")

    def test_case_insensitive_hostname(self):
        """Test that hostname comparison is case-insensitive."""
        allowlist = KASAllowlist()
        allowlist.add("https://KAS.Example.COM")

        assert allowlist.is_allowed("https://kas.example.com")
        assert allowlist.is_allowed("https://KAS.EXAMPLE.COM")

    def test_validate_raises_exception(self):
        """Test that validate() raises exception for disallowed URLs."""
        allowlist = KASAllowlist(["https://trusted.com"])

        # Should not raise for allowed URL
        allowlist.validate("https://trusted.com/kas")

        # Should raise for disallowed URL
        with pytest.raises(SDK.KasAllowlistException) as excinfo:
            allowlist.validate("https://evil.com/kas")

        assert "evil.com" in str(excinfo.value)
        assert "trusted.com" in str(excinfo.value)

    def test_exception_contains_url_and_origins(self):
        """Test that exception contains useful debugging information."""
        allowlist = KASAllowlist(["https://kas1.com", "https://kas2.com"])

        with pytest.raises(SDK.KasAllowlistException) as excinfo:
            allowlist.validate("https://attacker.com")

        exception = excinfo.value
        assert exception.url == "https://attacker.com"
        assert "https://kas1.com:443" in exception.allowed_origins
        assert "https://kas2.com:443" in exception.allowed_origins

    def test_allowed_origins_property(self):
        """Test the allowed_origins property returns a copy."""
        allowlist = KASAllowlist(["https://example.com"])

        origins = allowlist.allowed_origins
        origins.add("https://modified.com")

        # Original should not be modified
        assert "https://modified.com:443" not in allowlist.allowed_origins

    def test_from_platform_url(self):
        """Test creating allowlist from platform URL."""
        allowlist = KASAllowlist.from_platform_url("https://platform.example.com")

        # Should allow the platform URL
        assert allowlist.is_allowed("https://platform.example.com")
        # Should allow the /kas endpoint
        assert allowlist.is_allowed("https://platform.example.com/kas")

    def test_from_platform_url_with_trailing_slash(self):
        """Test creating allowlist from platform URL with trailing slash."""
        allowlist = KASAllowlist.from_platform_url("https://platform.example.com/")

        assert allowlist.is_allowed("https://platform.example.com")
        assert allowlist.is_allowed("https://platform.example.com/kas")

    def test_allow_all_logs_warning(self, caplog):
        """Test that allow_all mode logs a warning."""
        with caplog.at_level(logging.WARNING):
            KASAllowlist(allow_all=True)

        assert "insecure" in caplog.text.lower()


class TestKASClientAllowlistIntegration:
    """Test KASClient integration with allowlist."""

    def test_client_without_allowlist_allows_all(self):
        """Client without allowlist should allow all URLs (backward compatibility)."""
        client = KASClient(kas_allowlist=None)

        # Should not raise - no validation without allowlist
        normalized = client._normalize_kas_url("https://any.domain.com/kas")
        assert "any.domain.com" in normalized

    def test_client_with_allowlist_validates(self):
        """Client with allowlist should validate URLs."""
        allowlist = KASAllowlist(["https://trusted.kas.com"])
        client = KASClient(kas_allowlist=allowlist)

        # Should work for trusted URL
        normalized = client._normalize_kas_url("https://trusted.kas.com/kas")
        assert "trusted.kas.com" in normalized

        # Should raise for untrusted URL
        with pytest.raises(SDK.KasAllowlistException):
            client._normalize_kas_url("https://evil.com/kas")

    def test_client_allowlist_checked_before_normalization(self):
        """Allowlist should be checked before any network operations."""
        allowlist = KASAllowlist(["https://trusted.com"])
        client = KASClient(kas_allowlist=allowlist)

        # Even malformed URLs should be rejected if not in allowlist
        with pytest.raises(SDK.KasAllowlistException):
            client._normalize_kas_url("https://evil.com")


class TestSDKBuilderAllowlist:
    """Test SDKBuilder allowlist configuration."""

    def test_with_kas_allowlist(self):
        """Test configuring explicit allowlist."""
        builder = SDKBuilder()
        result = builder.with_kas_allowlist(["https://kas1.com", "https://kas2.com"])

        assert result is builder  # Returns self for chaining
        assert builder._kas_allowlist_urls == ["https://kas1.com", "https://kas2.com"]

    def test_with_ignore_kas_allowlist(self):
        """Test ignoring allowlist."""
        builder = SDKBuilder()
        result = builder.with_ignore_kas_allowlist(True)

        assert result is builder
        assert builder._ignore_kas_allowlist is True

    def test_with_ignore_kas_allowlist_false(self):
        """Test explicitly not ignoring allowlist."""
        builder = SDKBuilder()
        builder.with_ignore_kas_allowlist(True)
        builder.with_ignore_kas_allowlist(False)

        assert builder._ignore_kas_allowlist is False

    def test_create_kas_allowlist_from_platform_url(self):
        """Test that allowlist is created from platform URL by default."""
        builder = SDKBuilder()
        builder.set_platform_endpoint("https://platform.example.com")

        allowlist = builder._create_kas_allowlist()

        assert allowlist is not None
        assert allowlist.is_allowed("https://platform.example.com")
        assert allowlist.is_allowed("https://platform.example.com/kas")
        assert not allowlist.is_allowed("https://other.com")

    def test_create_kas_allowlist_explicit(self):
        """Test that explicit allowlist is used when provided."""
        builder = SDKBuilder()
        builder.set_platform_endpoint("https://platform.example.com")
        builder.with_kas_allowlist(["https://external-kas.com"])

        allowlist = builder._create_kas_allowlist()

        assert allowlist is not None
        # Should include explicit URL
        assert allowlist.is_allowed("https://external-kas.com")
        # Should also include platform URL
        assert allowlist.is_allowed("https://platform.example.com")

    def test_create_kas_allowlist_ignore(self):
        """Test that allow_all is returned when ignoring."""
        builder = SDKBuilder()
        builder.set_platform_endpoint("https://platform.example.com")
        builder.with_ignore_kas_allowlist(True)

        allowlist = builder._create_kas_allowlist()

        assert allowlist is not None
        assert allowlist.allow_all is True
        assert allowlist.is_allowed("https://any.domain.com")

    def test_allowlist_with_ignore_logs_warning(self, caplog):
        """Test that ignoring allowlist logs a warning."""
        builder = SDKBuilder()

        with caplog.at_level(logging.WARNING):
            builder.with_ignore_kas_allowlist(True)

        assert "insecure" in caplog.text.lower()


class TestSSRFProtection:
    """Test SSRF protection scenarios."""

    def test_malicious_tdf_url_rejected(self):
        """Simulate a malicious TDF with attacker-controlled KAS URL."""
        # Simulate SDK configured with platform URL
        allowlist = KASAllowlist.from_platform_url("https://legitimate-platform.com")
        client = KASClient(kas_allowlist=allowlist)

        # Attacker crafts TDF with their KAS URL
        malicious_kas_url = "https://attacker.evil.com/steal-tokens"

        # SDK should reject this URL before sending any credentials
        with pytest.raises(SDK.KasAllowlistException) as excinfo:
            client._normalize_kas_url(malicious_kas_url)

        assert "attacker.evil.com" in str(excinfo.value)

    def test_legitimate_kas_url_accepted(self):
        """Verify legitimate KAS URLs are accepted."""
        allowlist = KASAllowlist.from_platform_url("https://platform.company.com")
        client = KASClient(kas_allowlist=allowlist)

        # TDF with legitimate KAS URL should work
        legitimate_url = "https://platform.company.com/kas"
        normalized = client._normalize_kas_url(legitimate_url)

        assert "platform.company.com" in normalized

    def test_multi_kas_deployment(self):
        """Test deployment with multiple KAS servers."""
        # Organization has multiple KAS servers
        allowlist = KASAllowlist(
            [
                "https://kas-primary.company.com",
                "https://kas-secondary.company.com",
                "https://kas-dr.company.com",
            ]
        )
        client = KASClient(kas_allowlist=allowlist)

        # All configured servers should work
        for url in [
            "https://kas-primary.company.com/kas",
            "https://kas-secondary.company.com/kas",
            "https://kas-dr.company.com/kas",
        ]:
            normalized = client._normalize_kas_url(url)
            assert normalized is not None

        # Unknown server should be rejected
        with pytest.raises(SDK.KasAllowlistException):
            client._normalize_kas_url("https://unknown-kas.other.com/kas")
