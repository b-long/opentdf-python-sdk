"""NanoTDF reader and writer implementation."""

import contextlib
import hashlib
import json
import secrets
from io import BytesIO
from typing import BinaryIO

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from otdf_python.collection_store import CollectionStore, NoOpCollectionStore
from otdf_python.config import KASInfo, NanoTDFConfig
from otdf_python.constants import MAGIC_NUMBER_AND_VERSION
from otdf_python.ecc_mode import ECCMode
from otdf_python.policy_info import PolicyInfo
from otdf_python.policy_object import AttributeObject, PolicyBody, PolicyObject
from otdf_python.policy_stub import NULL_POLICY_UUID
from otdf_python.resource_locator import ResourceLocator
from otdf_python.sdk_exceptions import SDKException
from otdf_python.symmetric_and_payload_config import SymmetricAndPayloadConfig

from .asym_crypto import AsymDecryption


class NanoTDFException(SDKException):
    """Base exception for NanoTDF operations."""

    pass


class NanoTDFMaxSizeLimit(NanoTDFException):
    """Exception for NanoTDF size limit exceeded."""

    pass


class UnsupportedNanoTDFFeature(NanoTDFException):
    """Exception for unsupported NanoTDF features."""

    pass


class InvalidNanoTDFConfig(NanoTDFException):
    """Exception for invalid NanoTDF configuration."""

    pass


