"""KAS Allowlist: Validates KAS URLs against a list of trusted hosts.

This module provides protection against SSRF attacks where malicious TDF files
could contain attacker-controlled KAS URLs to steal OIDC credentials.
"""

import logging
from urllib.parse import urlparse


class KASAllowlist:
    """Validates KAS URLs against an allowlist of trusted hosts.

    This class prevents credential theft by ensuring the SDK only sends
    authentication tokens to trusted KAS endpoints.

    Example:
        allowlist = KASAllowlist(["https://kas.example.com"])
        allowlist.is_allowed("https://kas.example.com/kas")  # True
        allowlist.is_allowed("https://evil.com/kas")  # False

    """

    def __init__(self, allowed_urls: list[str] | None = None, allow_all: bool = False):
        """Initialize the KAS allowlist.

        Args:
            allowed_urls: List of trusted KAS URLs. Each URL is normalized to
                its origin (scheme://host:port) for comparison.
            allow_all: If True, all URLs are allowed. Use only for testing.
                A warning is logged when this is enabled.

        """
        self._allowed_origins: set[str] = set()
        self._allow_all = allow_all

        if allow_all:
            logging.warning(
                "KAS allowlist is disabled (allow_all=True). "
                "This is insecure and should only be used for testing."
            )

        if allowed_urls:
            for url in allowed_urls:
                self.add(url)

    def add(self, url: str) -> None:
        """Add a URL to the allowlist.

        The URL is normalized to its origin (scheme://host:port) before storage.
        Paths and query strings are stripped.

        Args:
            url: The KAS URL to allow. Can include path components which
                will be stripped for origin comparison.

        """
        origin = self._get_origin(url)
        self._allowed_origins.add(origin)
        logging.debug(f"Added KAS origin to allowlist: {origin}")

    def is_allowed(self, url: str) -> bool:
        """Check if a URL is allowed by the allowlist.

        Args:
            url: The KAS URL to check.

        Returns:
            True if the URL's origin is in the allowlist or allow_all is True.
            False otherwise.

        """
        if self._allow_all:
            logging.debug(f"KAS URL allowed (allow_all=True): {url}")
            return True

        if not self._allowed_origins:
            logging.debug(f"KAS URL rejected (empty allowlist): {url}")
            return False

        origin = self._get_origin(url)
        allowed = origin in self._allowed_origins
        if allowed:
            logging.debug(f"KAS URL allowed: {url} (origin: {origin})")
        else:
            logging.debug(
                f"KAS URL rejected: {url} (origin: {origin}, "
                f"allowed: {self._allowed_origins})"
            )
        return allowed

    def validate(self, url: str) -> None:
        """Validate a URL against the allowlist, raising an exception if not allowed.

        Args:
            url: The KAS URL to validate.

        Raises:
            SDK.KasAllowlistException: If the URL is not in the allowlist.

        """
        if not self.is_allowed(url):
            # Import here to avoid circular imports
            from .sdk import SDK

            raise SDK.KasAllowlistException(url, self._allowed_origins)

    @property
    def allowed_origins(self) -> set[str]:
        """Return the set of allowed origins (read-only copy)."""
        return self._allowed_origins.copy()

    @property
    def allow_all(self) -> bool:
        """Return whether all URLs are allowed."""
        return self._allow_all

    @staticmethod
    def _get_origin(url: str) -> str:
        """Extract the origin (scheme://host:port) from a URL.

        This normalizes URLs for comparison by stripping paths and query strings.
        Default ports (80 for http, 443 for https) are included explicitly.

        Args:
            url: The URL to extract the origin from.

        Returns:
            Normalized origin string in format scheme://host:port

        """
        # Add scheme if missing
        if "://" not in url:
            url = "https://" + url

        try:
            parsed = urlparse(url)
        except Exception as e:
            logging.warning(f"Failed to parse URL {url}: {e}")
            # Return the URL as-is if parsing fails
            return url.lower()

        scheme = (parsed.scheme or "https").lower()
        hostname = (parsed.hostname or "").lower()

        if not hostname:
            # URL might be malformed, return as-is
            logging.warning(f"Could not extract hostname from URL: {url}")
            return url.lower()

        # Determine port (use explicit port or default for scheme)
        if parsed.port:
            port = parsed.port
        elif scheme == "http":
            port = 80
        else:
            port = 443

        return f"{scheme}://{hostname}:{port}"

    @classmethod
    def from_platform_url(cls, platform_url: str) -> "KASAllowlist":
        """Create an allowlist from a platform URL.

        This is the default behavior: auto-allow the platform's KAS endpoint.

        Args:
            platform_url: The OpenTDF platform URL. The KAS endpoint is
                assumed to be at {platform_url}/kas.

        Returns:
            KASAllowlist configured to allow the platform's KAS endpoint.

        """
        allowlist = cls()
        # Add the platform URL itself (KAS might be at root or /kas)
        allowlist.add(platform_url)
        # Also construct the /kas endpoint explicitly
        kas_url = platform_url.rstrip("/") + "/kas"
        allowlist.add(kas_url)
        logging.info(f"Created KAS allowlist from platform URL: {platform_url}")
        return allowlist
