"""Test CLI encryption functionality and TDF validation"""

import json
import tempfile
import zipfile
from pathlib import Path

import pytest

from otdf_python.tdf_reader import TDF_MANIFEST_FILE_NAME, TDF_PAYLOAD_FILE_NAME
from tests.support_cli_args import (
    run_cli_decrypt,
    run_cli_encrypt,
)
from tests.support_common import (
    handle_subprocess_error,
    validate_plaintext_file_created,
    validate_tdf3_file,
)
from tests.support_otdfctl_args import (
    run_otdfctl_decrypt_command,
    run_otdfctl_encrypt_command,
)


def _create_test_input_file(temp_path: Path, content: str) -> Path:
    """Create a test input file with the given content."""
    input_file = temp_path / "input.txt"
    with input_file.open("w") as f:
        f.write(content)
    return input_file


def _validate_key_access_objects(key_access: list) -> None:
    """Validate the keyAccessObjects (or KAO) structure in the TDF manifest."""
    # New format - keyAccess is an array
    print(f"keyAccess (array) with {len(key_access)} items")
    assert len(key_access) > 0, "keyAccess array should not be empty"

    # Validate first keyAccess object
    first_key_access = key_access[0]
    print(f"first keyAccess keys: {list(first_key_access.keys())}")

    # Required keyAccess fields for newer TDF format
    required_key_access_fields = [
        "protocol",
        "type",
        "url",
        "kid",
        "wrappedKey",
        "policyBinding",
    ]
    for field in required_key_access_fields:
        assert field in first_key_access, (
            f"keyAccess[0] missing required field: {field}"
        )

    # Validate protocol is "kas"
    assert first_key_access["protocol"] == "kas", (
        f"Expected keyAccess[0].protocol to be 'kas', got '{first_key_access['protocol']}'"
    )

    # Validate type is "wrapped"
    assert first_key_access["type"] == "wrapped", (
        f"Expected keyAccess[0].type to be 'wrapped', got '{first_key_access['type']}'"
    )

    # Validate policyBinding structure
    policy_binding = first_key_access["policyBinding"]
    assert isinstance(policy_binding, dict), "policyBinding should be a dictionary"
    assert "alg" in policy_binding, "policyBinding missing 'alg' field"
    assert "hash" in policy_binding, "policyBinding missing 'hash' field"
    assert policy_binding["alg"] == "HS256", (
        f"Expected policyBinding.alg to be 'HS256', got '{policy_binding['alg']}'"
    )


