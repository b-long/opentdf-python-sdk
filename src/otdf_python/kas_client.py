"""
KASClient: Handles communication with the Key Access Service (KAS).
"""
import json
import time
import logging
from base64 import b64decode
from dataclasses import dataclass
import httpx

from .kas_key_cache import KASKeyCache
from .sdk_exceptions import SDKException, KasBadRequestException
from .crypto_utils import CryptoUtils
from .asym_decryption import AsymDecryption
from .kas_info import KASInfo
from .key_type_constants import RSA_KEY_TYPE, EC_KEY_TYPE

@dataclass
class KeyAccess:
    url: str
    wrapped_key: str
    ephemeral_public_key: str = None

class KASClient:
    def __init__(self, kas_url=None, token_source=None, cache=None, use_plaintext=False):
        self.kas_url = kas_url
        self.token_source = token_source
        self.cache = cache or KASKeyCache()
        self.use_plaintext = use_plaintext
        self.decryptor = None
        self.client_public_key = None

    def get_public_key(self, kas_info: KASInfo) -> KASInfo:
        """
        Retrieves the public key from the KAS for RSA operations.

        Args:
            kas_info: KASInfo object containing the URL and algorithm

        Returns:
            Updated KASInfo object with KID and PublicKey populated
        """
        cached_value = self.cache.get(kas_info.url, kas_info.algorithm)
        if cached_value:
            return cached_value

        try:
            url = f"{kas_info.url}/public-key"
            if kas_info.algorithm:
                url += f"?algorithm={kas_info.algorithm}"

            token = self.token_source() if self.token_source else None
            headers = {"Authorization": f"Bearer {token}"} if token else {}

            resp = httpx.get(url, headers=headers)
            resp.raise_for_status()

            response_data = resp.json()
            kas_info_copy = kas_info.clone()
            kas_info_copy.kid = response_data.get('kid')
            kas_info_copy.public_key = response_data.get('publicKey')

            self.cache.store(kas_info_copy)
            return kas_info_copy
        except Exception as e:
            raise SDKException(f"Error getting public key: {e}")

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
                logging.warning(f"Unknown session key type: {session_key_type}, defaulting to RSA")
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
        curve_name = session_key_type.curve_name
        ec_key_pair = ECKeyPair(curve_name=curve_name)
        client_public_key = ec_key_pair.public_key_in_pem_format()
        return ec_key_pair, client_public_key

    def _prepare_rsa_keypair(self):
        """
        Prepare RSA key pair for unwrapping, reusing if possible.

        Returns:
            Client public key
        """
        if self.decryptor is None:
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
            raise SDKException("ECKeyPair is null. Unable to proceed with the unwrap operation.")

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

    def unwrap(self, key_access: KeyAccess, policy: str, session_key_type=None):
        """
        Unwraps a key using the KAS.

        Args:
            key_access: KeyAccess object with the wrapped key
            policy: Policy string
            session_key_type: Type of the session key (KeyType enum or string "RSA"/"EC")

        Returns:
            Unwrapped key as bytes
        """
        session_key_type = self._normalize_session_key_type(session_key_type)
        ec_key_pair = None

        # Handle key generation based on session key type
        if session_key_type.is_ec:
            ec_key_pair, self.client_public_key = self._prepare_ec_keypair(session_key_type)
        else:
            self.client_public_key = self._prepare_rsa_keypair()

        # Prepare the request
        request_body = {
            "policy": policy,
            "clientPublicKey": self.client_public_key,
            "keyAccess": {
                "url": key_access.url,
                "wrappedKey": key_access.wrapped_key,
                "ephemeralPublicKey": key_access.ephemeral_public_key
            }
        }

        # Add JWT claims similar to Java implementation
        claims = {
            "requestBody": json.dumps(request_body),
            "iat": int(time.time()),
            "exp": int(time.time() + 60)  # 1 minute expiration
        }

        try:
            token = self.token_source() if self.token_source else None
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            headers["Content-Type"] = "application/json"

            # In Java this uses a signed JWT, but for simplicity we'll just send the request directly
            url = f"{key_access.url}/rewrap"
            resp = httpx.post(url, json=claims, headers=headers)

            if resp.status_code == 400:
                raise KasBadRequestException(f"Rewrap request 400: {resp.text}")
            resp.raise_for_status()

            response_data = resp.json()
            wrapped_key = b64decode(response_data.get("entityWrappedKey", ""))

            # Handle decryption based on session key type
            if session_key_type.is_ec:
                return self._unwrap_with_ec(wrapped_key, ec_key_pair, response_data)
            else:
                # RSA key unwrapping
                return self.decryptor.decrypt(wrapped_key)

        except KasBadRequestException as e:
            raise e
        except Exception as e:
            raise SDKException(f"Error unwrapping key: {e}")

    def get_key_cache(self) -> KASKeyCache:
        """Returns the key cache"""
        return self.cache
