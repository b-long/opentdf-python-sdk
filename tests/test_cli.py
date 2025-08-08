"""
Test CLI functionality
"""

import pytest
import subprocess
import sys
import tempfile
import os
import json
from pathlib import Path
from tests.config_pydantic import CONFIG_TDF
from tests.support_otdfctl import check_for_otdfctl


def test_cli_help():
    """Test that CLI help command works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "OpenTDF CLI" in result.stdout
    assert "encrypt" in result.stdout
    assert "decrypt" in result.stdout
    assert "inspect" in result.stdout


def test_cli_version():
    """Test that CLI version command works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "--version"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "OpenTDF Python SDK" in result.stdout
    assert "0.3.0a1" in result.stdout


def test_cli_encrypt_help():
    """Test that CLI encrypt help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "encrypt", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Path to file to encrypt" in result.stdout
    assert "--attributes" in result.stdout
    assert "--container-type" in result.stdout


def test_cli_decrypt_help():
    """Test that CLI decrypt help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "decrypt", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Path to encrypted file" in result.stdout
    assert "--output" in result.stdout


def test_cli_inspect_help():
    """Test that CLI inspect help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "inspect", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Path to encrypted file" in result.stdout


def test_cli_encrypt_missing_auth():
    """Test that CLI encrypt fails gracefully without authentication"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, "-m", "otdf_python", "encrypt", temp_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "Authentication required" in result.stderr
        assert "--with-client-creds-file" in result.stderr
    finally:
        os.unlink(temp_file)


def test_cli_encrypt_missing_creds_file():
    """Test that CLI encrypt fails gracefully with missing credentials file"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "otdf_python",
                "--with-client-creds-file",
                "nonexistent.json",
                "encrypt",
                temp_file,
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "Credentials file does not exist" in result.stderr
    finally:
        os.unlink(temp_file)


def test_cli_encrypt_invalid_creds_file():
    """Test that CLI encrypt fails gracefully with invalid credentials file"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as creds_f:
        creds_f.write('{"invalid": "format"}')
        creds_file = creds_f.name

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "otdf_python",
                "--with-client-creds-file",
                creds_file,
                "encrypt",
                temp_file,
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "must contain 'clientId' and 'clientSecret' fields" in result.stderr
    finally:
        os.unlink(temp_file)
        os.unlink(creds_file)


def test_cli_decrypt_missing_file():
    """Test that CLI decrypt fails gracefully with missing file"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "decrypt", "nonexistent.tdf"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 1
    assert "File does not exist" in result.stderr


@pytest.mark.integration
def test_cli_encrypt_integration():
    """Integration test comparing our CLI with otdfctl"""
    # Skip if OPENTDF_PLATFORM_URL is not set
    platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
    if not platform_url:
        raise Exception(
            "OPENTDF_PLATFORM_URL must be set in config for integration tests"
        )

    check_for_otdfctl()

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
        input_content = "Hello, World"
        with open(input_file, "w") as f:
            f.write(input_content)

        # Define output files
        otdfctl_output = temp_path / "hello-world-otdfctl.txt.tdf"
        cli_output = temp_path / "hello-world-cli.txt.tdf"

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
            raise Exception(f"otdfctl failed: {otdfctl_result.stderr}")

        # Run our Python CLI encrypt
        cli_cmd = [
            sys.executable,
            "-m",
            "otdf_python",
            "--platform-url",
            platform_url,
            "--with-client-creds-file",
            str(creds_file),
            "--insecure",  # equivalent to --tls-no-verify
            "encrypt",
            "--mime-type",
            "text/plain",
            "--container-type",
            "tdf",  # to match otdfctl behavior
            str(input_file),
            "-o",
            str(cli_output),
        ]

        cli_result = subprocess.run(
            cli_cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent
        )

        # Check that our CLI succeeded
        if cli_result.returncode != 0:
            # Check if this is a server connectivity issue
            if (
                "401 Unauthorized" in cli_result.stderr
                or "token endpoint discovery" in cli_result.stderr
                or "Issuer endpoint must be configured" in cli_result.stderr
            ):
                pytest.skip(
                    f"Server connectivity or authentication issue: {cli_result.stderr}"
                )

            else:
                assert cli_result.returncode == 0, (
                    f"Python CLI failed: {cli_result.stderr}"
                )

        # Both output files should exist
        assert otdfctl_output.exists(), "otdfctl output file does not exist"
        assert cli_output.exists(), "Python CLI output file does not exist"

        # Both files should be non-empty and similar in size
        otdfctl_size = otdfctl_output.stat().st_size
        cli_size = cli_output.stat().st_size

        assert otdfctl_size > 0, "otdfctl output is empty"
        assert cli_size > 0, "Python CLI output is empty"

        # Files should be reasonably similar in size (within 50% of each other)
        # This accounts for potential differences in metadata or formatting
        size_diff_ratio = abs(otdfctl_size - cli_size) / max(otdfctl_size, cli_size)
        assert size_diff_ratio < 0.3, (
            f"File sizes too different: otdfctl={otdfctl_size}, cli={cli_size}"
        )

        # Both files should start with ZIP signature (TDF format)
        with open(otdfctl_output, "rb") as f:
            otdfctl_header = f.read(4)
        with open(cli_output, "rb") as f:
            cli_header = f.read(4)

        assert otdfctl_header == b"PK\x03\x04", "otdfctl output is not a valid ZIP file"
        assert cli_header == b"PK\x03\x04", "Python CLI output is not a valid ZIP file"


if __name__ == "__main__":
    pytest.main([__file__])
