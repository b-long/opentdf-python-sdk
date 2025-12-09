"""Validation tests for OpenTDF Python SDK.

This module provides the same test coverage as:
https://github.com/b-long/opentdf-python-sdk/blob/v0.2.17/validate_otdf_python.py

Execute using:
    uv run pytest tests/test_validate_otdf_python.py
"""

import logging
import sys
import tempfile
from pathlib import Path

import pytest

from tests.integration.support_sdk import get_sdk

# Set up detailed logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

_test_attributes = []


def _get_sdk_and_tdf_config() -> tuple:
    sdk = get_sdk()

    # Let the SDK create the default KAS info from the platform URL
    # This will automatically append /kas to the platform URL
    tdf_config = sdk.new_tdf_config(
        attributes=_test_attributes,
        # Don't override kas_info_list - let SDK use platform_url + /kas
    )
    return sdk, tdf_config


def encrypt_file(input_path: Path) -> Path:
    """Encrypt a file and return the path to the encrypted file."""
    # Build the SDK
    sdk, tdf_config = _get_sdk_and_tdf_config()

    output_path = input_path.with_suffix(input_path.suffix + ".tdf")
    with input_path.open("rb") as infile, output_path.open("wb") as outfile:
        sdk.create_tdf(infile.read(), tdf_config, output_stream=outfile)
    return output_path


def decrypt_file(encrypted_path: Path) -> Path:
    """Decrypt a file and return the path to the decrypted file."""
    sdk = get_sdk()

    output_path = encrypted_path.with_suffix(".decrypted")
    with encrypted_path.open("rb") as infile, output_path.open("wb") as outfile:
        # Use KAS client for key unwrapping
        reader = sdk.load_tdf(infile.read())
        # TDFReader is a dataclass with payload attribute
        outfile.write(reader.payload)
    return output_path


def verify_encrypt_str() -> None:
    """Verify string encryption functionality."""
    print("Validating string encryption (local TDF)")
    try:
        sdk = get_sdk()

        payload = b"Hello from Python"

        # Let the SDK create the default KAS info from the platform URL
        # This will automatically append /kas to the platform URL
        tdf_config = sdk.new_tdf_config(
            attributes=_test_attributes,
            # Don't override kas_info_list - let SDK use platform_url + /kas
        )

        # Use BytesIO to mimic file-like API
        from io import BytesIO

        output = BytesIO()
        sdk.create_tdf(payload, tdf_config, output_stream=output)
        manifest_bytes = output.getvalue()
        print(f"Manifest returned: {manifest_bytes[:60]}... (truncated)")
        assert manifest_bytes
        assert len(manifest_bytes) > 0
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise RuntimeError(
            f"An unexpected error occurred testing otdf_python string encryption: {e}"
        ) from e


@pytest.mark.integration
def test_verify_encrypt_str():
    """Run the string encryption verification test."""
    verify_encrypt_str()


def verify_encrypt_file() -> None:
    """Verify file encryption functionality."""
    print("Validating file encryption (local TDF)")
    try:
        with tempfile.TemporaryDirectory() as tmpDir:
            print("Created temporary directory", tmpDir)
            some_plaintext_file = Path(tmpDir) / "new-file.txt"
            some_plaintext_file.write_text("Hello world")
            encrypted_path = encrypt_file(some_plaintext_file)
            print(f"Encrypted file at: {encrypted_path}")
            # Optionally, check the file exists and is not empty
            assert encrypted_path.exists()
            assert encrypted_path.stat().st_size > 0
    except Exception as e:
        raise RuntimeError(
            "An unexpected error occurred testing otdf_python file encryption"
        ) from e


@pytest.mark.integration
def test_verify_encrypt_file():
    """Run the file encryption verification test."""
    verify_encrypt_file()


def verify_encrypt_decrypt_file() -> None:
    """Verify encrypt/decrypt roundtrip functionality."""
    print("Validating encrypt/decrypt roundtrip (local TDF)")
    try:
        with tempfile.TemporaryDirectory() as tmpDir:
            tmpDir = Path(tmpDir)
            input_file = tmpDir / "plain.txt"
            input_file.write_text("Secret message")

            try:
                encrypted_path = encrypt_file(input_file)
                print(f"Encrypted file at: {encrypted_path}")

                # Decrypt the file using the same SDK
                decrypted_path = decrypt_file(encrypted_path)
                print(f"Decrypted file at: {decrypted_path}")

                # Verify the result
                assert decrypted_path.exists()

                # Validate content
                with input_file.open("rb") as f:
                    original = f.read()
                with decrypted_path.open("rb") as f:
                    decrypted = f.read()
                assert original == decrypted, "Decrypted content doesn't match original"

            except Exception as e:
                import traceback

                traceback.print_exc()
                print(f"Error during encryption/decryption test: {e}")
                raise
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred testing otdf_python encrypt/decrypt: {e}"
        ) from e


@pytest.mark.integration
def test_verify_encrypt_decrypt_file():
    """Run the encrypt/decrypt verification test."""
    verify_encrypt_decrypt_file()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        tdf_file = Path(sys.argv[1])
        print(f"Decrypting provided TDF file: {tdf_file}")
        output = decrypt_file(tdf_file)
        print(f"Decrypted file written to: {output}")
    else:
        print("Attempting string encryption")
        verify_encrypt_str()

        print("Attempting file encryption")
        verify_encrypt_file()

        print("Attempting encrypt/decrypt roundtrip")
        verify_encrypt_decrypt_file()

        print("All tests have passed 👍")
