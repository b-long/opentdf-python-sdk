"""KASClient: Handles communication with the Key Access Service (KAS)."""

import base64
import hashlib
import logging
import secrets
import time
from base64 import b64decode
from dataclasses import dataclass

import jwt

from .asym_crypto import AsymDecryption
from .crypto_utils import CryptoUtils
from .kas_connect_rpc_client import KASConnectRPCClient
from .kas_key_cache import KASKeyCache
from .key_type_constants import EC_KEY_TYPE, RSA_KEY_TYPE
from .sdk_exceptions import SDKException


@dataclass
class KeyAccess:
    """Key access response from KAS."""

    url: str
    wrapped_key: str
    ephemeral_public_key: str | None = None
    header: bytes | None = None  # For NanoTDF: entire header including ephemeral key


class KASClient:
    """Client for communicating with the Key Access Service (KAS)."""

    def __init__(
        self,
        kas_url=None,
        token_source=None,
        cache=None,
        use_plaintext=False,
        verify_ssl=True,
    ):
        """Initialize KAS client."""
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
        """Normalize KAS URLs based on client security settings.

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
            raise SDKException(f"error trying to parse URL [{url}]: {e}") from e

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
                except ValueError as err:
                    raise SDKException(
                        f"error trying to create URL for host and port [{url}]"
                    ) from err
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
            ) from e

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
            raise SDKException(f"error creating KAS address: {e}") from e

    def _get_wrapped_key_base64(self, key_access):
        """Extract and normalize the wrapped key to base64-encoded string.

        Args:
            key_access: KeyAccess object

        Returns:
            Base64-encoded wrapped key string

        """
        wrapped_key = getattr(key_access, "wrappedKey", None) or getattr(
            key_access, "wrapped_key", None
        )
        if wrapped_key is None:
            raise SDKException("No wrapped key found in key access object")

        if isinstance(wrapped_key, bytes):
            # Only encode if it's raw bytes (shouldn't happen from manifest)
            return base64.b64encode(wrapped_key).decode("utf-8")
        elif not isinstance(wrapped_key, str):
            # Convert to string if it's something else
            return str(wrapped_key)
        # If it's already a string (from manifest), use it as-is since it's already base64-encoded
        return wrapped_key

    def _build_key_access_dict(self, key_access):
        """Build key access dictionary from KeyAccess object, handling both old and new field names.

        Args:
            key_access: KeyAccess object

        Returns:
            Dictionary with key access information

        """
        wrapped_key = self._get_wrapped_key_base64(key_access)

        key_access_dict = {
            "url": key_access.url,
            "wrappedKey": wrapped_key,
        }

        # Add type and protocol - handle both old and new field names
        key_type = getattr(key_access, "type", None) or getattr(
            key_access, "key_type", None
        )
        key_access_dict["type"] = key_type if key_type is not None else "wrapped"

        protocol = getattr(key_access, "protocol", None)
        key_access_dict["protocol"] = protocol if protocol is not None else "kas"

        # Add optional fields
        self._add_optional_fields(key_access_dict, key_access)

        return key_access_dict

    def _add_optional_fields(self, key_access_dict, key_access):
        """Add optional fields to key access dictionary.

        Args:
            key_access_dict: Dictionary to add fields to
            key_access: KeyAccess object to extract fields from

        """
        # Policy binding
        policy_binding = getattr(key_access, "policyBinding", None) or getattr(
            key_access, "policy_binding", None
        )
        if policy_binding is not None:
            key_access_dict["policyBinding"] = policy_binding

        # Encrypted metadata
        encrypted_metadata = getattr(key_access, "encryptedMetadata", None) or getattr(
            key_access, "encrypted_metadata", None
        )
        if encrypted_metadata is not None:
            key_access_dict["encryptedMetadata"] = encrypted_metadata

        # Simple optional fields
        for field in ["kid", "sid"]:
            value = getattr(key_access, field, None)
            if value is not None:
                key_access_dict[field] = value

        # Schema version
        schema_version = getattr(key_access, "schemaVersion", None) or getattr(
            key_access, "schema_version", None
        )
        if schema_version is not None:
            key_access_dict["schemaVersion"] = schema_version

        # Ephemeral public key
        ephemeral_public_key = getattr(
            key_access, "ephemeralPublicKey", None
        ) or getattr(key_access, "ephemeral_public_key", None)
        if ephemeral_public_key is not None:
            key_access_dict["ephemeralPublicKey"] = ephemeral_public_key

        # NanoTDF header
        header = getattr(key_access, "header", None)
        if header is not None:
            key_access_dict["header"] = base64.b64encode(header).decode("utf-8")

    def _get_algorithm_from_session_key_type(self, session_key_type):
        """Convert session key type to algorithm string for KAS.

        Args:
            session_key_type: Session key type (EC_KEY_TYPE or RSA_KEY_TYPE)

        Returns:
            Algorithm string or None

        """
        if session_key_type == EC_KEY_TYPE:
            return "ec:secp256r1"  # Default EC curve for NanoTDF
        elif session_key_type == RSA_KEY_TYPE:
            return "rsa:2048"  # Default RSA key size
        return None

    def _build_rewrap_request(
        self, policy_json, client_public_key, key_access_dict, algorithm, has_header
    ):
        """Build the unsigned rewrap request structure.

        Args:
            policy_json: Policy JSON string
            client_public_key: Client public key PEM string
            key_access_dict: Key access dictionary
            algorithm: Algorithm string (e.g., "ec:secp256r1" or "rsa:2048")
            has_header: Whether NanoTDF header is present

        Returns:
            Dictionary with unsigned rewrap request

        """
        import json

        policy_uuid = "policy"  # otdfctl uses "policy" as the policy ID
        policy_base64 = base64.b64encode(policy_json.encode("utf-8")).decode("utf-8")

        # Build the request object
        request_item = {
            "keyAccessObjects": [
                {
                    "keyAccessObjectId": "kao-0",  # Standard KAO ID
                    "keyAccessObject": key_access_dict,
                }
            ],
            "policy": {
                "id": policy_uuid,
            },
        }

        # Only include policy body if header is NOT provided (standard TDF)
        if not has_header:
            request_item["policy"]["body"] = policy_base64

        # Add algorithm if provided (required for NanoTDF/ECDH)
        if algorithm:
            request_item["algorithm"] = algorithm

        unsigned_rewrap_request = {
            "clientPublicKey": client_public_key,
            "requests": [request_item],
            "keyAccess": key_access_dict,
        }

        # Only include legacy policy field for standard TDF (not NanoTDF with header)
        if not has_header:
            unsigned_rewrap_request["policy"] = policy_base64

        return json.dumps(unsigned_rewrap_request)

    def _create_signed_request_jwt(
        self, policy_json, client_public_key, key_access, session_key_type=None
    ):
        """Create a signed JWT for the rewrap request.
        The JWT is signed with the DPoP private key.

        Args:
            policy_json: Policy JSON string
            client_public_key: Client public key PEM string
            key_access: KeyAccess object
            session_key_type: Optional session key type (RSA_KEY_TYPE or EC_KEY_TYPE)

        """
        # Build key access dictionary handling both old and new field names
        key_access_dict = self._build_key_access_dict(key_access)

        # Get current timestamp
        now = int(time.time())

        # Convert session_key_type to algorithm string for KAS
        algorithm = self._get_algorithm_from_session_key_type(session_key_type)

        # Check if header is present (for NanoTDF)
        has_header = getattr(key_access, "header", None) is not None

        # Build the unsigned rewrap request
        request_body_json = self._build_rewrap_request(
            policy_json, client_public_key, key_access_dict, algorithm, has_header
        )

        # JWT payload with requestBody field containing the JSON string
        payload = {
            "requestBody": request_body_json,
            "iat": now,  # Issued at timestamp (required)
            "exp": now + 7200,  # Expires in 2 hours (required)
        }

        # Sign the JWT with the DPoP private key (RS256)
        return jwt.encode(payload, self._dpop_private_key_pem, algorithm="RS256")

    def _create_connect_rpc_signed_token(self, key_access, policy_json):
        """Create a signed token specifically for Connect RPC requests.
        For now, this delegates to the existing JWT creation method.
        """
        return self._create_signed_request_jwt(
            policy_json, self.client_public_key, key_access
        )

    def _create_dpop_proof(self, method, url, access_token=None):
        """Create a DPoP proof JWT as per RFC 9449.

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
        """Get KAS public key using Connect RPC.
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
        """Get KAS public key using Connect RPC."""
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
            raise SDKException(f"Connect RPC public key request failed: {e}") from e

    def _normalize_session_key_type(self, session_key_type):
        """Normalize session key type to the appropriate enum value.

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
        """Prepare EC key pair for unwrapping.

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
        """Prepare RSA key pair for unwrapping, reusing if possible.
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
        """Unwrap a key using EC cryptography.

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
        """Ensure client keypair is generated and stored."""
        if session_key_type == RSA_KEY_TYPE:
            if self.decryptor is None:
                private_key, public_key = CryptoUtils.generate_rsa_keypair()
                private_key_pem = CryptoUtils.get_rsa_private_key_pem(private_key)
                self.decryptor = AsymDecryption(private_key_pem)
                self.client_public_key = CryptoUtils.get_rsa_public_key_pem(public_key)
        else:
            # For EC keys (NanoTDF/ECDH), still need RSA keypair for encrypting the rewrap response
            # KAS uses client public key to encrypt the symmetric key it derived via ECDH
            if self.decryptor is None:
                private_key, public_key = CryptoUtils.generate_rsa_keypair()
                private_key_pem = CryptoUtils.get_rsa_private_key_pem(private_key)
                self.decryptor = AsymDecryption(private_key_pem)
                self.client_public_key = CryptoUtils.get_rsa_public_key_pem(public_key)

    def _parse_and_decrypt_response(self, response):
        """Parse JSON response and decrypt the wrapped key."""
        try:
            response_data = response.json()
        except Exception as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response content: {response.content}")
            raise SDKException(f"Invalid JSON response from KAS: {e}") from e

        entity_wrapped_key = response_data.get("entityWrappedKey")
        if not entity_wrapped_key:
            raise SDKException("No entityWrappedKey in KAS response")

        # Decrypt the wrapped key
        if not self.decryptor:
            raise SDKException("Decryptor not initialized")
        encrypted_key = b64decode(entity_wrapped_key)
        return self.decryptor.decrypt(encrypted_key)

    def unwrap(self, key_access, policy_json, session_key_type=None) -> bytes:
        """Unwrap a key using Connect RPC.

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
            session_key_type,  # Pass algorithm type for NanoTDF
        )

        # Call Connect RPC unwrap
        return self._unwrap_with_connect_rpc(key_access, signed_token, session_key_type)

    def _unwrap_with_connect_rpc(
        self, key_access, signed_token, session_key_type=None
    ) -> bytes:
        """Connect RPC method for unwrapping keys.

        Args:
            key_access: KeyAccess object
            signed_token: Signed JWT token
            session_key_type: Optional session key type (RSA_KEY_TYPE or EC_KEY_TYPE)

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

            # Both ECDH and RSA modes return an RSA-encrypted key
            # For ECDH (EC_KEY_TYPE): KAS performs ECDH to derive symmetric key, then RSA-encrypts it with client public key
            # For RSA (RSA_KEY_TYPE): KAS RSA-decrypts wrapped key, then RSA-encrypts it with client public key
            # In both cases, we need to RSA-decrypt using our client private key
            if not self.decryptor:
                raise SDKException("Decryptor not initialized")

            result = self.decryptor.decrypt(entity_wrapped_key)

            if session_key_type == EC_KEY_TYPE:
                logging.info(
                    f"Connect RPC rewrap succeeded (ECDH - KAS derived key via ECDH, length={len(result)} bytes)"
                )
            else:
                logging.info(
                    f"Connect RPC rewrap succeeded (RSA - length={len(result)} bytes)"
                )
            return result

        except Exception as e:
            logging.error(f"Connect RPC rewrap failed: {e}")
            raise SDKException(f"Connect RPC rewrap failed: {e}") from e

    def get_key_cache(self) -> KASKeyCache:
        """Return the KAS key cache used for storing and retrieving encryption keys."""
        return self.cache
