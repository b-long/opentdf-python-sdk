"""Tests for TDF key management."""

import base64
import io
import unittest
import zipfile
from unittest.mock import Mock, patch

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
from otdf_python.tdf import TDF, TDFReaderConfig


class TestTDFKeyManagement(unittest.TestCase):
    """Tests for the TDF class key management pattern."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock Services object
        self.mock_services = Mock()
        self.mock_kas_client = Mock()
        self.mock_services.kas.return_value = self.mock_kas_client

        # Create a TDF instance with mock services
        self.tdf = TDF(services=self.mock_services)

        # Create a sample TDF file in memory
        self.tdf_bytes = self._create_mock_tdf()

    def _create_mock_tdf(self):
        """Create a mock TDF file with a minimal manifest."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Create key access object
            key_access = ManifestKeyAccess(
                type="rsa",
                url="https://kas.example.com",
                protocol="https",
                wrappedKey=base64.b64encode(b"wrapped_key_data").decode(),
                policyBinding=None,
            )

            # Create encryption info
            integrity_info = ManifestIntegrityInformation(
                rootSignature=ManifestRootSignature(alg="HS256", sig="signature"),
                segmentHashAlg="SHA256",
                segmentSizeDefault=1024,
                encryptedSegmentSizeDefault=1052,
                segments=[
                    ManifestSegment(
                        hash=base64.b64encode(b"hash").decode(),
                        segmentSize=10,
                        encryptedSegmentSize=38,
                    )
                ],
            )

            method = ManifestMethod(algorithm="AES-256-GCM", iv="", isStreamable=True)
            enc_info = ManifestEncryptionInformation(
                type="rsa",
                policy="{}",
                keyAccess=[key_access],
                method=method,
                integrityInformation=integrity_info,
            )

            # Create payload info
            payload_info = ManifestPayload(
                type="file",
                url="0.payload",
                protocol="zip",
                mimeType="application/octet-stream",
                isEncrypted=True,
            )

            # Create manifest
            manifest = Manifest(
                schemaVersion="4.3.0",
                encryptionInformation=enc_info,
                payload=payload_info,
                assertions=[],
            )

            # Add manifest to zip
            zf.writestr("0.manifest.json", manifest.to_json())

            # Add encrypted payload
            zf.writestr(
                "0.payload", b"\x00\x01\x02\x03\x04\x05"
            )  # dummy encrypted data

        return buffer.getvalue()

    def test_load_tdf_with_kas(self):
        """Test loading a TDF without providing a KAS private key."""
        # Configure the mock KAS client - use a proper 32-byte AES-GCM key
        self.mock_kas_client.unwrap.return_value = b"x" * 32  # 32-byte key

        # Patch the decrypt method
        with patch(
            "otdf_python.aesgcm.AesGcm.decrypt", return_value=b"decrypted_payload"
        ):
            # Load the TDF without a kas_private_key
            config = TDFReaderConfig(attributes=["attr1"])
            result = self.tdf.load_tdf(self.tdf_bytes, config)

            # Verify KAS client was used
            self.mock_kas_client.unwrap.assert_called_once()

            # Verify payload was decrypted
            self.assertEqual(result.payload, b"decrypted_payload")

    def test_load_tdf_with_private_key(self):
        """Test loading a TDF with a provided KAS private key (testing mode)."""
        # Patch AsymDecryption
        with patch(
            "otdf_python.asym_crypto.AsymDecryption"
        ) as mock_asym_decryption_class:
            mock_asym_decryption = Mock()
            mock_asym_decryption.decrypt.return_value = b"x" * 32  # 32-byte key
            mock_asym_decryption_class.return_value = mock_asym_decryption

            # Patch the decrypt method
            with patch(
                "otdf_python.aesgcm.AesGcm.decrypt", return_value=b"decrypted_payload"
            ):
                # Load the TDF with a kas_private_key
                config = TDFReaderConfig(
                    kas_private_key="PRIVATE_KEY_PEM", attributes=["attr1"]
                )
                result = self.tdf.load_tdf(self.tdf_bytes, config)

                # Verify AsymDecryption was used
                mock_asym_decryption_class.assert_called_once_with("PRIVATE_KEY_PEM")
                mock_asym_decryption.decrypt.assert_called_once()

                # Verify KAS client was NOT used
                self.mock_kas_client.unwrap.assert_not_called()

                # Verify payload was decrypted
                self.assertEqual(result.payload, b"decrypted_payload")


if __name__ == "__main__":
    unittest.main()
