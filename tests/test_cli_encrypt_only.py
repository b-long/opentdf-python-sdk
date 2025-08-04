"""
Test CLI functionality
"""

from otdf_python.tdf_reader import TDF_MANIFEST_FILE_NAME, TDF_PAYLOAD_FILE_NAME
import pytest
import subprocess
import tempfile
import json
from pathlib import Path
from tests.config_pydantic import CONFIG_TDF
import zipfile
import os

original_env = os.environ.copy()
original_env["GRPC_ENFORCE_ALPN_ENABLED"] = "false"

# Fail fast if OPENTDF_PLATFORM_URL is not set
platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
if not platform_url:
    raise Exception("OPENTDF_PLATFORM_URL must be set in config for integration tests")


def _create_test_credentials(temp_path: Path) -> Path:
    """Create a test credentials file in the given temporary directory."""
    creds_file = temp_path / "test-creds.json"
    creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
    with open(creds_file, "w") as f:
        json.dump(creds_data, f)
    return creds_file


def _create_test_input_file(temp_path: Path, content: str) -> Path:
    """Create a test input file with the given content."""
    input_file = temp_path / "input.txt"
    with open(input_file, "w") as f:
        f.write(content)
    return input_file


def _validate_tdf_file(tdf_path: Path, tool_name: str) -> None:
    """Validate that a TDF file exists, is not empty, and has correct ZIP structure."""
    assert tdf_path.exists(), f"{tool_name} did not create TDF file"
    assert tdf_path.stat().st_size > 0, f"{tool_name} created empty TDF file"
    assert zipfile.is_zipfile(tdf_path), f"{tool_name} output is not a valid ZIP file"

    # Verify TDF file has correct ZIP signature
    with open(tdf_path, "rb") as f:
        tdf_header = f.read(4)
    assert tdf_header == b"PK\x03\x04", f"{tool_name} output is not a valid ZIP file"


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
                raise AssertionError(f"Failed to decode base64 policy: {e}")

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
            raise AssertionError(f"Manifest is not valid JSON: {e}")
        except KeyError as e:
            raise AssertionError(f"Manifest missing required field: {e}")

        # Check for payload file (usually 0.payload)
        payload_files = [f for f in file_list if f.endswith(".payload")]
        assert len(payload_files) > 0, "TDF missing payload file"
        print(f"Payload files found: {payload_files}")

        print(f"✓ TDF structure validated: {len(file_list)} files, manifest valid")
        print("=" * 50)


def _handle_subprocess_error(
    result: subprocess.CompletedProcess, collect_server_logs, tool_name: str
) -> None:
    """Handle subprocess errors with proper server log collection and error reporting."""
    if result.returncode != 0:
        # Collect server logs for debugging
        logs = collect_server_logs()
        print(f"Server logs when {tool_name} failed:\n{logs}")

        assert result.returncode == 0, f"{tool_name} failed: {result.stderr}"


def _run_otdfctl_inspect(
    tdf_path: Path,
    platform_url: str,
    creds_file: Path,
    temp_path: Path,
    collect_server_logs,
) -> str:
    """Run otdfctl inspect on a TDF file and return the output."""
    otdfctl_inspect_cmd = [
        "otdfctl",
        "inspect",
        str(tdf_path),
        "--host",
        platform_url,
        "--with-client-creds-file",
        str(creds_file),
        "--tls-no-verify",
    ]

    otdfctl_inspect_result = subprocess.run(
        otdfctl_inspect_cmd,
        capture_output=True,
        text=True,
        cwd=temp_path,
        env=original_env,
    )

    _handle_subprocess_error(
        otdfctl_inspect_result, collect_server_logs, "otdfctl inspect"
    )

    # Verify inspect output contains expected information
    inspect_output = otdfctl_inspect_result.stdout
    assert "manifest" in inspect_output.lower(), (
        "Inspect output should contain manifest information"
    )

    return inspect_output


@pytest.mark.integration
def test_otdfctl_encrypt(collect_server_logs):
    """Integration test that uses otdfctl for encryption only and verifies the TDF can be inspected"""
    # Check if otdfctl is available
    try:
        subprocess.run(
            ["otdfctl", "--version"], capture_output=True, check=True, env=original_env
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception(
            "otdfctl command not found on system. Please install otdfctl to run this test."
        )

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        creds_file = _create_test_credentials(temp_path)
        input_content = "Hello, World"
        input_file = _create_test_input_file(temp_path, input_content)

        # Define TDF file created by otdfctl
        otdfctl_tdf_output = temp_path / "debug_otdfctl.txt.tdf"

        # Run otdfctl encrypt to create a TDF file
        otdfctl_encrypt_cmd = [
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
            str(otdfctl_tdf_output),
        ]

        otdfctl_encrypt_result = subprocess.run(
            otdfctl_encrypt_cmd,
            capture_output=True,
            text=True,
            cwd=temp_path,
            env=original_env,
        )

        # Handle any encryption errors
        _handle_subprocess_error(
            otdfctl_encrypt_result, collect_server_logs, "otdfctl encrypt"
        )

        # Validate the TDF file
        _validate_tdf_file(otdfctl_tdf_output, "otdfctl")
        _validate_tdf_zip_structure(otdfctl_tdf_output)

        # Test that the TDF can be inspected
        _run_otdfctl_inspect(
            otdfctl_tdf_output, platform_url, creds_file, temp_path, collect_server_logs
        )

        print("✓ otdfctl successfully encrypted and TDF can be inspected")
        print(f"TDF file size: {otdfctl_tdf_output.stat().st_size} bytes")


@pytest.mark.integration
def test_python_encrypt(collect_server_logs):
    """Integration test that uses Python CLI for encryption only and verifies the TDF can be inspected"""
    # Check if otdfctl is available for inspection
    try:
        subprocess.run(
            ["otdfctl", "--version"], capture_output=True, check=True, env=original_env
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception(
            "otdfctl command not found on system. Please install otdfctl to run this test."
        )

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        creds_file = _create_test_credentials(temp_path)
        input_content = "Hello, World"
        input_file = _create_test_input_file(temp_path, input_content)

        # Define TDF file created by Python CLI
        python_tdf_output = temp_path / "debug_python.txt.tdf"

        # Run Python CLI encrypt to create a TDF file
        python_encrypt_cmd = [
            "uv",
            "run",
            "python",
            "-m",
            "otdf_python",
            "--platform-url",
            platform_url,
            "--with-client-creds-file",
            str(creds_file),
            "--insecure",  # equivalent to --tls-no-verify
            "encrypt",
            str(input_file),
            "-o",
            str(python_tdf_output),
        ]

        python_encrypt_result = subprocess.run(
            python_encrypt_cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            env=original_env,
        )

        # Handle any encryption errors
        _handle_subprocess_error(
            python_encrypt_result, collect_server_logs, "Python CLI encrypt"
        )

        # Validate the TDF file
        _validate_tdf_file(python_tdf_output, "Python CLI")
        _validate_tdf_zip_structure(python_tdf_output)

        # Test that the TDF can be inspected
        _run_otdfctl_inspect(
            python_tdf_output, platform_url, creds_file, temp_path, collect_server_logs
        )

        print("✓ Python CLI successfully encrypted and TDF can be inspected")
        print(f"TDF file size: {python_tdf_output.stat().st_size} bytes")


if __name__ == "__main__":
    pytest.main([__file__])
