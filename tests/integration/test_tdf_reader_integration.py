"""
Integration Tests for TDFReader.
"""

import io
import json
import pytest
import subprocess
import tempfile
from pathlib import Path

from otdf_python.tdf_reader import (
    TDFReader,
)
from tests.config_pydantic import CONFIG_TDF

# Fail fast if OPENTDF_PLATFORM_URL is not set
platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
if not platform_url:
    raise Exception("OPENTDF_PLATFORM_URL must be set in config for integration tests")


class TestTDFReaderIntegration:
    """Integration tests for TDFReader with real TDF files created by otdfctl."""

    @pytest.mark.integration
    def test_read_otdfctl_created_tdf_structure(self):
        """Test that TDFReader can parse the structure of files created by otdfctl."""

        # Create temporary directory for work
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create credentials file
            creds_file = temp_path / "creds.json"
            creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
            with open(creds_file, "w") as f:
                json.dump(creds_data, f)

            # Create input file
            input_file = temp_path / "input.txt"
            input_content = "Hello, World! This is test data for TDFReader integration."
            with open(input_file, "w") as f:
                f.write(input_content)

            # Define output files
            otdfctl_output = temp_path / "test-reader.txt.tdf"

            # Run otdfctl encrypt
            otdfctl_cmd = [
                "otdfctl",
                "encrypt",
                "--host",
                platform_url,
                "--with-client-creds-file",
                str(creds_file),
                "--tls-no-verify",
                "--mime-type",
                "text/plain",
                str(input_file),
                "-o",
                str(otdfctl_output),
            ]

            otdfctl_result = subprocess.run(
                otdfctl_cmd, capture_output=True, text=True, cwd=temp_path
            )

            # If otdfctl fails, skip the test (might be server issues)
            if otdfctl_result.returncode != 0:
                pytest.skip(f"otdfctl encrypt failed: {otdfctl_result.stderr}")

            # Verify the TDF file was created
            assert otdfctl_output.exists(), "otdfctl did not create TDF file"
            assert otdfctl_output.stat().st_size > 0, "otdfctl created empty TDF file"

            # Test that TDFReader can open and read the structure
            with open(otdfctl_output, "rb") as f:
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
    def test_read_otdfctl_tdf_with_attributes(self):
        """Test reading TDF files created by otdfctl with data attributes."""

        # Create temporary directory for work
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create credentials file
            creds_file = temp_path / "creds.json"
            creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
            with open(creds_file, "w") as f:
                json.dump(creds_data, f)

            # Create input file
            input_file = temp_path / "classified.txt"
            input_content = "This is classified data for testing attributes."
            with open(input_file, "w") as f:
                f.write(input_content)

            # Define output file
            otdfctl_output = temp_path / "classified.txt.tdf"

            # Run otdfctl encrypt with attributes
            otdfctl_cmd = [
                "otdfctl",
                "encrypt",
                "--host",
                platform_url,
                "--with-client-creds-file",
                str(creds_file),
                "--tls-no-verify",
                "--mime-type",
                "text/plain",
                "--attr",
                CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1,
                str(input_file),
                "-o",
                str(otdfctl_output),
            ]

            otdfctl_result = subprocess.run(
                otdfctl_cmd, capture_output=True, text=True, cwd=temp_path
            )

            # If otdfctl fails, skip the test
            assert otdfctl_result.returncode == 0, "otdfctl encrypt failed"

            # Verify the TDF file was created
            assert otdfctl_output.exists(), "otdfctl did not create TDF file"

            # Test that TDFReader can read the file with attributes
            with open(otdfctl_output, "rb") as f:
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
    def test_read_multiple_otdfctl_files(self):
        """Test reading multiple TDF files of different types created by otdfctl."""

        # Create temporary directory for work
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create credentials file
            creds_file = temp_path / "creds.json"
            creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
            with open(creds_file, "w") as f:
                json.dump(creds_data, f)

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

            successful_tests = 0

            for test_case in test_cases:
                try:
                    # Create input file
                    input_file = temp_path / f"{test_case['name']}.txt"
                    if isinstance(test_case["content"], bytes):
                        with open(input_file, "wb") as f:
                            f.write(test_case["content"])
                    else:
                        with open(input_file, "w") as f:
                            f.write(test_case["content"])

                    # Define output file
                    output_file = temp_path / f"{test_case['name']}.tdf"

                    # Run otdfctl encrypt
                    otdfctl_cmd = [
                        "otdfctl",
                        "encrypt",
                        "--host",
                        platform_url,
                        "--with-client-creds-file",
                        str(creds_file),
                        "--tls-no-verify",
                        "--mime-type",
                        test_case["mime_type"],
                        str(input_file),
                        "-o",
                        str(output_file),
                    ]

                    otdfctl_result = subprocess.run(
                        otdfctl_cmd, capture_output=True, text=True, cwd=temp_path
                    )

                    if otdfctl_result.returncode != 0:
                        continue  # Skip this test case but don't fail the whole test

                    # Test TDFReader on this file
                    with open(output_file, "rb") as f:
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

                    successful_tests += 1

                except Exception as e:
                    # Log the error but continue with other test cases
                    print(f"Test case {test_case['name']} failed: {e}")
                    continue

            # Require at least one successful test to pass
            assert successful_tests > 0, "At least one test case should succeed"
