"""
This file is effectively the same test coverage as:
https://github.com/b-long/opentdf-python-sdk/blob/v0.2.17/validate_otdf_python.py

Execute using:
    uv run vop
"""

import os
import sys
import tempfile
from pathlib import Path


# Add the local otdf_python source directory to sys.path
# sys.path.insert(0, str(Path(__file__).parent / "src"))

from otdf_python.tdf import TDFConfig
from otdf_python.kas_info import KASInfo
from otdf_python.sdk_builder import SDKBuilder
from otdf_python.tdf import TDFReaderConfig
from otdf_python.config_pydantic import CONFIG_TDF


def get_kas_public_key() -> str:
    """
    Get the KAS public key from environment variables or use a fallback.

    Returns:
        str: The KAS public key
    """
    # Try to get from environment
    kas_public_key = os.environ.get("OPENTDF_KAS_PUBLIC_KEY")
    if kas_public_key:
        return kas_public_key

    # Fallback to default test key
    return """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvxW+N0O+ZdYG9JDAXhCP
0bc9OHCIa9IHrP0O6I1a1/gYnZXUVkL/5VX1HCTwg8lYYGjFpDXCYl7kzr42RW9K
nzpgmH3A7erLp0X87Jzi7CgANu38/drJ5EnjWYQ7jkGY9vF/lJFG13RlM3HjhzGV
eIocJaQM3U4r1WMzUwYUoZ9/QfGUdwxbGKxkaY/Z2KjaS6A35RCiQyy2K8unmY9T
HPQHcm0OCZZkp4mXTWF8VoGIpPACCtSBR1t6tt3nZGH+pmIYYnV+gulYbJEvcaj/
n1UDtivFEh1ZSWKdVLzvwBGS6+pVaXLQH+tPRUSQ7/oBL5GQEMxYnTsQcmGPJxrL
pQIDAQAB
-----END PUBLIC KEY-----"""


# Helper to build TDFConfig safely, using environment variables for defaults
def build_tdf_config() -> TDFConfig:
    config = {}

    # Helper to build a KASInfo from dict or env
    def build_kasinfo_from_env_or_dict(kas):
        if isinstance(kas, KASInfo):
            return kas
        if isinstance(kas, dict):
            return KASInfo(**kas)
        # Use environment variables for defaults
        return KASInfo(
            url=os.environ.get("OPENTDF_KAS_URL", "https://default.kas.example.com"),
            public_key=os.environ.get("OPENTDF_KAS_PUBLIC_KEY", None),
            kid=os.environ.get("OPENTDF_KAS_KID", None),
            default=None,
            algorithm=None,
        )

    kas_info = config.get("kas_info")
    if not kas_info:
        kas_info = build_kasinfo_from_env_or_dict(None)
    elif isinstance(kas_info, list):
        kas_info = [build_kasinfo_from_env_or_dict(k) for k in kas_info]
    else:
        kas_info = build_kasinfo_from_env_or_dict(kas_info)

    # Only pass valid fields for TDFConfig
    valid_keys = {
        "kas_info",
        "kas_private_key",
        "policy_object",
        "attributes",
        "segment_size",
    }
    filtered = {k: v for k, v in config.items() if k in valid_keys}
    filtered["kas_info"] = kas_info

    # Optionally, set kas_private_key from env if not provided
    if "kas_private_key" not in filtered or not filtered["kas_private_key"]:
        filtered["kas_private_key"] = os.environ.get("OPENTDF_KAS_PRIVATE_KEY", None)

    # Use the new builder pattern if available
    from otdf_python.sdk_builder import SDKBuilder

    sdk = (
        SDKBuilder()
        .set_platform_endpoint(
            os.environ.get("OPENTDF_KAS_URL", "https://default.kas.example.com")
        )
        .use_insecure_plaintext_connection(True)
        .build()
    )
    return sdk.new_tdf_config(**filtered)


def encrypt_file(input_path: Path, sdk=None) -> Path:
    """Encrypt a file and return the path to the encrypted file."""
    if sdk is None:
        from otdf_python.kas_info import KASInfo

        kas_url = os.environ.get("OPENTDF_KAS_URL", "https://default.kas.example.com")

        # Build the SDK
        sdk = (
            SDKBuilder()
            .set_platform_endpoint(kas_url)
            .use_insecure_plaintext_connection(True)
            .build()
        )

        # Get or generate a public key
        kas_public_key = get_kas_public_key()

        # Create KASInfo with public key
        kas_info = KASInfo(url=kas_url, public_key=kas_public_key)

        # Create config with the KASInfo
        config = sdk.new_tdf_config(
            attributes=["attr1", "attr2"], kas_info_list=[kas_info]
        )
    else:
        # If SDK is provided, we need to create a config with attributes and KASInfo
        # Get the platform URL from the SDK
        kas_url = sdk.get_platform_url() or "https://default.kas.example.com"

        # Get or generate a public key
        kas_public_key = get_kas_public_key()

        # Create KASInfo
        from otdf_python.kas_info import KASInfo

        kas_info = KASInfo(url=kas_url, public_key=kas_public_key)

        # Create config with attributes and KASInfo
        config = sdk.new_tdf_config(
            attributes=["attr1", "attr2"], kas_info_list=[kas_info]
        )

    output_path = input_path.with_suffix(input_path.suffix + ".tdf")
    with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
        sdk.create_tdf(infile.read(), config, output_stream=outfile)
    return output_path


