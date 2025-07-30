import unittest
from unittest.mock import Mock, patch
import base64
import io
import zipfile

from otdf_python.tdf import TDF, TDFReaderConfig
from otdf_python.manifest import (
    Manifest,
    ManifestEncryptionInformation,
    ManifestMethod,
    ManifestPayload,
    ManifestKeyAccess,
    ManifestIntegrityInformation,
    ManifestRootSignature,
    ManifestSegment,
)
from otdf_python.aesgcm import AesGcm


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
                key_type="rsa",
                url="https://kas.example.com",
                protocol="https",
                wrapped_key=base64.b64encode(b"wrapped_key_data").decode(),
                policy_binding=None,
                kid="test-kid",
            )

            # Create encryption info
            integrity_info = ManifestIntegrityInformation(
                root_signature=ManifestRootSignature(
                    algorithm="HS256", signature="signature"
                ),
                segment_hash_alg="SHA256",
                segment_size_default=1024,
                encrypted_segment_size_default=1052,
                segments=[
                    ManifestSegment(
                        hash=base64.b64encode(b"hash").decode(),
                        segment_size=10,
                        encrypted_segment_size=38,
                    )
                ],
            )

            method = ManifestMethod(algorithm="AES-256-GCM", iv="", is_streamable=True)
            enc_info = ManifestEncryptionInformation(
                key_access_type="rsa",
                policy="{}",
                key_access_obj=[key_access],
                method=method,
                integrity_information=integrity_info,
            )

            # Create payload info
            payload_info = ManifestPayload(
                type="file",
                url="0.payload",
                protocol="zip",
                mime_type="application/octet-stream",
                is_encrypted=True,
            )

            # Create manifest
            manifest = Manifest(
                tdf_version="4.3.0",
                encryption_information=enc_info,
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

        # Create a mock for the AesGcm.decrypt method
        original_decrypt = AesGcm.decrypt

        try:
            # Patch the decrypt method directly
            AesGcm.decrypt = Mock(return_value=b"decrypted_payload")

            # Load the TDF without a kas_private_key
            config = TDFReaderConfig(attributes=["attr1"])
            result = self.tdf.load_tdf(self.tdf_bytes, config)

            # Verify KAS client was used
            self.mock_kas_client.unwrap.assert_called_once()

            # Verify payload was decrypted
            self.assertEqual(result.payload, b"decrypted_payload")
        finally:
            # Restore original method
            AesGcm.decrypt = original_decrypt

    def test_load_tdf_with_private_key(self):
        """Test loading a TDF with a provided KAS private key (testing mode)."""
        # Patch AsymDecryption
        with patch(
            "otdf_python.asym_decryption.AsymDecryption"
        ) as mock_asym_decryption_class:
            mock_asym_decryption = Mock()
            mock_asym_decryption.decrypt.return_value = b"x" * 32  # 32-byte key
            mock_asym_decryption_class.return_value = mock_asym_decryption

            # Create a mock for the AesGcm.decrypt method
            original_decrypt = AesGcm.decrypt

            try:
                # Patch the decrypt method directly
                AesGcm.decrypt = Mock(return_value=b"decrypted_payload")

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
            finally:
                # Restore original method
                AesGcm.decrypt = original_decrypt


if __name__ == "__main__":
    unittest.main()