def _validate_tdf_zip_structure(tdf_path: Path) -> None:
    """Validate the internal structure of a TDF ZIP file."""
    with zipfile.ZipFile(tdf_path, "r") as zip_file:
        file_list = zip_file.namelist()

        # Print detailed file structure information for debugging
        print(f"\n=== TDF ZIP Structure Analysis for {tdf_path.name} ===")
        print(f"Files in ZIP: {len(file_list)}")
        for i, filename in enumerate(sorted(file_list)):
            file_info = zip_file.getinfo(filename)
            print(
                f"  {i + 1}. {filename} (size: {file_info.file_size} bytes, compressed: {file_info.compress_size} bytes)"
            )

        # TDF files should contain specific files
        required_files = [TDF_MANIFEST_FILE_NAME, TDF_PAYLOAD_FILE_NAME]
        for required_file in required_files:
            assert required_file in file_list, (
                f"TDF missing required file: {required_file}"
            )

        # Validate manifest.json can be read and parsed
        try:
            manifest_content = zip_file.read(TDF_MANIFEST_FILE_NAME)
            manifest_data = json.loads(manifest_content.decode("utf-8"))

            print("\n=== Manifest Structure Analysis ===")
            print(f"Manifest size: {len(manifest_content)} bytes")
            print(f"Top-level keys: {list(manifest_data.keys())}")

            # Check required top-level fields
            assert "encryptionInformation" in manifest_data, (
                "Manifest missing encryptionInformation"
            )
            assert "payload" in manifest_data, "Manifest missing payload information"

            # Validate schema version is present
            assert "schemaVersion" in manifest_data, "Manifest missing schemaVersion"

            # Analyze encryptionInformation structure
            enc_info = manifest_data["encryptionInformation"]
            print(f"encryptionInformation keys: {list(enc_info.keys())}")

            # Required encryptionInformation fields
            required_enc_fields = [
                "type",
                "policy",
                "keyAccess",
                "method",
                "integrityInformation",
            ]
            for field in required_enc_fields:
                assert field in enc_info, (
                    f"encryptionInformation missing required field: {field}"
                )

            # Validate that type is "split"
            assert enc_info["type"] == "split", (
                f"Expected encryptionInformation.type to be 'split', got '{enc_info['type']}'"
            )

            # Validate keyAccess structure
            key_access = enc_info["keyAccess"]
            print(f"keyAccess type: {type(key_access)}")

            if isinstance(key_access, list):
                _validate_key_access_objects(key_access)
            else:
                raise AssertionError(
                    f"Unexpected keyAccess type: {type(key_access)}. Expected list."
                )
            # Policy should be a base64-encoded string in the manifest
            policy = enc_info["policy"]
            assert isinstance(policy, str), "policy should be a base64-encoded string"
            assert len(policy) > 0, "policy should not be empty"

            # Validate that policy can be decoded from base64
            try:
                import base64

                policy_decoded = base64.b64decode(policy).decode("utf-8")
                policy_obj = json.loads(policy_decoded)
                assert isinstance(policy_obj, dict), (
                    "decoded policy should be a dictionary"
                )
                assert "uuid" in policy_obj, "policy missing 'uuid' field"
                assert "body" in policy_obj, "policy missing 'body' field"
            except Exception as e:
                raise AssertionError(f"Failed to decode base64 policy: {e}") from e

            # Validate method structure
            method = enc_info["method"]
            assert isinstance(method, dict), "method should be a dictionary"
            assert "algorithm" in method, "method missing 'algorithm' field"
            assert "isStreamable" in method, "method missing 'isStreamable' field"

            # Validate integrityInformation structure
            integrity_info = enc_info["integrityInformation"]
            assert isinstance(integrity_info, dict), (
                "integrityInformation should be a dictionary"
            )
            assert "rootSignature" in integrity_info, (
                "integrityInformation missing 'rootSignature' field"
            )
            assert "segmentSizeDefault" in integrity_info, (
                "integrityInformation missing 'segmentSizeDefault' field"
            )
            assert "encryptedSegmentSizeDefault" in integrity_info, (
                "integrityInformation missing 'encryptedSegmentSizeDefault' field"
            )

            # Check for keyAccessObjects (should not be present in newer format)
            if "keyAccessObjects" in enc_info:
                print(
                    "WARNING: Found keyAccessObjects in encryptionInformation - this is legacy format"
                )

            # Analyze payload structure
            payload_info = manifest_data["payload"]
            print(f"payload keys: {list(payload_info.keys())}")

            # Check for expected fields in payload
            expected_payload_fields = ["type", "url", "protocol", "isEncrypted"]
            for field in expected_payload_fields:
                assert field in payload_info, f"payload missing required field: {field}"
                print(f"  {field}: {payload_info[field]}")

            # Validate payload field values
            assert payload_info["type"] == "reference", (
                f"Expected payload.type to be 'reference', got '{payload_info['type']}'"
            )
            assert payload_info["protocol"] == "zip", (
                f"Expected payload.protocol to be 'zip', got '{payload_info['protocol']}'"
            )
            assert payload_info["isEncrypted"], (
                f"Expected payload.isEncrypted to be True, got '{payload_info['isEncrypted']}'"
            )

        except json.JSONDecodeError as e:
            raise AssertionError(f"Manifest is not valid JSON: {e}") from e
        except KeyError as e:
            raise AssertionError(f"Manifest missing required field: {e}") from e

        # Check for payload file (usually 0.payload)
        payload_files = [f for f in file_list if f.endswith(".payload")]
        assert len(payload_files) > 0, "TDF missing payload file"
        print(f"Payload files found: {payload_files}")

        print(f"✓ TDF structure validated: {len(file_list)} files, manifest valid")
        print("=" * 50)


