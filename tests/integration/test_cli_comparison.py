"""
Test CLI functionality
"""

import subprocess
import tempfile
from pathlib import Path

import pytest

from tests.support_otdfctl_args import get_platform_url

platform_url = get_platform_url()


@pytest.mark.integration
def test_otdfctl_encrypt_python_decrypt(collect_server_logs, temp_credentials_file):
    """Integration test that uses otdfctl for encryption and the Python CLI for decryption"""

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = "Hello, World! This is a test for otdfctl decrypt comparison."
        with open(input_file, "w") as f:
            f.write(input_content)

        # Define TDF file created by otdfctl
        otdfctl_tdf_output = temp_path / "hello-world-otdfctl.txt.tdf"

        # Define decrypted outputs from both tools
        otdfctl_decrypt_output = temp_path / "decrypted-by-otdfctl.txt"
        cli_decrypt_output = temp_path / "decrypted-by-cli.txt"

        # Run otdfctl encrypt first to create a TDF file
        otdfctl_encrypt_cmd = [
            "otdfctl",
            "encrypt",
            "--host",
            platform_url,
            "--with-client-creds-file",
            str(temp_credentials_file),
            "--tls-no-verify",
            "--mime-type",
            "text/plain",
            str(input_file),
            "-o",
            str(otdfctl_tdf_output),
        ]

        otdfctl_encrypt_result = subprocess.run(
            otdfctl_encrypt_cmd, capture_output=True, text=True, cwd=temp_path
        )

        # If otdfctl encrypt fails, skip the test (might be server issues)
        if otdfctl_encrypt_result.returncode != 0:
            raise Exception(f"otdfctl encrypt failed: {otdfctl_encrypt_result.stderr}")

        # Verify the TDF file was created
        assert otdfctl_tdf_output.exists(), "otdfctl did not create TDF file"
        assert otdfctl_tdf_output.stat().st_size > 0, "otdfctl created empty TDF file"

        # Now run otdfctl decrypt (this is the reference implementation)
        otdfctl_decrypt_cmd = [
            "otdfctl",
            "decrypt",
            "--host",
            platform_url,
            "--with-client-creds-file",
            str(temp_credentials_file),
            "--tls-no-verify",
            str(otdfctl_tdf_output),
            "-o",
            str(otdfctl_decrypt_output),
        ]

        otdfctl_decrypt_result = subprocess.run(
            otdfctl_decrypt_cmd, capture_output=True, text=True, cwd=temp_path
        )

        # Check that otdfctl decrypt succeeded
        if otdfctl_decrypt_result.returncode != 0:
            # Collect server logs for debugging
            logs = collect_server_logs()
            print(f"Server logs when otdfctl decrypt failed:\n{logs}")

            # Check if this is a server connectivity issue
            if (
                "401 Unauthorized" in otdfctl_decrypt_result.stderr
                or "token endpoint discovery" in otdfctl_decrypt_result.stderr
                or "Issuer endpoint must be configured" in otdfctl_decrypt_result.stderr
            ):
                pytest.skip(
                    f"Server connectivity or authentication issue: {otdfctl_decrypt_result.stderr}"
                )
            else:
                assert otdfctl_decrypt_result.returncode == 0, (
                    f"otdfctl decrypt failed: {otdfctl_decrypt_result.stderr}"
                )

        # Run our Python CLI decrypt on the same TDF
        cli_decrypt_cmd = [
            "uv",
            "run",
            "python",
            "-m",
            "otdf_python",
            "--platform-url",
            platform_url,
            "--with-client-creds-file",
            str(temp_credentials_file),
            "--insecure",  # equivalent to --tls-no-verify
            "decrypt",
            str(otdfctl_tdf_output),
            "-o",
            str(cli_decrypt_output),
        ]

        cli_decrypt_result = subprocess.run(
            cli_decrypt_cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Check that our CLI succeeded
        if cli_decrypt_result.returncode != 0:
            # Collect server logs for debugging
            logs = collect_server_logs()
            print(f"Server logs when Python CLI decrypt failed:\n{logs}")

            # Check if this is a server connectivity issue
            if (
                "401 Unauthorized" in cli_decrypt_result.stderr
                or "token endpoint discovery" in cli_decrypt_result.stderr
                or "Issuer endpoint must be configured" in cli_decrypt_result.stderr
            ):
                pytest.skip(
                    f"Server connectivity or authentication issue: {cli_decrypt_result.stderr}"
                )
            else:
                assert cli_decrypt_result.returncode == 0, (
                    f"Python CLI decrypt failed: {cli_decrypt_result.stderr}"
                )

        # Verify both decrypted files were created
        assert otdfctl_decrypt_output.exists(), "otdfctl did not create decrypted file"
        assert otdfctl_decrypt_output.stat().st_size > 0, (
            "otdfctl created empty decrypted file"
        )
        assert cli_decrypt_output.exists(), "Python CLI did not create decrypted file"
        assert cli_decrypt_output.stat().st_size > 0, (
            "Python CLI created empty decrypted file"
        )

        # Verify both tools produce the same decrypted content
        with open(otdfctl_decrypt_output) as f:
            otdfctl_decrypted_content = f.read()
        with open(cli_decrypt_output) as f:
            cli_decrypted_content = f.read()

        # Both should match the original content
        assert otdfctl_decrypted_content == input_content, (
            f"otdfctl decrypted content does not match original. "
            f"Expected: '{input_content}', Got: '{otdfctl_decrypted_content}'"
        )
        assert cli_decrypted_content == input_content, (
            f"Python CLI decrypted content does not match original. "
            f"Expected: '{input_content}', Got: '{cli_decrypted_content}'"
        )

        # Both tools should produce identical results
        assert otdfctl_decrypted_content == cli_decrypted_content, (
            f"Decrypted content differs between tools. "
            f"otdfctl: '{otdfctl_decrypted_content}', Python CLI: '{cli_decrypted_content}'"
        )

        print(
            "✓ Both otdfctl and Python CLI successfully decrypted the TDF with identical results"
        )


@pytest.mark.integration
def test_otdfctl_encrypt_otdfctl_decrypt(collect_server_logs, temp_credentials_file):
    """Integration test that uses otdfctl for both encryption and decryption to verify roundtrip functionality"""

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = (
            "Hello, World! This is a test for otdfctl roundtrip encryption/decryption."
        )
        with open(input_file, "w") as f:
            f.write(input_content)

        # Define TDF file and decrypted output
        otdfctl_tdf_output = temp_path / "otdfctl-roundtrip.txt.tdf"
        otdfctl_decrypt_output = temp_path / "otdfctl-roundtrip-decrypted.txt"

        # Run otdfctl encrypt
        otdfctl_encrypt_cmd = [
            "otdfctl",
            "encrypt",
            "--host",
            platform_url,
            "--with-client-creds-file",
            str(temp_credentials_file),
            "--tls-no-verify",
            "--mime-type",
            "text/plain",
            str(input_file),
            "-o",
            str(otdfctl_tdf_output),
        ]

        otdfctl_encrypt_result = subprocess.run(
            otdfctl_encrypt_cmd, capture_output=True, text=True, cwd=temp_path
        )

        # If otdfctl encrypt fails, skip the test (might be server issues)
        if otdfctl_encrypt_result.returncode != 0:
            # Collect server logs for debugging
            logs = collect_server_logs()
            print(f"Server logs when otdfctl encrypt failed:\n{logs}")

            # Check if this is a server connectivity issue
            if (
                "401 Unauthorized" in otdfctl_encrypt_result.stderr
                or "token endpoint discovery" in otdfctl_encrypt_result.stderr
                or "Issuer endpoint must be configured" in otdfctl_encrypt_result.stderr
            ):
                pytest.skip(
                    f"Server connectivity or authentication issue: {otdfctl_encrypt_result.stderr}"
                )
            else:
                assert otdfctl_encrypt_result.returncode == 0, (
                    f"otdfctl encrypt failed: {otdfctl_encrypt_result.stderr}"
                )

        # Verify the TDF file was created
        assert otdfctl_tdf_output.exists(), "otdfctl did not create TDF file"
        assert otdfctl_tdf_output.stat().st_size > 0, "otdfctl created empty TDF file"

        # Verify TDF file has correct ZIP signature
        with open(otdfctl_tdf_output, "rb") as f:
            tdf_header = f.read(4)
        assert tdf_header == b"PK\x03\x04", "otdfctl output is not a valid ZIP file"

        # Run otdfctl decrypt
        otdfctl_decrypt_cmd = [
            "otdfctl",
            "decrypt",
            "--host",
            platform_url,
            "--with-client-creds-file",
            str(temp_credentials_file),
            "--tls-no-verify",
            str(otdfctl_tdf_output),
            "-o",
            str(otdfctl_decrypt_output),
        ]

        otdfctl_decrypt_result = subprocess.run(
            otdfctl_decrypt_cmd, capture_output=True, text=True, cwd=temp_path
        )

        # Check that otdfctl decrypt succeeded
        if otdfctl_decrypt_result.returncode != 0:
            # Collect server logs for debugging
            logs = collect_server_logs()
            print(f"Server logs when otdfctl decrypt failed:\n{logs}")

            # Check if this is a server connectivity issue
            if (
                "401 Unauthorized" in otdfctl_decrypt_result.stderr
                or "token endpoint discovery" in otdfctl_decrypt_result.stderr
                or "Issuer endpoint must be configured" in otdfctl_decrypt_result.stderr
            ):
                pytest.skip(
                    f"Server connectivity or authentication issue: {otdfctl_decrypt_result.stderr}"
                )
            else:
                assert otdfctl_decrypt_result.returncode == 0, (
                    f"otdfctl decrypt failed: {otdfctl_decrypt_result.stderr}"
                )

        # Verify the decrypted file was created
        assert otdfctl_decrypt_output.exists(), "otdfctl did not create decrypted file"
        assert otdfctl_decrypt_output.stat().st_size > 0, (
            "otdfctl created empty decrypted file"
        )

        # Verify the decrypted content matches the original
        with open(otdfctl_decrypt_output) as f:
            decrypted_content = f.read()

        assert decrypted_content == input_content, (
            f"otdfctl roundtrip failed - decrypted content does not match original. "
            f"Expected: '{input_content}', Got: '{decrypted_content}'"
        )

        # Verify file sizes are reasonable
        original_size = input_file.stat().st_size
        tdf_size = otdfctl_tdf_output.stat().st_size
        decrypted_size = otdfctl_decrypt_output.stat().st_size

        assert tdf_size > original_size, "TDF file should be larger than original"
        assert decrypted_size == original_size, (
            "Decrypted file should match original size"
        )

        print(
            f"✓ otdfctl roundtrip successful: {original_size} bytes -> {tdf_size} bytes -> {decrypted_size} bytes"
        )


if __name__ == "__main__":
    pytest.main([__file__])
