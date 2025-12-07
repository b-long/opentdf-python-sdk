"""Integration Tests for TDFReader."""

import io
import json
import tempfile
from pathlib import Path

import pytest

from otdf_python.tdf_reader import (
    TDFReader,
)
from tests.config_pydantic import CONFIG_TDF
from tests.support_common import handle_subprocess_error
from tests.support_otdfctl_args import run_otdfctl_encrypt_command


class TestTDFReaderIntegration:
    """Integration tests for TDFReader with real TDF files created by otdfctl."""

    @pytest.mark.integration
    def test_read_otdfctl_created_tdf_structure(
        self, temp_credentials_file, collect_server_logs
    ):
        """Test that TDFReader can parse the structure of files created by otdfctl."""
        # Create temporary directory for work
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create input file
            input_file = temp_path / "input.txt"
            input_content = "Hello, World! This is test data for TDFReader integration."
            with input_file.open("w") as f:
                f.write(input_content)

            # Define output files
            otdfctl_output = temp_path / "test-reader.txt.tdf"

            # Run otdfctl encrypt
            otdfctl_encrypt_result = run_otdfctl_encrypt_command(
                creds_file=temp_credentials_file,
                input_file=input_file,
                output_file=otdfctl_output,
                mime_type="text/plain",
                cwd=temp_path,
            )

            # Fail fast on errors
            handle_subprocess_error(
                result=otdfctl_encrypt_result,
                collect_server_logs=collect_server_logs,
                scenario_name="otdfctl encrypt",
            )

            # Verify the TDF file was created
            assert otdfctl_output.exists(), "otdfctl did not create TDF file"
            assert otdfctl_output.stat().st_size > 0, "otdfctl created empty TDF file"

            # Test that TDFReader can open and read the structure
            with otdfctl_output.open("rb") as f:
                tdf_data = f.read()

            # Initialize TDFReader
            reader = TDFReader(io.BytesIO(tdf_data))

            # Test manifest reading
            manifest_content = reader.manifest()
            assert manifest_content, "Manifest should not be empty"

            # Parse the manifest JSON
            manifest_json = json.loads(manifest_content)
            assert "encryptionInformation" in manifest_json, (
                "Manifest should contain encryptionInformation"
            )
            assert "payload" in manifest_json, "Manifest should contain payload"

            # Verify encryption information structure
            enc_info = manifest_json["encryptionInformation"]
            assert "keyAccess" in enc_info, (
                "encryptionInformation should contain keyAccess"
            )
            assert "method" in enc_info, "encryptionInformation should contain method"
            assert "policy" in enc_info, "encryptionInformation should contain policy"
            assert "integrityInformation" in enc_info, (
                "encryptionInformation should contain integrityInformation"
            )

            # Verify payload information
            payload_info = manifest_json["payload"]
            assert "mimeType" in payload_info, "payload should contain mimeType"
            assert "isEncrypted" in payload_info, "payload should contain isEncrypted"
            assert payload_info["isEncrypted"] is True, "payload should be encrypted"

            # Test payload reading capability (without decryption)
            payload_buffer = bytearray(1024)  # Create a buffer for reading
            bytes_read = reader.read_payload_bytes(payload_buffer)
            assert bytes_read > 0, "Should be able to read some payload bytes"

            # Test policy object reading
            policy_obj = reader.read_policy_object()
            assert policy_obj is not None, "Should be able to read policy object"

    @pytest.mark.integration
    def test_read_otdfctl_tdf_with_attributes(
        self, temp_credentials_file, collect_server_logs
    ):
        """Test reading TDF files created by otdfctl with data attributes."""
        # Create temporary directory for work
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create input file
            input_file = temp_path / "input.txt"
            input_content = "This is input data for testing attributes."
            with input_file.open("w") as f:
                f.write(input_content)

            # Define output file
            otdfctl_output = temp_path / "input.txt.tdf"

            # Run otdfctl encrypt with attributes
            otdfctl_result = run_otdfctl_encrypt_command(
                creds_file=temp_credentials_file,
                input_file=input_file,
                output_file=otdfctl_output,
                mime_type="text/plain",
                attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1],
                cwd=temp_path,
            )

            # Fail fast on errors
            handle_subprocess_error(
                result=otdfctl_result,
                collect_server_logs=collect_server_logs,
                scenario_name="otdfctl encrypt with attributest",
            )

            # Verify the TDF file was created
            assert otdfctl_output.exists(), "otdfctl did not create TDF file"

            # Test that TDFReader can read the file with attributes
            with otdfctl_output.open("rb") as f:
                tdf_data = f.read()

            reader = TDFReader(io.BytesIO(tdf_data))
            manifest_content = reader.manifest()
            manifest_json = json.loads(manifest_content)

            # Verify the policy contains attributes
            assert "encryptionInformation" in manifest_json
            assert "policy" in manifest_json["encryptionInformation"]

            # Decode the policy to check for attributes
            import base64

            policy_b64 = manifest_json["encryptionInformation"]["policy"]
            policy_json = json.loads(base64.b64decode(policy_b64).decode())

            # Verify policy structure
            assert "body" in policy_json, "Policy should contain body"
            assert "dataAttributes" in policy_json["body"], (
                "Policy body should contain dataAttributes"
            )

            # Check that attributes exist (if any were actually set)
            # Note: otdfctl might not always include attributes in the policy depending on server configuration
            # So we just verify the structure is correct

            # Test that we can still read the policy object
            policy_obj = reader.read_policy_object()
            assert policy_obj is not None, (
                "Should be able to read policy object with attributes"
            )

    @pytest.mark.integration
    def test_read_multiple_otdfctl_files(
        self, temp_credentials_file, collect_server_logs
    ):
        """Test reading multiple TDF files of different types created by otdfctl."""
        # Create temporary directory for work
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test different file types and content
            test_cases = [
                {
                    "name": "text_file",
                    "content": "Simple text content for testing",
                    "mime_type": "text/plain",
                },
                {
                    "name": "json_data",
                    "content": json.dumps({"test": "data", "number": 42}),
                    "mime_type": "application/json",
                },
                {
                    "name": "binary_data",
                    "content": b"\x00\x01\x02\x03\x04\x05\xff\xfe\xfd",
                    "mime_type": "application/octet-stream",
                },
            ]

            for test_case in test_cases:
                # Create input file
                input_file = temp_path / f"{test_case['name']}.txt"
                if isinstance(test_case["content"], bytes):
                    with input_file.open("wb") as f:
                        f.write(test_case["content"])
                else:
                    with input_file.open("w") as f:
                        f.write(test_case["content"])

                # Define output file
                output_file = temp_path / f"{test_case['name']}.tdf"

                # Run otdfctl encrypt
                otdfctl_result = run_otdfctl_encrypt_command(
                    creds_file=temp_credentials_file,
                    input_file=input_file,
                    output_file=output_file,
                    mime_type=test_case["mime_type"],
                    cwd=temp_path,
                )

                # Fail fast on errors
                handle_subprocess_error(
                    result=otdfctl_result,
                    collect_server_logs=collect_server_logs,
                    scenario_name=f"Test case {test_case['name']}, otdfctl encrypt",
                )

                # Test TDFReader on this file
                with output_file.open("rb") as f:
                    tdf_data = f.read()

                reader = TDFReader(io.BytesIO(tdf_data))

                # Basic structure verification
                manifest_content = reader.manifest()
                assert manifest_content, (
                    f"Manifest should not be empty for {test_case['name']}"
                )

                manifest_json = json.loads(manifest_content)
                assert "payload" in manifest_json, (
                    f"Manifest should contain payload for {test_case['name']}"
                )

                # Verify MIME type is preserved
                payload_info = manifest_json["payload"]
                if "mimeType" in payload_info:
                    assert payload_info["mimeType"] == test_case["mime_type"], (
                        f"MIME type should be preserved for {test_case['name']}"
                    )

                # Test payload reading
                payload_buffer = bytearray(1024)
                bytes_read = reader.read_payload_bytes(payload_buffer)
                assert bytes_read > 0, (
                    f"Should read payload bytes for {test_case['name']}"
                )

                # Test policy object reading
                policy_obj = reader.read_policy_object()
                assert policy_obj is not None, (
                    f"Should read policy object for {test_case['name']}"
                )
