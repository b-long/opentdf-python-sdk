"""KASConnectRPCClient: Handles Connect RPC communication with the Key Access Service (KAS).
This class encapsulates all interactions with otdf_python_proto.
"""

import logging

import urllib3
from otdf_python_proto.kas import kas_pb2
from otdf_python_proto.kas.kas_pb2_connect import AccessServiceClient

from otdf_python.auth_headers import AuthHeaders

from .sdk_exceptions import SDKException


class KASConnectRPCClient:
    """Handles Connect RPC communication with KAS service using otdf_python_proto."""

    def __init__(self, use_plaintext=False, verify_ssl=True):
        """Initialize the Connect RPC client.

        Args:
            use_plaintext: Whether to use plaintext (HTTP) connections
            verify_ssl: Whether to verify SSL certificates

        """
        self.use_plaintext = use_plaintext
        self.verify_ssl = verify_ssl

    def _create_http_client(self):
        """Create HTTP client with SSL verification configuration.

        Returns:
            urllib3.PoolManager configured for SSL verification settings

        """
        if self.verify_ssl:
            logging.info("Using SSL verification enabled HTTP client")
            return urllib3.PoolManager()
        else:
            logging.info("Using SSL verification disabled HTTP client")
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            return urllib3.PoolManager(cert_reqs="CERT_NONE")

    def _prepare_connect_rpc_url(self, kas_url):
        """Prepare the base URL for Connect RPC client.

        Args:
            kas_url: The normalized KAS URL

        Returns:
            Base URL for Connect RPC client (without /kas suffix)

        """
        connect_rpc_base_url = kas_url
        # Remove /kas suffix, if present
        connect_rpc_base_url = connect_rpc_base_url.removesuffix("/kas")
        return connect_rpc_base_url

    def _prepare_auth_headers(self, access_token):
        """Prepare authentication headers if access token is available.

        Args:
            access_token: Bearer token for authentication

        Returns:
            Dictionary with authentication headers or None

        """
        if access_token:
            auth_headers = AuthHeaders(
                auth_header=f"Bearer {access_token}",
                dpop_header="",  # Empty for now, ready for future DPoP support
            )
            return auth_headers.to_dict()
        return None

    def get_public_key(self, normalized_kas_url, kas_info, access_token=None):
        """Get KAS public key using Connect RPC.

        Args:
            normalized_kas_url: The normalized KAS URL
            kas_info: KAS information object with algorithm
            access_token: Optional access token for authentication

        Returns:
            Updated kas_info with public_key and kid

        """
        logging.info(
            f"KAS Connect RPC client settings for public key retrieval: "
            f"verify_ssl={self.verify_ssl}, use_plaintext={self.use_plaintext}, "
            f"kas_url={kas_info.url}"
        )

        http_client = self._create_http_client()

        try:
            connect_rpc_base_url = self._prepare_connect_rpc_url(normalized_kas_url)

            logging.info(
                f"Creating Connect RPC client for base URL: {connect_rpc_base_url}, "
                f"for public key retrieval"
            )

            # Create Connect RPC client with configured HTTP client using Connect protocol
            # Note: gRPC protocol is not supported with urllib3, use default Connect protocol
            client = AccessServiceClient(connect_rpc_base_url, http_client=http_client)

            # Create public key request
            algorithm = getattr(kas_info, "algorithm", "") or ""
            request = (
                kas_pb2.PublicKeyRequest(algorithm=algorithm)
                if algorithm
                else kas_pb2.PublicKeyRequest()
            )

            # Prepare headers with authentication if available
            extra_headers = self._prepare_auth_headers(access_token)

            # Make the public key call with authentication headers
            response = client.public_key(request, extra_headers=extra_headers)

            # Update kas_info with response
            kas_info.public_key = response.public_key
            kas_info.kid = response.kid

            return kas_info

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            logging.error(
                f"Connect RPC public key request failed: {type(e).__name__}: {e}"
            )
            logging.error(f"Full traceback: {error_details}")
            raise SDKException(f"Connect RPC public key request failed: {e}") from e

    def unwrap_key(
        self, normalized_kas_url, key_access, signed_token, access_token=None
    ):
        """Unwrap a key using Connect RPC.

        Args:
            normalized_kas_url: The normalized KAS URL
            key_access: Key access information
            signed_token: Signed JWT token for the request
            access_token: Optional access token for authentication

        Returns:
            Unwrapped key bytes from the response

        """
        logging.info(
            f"KAS Connect RPC client settings for unwrap: "
            f"verify_ssl={self.verify_ssl}, use_plaintext={self.use_plaintext}, "
            f"kas_url={key_access.url}"
        )

        http_client = self._create_http_client()

        try:
            kas_service_url = self._prepare_connect_rpc_url(normalized_kas_url)

            logging.info(
                f"Creating Connect RPC client for base URL: {kas_service_url}, for unwrap"
            )

            # Note: gRPC protocol is not supported with urllib3, use default Connect protocol
            client = AccessServiceClient(kas_service_url, http_client=http_client)

            # Create rewrap request
            request = kas_pb2.RewrapRequest(
                signed_request_token=signed_token,
            )

            # Debug: Log the signed token details
            logging.info(f"Connect RPC signed token: {signed_token}")

            # Prepare headers with authentication if available
            extra_headers = self._prepare_auth_headers(access_token)

            # Make the rewrap call with authentication headers
            response = client.rewrap(request, extra_headers=extra_headers)

            # Extract the entity wrapped key from v2 response structure
            # The v2 response has responses[] array with results[] for each policy
            if response.responses and len(response.responses) > 0:
                policy_result = response.responses[0]  # First policy
                if policy_result.results and len(policy_result.results) > 0:
                    kao_result = policy_result.results[0]  # First KAO result
                    if kao_result.kas_wrapped_key:
                        entity_wrapped_key = kao_result.kas_wrapped_key
                    else:
                        raise SDKException(f"KAO result error: {kao_result.error}")
                else:
                    raise SDKException("No KAO results in policy response")
            else:
                # Fallback to legacy entity_wrapped_key field for backward compatibility
                entity_wrapped_key = response.entity_wrapped_key
                if not entity_wrapped_key:
                    raise SDKException("No entity_wrapped_key in Connect RPC response")

            logging.info("Connect RPC rewrap succeeded")
            return entity_wrapped_key

        except Exception as e:
            logging.error(f"Connect RPC rewrap failed: {e}")
            raise SDKException(f"Connect RPC rewrap failed: {e}") from e
