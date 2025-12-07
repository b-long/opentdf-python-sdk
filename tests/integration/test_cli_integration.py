"""Integration Test CLI functionality"""

import tempfile
from pathlib import Path

import pytest

from tests.support_cli_args import run_cli_decrypt, run_cli_encrypt
from tests.support_common import (
    compare_tdf3_file_size,
    handle_subprocess_error,
    validate_plaintext_file_created,
    validate_tdf3_file,
)
from tests.support_otdfctl_args import (
    run_otdfctl_decrypt_command,
    run_otdfctl_encrypt_command,
)


@pytest.mark.integration
def test_cli_decrypt_otdfctl_tdf(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test that the Python CLI can successfully decrypt TDF files created by otdfctl."""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = "Hello, World! This is a test for decryption."
        with input_file.open("w") as f:
            f.write(input_content)

        # Define TDF file created by otdfctl
        otdfctl_tdf_output = temp_path / "hello-world-otdfctl.txt.tdf"

        # Define decrypted output from our CLI
        cli_decrypt_output = temp_path / "decrypted-by-cli.txt"

        # Run otdfctl encrypt
        otdfctl_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_tdf_output,
            mime_type="text/plain",
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        validate_tdf3_file(otdfctl_tdf_output, "otdfctl")

        # Run our Python CLI decrypt on the otdfctl-created TDF
        cli_decrypt_result = run_cli_decrypt(
            creds_file=temp_credentials_file,
            input_file=otdfctl_tdf_output,
            output_file=cli_decrypt_output,
            cwd=project_root,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt",
        )

        validate_plaintext_file_created(
            path=cli_decrypt_output,
            scenario="Python decrypt",
            expected_content=input_content,
        )


@pytest.mark.integration
def test_otdfctl_decrypt_comparison(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test comparative decryption between otdfctl and Python CLI on the same TDF."""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = "Hello, World! This is a test for otdfctl decrypt comparison."
        with input_file.open("w") as f:
            f.write(input_content)

        # Define TDF file created by otdfctl
        otdfctl_tdf_output = temp_path / "hello-world-otdfctl.txt.tdf"

        # Define decrypted outputs from both tools
        otdfctl_decrypt_output = temp_path / "decrypted-by-otdfctl.txt"
        cli_decrypt_output = temp_path / "decrypted-by-cli.txt"

        # Run otdfctl encrypt first to create a TDF file
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_tdf_output,
            mime_type="text/plain",
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        validate_tdf3_file(otdfctl_tdf_output, "otdfctl")

        # Now run otdfctl decrypt (this is the reference implementation)
        otdfctl_decrypt_result = run_otdfctl_decrypt_command(
            temp_credentials_file,
            otdfctl_tdf_output,
            otdfctl_decrypt_output,
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl decrypt",
        )

        cli_decrypt_result = run_cli_decrypt(
            creds_file=temp_credentials_file,
            input_file=otdfctl_tdf_output,
            output_file=cli_decrypt_output,
            cwd=project_root,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt",
        )

        validate_plaintext_file_created(
            path=otdfctl_decrypt_output,
            scenario="otdfctl",
            expected_content=input_content,
        )
        validate_plaintext_file_created(
            path=cli_decrypt_output,
            scenario="Python CLI",
            expected_content=input_content,
        )


@pytest.mark.integration
def test_otdfctl_encrypt_decrypt_roundtrip(collect_server_logs, temp_credentials_file):
    """Test complete encrypt-decrypt roundtrip using otdfctl to verify functionality."""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = (
            "Hello, World! This is a test for otdfctl roundtrip encryption/decryption."
        )
        with input_file.open("w") as f:
            f.write(input_content)

        # Define TDF file and decrypted output
        otdfctl_tdf_output = temp_path / "otdfctl-roundtrip.txt.tdf"
        otdfctl_decrypt_output = temp_path / "otdfctl-roundtrip-decrypted.txt"

        # Run otdfctl encrypt
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_tdf_output,
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
        validate_tdf3_file(otdfctl_tdf_output, "otdfctl")

        # Run otdfctl decrypt
        otdfctl_decrypt_result = run_otdfctl_decrypt_command(
            temp_credentials_file,
            otdfctl_tdf_output,
            otdfctl_decrypt_output,
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl decrypt",
        )

        validate_plaintext_file_created(
            path=otdfctl_decrypt_output,
            scenario="otdfctl",
            expected_content=input_content,
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


@pytest.mark.integration
def test_cli_encrypt_integration(
    collect_server_logs, temp_credentials_file, project_root
):
    """Integration test comparing our CLI with otdfctl"""
    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = "Hello, World"
        with input_file.open("w") as f:
            f.write(input_content)

        # Define output files
        otdfctl_output = temp_path / "hello-world-otdfctl.txt.tdf"
        cli_output = temp_path / "hello-world-cli.txt.tdf"

        # Run otdfctl encrypt
        otdfctl_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_output,
            mime_type="text/plain",
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        # Run our Python CLI encrypt
        cli_result = run_cli_encrypt(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=cli_output,
            mime_type="text/plain",
            attributes=None,
            cwd=project_root,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI encrypt",
        )

        validate_tdf3_file(otdfctl_output, "otdfctl")
        validate_tdf3_file(cli_output, "Python CLI")

        compare_tdf3_file_size(otdfctl_output, cli_output)