class NanoTDF:
    """NanoTDF reader and writer for compact TDF format."""

    MAGIC_NUMBER_AND_VERSION = MAGIC_NUMBER_AND_VERSION
    K_MAX_TDF_SIZE = (16 * 1024 * 1024) - 3 - 32
    K_NANOTDF_GMAC_LENGTH = 8
    K_IV_PADDING = 9
    K_NANOTDF_IV_SIZE = 3
    K_EMPTY_IV = bytes([0x0] * 12)

    def __init__(self, services=None, collection_store: CollectionStore | None = None):
        """Initialize NanoTDF reader/writer."""
        self.services = services
        self.collection_store = collection_store or NoOpCollectionStore()

    def _create_policy_object(self, attributes: list[str]) -> PolicyObject:
        # TODO: Replace this with a proper Policy UUID value
        policy_uuid = NULL_POLICY_UUID
        data_attributes = [AttributeObject(attribute=a) for a in attributes]
        body = PolicyBody(data_attributes=data_attributes, dissem=[])
        return PolicyObject(uuid=policy_uuid, body=body)

    def _serialize_policy_object(self, obj):
        """Serialize policy object to compatible JSON format."""
        from otdf_python.policy_object import AttributeObject, PolicyBody

        if isinstance(obj, PolicyBody):
            # Convert data_attributes to dataAttributes and use null instead of empty array
            result = {
                "dataAttributes": obj.data_attributes if obj.data_attributes else None,
                "dissem": obj.dissem if obj.dissem else None,
            }
            return result
        elif isinstance(obj, AttributeObject):
            # Convert snake_case field names to camelCase for JSON serialization
            return {
                "attribute": obj.attribute,
                "displayName": obj.display_name,
                "isDefault": obj.is_default,
                "pubKey": obj.pub_key,
                "kasUrl": obj.kas_url,
            }
        else:
            return obj.__dict__

    def _prepare_payload(self, payload: bytes | BytesIO) -> bytes:
        """Convert BytesIO to bytes and validate payload size.

        Args:
            payload: The payload data as bytes or BytesIO

        Returns:
            bytes: The payload as bytes

        Raises:
            NanoTDFMaxSizeLimit: If the payload exceeds the maximum size

        """
        if isinstance(payload, BytesIO):
            payload = payload.getvalue()
        if len(payload) > self.K_MAX_TDF_SIZE:
            raise NanoTDFMaxSizeLimit("exceeds max size for nano tdf")
        return payload

    def _prepare_policy_data(self, config: NanoTDFConfig) -> tuple[bytes, str]:
        """Prepare policy data from configuration.

        Args:
            config: NanoTDFConfig configuration

        Returns:
            tuple: (policy_body, policy_type)

        """
        attributes = config.attributes if config.attributes else []
        policy_object = self._create_policy_object(attributes)
        policy_json = json.dumps(
            policy_object, default=self._serialize_policy_object
        ).encode("utf-8")
        policy_type = (
            config.policy_type if config.policy_type else "EMBEDDED_POLICY_PLAIN_TEXT"
        )

        if policy_type == "EMBEDDED_POLICY_PLAIN_TEXT":
            policy_body = policy_json
        else:
            # Encrypt policy
            policy_key = secrets.token_bytes(32)
            aesgcm = AESGCM(policy_key)
            iv = secrets.token_bytes(12)
            policy_body = aesgcm.encrypt(iv, policy_json, None)

        return policy_body, policy_type

    def _prepare_encryption_key(self, config: NanoTDFConfig) -> bytes:
        """Get encryption key from config if provided as hex string, otherwise generate a new random key."""
        key = None
        if (
            config.cipher
            and isinstance(config.cipher, str)
            and all(c in "0123456789abcdefABCDEF" for c in config.cipher)
        ):
            key = bytes.fromhex(config.cipher)
        if not key:
            key = secrets.token_bytes(32)
        return key

    def _create_header(
        self,
        policy_body: bytes,
        policy_type: str,
        config: NanoTDFConfig,
        ephemeral_public_key: bytes | None = None,
    ) -> bytes:
        """Create the NanoTDF header.

        Args:
            policy_body: The policy body bytes
            policy_type: The policy type string
            config: NanoTDFConfig configuration
            ephemeral_public_key: Optional compressed ephemeral public key (from ECDH)

        Returns:
            bytes: The header bytes

        """
        from otdf_python.header import Header  # Local import to avoid circular import

        # KAS URL from KASInfo or default
        kas_url = "https://kas.example.com"
        if config.kas_info_list and len(config.kas_info_list) > 0:
            kas_url = config.kas_info_list[0].url

        # KAS Key ID - use "e1" for EC (ECDH) mode or "r1" for RSA mode
        # If ephemeral_public_key is provided, we're using ECDH (EC), otherwise RSA
        # EC key ID, use "e1"
        # RSA key ID, use "r1"
        kas_id = "e1" if ephemeral_public_key else "r1"

        kas_locator = ResourceLocator(kas_url, kas_id)

        # Get ECC mode from config or use default
        ecc_mode = ECCMode(0, False)
        if config.ecc_mode:
            if isinstance(config.ecc_mode, str):
                ecc_mode = ECCMode.from_string(config.ecc_mode)
            else:
                ecc_mode = config.ecc_mode

        # Default payload config
        # Use cipher_type=5 for AES-256-GCM with 128-bit tag (16 bytes)
        # This matches Python's cryptography AESGCM default
        payload_config = SymmetricAndPayloadConfig(5, 0, False)

        # Create policy info
        policy_info = PolicyInfo()
        if policy_type == "EMBEDDED_POLICY_PLAIN_TEXT":
            policy_info.set_embedded_plain_text_policy(policy_body)
        else:
            policy_info.set_embedded_encrypted_text_policy(policy_body)

        # Create policy binding (GMAC)
        policy_binding = hashlib.sha256(policy_body).digest()[
            -self.K_NANOTDF_GMAC_LENGTH :
        ]

        # Build the header
        header = Header()
        header.set_kas_locator(kas_locator)
        header.set_ecc_mode(ecc_mode)
        header.set_payload_config(payload_config)
        header.set_policy_info(policy_info)
        header.policy_binding = policy_binding

        # Set ephemeral key - use provided ECDH key or generate random placeholder
        if ephemeral_public_key:
            header.set_ephemeral_key(ephemeral_public_key)
        else:
            # Fallback: generate random bytes as placeholder (for symmetric key case)
            header.set_ephemeral_key(
                secrets.token_bytes(
                    ECCMode.get_ec_compressed_pubkey_size(
                        ecc_mode.get_elliptic_curve_type()
                    )
                )
            )

        # Generate and return the header bytes with magic number
        header_bytes = header.to_bytes()
        return self.MAGIC_NUMBER_AND_VERSION + header_bytes

    def _is_ec_key(self, key_pem: str) -> bool:
        """Detect if a PEM key is an EC key (vs RSA).

        Args:
            key_pem: PEM-formatted key string

        Returns:
            bool: True if EC key, False if RSA key

        Raises:
            SDKException: If key cannot be parsed

        """
        try:
            # Try to load as public key first
            if "BEGIN PUBLIC KEY" in key_pem or "BEGIN CERTIFICATE" in key_pem:
                if "BEGIN CERTIFICATE" in key_pem:
                    from cryptography.x509 import load_pem_x509_certificate

                    cert = load_pem_x509_certificate(key_pem.encode())
                    public_key = cert.public_key()
                else:
                    public_key = serialization.load_pem_public_key(key_pem.encode())
                return isinstance(public_key, ec.EllipticCurvePublicKey)
            # Try to load as private key
            elif "BEGIN" in key_pem and "PRIVATE KEY" in key_pem:
                private_key = serialization.load_pem_private_key(
                    key_pem.encode(), password=None
                )
                return isinstance(private_key, ec.EllipticCurvePrivateKey)
            else:
                raise SDKException("Invalid PEM format - no BEGIN header found")
        except Exception as e:
            raise SDKException(f"Failed to detect key type: {e}") from e

    def _derive_key_with_ecdh(  # noqa: C901
        self, config: NanoTDFConfig
    ) -> tuple[bytes, bytes | None, bytes | None]:
        """Derive encryption key using ECDH if KAS public key is provided or can be fetched.

        This implements the NanoTDF spec's ECDH + HKDF key derivation:
        1. Generate ephemeral keypair
        2. Perform ECDH with KAS public key to get shared secret
        3. Use HKDF to derive symmetric key from shared secret

        For backward compatibility, also supports RSA key wrapping when an RSA key is detected.

        Args:
            config: NanoTDFConfig with potential KASInfo and ECC mode

        Returns:
            tuple: (derived_key, ephemeral_public_key_compressed, kas_public_key)
                - derived_key: 32-byte AES-256 key for encrypting the payload
                - ephemeral_public_key_compressed: Compressed ephemeral public key to store in header (None for RSA)
                - kas_public_key: KAS public key PEM string (or None if not available)

        """
        import logging

        from otdf_python.ecdh import encrypt_key_with_ecdh

        kas_public_key = None
        derived_key = None
        ephemeral_public_key_compressed = None

        if config.kas_info_list and len(config.kas_info_list) > 0:
            # Get the first KASInfo with a public_key or fetch it
            for kas_info in config.kas_info_list:
                if kas_info.public_key:
                    kas_public_key = kas_info.public_key
                    break
                elif self.services:
                    # Try to fetch public key from KAS service
                    try:
                        # For NanoTDF, prefer EC keys for ECDH - set algorithm if not specified
                        if not kas_info.algorithm:
                            # Default to EC secp256r1 for NanoTDF ECDH
                            kas_info.algorithm = "ec:secp256r1"
                            logging.info(
                                f"Fetching EC public key from KAS for NanoTDF ECDH: {kas_info.url}"
                            )
                        else:
                            logging.info(
                                f"Fetching public key (algorithm={kas_info.algorithm}) from KAS: {kas_info.url}"
                            )

                        updated_kas = self.services.kas().get_public_key(kas_info)
                        kas_public_key = updated_kas.public_key
                        # Update the config with the fetched public key
                        kas_info.public_key = kas_public_key
                        break
                    except Exception as e:
                        logging.warning(
                            f"Failed to fetch public key from KAS {kas_info.url}: {e}"
                        )
                        # Continue to next KAS or proceed without wrapping

        if kas_public_key:
            # Detect if key is EC or RSA
            is_ec = self._is_ec_key(kas_public_key)

            if is_ec:
                # EC key - use ECDH + HKDF
                # Determine curve from config
                curve_name = "secp256r1"  # Default
                if config.ecc_mode:
                    if isinstance(config.ecc_mode, str):
                        # Parse the string to get actual curve name
                        # Handles cases like "gmac" or "ecdsa" which map to secp256r1
                        try:
                            ecc_mode_obj = ECCMode.from_string(config.ecc_mode)
                            curve_name = ecc_mode_obj.get_curve_name()
                        except (ValueError, AttributeError):
                            # If parsing fails, stick with default
                            logging.warning(
                                f"Could not parse ecc_mode '{config.ecc_mode}', using default secp256r1"
                            )
                            curve_name = "secp256r1"
                    else:
                        # Get curve name from ECCMode object
                        curve_name = config.ecc_mode.get_curve_name()

                try:
                    # Use ECDH to derive key and generate ephemeral keypair
                    derived_key, ephemeral_public_key_compressed = (
                        encrypt_key_with_ecdh(kas_public_key, curve_name=curve_name)
                    )
                    logging.info(
                        f"Successfully derived NanoTDF key using ECDH with curve {curve_name}"
                    )
                except Exception as e:
                    logging.warning(f"Failed to derive key with ECDH: {e}")
                    derived_key = None
                    ephemeral_public_key_compressed = None
            else:
                # RSA key - use RSA wrapping for backward compatibility
                try:
                    # Generate random symmetric key
                    derived_key = secrets.token_bytes(32)
                    # For RSA mode, we don't use ephemeral keys - the symmetric key
                    # will be wrapped by KAS using RSA
                    ephemeral_public_key_compressed = None
                    logging.info(
                        "Generated symmetric key for RSA wrapping (backward compatibility)"
                    )
                except Exception as e:
                    logging.warning(f"Failed to generate key for RSA wrapping: {e}")
                    derived_key = None
                    ephemeral_public_key_compressed = None
        else:
            logging.warning(
                "No KAS public key available - creating NanoTDF without key derivation"
            )

        return derived_key, ephemeral_public_key_compressed, kas_public_key

    def _encrypt_payload(self, payload: bytes, key: bytes) -> tuple[bytes, bytes]:
        """Encrypt the payload using AES-GCM.

        Args:
            payload: The payload to encrypt
            key: The encryption key

        Returns:
            tuple: (iv, ciphertext)

        """
        iv = secrets.token_bytes(self.K_NANOTDF_IV_SIZE)
        iv_padded = self.K_EMPTY_IV[: self.K_IV_PADDING] + iv
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(iv_padded, payload, None)
        return iv, ciphertext

    def create_nano_tdf(
        self, payload: bytes | BytesIO, output_stream: BinaryIO, config: NanoTDFConfig
    ) -> int:
        """Stream-based NanoTDF creation - writes encrypted payload to an output stream.

        For convenience method that returns bytes, use create_nanotdf() instead.
        Supports ECDH key derivation if KAS info with public key is provided in config.

        Args:
            payload: The payload data as bytes or BytesIO
            output_stream: The output stream to write the NanoTDF to
            config: NanoTDFConfig configuration for the NanoTDF creation

        Returns:
            int: The size of the created NanoTDF

        Raises:
            NanoTDFMaxSizeLimit: If the payload exceeds the maximum size
            UnsupportedNanoTDFFeature: If an unsupported feature is requested
            InvalidNanoTDFConfig: If the configuration is invalid
            SDKException: For other errors

        """
        # Process payload and validate size
        payload = self._prepare_payload(payload)

        # Process policy data
        policy_body, policy_type = self._prepare_policy_data(config)

        # Try to derive key using ECDH or RSA
        (
            derived_key,
            ephemeral_public_key_compressed,
            kas_public_key,  # noqa: RUF059
        ) = self._derive_key_with_ecdh(config)

        # Use ECDH-derived key if available; otherwise use/generate symmetric key
        # Fallback to symmetric key (for testing or when KAS is not available)
        key = derived_key or self._prepare_encryption_key(config)

        # Create header with ephemeral public key (if ECDH was used)
        header_bytes = self._create_header(
            policy_body, policy_type, config, ephemeral_public_key_compressed
        )
        output_stream.write(header_bytes)

        # Encrypt payload
        iv, ciphertext_with_tag = self._encrypt_payload(payload, key)

        # NanoTDF payload format per spec:
        # [3 bytes: length] [3 bytes: IV] [variable: ciphertext] [tag]
        # Note: ciphertext_with_tag from AESGCM already includes the tag
        payload_data = iv + ciphertext_with_tag
        payload_length = len(payload_data)

        # Write payload length as 3 bytes (big-endian)
        length_bytes = payload_length.to_bytes(4, "big")[1:]  # Take last 3 bytes
        output_stream.write(length_bytes)

        # Write payload (IV + ciphertext + tag)
        output_stream.write(payload_data)

        return len(header_bytes) + 3 + payload_length

    def _kas_unwrap(
        self, nano_tdf_data: bytes, header_len: int, wrapped_key: bytes
    ) -> bytes | None:
        try:
            # For NanoTDF, send the entire header to KAS
            # KAS will extract the policy, ephemeral key, and perform ECDH
            import logging

            from otdf_python.header import Header
            from otdf_python.kas_client import KeyAccess

            # Extract header bytes (excluding magic number/version which is at start of nano_tdf_data)
            # The header starts at offset 0 (magic number) and goes for header_len bytes
            header_bytes = nano_tdf_data[:header_len]

            # Parse just to get KAS URL (we still need this for routing)
            header_obj = Header.from_bytes(header_bytes)
            kas_url = header_obj.kas_locator.get_resource_url()

            # Get KAS client from services
            kas_client = self.services.kas()

            # For NanoTDF: Pass header bytes to KAS
            # KAS will extract ephemeral key, decrypt policy if needed, and derive/unwrap the key
            # Use minimal policy JSON since KAS will extract it from the header
            policy_json = '{"uuid":"00000000-0000-0000-0000-000000000000","body":{"dataAttributes":[]}}'

            key_access = KeyAccess(
                url=kas_url,
                wrapped_key="",  # NanoTDF uses ECDH, not wrapped keys
                header=header_bytes,  # Send entire header to KAS
            )

            # Use EC key type for NanoTDF (always uses ECDH)
            from otdf_python.key_type_constants import EC_KEY_TYPE

            key = kas_client.unwrap(key_access, policy_json, EC_KEY_TYPE)
            logging.info("Successfully unwrapped NanoTDF key using KAS with header")

        except Exception as e:
            # If KAS unwrap fails, log and fall through to local unwrap methods
            import logging

            logging.warning(f"KAS unwrap failed for NanoTDF: {e}, trying local unwrap")
            key = None

        return key

    def _local_unwrap(self, wrapped_key: bytes, config: NanoTDFConfig) -> bytes:
        """Unwrap key locally using private key or mock unwrap (for testing/offline use)."""
        kas_private_key = None
        # Try to get from cipher field if it looks like a PEM key
        if (
            config.cipher
            and isinstance(config.cipher, str)
            and "-----BEGIN" in config.cipher
        ):
            kas_private_key = config.cipher

        # Check if mock unwrap is enabled in config string
        kas_mock_unwrap = False
        if config.config and "mock_unwrap=true" in config.config.lower():
            kas_mock_unwrap = True

        if not kas_private_key and not kas_mock_unwrap:
            raise InvalidNanoTDFConfig(
                "Unable to unwrap NanoTDF key: KAS unwrap failed and no local private key available. "
                "Ensure SDK has valid credentials or provide kas_private_key in config for offline use."
            )

        if kas_mock_unwrap:
            # Use the KAS mock unwrap_nanotdf logic
            from otdf_python.sdk import KAS

            return KAS().unwrap_nanotdf(
                curve=None,
                header=None,
                kas_url=None,
                wrapped_key=wrapped_key,
                kas_private_key=kas_private_key,
                mock=True,
            )
        else:
            asym = AsymDecryption(kas_private_key)
            return asym.decrypt(wrapped_key)

    def read_nano_tdf(  # noqa: C901
        self,
        nano_tdf_data: bytes | BytesIO,
        output_stream: BinaryIO,
        config: NanoTDFConfig,
    ) -> None:
        """Stream-based NanoTDF decryption - writes decrypted payload to an output stream.

        For convenience method that returns bytes, use read_nanotdf() instead.
        Supports ECDH key derivation and KAS key unwrapping.

        Args:
            nano_tdf_data: The NanoTDF data as bytes or BytesIO
            output_stream: The output stream to write the payload to
            config: Configuration for the NanoTDF reader

        Raises:
            InvalidNanoTDFConfig: If the NanoTDF format is invalid or config is missing required info
            SDKException: For other errors

        """
        # Convert to bytes if BytesIO
        if isinstance(nano_tdf_data, BytesIO):
            nano_tdf_data = nano_tdf_data.getvalue()

        from otdf_python.header import Header  # Local import to avoid circular import

        try:
            header_len = Header.peek_length(nano_tdf_data)
            header_obj = Header.from_bytes(nano_tdf_data[:header_len])
        except Exception as e:
            raise InvalidNanoTDFConfig(f"Failed to parse NanoTDF header: {e}") from e

        # Read payload section per NanoTDF spec:
        # [3 bytes: length] [3 bytes: IV] [variable: ciphertext] [tag]
        payload_offset = header_len

        # Read 3-byte payload length
        payload_length = int.from_bytes(
            nano_tdf_data[payload_offset : payload_offset + 3], "big"
        )
        payload_offset += 3

        # Read payload data (IV + ciphertext + tag)
        payload = nano_tdf_data[payload_offset : payload_offset + payload_length]

        # Extract IV (first 3 bytes)
        iv = payload[0:3]
        iv_padded = self.K_EMPTY_IV[: self.K_IV_PADDING] + iv

        # The rest is ciphertext + tag
        ciphertext_with_tag = payload[3:]

        key = None

        import logging

        from otdf_python.ecdh import decrypt_key_with_ecdh

        # Extract ephemeral public key from header
        ephemeral_public_key = header_obj.ephemeral_key
        ecc_mode = header_obj.ecc_mode

        # Get curve name from ECC mode
        curve_name = ecc_mode.get_curve_name()  # e.g., "secp256r1"

        # Try KAS unwrap first if services available
        if self.services:
            try:
                key = self._kas_unwrap(nano_tdf_data, header_len, wrapped_key=b"")
                if key:
                    logging.info(
                        "Successfully unwrapped NanoTDF key via KAS (ECDH mode)"
                    )
            except Exception as e:
                logging.warning(f"KAS unwrap failed for ECDH mode: {e}")
                key = None

        # If KAS unwrap didn't work, try local private key from config
        if not key:
            recipient_private_key_pem = None
            if config and hasattr(config, "cipher") and isinstance(config.cipher, str):
                if "-----BEGIN" in config.cipher:
                    # It's a PEM private key
                    recipient_private_key_pem = config.cipher
                else:
                    # Try to parse as hex symmetric key (fallback)
                    with contextlib.suppress(ValueError):
                        key = bytes.fromhex(config.cipher)

            # If we have a private key, detect type and use appropriate method
            if recipient_private_key_pem:
                # Detect if key is EC or RSA
                is_ec = self._is_ec_key(recipient_private_key_pem)

                if is_ec:
                    # EC key - use ECDH to derive the decryption key
                    try:
                        key = decrypt_key_with_ecdh(
                            recipient_private_key_pem,
                            ephemeral_public_key,
                            curve_name=curve_name,
                        )
                        logging.info(
                            f"Successfully derived NanoTDF decryption key using ECDH with curve {curve_name}"
                        )
                    except Exception as e:
                        logging.warning(f"Failed to derive key with ECDH: {e}")
                        key = None
                else:
                    # RSA key - this shouldn't happen for ECDH mode (wrapped_key_len should be > 0)
                    # But handle it gracefully
                    logging.warning(
                        "RSA private key provided for ECDH mode NanoTDF - this is unexpected. "
                        "NanoTDF should use wrapped_key_len > 0 for RSA mode."
                    )
                    key = None

        # If no key yet, raise error
        if not key:
            raise InvalidNanoTDFConfig(
                "Missing decryption key. Provide either:\n"
                "  1. KAS service for key unwrapping, or\n"
                "  2. Recipient's private key (PEM format) in config.cipher for ECDH, or\n"
                "  3. Symmetric key (hex) in config.cipher for symmetric decryption"
            )

        # Decrypt the ciphertext using AES-GCM
        # Use cipher type from header to determine tag size
        import logging

        tag_size_map = {
            0: 8,  # 64-bit
            1: 12,  # 96-bit
            2: 13,  # 104-bit
            3: 14,  # 112-bit
            4: 15,  # 120-bit
            5: 16,  # 128-bit
        }

        cipher_type = (
            header_obj.payload_config.get_cipher_type()
            if header_obj.payload_config
            else 5
        )
        tag_size = tag_size_map.get(cipher_type, 16)

        logging.info(
            f"Decrypting payload: key_len={len(key)}, key_hex={key.hex()[:40]}..., iv_3byte={iv.hex()}, iv_padded={iv_padded.hex()}, cipher_type={cipher_type}, tag_size={tag_size}, ciphertext_len={len(ciphertext_with_tag)}"
        )

        # For variable tag sizes, use lower-level Cipher API
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

        # Split ciphertext and tag
        ciphertext = ciphertext_with_tag[:-tag_size]
        tag = ciphertext_with_tag[-tag_size:]

        logging.info(
            f"Split: ciphertext={len(ciphertext)} bytes, tag={len(tag)} bytes ({tag.hex()})"
        )

        # Create cipher with GCM mode specifying tag and min_tag_length
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv_padded, tag=tag, min_tag_length=tag_size),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        output_stream.write(plaintext)

    def _convert_dict_to_nanotdf_config(self, config: dict) -> NanoTDFConfig:
        """Convert a dictionary config to a NanoTDFConfig object."""
        converted_config = NanoTDFConfig()
        if "attributes" in config:
            converted_config.attributes = config["attributes"]
        if "key" in config:
            converted_config.cipher = (
                config["key"].hex()
                if isinstance(config["key"], bytes)
                else config["key"]
            )
        if "kas_public_key" in config:
            kas_info = KASInfo(
                url="https://kas.example.com", public_key=config["kas_public_key"]
            )
            converted_config.kas_info_list = [kas_info]
        if "policy_type" in config:
            converted_config.policy_type = config["policy_type"]
        return converted_config

    def _handle_legacy_key_config(
        self, config: dict | NanoTDFConfig
    ) -> tuple[bytes, dict | NanoTDFConfig]:
        """Handle key configuration for legacy method."""
        key = None
        if isinstance(config, dict) and "key" in config:
            key = config["key"]
        elif (
            hasattr(config, "cipher")
            and config.cipher
            and isinstance(config.cipher, str)
            and all(c in "0123456789abcdefABCDEF" for c in config.cipher)
        ):
            key = bytes.fromhex(config.cipher)

        if not key:
            key = secrets.token_bytes(32)
            if isinstance(config, dict):
                config["key"] = key
            else:
                config.cipher = key.hex()
        return key, config

    def create_nanotdf(self, data: bytes, config: dict | NanoTDFConfig) -> bytes:
        """Create a NanoTDF and return the encrypted bytes.

        For stream-based version, use create_nano_tdf() instead.
        """
        if len(data) > self.K_MAX_TDF_SIZE:
            raise NanoTDFMaxSizeLimit("exceeds max size for nano tdf")

        # If config is already a NanoTDFConfig, use it; otherwise create one
        if not isinstance(config, NanoTDFConfig):
            config = self._convert_dict_to_nanotdf_config(config)

        # Create output buffer
        output = BytesIO()

        # Create NanoTDF using the new method
        self.create_nano_tdf(data, output, config)

        # Return the bytes
        output.seek(0)
        return output.getvalue()
        # Header construction, based on Java implementation
        # This method now uses the more modular create_nano_tdf method

    def _convert_dict_to_read_config(self, config: dict) -> NanoTDFConfig:
        """Convert a dictionary config to a NanoTDFConfig object for reading."""
        converted_config = NanoTDFConfig()
        if "key" in config:
            converted_config.cipher = (
                config["key"].hex()
                if isinstance(config["key"], bytes)
                else config["key"]
            )
        if "kas_private_key" in config:
            converted_config.cipher = config["kas_private_key"]
        return converted_config

    def _extract_key_for_reading(
        self, config: dict | NanoTDFConfig | None, wrapped_key: bytes | None
    ) -> bytes:
        """Extract the decryption key from config or unwrap it."""
        # For wrapped key case
        if wrapped_key:
            kas_private_key = None
            if isinstance(config, dict):
                kas_private_key = config.get("kas_private_key")
            elif (
                config
                and config.cipher
                and isinstance(config.cipher, str)
                and "-----BEGIN" in config.cipher
            ):
                kas_private_key = config.cipher

            if not kas_private_key:
                raise InvalidNanoTDFConfig("Missing kas_private_key for unwrap.")

            asym = AsymDecryption(kas_private_key)
            return asym.decrypt(wrapped_key)

        # For symmetric key case
        key = None
        if isinstance(config, dict):
            key = config.get("key")
        elif (
            config
            and config.cipher
            and isinstance(config.cipher, str)
            and all(c in "0123456789abcdefABCDEF" for c in config.cipher)
        ):
            key = bytes.fromhex(config.cipher)
        if not key:
            raise InvalidNanoTDFConfig("Missing decryption key in config.")
        return key

    def read_nanotdf(
        self, nanotdf_bytes: bytes, config: dict | NanoTDFConfig | None = None
    ) -> bytes:
        """Decrypt a NanoTDF and return the plaintext bytes.

        For stream-based version, use read_nano_tdf() instead.
        """
        output = BytesIO()

        # Convert config to NanoTDFConfig if it's a dict
        if isinstance(config, dict):
            config = self._convert_dict_to_read_config(config)

        # Use the stream-based method internally
        self.read_nano_tdf(nanotdf_bytes, output, config)

        return output.getvalue()
