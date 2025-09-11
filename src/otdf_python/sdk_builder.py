"""
Python port of the SDKBuilder class for OpenTDF platform interaction.
Provides methods to configure and build SDK instances.
"""

import logging
import os
import ssl
from dataclasses import dataclass
from typing import Any

import httpx

from otdf_python.sdk import KAS, SDK
from otdf_python.sdk_exceptions import AutoConfigureException

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    grant_type: str = "client_credentials"
    scope: str = "openid profile email"
    token_endpoint: str | None = None
    access_token: str | None = None


class SDKBuilder:
    """
    A builder class for creating instances of the SDK class.
    """

    PLATFORM_ISSUER = "platform_issuer"

    # Class variable to store the latest platform URL
    _platform_url = None

    def __init__(self):
        self.platform_endpoint: str | None = None
        self.issuer_endpoint: str | None = None
        self.oauth_config: OAuthConfig | None = None
        self.use_plaintext: bool = False
        self.insecure_skip_verify: bool = False
        self.ssl_context: ssl.SSLContext | None = None
        self.auth_token: str | None = None
        self.cert_paths: list[str] = []

    @staticmethod
    def new_builder() -> "SDKBuilder":
        """
        Creates a new SDKBuilder instance.
        Returns:
            SDKBuilder: A new builder instance
        """
        return SDKBuilder()

    @staticmethod
    def get_platform_url() -> str | None:
        """
        Gets the last set platform URL.
        Returns:
            str | None: The platform URL or None if not set
        """
        return SDKBuilder._platform_url

    def ssl_context_from_directory(self, certs_dir_path: str) -> "SDKBuilder":
        """
        Add SSL Context with trusted certs from certDirPath
        Args:
            certs_dir_path: Path to a directory containing .pem or .crt trusted certs
        Returns:
            self: The builder instance for chaining
        """
        self.cert_paths = []

        # Find all .pem and .crt files in the directory
        for filename in os.listdir(certs_dir_path):
            if filename.endswith(".pem") or filename.endswith(".crt"):
                self.cert_paths.append(os.path.join(certs_dir_path, filename))

        # Create SSL context with these certificates
        if self.cert_paths:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            for cert_path in self.cert_paths:
                context.load_verify_locations(cert_path)
            self.ssl_context = context

        return self

    def client_secret(self, client_id: str, client_secret: str) -> "SDKBuilder":
        """
        Sets client credentials for OAuth 2.0 client_credentials grant.
        Args:
            client_id: The OAuth client ID
            client_secret: The OAuth client secret
        Returns:
            self: The builder instance for chaining
        """
        self.oauth_config = OAuthConfig(
            client_id=client_id, client_secret=client_secret
        )
        return self

    def set_platform_endpoint(self, endpoint: str) -> "SDKBuilder":
        """
        Sets the OpenTDF platform endpoint URL.
        Args:
            endpoint: The platform endpoint URL
        Returns:
            self: The builder instance for chaining
        """
        # Normalize the endpoint URL
        if endpoint and not (
            endpoint.startswith("http://") or endpoint.startswith("https://")
        ):
            if self.use_plaintext:
                endpoint = f"http://{endpoint}"
            else:
                endpoint = f"https://{endpoint}"

        self.platform_endpoint = endpoint
        # Store in class variable for access from other components
        SDKBuilder._platform_url = endpoint
        return self

    def set_issuer_endpoint(self, issuer: str) -> "SDKBuilder":
        """
        Sets the OpenID Connect issuer endpoint URL.
        Args:
            issuer: The issuer endpoint URL
        Returns:
            self: The builder instance for chaining
        """
        # Normalize the issuer URL
        if issuer and not (
            issuer.startswith("http://") or issuer.startswith("https://")
        ):
            issuer = f"https://{issuer}"

        self.issuer_endpoint = issuer
        return self

    def use_insecure_plaintext_connection(
        self, use_plaintext: bool = True
    ) -> "SDKBuilder":
        """
        Configures whether to use plain text (HTTP) connection instead of HTTPS.
        Args:
            use_plaintext: Whether to use plain text connection
        Returns:
            self: The builder instance for chaining
        """
        self.use_plaintext = use_plaintext

        # Update platform endpoint protocol if necessary
        if self.platform_endpoint:
            if use_plaintext and self.platform_endpoint.startswith("https://"):
                self.platform_endpoint = f"http://{self.platform_endpoint[8:]}"
            elif not use_plaintext and self.platform_endpoint.startswith("http://"):
                self.platform_endpoint = f"https://{self.platform_endpoint[7:]}"

            # Update the class variable as well since kas() method uses it
            SDKBuilder._platform_url = self.platform_endpoint

        return self

    def use_insecure_skip_verify(self, skip_verify: bool = True) -> "SDKBuilder":
        """
        Configures whether to skip SSL verification.
        Args:
            skip_verify: Whether to skip SSL verification
        Returns:
            self: The builder instance for chaining
        """
        self.insecure_skip_verify = skip_verify

        # If skipping verification, create a default SSL context that does not verify
        if skip_verify:
            self.ssl_context = ssl._create_unverified_context()

        return self

    def bearer_token(self, token: str) -> "SDKBuilder":
        """
        Sets a bearer token to use for authorization.
        Args:
            token: The bearer token
        Returns:
            self: The builder instance for chaining
        """
        self.auth_token = token
        return self

    def _discover_token_endpoint_from_platform(self) -> None:
        """
        Discover token endpoint using OpenTDF platform configuration.
        Raises:
            AutoConfigureException: If discovery fails
        """
        if not self.platform_endpoint or not self.oauth_config:
            return

        # Try to get OpenTDF configuration first
        well_known_url = f"{self.platform_endpoint}/.well-known/opentdf-configuration"
        response = httpx.get(well_known_url, verify=not self.insecure_skip_verify)

        if response.status_code != 200:
            raise AutoConfigureException(
                f"Failed to retrieve OpenTDF configuration from {well_known_url} (status: {response.status_code}). "
                "Please provide an explicit issuer endpoint or check platform URL."
            )

        config_doc = response.json()
        configuration = config_doc.get("configuration", {})

        # Try to get token endpoint from IDP configuration
        idp_config = configuration.get("idp", {})
        if idp_config.get("token_endpoint"):
            self.oauth_config.token_endpoint = idp_config["token_endpoint"]
            return

        # Fall back to using platform_issuer for OIDC discovery
        platform_issuer = configuration.get("platform_issuer")
        if not platform_issuer:
            raise AutoConfigureException(
                "No platform_issuer found in OpenTDF configuration"
            )

        self._discover_token_endpoint_from_issuer(platform_issuer)

    def _discover_token_endpoint_from_issuer(self, issuer_url: str) -> None:
        """
        Discover token endpoint using OIDC discovery from issuer.
        Args:
            issuer_url: The issuer URL to use for discovery
        Raises:
            AutoConfigureException: If discovery fails
        """
        if not self.oauth_config:
            return

        oidc_discovery_url = f"{issuer_url}/.well-known/openid-configuration"
        oidc_response = httpx.get(
            oidc_discovery_url, verify=not self.insecure_skip_verify
        )

        if oidc_response.status_code != 200:
            raise AutoConfigureException(
                f"Failed to retrieve OIDC configuration from {oidc_discovery_url}: {oidc_response.status_code}"
            )

        oidc_doc = oidc_response.json()
        self.oauth_config.token_endpoint = oidc_doc.get("token_endpoint")
        if not self.oauth_config.token_endpoint:
            raise AutoConfigureException(
                "Token endpoint not found in OIDC discovery document"
            )

    def _discover_token_endpoint(self) -> None:
        """
        Discover the token endpoint using available configuration.
        Raises:
            AutoConfigureException: If discovery fails
        """
        # Try platform endpoint first
        if self.platform_endpoint:
            try:
                self._discover_token_endpoint_from_platform()
                return
            except Exception as e:
                # If platform fails and we have an explicit issuer, try that
                if self.issuer_endpoint:
                    try:
                        realm_name = "opentdf"  # Default realm name
                        issuer_url = f"{self.issuer_endpoint}/realms/{realm_name}"
                        self._discover_token_endpoint_from_issuer(issuer_url)
                        return
                    except Exception:
                        # Re-raise the original platform error
                        pass
                raise AutoConfigureException(
                    f"Error during token endpoint discovery: {e!s}"
                )

        # Fall back to explicit issuer endpoint
        if self.issuer_endpoint:
            realm_name = "opentdf"  # Default realm name
            issuer_url = f"{self.issuer_endpoint}/realms/{realm_name}"
            self._discover_token_endpoint_from_issuer(issuer_url)
            return

        raise AutoConfigureException(
            "Platform endpoint or issuer endpoint must be configured for OIDC token discovery"
        )

    def _get_token_from_client_credentials(self) -> str:
        """
        Obtains an OAuth token using client credentials.
        Returns:
            str: The access token
        Raises:
            AutoConfigureException: If token acquisition fails
        """
        if not self.oauth_config:
            raise AutoConfigureException("OAuth configuration is not set")

        if not self.oauth_config.token_endpoint:
            self._discover_token_endpoint()

        # Ensure we have a token endpoint before proceeding
        if not self.oauth_config.token_endpoint:
            raise AutoConfigureException("Token endpoint discovery failed")

        # Request the token
        try:
            token_data = {
                "grant_type": self.oauth_config.grant_type,
                "client_id": self.oauth_config.client_id,
                "client_secret": self.oauth_config.client_secret,
                "scope": self.oauth_config.scope,
            }

            response = httpx.post(
                self.oauth_config.token_endpoint,
                data=token_data,
                verify=not self.insecure_skip_verify,
            )

            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get("access_token")
                if not access_token:
                    raise AutoConfigureException("No access_token in token response")
                return access_token
            else:
                raise AutoConfigureException(
                    f"Token request failed: {response.status_code} - {response.text}"
                )

        except Exception as e:
            raise AutoConfigureException(f"Error during token acquisition: {e!s}")

    def _create_auth_interceptor(self) -> Any:
        """
        Creates an authentication interceptor for API requests (httpx).
        Returns:
            Any: An auth interceptor object
        Raises:
            AutoConfigureException: If auth configuration fails
        """
        # For now, this is just a placeholder returning a dict with auth headers
        # In a real implementation, this would create a proper interceptor object
        # that injects auth headers into httpx requests

        token = None

        if self.auth_token:
            # Use provided token
            token = self.auth_token
        elif self.oauth_config:
            # Get token from OAuth
            token = self._get_token_from_client_credentials()

        if token:
            return {"Authorization": f"Bearer {token}"}

        return None

    def _create_services(self) -> SDK.Services:
        """
        Creates service client instances.
        Returns:
            SDK.Services: The service client instances
        Raises:
            AutoConfigureException: If service creation fails
        """
        # For now, return a simple implementation of Services
        # In a real implementation, this would create actual service clients
        # connecting to the platform endpoints

        ssl_verify = not self.insecure_skip_verify
        auth_interceptor = self._create_auth_interceptor()

        class ServicesImpl(SDK.Services):
            def __init__(self, builder_instance):
                self.closed = False
                self._ssl_verify = ssl_verify
                self._auth_headers = auth_interceptor if auth_interceptor else {}
                self._builder = builder_instance

            def kas(self) -> KAS:
                """
                Returns the KAS interface with SSL verification settings.
                """
                platform_url = SDKBuilder.get_platform_url()

                # Create a token source function that can refresh tokens
                def token_source():
                    if self._builder.auth_token:
                        return self._builder.auth_token
                    elif self._builder.oauth_config:
                        return self._builder._get_token_from_client_credentials()
                    return None

                kas_impl = KAS(
                    platform_url=platform_url,
                    token_source=token_source,
                    sdk_ssl_verify=self._ssl_verify,
                    use_plaintext=self._builder.use_plaintext,
                )
                return kas_impl

            def close(self):
                self.closed = True

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.close()

        return ServicesImpl(self)

    def build(self) -> SDK:
        """
        Builds and returns an SDK instance with the configured properties.
        Returns:
            SDK: The configured SDK instance
        Raises:
            AutoConfigureException: If the build fails
        """
        if not self.platform_endpoint:
            raise AutoConfigureException("Platform endpoint is not set")

        # Create the auth interceptor
        auth_interceptor = self._create_auth_interceptor()

        # Create services
        services = self._create_services()

        # Return the SDK instance, platform_url is set for new_tdf_config
        return SDK(
            services=services,
            auth_interceptor=auth_interceptor,
            platform_url=self.platform_endpoint,
            ssl_verify=not self.insecure_skip_verify,
            use_plaintext=getattr(self, "use_plaintext", False),
        )
