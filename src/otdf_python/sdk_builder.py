"""
Python port of the SDKBuilder class for OpenTDF platform interaction.
Provides methods to configure and build SDK instances.
"""

from typing import Any
import os
import logging
import ssl
import httpx
from dataclasses import dataclass

from otdf_python.sdk import SDK
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
        self.oauth_config: OAuthConfig | None = None
        self.use_plain_text: bool = False
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
            if self.use_plain_text:
                endpoint = f"http://{endpoint}"
            else:
                endpoint = f"https://{endpoint}"

        self.platform_endpoint = endpoint
        # Store in class variable for access from other components
        SDKBuilder._platform_url = endpoint
        return self

    def use_insecure_plaintext_connection(
        self, use_plain_text: bool = True
    ) -> "SDKBuilder":
        """
        Configures whether to use plain text (HTTP) connection instead of HTTPS.
        Args:
            use_plain_text: Whether to use plain text connection
        Returns:
            self: The builder instance for chaining
        """
        self.use_plain_text = use_plain_text

        # Update platform endpoint protocol if necessary
        if self.platform_endpoint:
            if use_plain_text and self.platform_endpoint.startswith("https://"):
                self.platform_endpoint = f"http://{self.platform_endpoint[8:]}"
            elif not use_plain_text and self.platform_endpoint.startswith("http://"):
                self.platform_endpoint = f"https://{self.platform_endpoint[7:]}"

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
            # Auto-discover the token endpoint
            try:
                # Default location for OpenID Connect discovery document
                well_known_url = (
                    f"{self.platform_endpoint}/.well-known/openid-configuration"
                )
                response = httpx.get(well_known_url, verify=not self.use_plain_text)

                if response.status_code == 200:
                    discovery_doc = response.json()
                    self.oauth_config.token_endpoint = discovery_doc.get(
                        "token_endpoint"
                    )
                    if not self.oauth_config.token_endpoint:
                        raise AutoConfigureException(
                            "Token endpoint not found in discovery document"
                        )
                else:
                    raise AutoConfigureException(
                        f"Failed to retrieve OpenID configuration: {response.status_code}"
                    )
            except Exception as e:
                raise AutoConfigureException(
                    f"Error during token endpoint discovery: {e!s}"
                )

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
                verify=not self.use_plain_text,
            )

            if response.status_code == 200:
                token_response = response.json()
                return token_response.get("access_token")
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

        class ServicesImpl(SDK.Services):
            def __init__(self):
                self.closed = False

            def close(self):
                self.closed = True

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.close()

        return ServicesImpl()

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
        )
