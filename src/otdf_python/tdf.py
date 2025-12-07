"""TDF reader and writer functionality for OpenTDF platform."""

import base64
import hashlib
import hmac
import io
import logging
import os
import zipfile
from typing import TYPE_CHECKING, BinaryIO

if TYPE_CHECKING:
    from otdf_python.kas_client import KASClient

from dataclasses import dataclass

from otdf_python.aesgcm import AesGcm
from otdf_python.config import TDFConfig
from otdf_python.key_type_constants import RSA_KEY_TYPE
from otdf_python.manifest import (
    Manifest,
    ManifestEncryptionInformation,
    ManifestIntegrityInformation,
    ManifestKeyAccess,
    ManifestMethod,
    ManifestPayload,
    ManifestRootSignature,
    ManifestSegment,
)
from otdf_python.policy_stub import NULL_POLICY_UUID
from otdf_python.tdf_writer import TDFWriter


@dataclass
class TDFReader:
    """Container for TDF payload and manifest after reading."""

    payload: bytes
    manifest: Manifest


@dataclass
class TDFReaderConfig:
    """Configuration for TDF reader operations."""

    kas_private_key: str | None = None
    attributes: list[str] | None = None


class TDF:
    """TDF reader and writer for handling TDF encryption and decryption."""

    MAX_TDF_INPUT_SIZE = 68719476736
    GCM_KEY_SIZE = 32
    GCM_IV_SIZE = 12
    TDF_VERSION = "4.3.0"
    KEY_ACCESS_SCHEMA_VERSION = "1.0"
    SEGMENT_SIZE = 1024 * 1024  # 1MB segments

    # Global salt for key derivation - based on Java implementation
    GLOBAL_KEY_SALT = b"TDF-Session-Key"

    def __init__(self, services=None, maximum_size: int | None = None):
        """Initialize TDF reader/writer.

        Args:
            services: SDK services for KAS operations
            maximum_size: Maximum size allowed for TDF operations

        """
        self.services = services
        self.maximum_size = maximum_size or self.MAX_TDF_INPUT_SIZE

    def _validate_kas_infos(self, kas_infos):
        if not kas_infos:
            raise ValueError("kas_info (or list of KAS info) required in config")
        if not isinstance(kas_infos, list):
            kas_infos = [kas_infos]

        validated_kas_infos = []
        for kas in kas_infos:
            # If public key is missing, try to fetch it from the KAS service
            if not hasattr(kas, "public_key") or not kas.public_key:
                if self.services and hasattr(self.services, "kas"):
                    try:
                        # Fetch public key from KAS service
                        updated_kas = self.services.kas().get_public_key(kas)
                        validated_kas_infos.append(updated_kas)
                    except Exception as e:
                        raise ValueError(
                            f"Failed to fetch public key for KAS {kas.url}: {e}"
                        ) from e
                else:
                    raise ValueError(
                        "Each KAS info must have a public_key, or SDK services must be available to fetch it"
                    )
            else:
                validated_kas_infos.append(kas)
        return validated_kas_infos

    def _wrap_key_for_kas(self, key, kas_infos, policy_json=None):
        import hashlib
        import hmac

        from .asym_crypto import AsymEncryption

        key_access_objs = []
        for kas in kas_infos:
            asym = AsymEncryption(kas.public_key)
            wrapped_key = base64.b64encode(asym.encrypt(key)).decode()

            # Calculate policy binding hash following OpenTDF specification
            # Per spec: HMAC(DEK, Base64(policyJSON)) then hex-encode result
            if policy_json:
                # Step 1: Base64 encode the policy JSON first (per OpenTDF spec)
                policy_b64 = base64.b64encode(policy_json.encode("utf-8")).decode(
                    "utf-8"
                )

                # Step 2: Calculate HMAC-SHA256 using DEK and Base64-encoded policy
                hmac_result = hmac.new(
                    key, policy_b64.encode("utf-8"), hashlib.sha256
                ).digest()

                # Step 3: Hex encode the HMAC result (required by OpenTDF implementation)
                policy_binding_hex = hmac_result.hex()

                # Step 4: Base64 encode the hex string for transmission
                policy_binding_b64 = base64.b64encode(
                    policy_binding_hex.encode("utf-8")
                ).decode("utf-8")

                policy_binding_hash = {
                    "alg": "HS256",
                    "hash": policy_binding_b64,
                }
            else:
                # Fallback for cases where policy is not available
                policy_binding_hash = {
                    "alg": "HS256",
                    "hash": hashlib.sha256(wrapped_key.encode()).hexdigest(),
                }

            key_access_objs.append(
                ManifestKeyAccess(
                    type="wrapped",  # Changed from "rsa" to "wrapped" to match Java SDK
                    url=kas.url,
                    protocol="kas",
                    wrappedKey=wrapped_key,  # Changed from wrapped_key to wrappedKey
                    policyBinding=policy_binding_hash,  # Changed from policy_binding to policyBinding
                    kid=kas.kid,
                    schemaVersion=self.KEY_ACCESS_SCHEMA_VERSION,  # Add schema version
                )
            )
        return key_access_objs

    def _build_policy_json(self, config: TDFConfig) -> str:
        policy_obj = config.policy_object
        attributes = config.attributes
        import json as _json

        if policy_obj:
            return _json.dumps(policy_obj, default=self._serialize_policy_object)
        else:
            # Always create a proper policy structure, even when empty
            from otdf_python.policy_object import (
                AttributeObject,
                PolicyBody,
                PolicyObject,
            )

            # Create attribute objects from the attributes list (empty if no attributes)
            attr_objs = [AttributeObject(attribute=a) for a in (attributes or [])]
            body = PolicyBody(data_attributes=attr_objs, dissem=[])
            # TODO: Replace this with a proper Policy UUID value
            policy = PolicyObject(uuid=NULL_POLICY_UUID, body=body)
            return _json.dumps(policy, default=self._serialize_policy_object)

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
            # Convert AttributeObject to match expected format with camelCase field names
            return {
                "attribute": obj.attribute,
                "displayName": obj.display_name,
                "isDefault": obj.is_default,
                "pubKey": obj.pub_key,
                "kasUrl": obj.kas_url,
            }
        else:
            return obj.__dict__

    def _unwrap_key(self, key_access_objs, private_key_pem):
        """Unwrap the key locally using provided private key (used for testing)."""
        from .asym_crypto import AsymDecryption

        key = None
        for ka in key_access_objs:
            try:
                wrapped_key = base64.b64decode(ka.wrappedKey)  # Changed field name
                asym = AsymDecryption(private_key_pem)
                key = asym.decrypt(wrapped_key)
                break
            except Exception:
                continue
        if key is None:
            raise ValueError("No matching KAS private key could unwrap any payload key")
        return key

    def _unwrap_key_with_kas(self, key_access_objs, policy_b64) -> bytes:
        """Unwrap the key using the KAS service (production method)."""
        # Get KAS client from services
        if not self.services:
            raise ValueError("SDK services required for KAS operations")

        kas_client: KASClient = (
            self.services.kas()
        )  # The 'kas_client' should be typed as KASClient

        # Decode base64 policy for KAS
        try:
            policy_json = base64.b64decode(policy_b64).decode()
        except:  # noqa: E722
            # If base64 decode fails, assume it's already JSON
            policy_json = policy_b64

        # Try each key access object
        for ka in key_access_objs:
            try:
                # Pass the manifest key access object directly
                key_access = ka

                # Determine session key type from key_access properties
                session_key_type = RSA_KEY_TYPE  # Default to RSA

                # Check if this is an EC key based on key_access properties
                # In a more complete implementation, we would parse the key_access
                # to determine the exact curve type (P-256, P-384, P-521)
                if hasattr(ka, "type") and ka.type and "ec" in ka.type.lower():
                    from .key_type_constants import EC_KEY_TYPE

                    session_key_type = EC_KEY_TYPE

                # Unwrap key with KAS client
                key = kas_client.unwrap(key_access, policy_json, session_key_type)
                if key:
                    return key

            except Exception as e:  # noqa: PERF203
                logging.warning(f"Error unwrapping key with KAS: {e}")
                # Continue to try next key access
                continue

        raise ValueError(
            "Unable to unwrap the key with any available key access objects"
        )

    def _decrypt_segments(self, aesgcm, segments, encrypted_payload):
        decrypted = b""
        offset = 0
        for seg in segments:
            enc_len = seg.encryptedSegmentSize  # Changed field name
            enc_bytes = encrypted_payload[offset : offset + enc_len]

            # Handle empty or invalid encrypted payload in test scenarios
            if not enc_bytes or len(enc_bytes) < AesGcm.GCM_NONCE_LENGTH:
                # For testing, generate mock data when real data is unavailable
                import os

                iv = os.urandom(AesGcm.GCM_NONCE_LENGTH)
                ct = os.urandom(16)
            else:
                iv = enc_bytes[: AesGcm.GCM_NONCE_LENGTH]
                ct = enc_bytes[AesGcm.GCM_NONCE_LENGTH :]

            decrypted += aesgcm.decrypt(aesgcm.Encrypted(iv, ct))
            offset += enc_len
        return decrypted

    def create_tdf(
        self,
        payload: bytes | BinaryIO,
        config: TDFConfig,
        output_stream: io.BytesIO | None = None,
    ):
        """Create a TDF with the provided payload and configuration.

        Args:
            payload: The payload data as bytes or BinaryIO
            config: TDFConfig for encryption settings
            output_stream: Optional output stream, creates new BytesIO if not provided

        Returns:
            Tuple of (manifest, size, output_stream)

        """
        if output_stream is None:
            output_stream = io.BytesIO()
        writer = TDFWriter(output_stream)
        kas_infos = self._validate_kas_infos(config.kas_info_list)
        key = os.urandom(self.GCM_KEY_SIZE)

        # Build policy JSON to pass to policy binding calculation
        policy_json = self._build_policy_json(config)

        key_access_objs = self._wrap_key_for_kas(key, kas_infos, policy_json)
        aesgcm = AesGcm(key)
        segments = []
        segment_size = (
            getattr(config, "default_segment_size", None) or self.SEGMENT_SIZE
        )
        segment_hashes_raw = []
        total = 0
        # Write encrypted payload in segments
        with writer.payload() as f:
            if isinstance(payload, bytes):
                payload = io.BytesIO(payload)
            while True:
                chunk = payload.read(segment_size)
                if not chunk:
                    break
                encrypted = aesgcm.encrypt(chunk)
                f.write(encrypted.as_bytes())
                # Calculate segment hash using GMAC (last 16 bytes of encrypted segment)
                # This matches the platform SDK when segmentHashAlg is "GMAC"
                encrypted_bytes = encrypted.as_bytes()
                gmac_length = 16  # kGMACPayloadLength from platform SDK
                if len(encrypted_bytes) < gmac_length:
                    raise ValueError("Encrypted segment too short for GMAC")
                seg_hash_raw = encrypted_bytes[-gmac_length:]  # Take last 16 bytes
                seg_hash = base64.b64encode(seg_hash_raw).decode()
                segments.append(
                    ManifestSegment(
                        hash=seg_hash,
                        segmentSize=len(
                            chunk
                        ),  # Changed from segment_size to segmentSize
                        encryptedSegmentSize=len(
                            encrypted.as_bytes()
                        ),  # Changed from encrypted_segment_size to encryptedSegmentSize
                    )
                )
                # Collect raw segment hash bytes for root signature calculation
                segment_hashes_raw.append(seg_hash_raw)
                total += len(chunk)
        # Use config fields for policy
        policy_json = self._build_policy_json(config)
        # Encode policy as base64 to match Java SDK
        policy_b64 = base64.b64encode(policy_json.encode()).decode()

        # Calculate root signature: HMAC-SHA256 over concatenated segment hash raw bytes
        # This matches the platform SDK approach
        aggregate_hash = b"".join(segment_hashes_raw)
        root_sig_raw = hmac.new(key, aggregate_hash, hashlib.sha256).digest()
        root_sig = base64.b64encode(root_sig_raw).decode()
        integrity_info = ManifestIntegrityInformation(
            rootSignature=ManifestRootSignature(
                alg="HS256", sig=root_sig
            ),  # Changed field names
            segmentHashAlg="GMAC",  # Changed from SHA256 to GMAC to match Java SDK
            segmentSizeDefault=segment_size,  # Changed field name
            encryptedSegmentSizeDefault=segment_size + 28,  # Changed field name, approx
            segments=segments,
        )
        method = ManifestMethod(
            algorithm="AES-256-GCM", iv="", isStreamable=True
        )  # Changed field name
        enc_info = ManifestEncryptionInformation(
            type="split",
            policy=policy_b64,  # Use base64-encoded policy
            keyAccess=key_access_objs,  # Changed from key_access_obj to keyAccess
            method=method,
            integrityInformation=integrity_info,  # Changed field name
        )
        payload_info = ManifestPayload(
            type="reference",  # Changed from "file" to "reference" to match Java SDK
            url="0.payload",
            protocol="zip",
            mimeType=config.mime_type,  # Use MIME type from config
            isEncrypted=True,  # Changed from is_encrypted to isEncrypted
        )
        manifest = Manifest(
            schemaVersion=self.TDF_VERSION,  # Changed from tdf_version to schemaVersion
            encryptionInformation=enc_info,  # Changed field name
            payload=payload_info,
            assertions=[],
        )
        manifest_json = manifest.to_json()
        writer.append_manifest(manifest_json)
        size = writer.finish()
        return manifest, size, output_stream

    def load_tdf(
        self, tdf_data: bytes | io.BytesIO, config: TDFReaderConfig
    ) -> TDFReader:
        """Load and decrypt a TDF from the provided data.

        Args:
            tdf_data: The TDF data as bytes or BytesIO
            config: TDFReaderConfig with optional private key for local unwrapping

        Returns:
            TDFReader containing payload and manifest

        """
        # Extract manifest, unwrap payload key using KAS client
        # Handle both bytes and BinaryIO input
        tdf_bytes_io = io.BytesIO(tdf_data) if isinstance(tdf_data, bytes) else tdf_data

        with zipfile.ZipFile(tdf_bytes_io, "r") as z:
            manifest_json = z.read("0.manifest.json").decode()
            manifest = Manifest.from_json(manifest_json)

            if not manifest.encryptionInformation:
                raise ValueError("Missing encryption information in manifest")

            key_access_objs = (
                manifest.encryptionInformation.keyAccess
            )  # Changed field name

            # If a private key is provided, use local unwrapping (for testing)
            if config.kas_private_key:
                key = self._unwrap_key(key_access_objs, config.kas_private_key)
            else:
                # Use KAS client to unwrap the key
                if not self.services or not hasattr(self.services, "kas"):
                    raise ValueError(
                        "SDK services with KAS client required for remote key unwrapping"
                    )

                key = self._unwrap_key_with_kas(
                    key_access_objs,
                    manifest.encryptionInformation.policy,  # Changed field name
                )

            aesgcm = AesGcm(key)
            if not manifest.encryptionInformation.integrityInformation:
                raise ValueError("Missing integrity information in manifest")
            segments = (
                manifest.encryptionInformation.integrityInformation.segments
            )  # Changed field name
            encrypted_payload = z.read("0.payload")
            payload = self._decrypt_segments(aesgcm, segments, encrypted_payload)
            return TDFReader(payload=payload, manifest=manifest)

    def read_payload(
        self, tdf_bytes: bytes, config: dict, output_stream: BinaryIO
    ) -> None:
        """Read and verify TDF segments, decrypt if needed, and write the payload.

        Args:
            tdf_bytes: The TDF data as bytes
            config: Configuration dictionary for reading
            output_stream: The output stream to write the payload to

        """
        import base64
        import zipfile

        from otdf_python.aesgcm import AesGcm

        from .asym_crypto import AsymDecryption

        with zipfile.ZipFile(io.BytesIO(tdf_bytes), "r") as z:
            manifest_json = z.read("0.manifest.json").decode()
            manifest = Manifest.from_json(manifest_json)

            if not manifest.encryptionInformation:
                raise ValueError("Missing encryption information in manifest")

            wrapped_key = base64.b64decode(
                manifest.encryptionInformation.keyAccess[
                    0
                ].wrappedKey  # Changed field names
            )
            private_key_pem = config.get("kas_private_key")
            if not private_key_pem:
                raise ValueError("kas_private_key required in config for unwrap")
            asym = AsymDecryption(private_key_pem)
            key = asym.decrypt(wrapped_key)
            aesgcm = AesGcm(key)

            if not manifest.encryptionInformation.integrityInformation:
                raise ValueError("Missing integrity information in manifest")
            segments = (
                manifest.encryptionInformation.integrityInformation.segments
            )  # Changed field names
            encrypted_payload = z.read("0.payload")
            offset = 0
            for seg in segments:
                enc_len = seg.encryptedSegmentSize  # Changed field name
                enc_bytes = encrypted_payload[offset : offset + enc_len]
                # Integrity check using GMAC (last 16 bytes of encrypted segment)
                # This matches how segments are hashed when segmentHashAlg is "GMAC"
                gmac_length = 16  # kGMACPayloadLength from platform SDK
                if len(enc_bytes) < gmac_length:
                    raise ValueError(
                        "Encrypted segment too short for GMAC verification"
                    )
                seg_hash_raw = enc_bytes[-gmac_length:]  # Take last 16 bytes
                seg_hash = base64.b64encode(seg_hash_raw).decode()
                if seg.hash != seg_hash:
                    raise ValueError("Segment signature mismatch")
                iv = enc_bytes[: AesGcm.GCM_NONCE_LENGTH]
                ct = enc_bytes[AesGcm.GCM_NONCE_LENGTH :]
                pt = aesgcm.decrypt(aesgcm.Encrypted(iv, ct))
                output_stream.write(pt)
                offset += enc_len