def _run_otdfctl_decrypt(
    tdf_path: Path,
    creds_file: Path,
    temp_path: Path,
    collect_server_logs,
    expected_content: str,
) -> Path:
    """Run otdfctl decrypt on a TDF file and verify the decrypted content matches expected."""
    decrypt_output = temp_path / f"{tdf_path.stem}_decrypted.txt"

    otdfctl_decrypt_result = run_otdfctl_decrypt_command(
        creds_file=creds_file,
        tdf_file=tdf_path,
        output_file=decrypt_output,
        cwd=temp_path,
    )

    handle_subprocess_error(
        otdfctl_decrypt_result, collect_server_logs, "otdfctl decrypt"
    )

    validate_plaintext_file_created(
        path=decrypt_output, scenario="otdfctl", expected_content=expected_content
    )

    return decrypt_output


def _run_python_cli_decrypt(
    tdf_path: Path,
    creds_file: Path,
    temp_path: Path,
    collect_server_logs,
    expected_content: str,
    cwd: Path,
) -> Path:
    """Run Python CLI decrypt on a TDF file and verify the decrypted content matches expected."""
    decrypt_output = temp_path / f"{tdf_path.stem}_python_decrypted.txt"

    python_decrypt_result = run_cli_decrypt(
        creds_file=creds_file, input_file=tdf_path, output_file=decrypt_output, cwd=cwd
    )

    handle_subprocess_error(
        python_decrypt_result, collect_server_logs, "Python CLI decrypt"
    )

    validate_plaintext_file_created(
        path=decrypt_output, scenario="Python CLI", expected_content=expected_content
    )
    return decrypt_output


@pytest.mark.integration
def test_otdfctl_encrypt_with_validation(collect_server_logs, temp_credentials_file):
    """Integration test that uses otdfctl for encryption and validates the TDF thoroughly."""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        input_content = "Hello, World! This is test content for otdfctl encryption."
        input_file = _create_test_input_file(temp_path, input_content)

        # Define TDF file created by otdfctl
        otdfctl_tdf_output = temp_path / "otdfctl_test.txt.tdf"

        # Run otdfctl encrypt to create a TDF file
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_tdf_output,
            mime_type="text/plain",
            cwd=temp_path,
        )

        # Handle any encryption errors
        handle_subprocess_error(
            otdfctl_encrypt_result, collect_server_logs, "otdfctl encrypt"
        )

        # Validate the TDF file structure
        validate_tdf3_file(otdfctl_tdf_output, "otdfctl")
        _validate_tdf_zip_structure(otdfctl_tdf_output)

        # Test that the TDF can be decrypted successfully
        _run_otdfctl_decrypt(
            otdfctl_tdf_output,
            temp_credentials_file,
            temp_path,
            collect_server_logs,
            input_content,
        )

        print("✓ otdfctl successfully encrypted and decrypted TDF with correct content")
        print(f"TDF file size: {otdfctl_tdf_output.stat().st_size} bytes")


@pytest.mark.integration
def test_python_encrypt(collect_server_logs, temp_credentials_file, project_root):
    """Integration test that uses Python CLI for encryption only and verifies the TDF can be inspected"""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        input_content = "Hello, World! This is test content for Python CLI encryption."
        input_file = _create_test_input_file(temp_path, input_content)

        # Define TDF file created by Python CLI
        python_tdf_output = temp_path / "python_cli_test.txt.tdf"

        # Run Python CLI encrypt to create a TDF file
        python_encrypt_result = run_cli_encrypt(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=python_tdf_output,
            cwd=project_root,
        )

        # Handle any encryption errors
        handle_subprocess_error(
            python_encrypt_result, collect_server_logs, "Python CLI encrypt"
        )

        # Validate the TDF file structure
        validate_tdf3_file(python_tdf_output, "Python CLI")
        _validate_tdf_zip_structure(python_tdf_output)

        # Test that the TDF can be decrypted by otdfctl
        _run_otdfctl_decrypt(
            python_tdf_output,
            temp_credentials_file,
            temp_path,
            collect_server_logs,
            input_content,
        )

        print(
            "✓ Python CLI successfully encrypted TDF that can be decrypted by otdfctl"
        )
        print(f"TDF file size: {python_tdf_output.stat().st_size} bytes")


