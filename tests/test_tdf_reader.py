"""Tests for TDFReader."""

import io
import json
from unittest.mock import MagicMock, patch

import pytest

from otdf_python.policy_object import PolicyObject
from otdf_python.tdf_reader import (
    TDF_MANIFEST_FILE_NAME,
    TDF_PAYLOAD_FILE_NAME,
    TDFReader,
)


class TestTDFReader:
    """Tests for the TDFReader class."""

    @pytest.fixture
    def mock_zip_reader(self):
        """Create a mock ZipReader for testing."""
        with patch("otdf_python.tdf_reader.ZipReader") as mock_zip_reader:
            # Mock data
            manifest_data = json.dumps({"test": "manifest"}).encode("utf-8")
            payload_data = b"test payload data"

            # Mock the ZipReader instance
            mock_reader_instance = mock_zip_reader.return_value
            mock_reader_instance.namelist.return_value = [
                TDF_MANIFEST_FILE_NAME,
                TDF_PAYLOAD_FILE_NAME,
            ]

            # Mock the read method to return appropriate data
            def mock_read(name):
                if name == TDF_MANIFEST_FILE_NAME:
                    return manifest_data
                elif name == TDF_PAYLOAD_FILE_NAME:
                    return payload_data
                return b""

            mock_reader_instance.read.side_effect = mock_read

            yield mock_reader_instance, manifest_data, payload_data

    def test_init_success(self, mock_zip_reader):
        """Test successful initialization of TDFReader."""
        mock_reader, _, _ = mock_zip_reader

        # Create a TDFReader with a mock file object
        TDFReader(io.BytesIO(b"fake tdf data"))

        # Verify ZipReader was created and its methods were called
        mock_reader.namelist.assert_called_once()

    def test_init_no_manifest(self, mock_zip_reader):
        """Test initialization fails when manifest is missing."""
        mock_reader, _, _ = mock_zip_reader
        # Return a list without manifest.json
        mock_reader.namelist.return_value = [TDF_PAYLOAD_FILE_NAME]

        # Should raise ValueError
        with pytest.raises(ValueError, match="tdf doesn't contain a manifest"):
            TDFReader(io.BytesIO(b"fake tdf data"))

    def test_init_no_payload(self, mock_zip_reader):
        """Test initialization fails when payload is missing."""
        mock_reader, _, _ = mock_zip_reader
        # Return a list without payload.bin
        mock_reader.namelist.return_value = [TDF_MANIFEST_FILE_NAME]

        # Should raise ValueError
        with pytest.raises(ValueError, match="tdf doesn't contain a payload"):
            TDFReader(io.BytesIO(b"fake tdf data"))

    def test_manifest(self, mock_zip_reader):
        """Test getting the manifest content."""
        mock_reader, _manifest_data, _ = mock_zip_reader
        manifest_content = json.dumps({"test": "manifest"})

        reader = TDFReader(io.BytesIO(b"fake tdf data"))

        # Get manifest content
        result = reader.manifest()

        # Verify result
        assert result == manifest_content
        mock_reader.read.assert_called_with(TDF_MANIFEST_FILE_NAME)

    def test_read_payload_bytes(self, mock_zip_reader):
        """Test reading bytes from the payload."""
        mock_reader, _, payload_data = mock_zip_reader

        reader = TDFReader(io.BytesIO(b"fake tdf data"))

        # Create buffer and read data
        buffer = bytearray(len(payload_data))
        bytes_read = reader.read_payload_bytes(buffer)

        # Verify result
        assert bytes_read == len(payload_data)
        assert bytes(buffer) == payload_data
        mock_reader.read.assert_called_with(TDF_PAYLOAD_FILE_NAME)

    @patch("otdf_python.tdf_reader.Manifest")
    def test_read_policy_object(self, mock_manifest, mock_zip_reader):
        """Test reading the policy object from the manifest."""
        mock_reader, _manifest_data, _ = mock_zip_reader

        # Create a realistic manifest with a base64 encoded policy
        import base64
        import json

        # Create a test policy object
        test_policy = {
            "uuid": "test-uuid-123",
            "body": {
                "dataAttributes": [
                    {
                        "attribute": "test.attr",
                        "displayName": "Test Attribute",
                        "isDefault": False,
                        "pubKey": "test-key",
                        "kasUrl": "https://kas.example.com",
                    }
                ],
                "dissem": ["user1", "user2"],
            },
        }

        # Encode the policy as base64
        policy_json = json.dumps(test_policy)
        policy_base64 = base64.b64encode(policy_json.encode("utf-8")).decode("utf-8")

        # Create a mock manifest object with the encoded policy
        mock_manifest_obj = MagicMock()
        mock_manifest_obj.encryptionInformation.policy = policy_base64
        mock_manifest.from_json.return_value = mock_manifest_obj

        reader = TDFReader(io.BytesIO(b"fake tdf data"))

        # Read policy object
        result = reader.read_policy_object()

        # Verify result
        assert isinstance(result, PolicyObject)
        assert result.uuid == "test-uuid-123"
        assert len(result.body.data_attributes) == 1
        assert result.body.data_attributes[0].attribute == "test.attr"
        assert result.body.dissem == ["user1", "user2"]
        mock_reader.read.assert_called_with(TDF_MANIFEST_FILE_NAME)
        mock_manifest.from_json.assert_called_once()
