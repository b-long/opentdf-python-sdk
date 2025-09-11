import hashlib
import json
import secrets
from io import BytesIO
from typing import BinaryIO

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from otdf_python.asym_crypto import AsymDecryption
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


class NanoTDFException(SDKException):
    pass


class NanoTDFMaxSizeLimit(NanoTDFException):
    pass


class UnsupportedNanoTDFFeature(NanoTDFException):
    pass


class InvalidNanoTDFConfig(NanoTDFException):
    pass


class NanoTDF:
    MAGIC_NUMBER_AND_VERSION = MAGIC_NUMBER_AND_VERSION
    K_MAX_TDF_SIZE = (16 * 1024 * 1024) - 3 - 32
    K_NANOTDF_GMAC_LENGTH = 8
    K_IV_PADDING = 9
    K_NANOTDF_IV_SIZE = 3
    K_EMPTY_IV = bytes([0x0] * 12)

    def __init__(self, services=None, collection_store: CollectionStore | None = None):
        self.services = services
        self.collection_store = collection_store or NoOpCollectionStore()

    def _create_policy_object(self, attributes: list[str]) -> PolicyObject:
        # TODO: Replace this with a proper Policy UUID value
        policy_uuid = NULL_POLICY_UUID
        data_attributes = [AttributeObject(attribute=a) for a in attributes]
        body = PolicyBody(data_attributes=data_attributes, dissem=[])
        return PolicyObject(uuid=policy_uuid, body=body)

    def _serialize_policy_object(self, obj):
        """Custom NanoTDF serializer to convert to compatible JSON format."""
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
        """
        Convert BytesIO to bytes and validate payload size.

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
        """
        Prepare policy data from configuration.

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
        self, policy_body: bytes, policy_type: str, config: NanoTDFConfig
    ) -> bytes:
        """
        Create the NanoTDF header.

        Args:
            policy_body: The policy body bytes
            policy_type: The policy type string
            config: NanoTDFConfig configuration

        Returns:
            bytes: The header bytes
        """
        from otdf_python.header import Header  # Local import to avoid circular import

        # KAS URL from KASInfo or default
        kas_url = "https://kas.example.com"
        if config.kas_info_list and len(config.kas_info_list) > 0:
            kas_url = config.kas_info_list[0].url

        kas_id = "kas-id"  # Default KAS ID
        kas_locator = ResourceLocator(kas_url, kas_id)

        # Get ECC mode from config or use default
        ecc_mode = ECCMode(0, False)
        if config.ecc_mode:
            if isinstance(config.ecc_mode, str):
                ecc_mode = ECCMode.from_string(config.ecc_mode)
            else:
                ecc_mode = config.ecc_mode

        # Default payload config
        payload_config = SymmetricAndPayloadConfig(0, 0, False)

        # Create policy info
        policy_info = PolicyInfo()
        if policy_type == "EMBEDDED_POLICY_PLAIN_TEXT":
            policy_info.set_embedded_plain_text_policy(policy_body)
        else:
            policy_info.set_embedded_encrypted_text_policy(policy_body)
        policy_info.set_policy_binding(
            hashlib.sha256(policy_body).digest()[-self.K_NANOTDF_GMAC_LENGTH :]
        )

        # Build the header
        header = Header()
        header.set_kas_locator(kas_locator)
        header.set_ecc_mode(ecc_mode)
        header.set_payload_config(payload_config)
        header.set_policy_info(policy_info)
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

    def _wrap_key_if_needed(
        self, key: bytes, config: NanoTDFConfig
    ) -> tuple[bytes, bytes | None]:
        """
        Wrap encryption key if KAS public key is provided.

        Args:
            key: The encryption key
            config: NanoTDFConfig with potential KASInfo

        Returns:
            tuple: (wrapped_key, kas_public_key)
        """
        kas_public_key = None
        wrapped_key = None

        if config.kas_info_list and len(config.kas_info_list) > 0:
            # Get the first KASInfo with a public_key
            for kas_info in config.kas_info_list:
                if kas_info.public_key:
                    kas_public_key = kas_info.public_key
                    break

        if kas_public_key:
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding

            public_key = serialization.load_pem_public_key(
                kas_public_key.encode(), backend=default_backend()
            )
            wrapped_key = public_key.encrypt(
                key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
            )

        return wrapped_key, kas_public_key

    def _encrypt_payload(self, payload: bytes, key: bytes) -> tuple[bytes, bytes]:
        """
        Encrypt the payload using AES-GCM.

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
        """
        Creates a NanoTDF with the provided payload and writes it to the output stream.
        Supports KAS key wrapping if KAS info with public key is provided in config.

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

        # Get or generate encryption key
        key = self._prepare_encryption_key(config)

        # Create header and write to output
        header_bytes = self._create_header(policy_body, policy_type, config)
        output_stream.write(header_bytes)

        # Encrypt payload
        iv, ciphertext = self._encrypt_payload(payload, key)

        # Wrap key if needed
        wrapped_key, kas_public_key = self._wrap_key_if_needed(key, config)

        # Compose the complete NanoTDF: [IV][CIPHERTEXT][WRAPPED_KEY][WRAPPED_KEY_LEN]
        if wrapped_key:
            nano_tdf_data = (
                iv + ciphertext + wrapped_key + len(wrapped_key).to_bytes(2, "big")
            )
        else:
            nano_tdf_data = iv + ciphertext + (0).to_bytes(2, "big")

        output_stream.write(nano_tdf_data)
        return len(header_bytes) + len(nano_tdf_data)

    def read_nano_tdf(
        self,
        nano_tdf_data: bytes | BytesIO,
        output_stream: BinaryIO,
        config: NanoTDFConfig,
        platform_url: str | None = None,
    ) -> None:
        """
        Reads a NanoTDF and writes the payload to the output stream.
        Supports KAS key unwrapping if kas_private_key is provided in config.

        Args:
            nano_tdf_data: The NanoTDF data as bytes or BytesIO
            output_stream: The output stream to write the payload to
            config: Configuration for the NanoTDF reader
            platform_url: Optional platform URL for KAS resolution

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
        except Exception:
            raise InvalidNanoTDFConfig("Failed to parse NanoTDF header.")
        payload_start = header_len
        payload = nano_tdf_data[payload_start:]
        # Do not check for magic/version in payload; it is only at the start of the header
        iv = payload[0:3]
        iv_padded = self.K_EMPTY_IV[: self.K_IV_PADDING] + iv
        # Find wrapped key
        wrapped_key_len = int.from_bytes(payload[-2:], "big")
        if wrapped_key_len > 0:
            wrapped_key = payload[-(2 + wrapped_key_len) : -2]

            # Get private key and mock unwrap config
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
                raise InvalidNanoTDFConfig("Missing kas_private_key for unwrap.")
            if kas_mock_unwrap:
                # Use the KAS mock unwrap_nanotdf logic
                from otdf_python.sdk import KAS

                key = KAS().unwrap_nanotdf(
                    curve=None,
                    header=None,
                    kas_url=None,
                    wrapped_key=wrapped_key,
                    kas_private_key=kas_private_key,
                    mock=True,
                )
            else:
                asym = AsymDecryption(kas_private_key)
                key = asym.decrypt(wrapped_key)
            ciphertext = payload[3 : -(2 + wrapped_key_len)]
        else:
            key = config.get("key")
            if not key:
                raise InvalidNanoTDFConfig("Missing decryption key in config.")
            ciphertext = payload[3:-2]
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(iv_padded, ciphertext, None)
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
        """Create a NanoTDF from input data using the provided configuration."""
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
        """Read and decrypt a NanoTDF, returning the original plaintext data."""
        output = BytesIO()
        from otdf_python.header import Header  # Local import to avoid circular import

        # Convert config to NanoTDFConfig if it's a dict
        if isinstance(config, dict):
            config = self._convert_dict_to_read_config(config)

        try:
            header_len = Header.peek_length(nanotdf_bytes)
            payload = nanotdf_bytes[header_len:]

            # Extract components
            iv = payload[0:3]
            iv_padded = self.K_EMPTY_IV[: self.K_IV_PADDING] + iv
            wrapped_key_len = int.from_bytes(payload[-2:], "big")

            wrapped_key = None
            if wrapped_key_len > 0:
                wrapped_key = payload[-(2 + wrapped_key_len) : -2]
                ciphertext = payload[3 : -(2 + wrapped_key_len)]
            else:
                ciphertext = payload[3:-2]

            # Get the decryption key
            key = self._extract_key_for_reading(config, wrapped_key)

            # Decrypt the payload
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(iv_padded, ciphertext, None)
            output.write(plaintext)

        except Exception as e:
            # Re-raise with a clearer message
            raise InvalidNanoTDFConfig(f"Error reading NanoTDF: {e!s}")

        return output.getvalue()
