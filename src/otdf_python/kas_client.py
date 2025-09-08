"""
KASClient: Handles communication with the Key Access Service (KAS).
"""

import base64
import hashlib
import logging
import secrets
import time
from base64 import b64decode
from dataclasses import dataclass

import jwt

from .asym_decryption import AsymDecryption
from .crypto_utils import CryptoUtils
from .kas_connect_rpc_client import KASConnectRPCClient
from .kas_key_cache import KASKeyCache
from .key_type_constants import EC_KEY_TYPE, RSA_KEY_TYPE
from .sdk_exceptions import SDKException


@dataclass
class KeyAccess:
    url: str
    wrapped_key: str
    ephemeral_public_key: str | None = None


class KASClient:
    def __init__(
        self,
        kas_url=None,
        token_source=None,
        cache=None,
        use_plaintext=False,
        verify_ssl=True,
    ):
        self.kas_url = kas_url
        self.token_source = token_source
        self.cache = cache or KASKeyCache()
        self.use_plaintext = use_plaintext
        self.verify_ssl = verify_ssl
        self.decryptor = None
        self.client_public_key = None

        # Initialize Connect RPC client for protobuf interactions
        self.connect_rpc_client = KASConnectRPCClient(
            use_plaintext=use_plaintext, verify_ssl=verify_ssl
        )

        # Generate DPoP key for JWT signing (separate from encryption keys)
        # This matches the web-SDK pattern where dpopKeys != ephemeralKeys
        self._dpop_private_key, self._dpop_public_key = (
            CryptoUtils.generate_rsa_keypair()
        )
        self._dpop_private_key_pem = CryptoUtils.get_rsa_private_key_pem(
            self._dpop_private_key
        )
        self._dpop_public_key_pem = CryptoUtils.get_rsa_public_key_pem(
            self._dpop_public_key
        )

    def _normalize_kas_url(self, url: str) -> str:
        """
        Normalize KAS URLs based on client security settings.

        Args:
            url: The KAS URL to normalize

        Returns:
            Normalized URL with appropriate protocol and port
        """
        from urllib.parse import urlparse

        try:
            # Parse the URL
            parsed = urlparse(url)
        except Exception as e:
            raise SDKException(f"error trying to parse URL [{url}]", e)

        # Check if we have a host or if this is likely a hostname:port combination
        if parsed.hostname is None:
            # No host means we likely have hostname:port being misinterpreted
            return self._handle_missing_scheme(url)
        else:
            # We have a host, handle the existing scheme
            return self._handle_existing_scheme(parsed)

    def _handle_missing_scheme(self, url: str) -> str:
        """Handle URLs without scheme by adding appropriate protocol and port."""
        scheme = "http" if self.use_plaintext else "https"
        default_port = 80 if self.use_plaintext else 443

        try:
            # Check if we have a hostname:port format (colon before any slash)
            if ":" in url and ("/" not in url or url.index(":") < url.index("/")):
                host, port_str = url.split(":", 1)
                try:
                    port = int(port_str)
                    return f"{scheme}://{host}:{port}"
                except ValueError:
                    raise SDKException(
                        f"error trying to create URL for host and port [{url}]"
                    )
            else:
                # Hostname with or without path, add default port
                if "/" in url:
                    # Split at first slash to separate hostname from path
                    host, path = url.split("/", 1)
                    return f"{scheme}://{host}:{default_port}/{path}"
                else:
                    # Just a hostname, add default port
                    return f"{scheme}://{url}:{default_port}"
        except Exception as e:
            raise SDKException(
                f"error trying to create URL for host and port [{url}]", e
            )

    def _handle_existing_scheme(self, parsed) -> str:
        """Handle URLs with existing scheme by normalizing protocol and port."""
        # Force the scheme based on client security settings
        scheme = "http" if self.use_plaintext else "https"

        # Determine the port
        if parsed.port is not None:
            port = parsed.port
        else:
            # Use default port based on target scheme
            port = 80 if self.use_plaintext else 443

        # Reconstruct URL preserving the path (especially /kas prefix)
        try:
            # Create URL preserving the path component for proper endpoint routing
            path = parsed.path if parsed.path else ""
            normalized_url = f"{scheme}://{parsed.hostname}:{port}{path}"
            logging.debug(f"normalized url [{parsed.geturl()}] to [{normalized_url}]")
            return normalized_url
        except Exception as e:
            raise SDKException("error creating KAS address", e)

    def _create_signed_request_jwt(self, policy_json, client_public_key, key_access):  # noqa: C901
        """
        Create a signed JWT for the rewrap request.
        The JWT is signed with the DPoP private key.
        """
        # Handle both ManifestKeyAccess (new camelCase and old snake_case) and simple KeyAccess (for tests)
        # TODO: This can probably be simplified to only camelCase

        # Ensure wrappedKey is a base64-encoded string
        # Note: wrappedKey from manifest is already base64-encoded
        wrapped_key = getattr(key_access, "wrappedKey", None) or getattr(
            key_access, "wrapped_key", None
        )
        if wrapped_key is None:
            raise SDKException("No wrapped key found in key access object")

        if isinstance(wrapped_key, bytes):
            # Only encode if it's raw bytes (shouldn't happen from manifest)
            wrapped_key = base64.b64encode(wrapped_key).decode("utf-8")
        elif not isinstance(wrapped_key, str):
            # Convert to string if it's something else
            wrapped_key = str(wrapped_key)
        # If it's already a string (from manifest), use it as-is since it's already base64-encoded

        key_access_dict = {
            "url": key_access.url,
            "wrappedKey": wrapped_key,
        }

        # Add type and protocol - handle both old and new field names
        key_type = getattr(key_access, "type", None) or getattr(
            key_access, "key_type", None
        )
        if key_type is not None:
            key_access_dict["type"] = key_type
        else:
            key_access_dict["type"] = "wrapped"  # Default type for tests

        protocol = getattr(key_access, "protocol", None)
        if protocol is not None:
            key_access_dict["protocol"] = protocol
        else:
            key_access_dict["protocol"] = "kas"  # Default protocol for tests

        # Optional fields - handle both old and new field names, only include if they exist and are not None
        policy_binding = getattr(key_access, "policyBinding", None) or getattr(
            key_access, "policy_binding", None
        )
        if policy_binding is not None:
            # Policy binding hash should be kept as base64-encoded
            # The server expects base64-encoded hash values in the JWT request
            key_access_dict["policyBinding"] = policy_binding

        encrypted_metadata = getattr(key_access, "encryptedMetadata", None) or getattr(
            key_access, "encrypted_metadata", None
        )
        if encrypted_metadata is not None:
            key_access_dict["encryptedMetadata"] = encrypted_metadata

        kid = getattr(key_access, "kid", None)
        if kid is not None:
            key_access_dict["kid"] = kid

        sid = getattr(key_access, "sid", None)
        if sid is not None:
            key_access_dict["sid"] = sid

        schema_version = getattr(key_access, "schemaVersion", None) or getattr(
            key_access, "schema_version", None
        )
        if schema_version is not None:
            key_access_dict["schemaVersion"] = schema_version

        ephemeral_public_key = getattr(
            key_access, "ephemeralPublicKey", None
        ) or getattr(key_access, "ephemeral_public_key", None)
        if ephemeral_public_key is not None:
            key_access_dict["ephemeralPublicKey"] = ephemeral_public_key

        # Get current timestamp in seconds since epoch (UNIX timestamp)
        now = int(time.time())

        # The server expects a JWT with a requestBody field containing the UnsignedRewrapRequest
        # Create the request body that matches UnsignedRewrapRequest protobuf structure
        # Use the v2 format with explicit policy ID and requests array for cross-tool compatibility

        # Use "policy" as policy ID for compatibility with otdfctl
        import json

        policy_uuid = "policy"  # otdfctl uses "policy" as the policy ID

        # For v2 format, the policy body must be base64-encoded
        policy_base64 = base64.b64encode(policy_json.encode("utf-8")).decode("utf-8")

        unsigned_rewrap_request = {
            "clientPublicKey": client_public_key,  # Maps to client_public_key
            "requests": [
                {  # Maps to requests array (v2 format)
                    "keyAccessObjects": [
                        {
                            "keyAccessObjectId": "kao-0",  # Standard KAO ID
                            "keyAccessObject": key_access_dict,
                        }
                    ],
                    "policy": {
                        "id": policy_uuid,  # Use the UUID from policy as the policy ID
                        "body": policy_base64,  # Base64-encoded policy JSON
                    },
                }
            ],
            "keyAccess": key_access_dict,
            "policy": policy_base64,
        }

        # Convert to JSON string
        request_body_json = json.dumps(unsigned_rewrap_request)

        # JWT payload with requestBody field containing the JSON string
        payload = {
            "requestBody": request_body_json,
            "iat": now,  # Issued at timestamp (required)
            "exp": now + 7200,  # Expires in 2 hours (required)
        }

        # Sign the JWT with the DPoP private key (RS256)
        signed_jwt = jwt.encode(payload, self._dpop_private_key_pem, algorithm="RS256")

        return signed_jwt

    def _create_connect_rpc_signed_token(self, key_access, policy_json):
        """
        Create a signed token specifically for Connect RPC requests.
        For now, this delegates to the existing JWT creation method.
        """
        return self._create_signed_request_jwt(
            policy_json, self.client_public_key, key_access
        )

    def _create_dpop_proof(self, method, url, access_token=None):
        """
        Create a DPoP proof JWT as per RFC 9449.

        Args:
            method: HTTP method (e.g., "POST")
            url: Full URL of the request
            access_token: Optional access token for ath claim

        Returns:
            DPoP proof JWT string
        """
        now = int(time.time())

        # Create DPoP proof claims
        proof_claims = {
            "jti": secrets.token_urlsafe(32),  # Unique identifier
            "htm": method,  # HTTP method
            "htu": url,  # HTTP URI
            "iat": now,  # Issued at
        }

        # Add access token hash if provided
        if access_token:
            token_hash = hashlib.sha256(access_token.encode("utf-8")).digest()
            proof_claims["ath"] = (
                base64.urlsafe_b64encode(token_hash).decode("utf-8").rstrip("=")
            )

        # DPoP proof must be signed with the DPoP key and include the public key in the header
        header = {
            "alg": "RS256",
            "typ": "dpop+jwt",
            "jwk": {
                "kty": "RSA",
                "n": base64.urlsafe_b64encode(
                    self._dpop_public_key.public_numbers().n.to_bytes(
                        (self._dpop_public_key.public_numbers().n.bit_length() + 7)
                        // 8,
                        "big",
                    )
                )
                .decode("utf-8")
                .rstrip("="),
                "e": base64.urlsafe_b64encode(
                    self._dpop_public_key.public_numbers().e.to_bytes(
                        (self._dpop_public_key.public_numbers().e.bit_length() + 7)
                        // 8,
                        "big",
                    )
                )
                .decode("utf-8")
                .rstrip("="),
            },
        }

        # Create and sign the DPoP proof JWT
        return jwt.encode(
            proof_claims, self._dpop_private_key_pem, algorithm="RS256", headers=header
        )

    def get_public_key(self, kas_info):
        """
        Get KAS public key using Connect RPC.
        Checks cache first if available.
        """
        try:
            # Check cache first if available (use original URL for cache key)
            if self.cache:
                cached_info = self.cache.get(kas_info.url)
                if cached_info:
                    return cached_info

            result = self._get_public_key_with_connect_rpc(kas_info)

            # Cache the result if cache is available
            if self.cache and result:
                self.cache.store(result)

            return result

        except Exception as e:
            logging.error(f"Error in get_public_key: {e}")
            raise

    def _get_public_key_with_connect_rpc(self, kas_info):
        """
        Get KAS public key using Connect RPC.
        """

        # Get access token for authentication if token source is available
        access_token = None
        if self.token_source:
            try:
                access_token = self.token_source()
            except Exception as e:
                logging.warning(f"Failed to get access token: {e}")

        # Normalize the URL
        normalized_url = self._normalize_kas_url(kas_info.url)

        try:
            # Delegate to the Connect RPC client
            result = self.connect_rpc_client.get_public_key(
                normalized_url, kas_info, access_token
            )

            # Cache the result
            if self.cache:
                self.cache.store(result)

            return result

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            logging.error(
                f"Connect RPC public key request failed: {type(e).__name__}: {e}"
            )
            logging.error(f"Full traceback: {error_details}")
            raise SDKException(f"Connect RPC public key request failed: {e}")

    def _normalize_session_key_type(self, session_key_type):
        """
        Normalize session key type to the appropriate enum value.

        Args:
            session_key_type: Type of the session key (KeyType enum or string "RSA"/"EC")

        Returns:
            Normalized key type enum
        """
        if isinstance(session_key_type, str):
            if session_key_type.upper() == "RSA":
                return RSA_KEY_TYPE
            elif session_key_type.upper() == "EC":
                return EC_KEY_TYPE
            else:
                logging.warning(
                    f"Unknown session key type: {session_key_type}, defaulting to RSA"
                )
                return RSA_KEY_TYPE
        elif session_key_type is None:
            # Default to RSA
            return RSA_KEY_TYPE
        return session_key_type

    def _prepare_ec_keypair(self, session_key_type):
        """
        Prepare EC key pair for unwrapping.

        Args:
            session_key_type: EC key type with curve information

        Returns:
            ECKeyPair instance and client public key
        """
        from .eckeypair import ECKeyPair

        # Use default curve for now - this would need to be based on session_key_type in a full implementation
        ec_key_pair = ECKeyPair()
        client_public_key = ec_key_pair.public_key_pem()
        return ec_key_pair, client_public_key

    def _prepare_rsa_keypair(self):
        """
        Prepare RSA key pair for unwrapping, reusing if possible.
        Uses separate ephemeral keys for encryption (not DPoP keys).

        Returns:
            Client public key PEM for the ephemeral encryption key
        """
        if self.decryptor is None:
            # Generate ephemeral keys for encryption (separate from DPoP keys)
            private_key, public_key = CryptoUtils.generate_rsa_keypair()
            self.decryptor = AsymDecryption(private_key_obj=private_key)
            self.client_public_key = CryptoUtils.get_rsa_public_key_pem(public_key)
        return self.client_public_key

    def _unwrap_with_ec(self, wrapped_key, ec_key_pair, response_data):
        """
        Unwrap a key using EC cryptography.

        Args:
            wrapped_key: The wrapped key to decrypt
            ec_key_pair: ECKeyPair instance
            response_data: Response data from KAS

        Returns:
            Unwrapped key as bytes
        """
        if ec_key_pair is None:
            raise SDKException(
                "ECKeyPair is null. Unable to proceed with the unwrap operation."
            )

        # Get the KAS ephemeral public key
        kas_ephemeral_public_key = response_data.get("sessionPublicKey")
        if not kas_ephemeral_public_key:
            raise SDKException("No session public key in KAS response")

        # Generate symmetric key using ECDH
        from .eckeypair import ECKeyPair

        public_key = ECKeyPair.public_key_from_pem(kas_ephemeral_public_key)
        sym_key = ECKeyPair.compute_ecdh_key(public_key, ec_key_pair.get_private_key())

        # Calculate HKDF and decrypt
        from otdf_python.tdf import TDF

        session_key = ECKeyPair.calculate_hkdf(TDF.GLOBAL_KEY_SALT, sym_key)

        from .aesgcm import AesGcm

        gcm = AesGcm(session_key)
        return gcm.decrypt(wrapped_key)

    def _ensure_client_keypair(self, session_key_type):
        """
        Ensure client keypair is generated and stored.
        """
        if session_key_type == RSA_KEY_TYPE:
            if self.decryptor is None:
                private_key, public_key = CryptoUtils.generate_rsa_keypair()
                private_key_pem = CryptoUtils.get_rsa_private_key_pem(private_key)
                self.decryptor = AsymDecryption(private_key_pem)
                self.client_public_key = CryptoUtils.get_rsa_public_key_pem(public_key)
        else:
            # For EC keys, generate fresh key pair each time
            # TODO: Implement proper EC key handling
            private_key, public_key = CryptoUtils.generate_rsa_keypair()
            private_key_pem = CryptoUtils.get_rsa_private_key_pem(private_key)
            self.client_public_key = CryptoUtils.get_rsa_public_key_pem(public_key)

    def _parse_and_decrypt_response(self, response):
        """
        Parse JSON response and decrypt the wrapped key.
        """
        try:
            response_data = response.json()
        except Exception as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response content: {response.content}")
            raise SDKException(f"Invalid JSON response from KAS: {e}")

        entity_wrapped_key = response_data.get("entityWrappedKey")
        if not entity_wrapped_key:
            raise SDKException("No entityWrappedKey in KAS response")

        # Decrypt the wrapped key
        if not self.decryptor:
            raise SDKException("Decryptor not initialized")
        encrypted_key = b64decode(entity_wrapped_key)
        return self.decryptor.decrypt(encrypted_key)

    def unwrap(self, key_access, policy_json, session_key_type=None) -> bytes:
        """
        Unwrap a key using Connect RPC.

        Args:
            key_access: Key access information
            policy_json: Policy as JSON string
            session_key_type: Type of session key (RSA_KEY_TYPE or EC_KEY_TYPE), defaults to RSA

        Returns:
            Unwrapped key bytes
        """
        # Default to RSA if not specified
        if session_key_type is None:
            session_key_type = RSA_KEY_TYPE

        # Ensure we have an ephemeral client keypair for encryption (separate from DPoP keys)
        session_key_type = self._normalize_session_key_type(session_key_type)
        self._ensure_client_keypair(session_key_type)

        # Create signed token for the request using DPoP key for signing
        # BUT use the ephemeral client public key in the request body
        signed_token = self._create_signed_request_jwt(
            policy_json,
            self.client_public_key,
            key_access,  # Use ephemeral key, not DPoP key
        )

        # Call Connect RPC unwrap
        return self._unwrap_with_connect_rpc(key_access, signed_token)

    def _unwrap_with_connect_rpc(self, key_access, signed_token) -> bytes:
        """
        Connect RPC method for unwrapping keys.
        """

        # Get access token for authentication if token source is available
        access_token = None
        if self.token_source:
            try:
                access_token = self.token_source()
            except Exception as e:
                logging.warning(f"Failed to get access token: {e}")

        # Normalize the URL
        normalized_kas_url = self._normalize_kas_url(key_access.url)

        try:
            # Delegate to the Connect RPC client
            entity_wrapped_key = self.connect_rpc_client.unwrap_key(
                normalized_kas_url, key_access, signed_token, access_token
            )

            # Decrypt the wrapped key
            if not self.decryptor:
                raise SDKException("Decryptor not initialized")

            result = self.decryptor.decrypt(entity_wrapped_key)
            logging.info("Connect RPC rewrap succeeded")
            return result

        except Exception as e:
            logging.error(f"Connect RPC rewrap failed: {e}")
            raise SDKException(f"Connect RPC rewrap failed: {e}")

    def get_key_cache(self) -> KASKeyCache:
        """Returns the KAS key cache used for storing and retrieving encryption keys."""
        return self.cache