def decrypt_file(encrypted_path: Path, sdk=None) -> Path:
    """Decrypt a file and return the path to the decrypted file."""
    if sdk is None:
        sdk = (
            SDKBuilder()
            .set_platform_endpoint(
                os.environ.get("OPENTDF_HOSTNAME", "https://your.cluster/")
            )
            .use_insecure_plaintext_connection(True)
            .build()
        )

    output_path = encrypted_path.with_suffix(".decrypted")
    with open(encrypted_path, "rb") as infile, open(output_path, "wb") as outfile:
        # Include attributes for policy enforcement
        reader_config = TDFReaderConfig(
            attributes=["attr1", "attr2"]  # Same attributes used in encrypt_file
        )

        # For testing or local development, you can still use kas_private_key from env if available
        kas_private_key = os.environ.get("OPENTDF_KAS_PRIVATE_KEY")
        if kas_private_key:
            reader_config.kas_private_key = kas_private_key
        reader = sdk.load_tdf(infile.read(), reader_config)
        # If TDFReader has a read_payload method, use it; else, write reader.payload
        if hasattr(reader, "read_payload"):
            reader.read_payload(outfile)
        else:
            outfile.write(reader.payload)
    return output_path


def verify_encrypt_str() -> None:
    print("Validating string encryption (local TDF)")
    try:
        # Get KAS URL from environment or use default
        kas_url = os.environ.get("OPENTDF_KAS_URL", "https://default.kas.example.com")
        platform_endpoint = CONFIG_TDF.OPENTDF_PLATFORM_URL
        sdk = (
            SDKBuilder()
            .set_platform_endpoint(platform_endpoint)
            .use_insecure_plaintext_connection(True)
            .build()
        )

        # Get KAS public key
        kas_public_key = get_kas_public_key()

        # Create a KASInfo with the public key
        from otdf_python.kas_info import KASInfo

        kas_info = KASInfo(url=kas_url, public_key=kas_public_key)

        payload = b"Hello from Python"
        config = sdk.new_tdf_config(
            attributes=["attr1", "attr2"], kas_info_list=[kas_info]
        )
        # Use BytesIO to mimic file-like API
        from io import BytesIO

        output = BytesIO()
        sdk.create_tdf(payload, config, output_stream=output)
        manifest_bytes = output.getvalue()
        print(f"Manifest returned: {manifest_bytes[:60]}... (truncated)")
        assert manifest_bytes and len(manifest_bytes) > 0
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise RuntimeError(
            f"An unexpected error occurred testing otdf_python string encryption: {e}"
        ) from e


def verify_encrypt_file() -> None:
    print("Validating file encryption (local TDF)")
    try:
        with tempfile.TemporaryDirectory() as tmpDir:
            print("Created temporary directory", tmpDir)
            some_plaintext_file = Path(tmpDir) / "new-file.txt"
            some_plaintext_file.write_text("Hello world")
            encrypted_path = encrypt_file(some_plaintext_file)
            print(f"Encrypted file at: {encrypted_path}")
            # Optionally, check the file exists and is not empty
            assert encrypted_path.exists() and encrypted_path.stat().st_size > 0
    except Exception as e:
        raise RuntimeError(
            "An unexpected error occurred testing otdf_python file encryption"
        ) from e


def verify_encrypt_decrypt_file() -> None:
    print("Validating encrypt/decrypt roundtrip (local TDF)")
    try:
        with tempfile.TemporaryDirectory() as tmpDir:
            tmpDir = Path(tmpDir)
            input_file = tmpDir / "plain.txt"
            input_file.write_text("Secret message")

            # Build the SDK
            kas_url = os.environ.get("OPENTDF_HOSTNAME", "https://your.cluster/")
            sdk = (
                SDKBuilder()
                .set_platform_endpoint(kas_url)
                .use_insecure_plaintext_connection(True)
                .build()
            )

            # Get public key from KAS
            try:
                # Use the encrypt_file function which now gets the public key from KAS
                encrypted_path = encrypt_file(input_file, sdk)
                print(f"Encrypted file at: {encrypted_path}")

                # Decrypt the file using the same SDK
                decrypted_path = decrypt_file(encrypted_path, sdk)
                print(f"Decrypted file at: {decrypted_path}")

                # Verify the result
                assert decrypted_path.exists()

                # Validate content
                with open(input_file, "rb") as f:
                    original = f.read()
                with open(decrypted_path, "rb") as f:
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