@pytest.mark.integration
def test_cross_tool_compatibility(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test that TDFs created by one tool can be decrypted by the other."""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        input_content = "Cross-tool compatibility test content. Testing 123!"
        input_file = _create_test_input_file(temp_path, input_content)

        # Test 1: otdfctl encrypt -> Python CLI decrypt
        otdfctl_tdf_output = temp_path / "otdfctl_for_python_decrypt.txt.tdf"

        # Encrypt with otdfctl
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_tdf_output,
            mime_type="text/plain",
            cwd=temp_path,
        )

        handle_subprocess_error(
            otdfctl_encrypt_result,
            collect_server_logs,
            "otdfctl encrypt (cross-tool test)",
        )

        # Decrypt with Python CLI
        _run_python_cli_decrypt(
            otdfctl_tdf_output,
            temp_credentials_file,
            temp_path,
            collect_server_logs,
            input_content,
            project_root,
        )

        # Test 2: Python CLI encrypt -> otdfctl decrypt
        python_tdf_output = temp_path / "python_for_otdfctl_decrypt.txt.tdf"

        # Encrypt with Python CLI
        python_encrypt_result = run_cli_encrypt(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=python_tdf_output,
            cwd=project_root,
        )

        handle_subprocess_error(
            python_encrypt_result,
            collect_server_logs,
            "Python CLI encrypt (cross-tool test)",
        )

        # Decrypt with otdfctl
        _run_otdfctl_decrypt(
            python_tdf_output,
            temp_credentials_file,
            temp_path,
            collect_server_logs,
            input_content,
        )

        print(
            "✓ Cross-tool compatibility verified: both tools can encrypt/decrypt each other's TDFs"
        )


@pytest.mark.integration
def test_different_content_types(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test encryption/decryption with different types of content."""
    test_cases = [
        ("short.txt", "x"),  # Single character
        ("multiline.txt", "Line 1\nLine 2\nLine 3\n"),  # Multi-line content
        ("unicode.txt", "Hello 世界! 🌍 Testing UTF-8 content."),  # Unicode content
        ("large.txt", "A" * 10000),  # Large content
    ]

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for filename, content in test_cases:
            print(f"\n--- Testing {filename} (content length: {len(content)}) ---")

            # Create input file
            input_file = temp_path / filename
            # Use binary mode for consistent handling of all content types
            with input_file.open("w", encoding="utf-8") as f:
                f.write(content)

            # Test with Python CLI
            python_tdf_output = temp_path / f"python_{filename}.tdf"

            python_encrypt_result = run_cli_encrypt(
                creds_file=temp_credentials_file,
                input_file=input_file,
                output_file=python_tdf_output,
                cwd=project_root,
            )

            handle_subprocess_error(
                python_encrypt_result,
                collect_server_logs,
                f"Python CLI encrypt ({filename})",
            )

            # Validate TDF structure
            validate_tdf3_file(python_tdf_output, f"Python CLI ({filename})")

            # Decrypt and validate content
            _run_otdfctl_decrypt(
                python_tdf_output,
                temp_credentials_file,
                temp_path,
                collect_server_logs,
                content,
            )

            print(f"✓ Successfully processed {filename}")

        print("✓ All content types processed successfully")


@pytest.mark.skip("Skipping test for now due to known issues with empty content")
@pytest.mark.integration
def test_different_content_types_empty(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test encryption/decryption with different types of content."""
    test_cases = [
        ("empty.txt", ""),  # Empty file
    ]

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for filename, content in test_cases:
            print(f"\n--- Testing {filename} (content length: {len(content)}) ---")

            # Create input file
            input_file = temp_path / filename
            # Use binary mode for consistent handling of all content types
            with input_file.open("w", encoding="utf-8") as f:
                f.write(content)

            # Test with Python CLI
            python_tdf_output = temp_path / f"python_{filename}.tdf"

            python_encrypt_result = run_cli_encrypt(
                creds_file=temp_credentials_file,
                input_file=input_file,
                output_file=python_tdf_output,
                cwd=project_root,
            )

            handle_subprocess_error(
                python_encrypt_result,
                collect_server_logs,
                f"Python CLI encrypt ({filename})",
            )

            # Validate TDF structure
            validate_tdf3_file(python_tdf_output, f"Python CLI ({filename})")

            # Decrypt and validate content
            _run_otdfctl_decrypt(
                python_tdf_output,
                temp_credentials_file,
                temp_path,
                collect_server_logs,
                content,
            )

            print(f"✓ Successfully processed {filename}")

        print("✓ All content types processed successfully")


if __name__ == "__main__":
    pytest.main([__file__])
