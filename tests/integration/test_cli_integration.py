"""
Integration Test CLI functionality
"""

import subprocess
import tempfile
from pathlib import Path

import pytest

from tests.support_cli_args import build_cli_decrypt_command, build_cli_encrypt_command
from tests.support_common import (
    get_platform_url,
    get_testing_environ,
    handle_subprocess_error,
)
from tests.support_otdfctl_args import (
    build_otdfctl_decrypt_command,
    build_otdfctl_encrypt_command,
)

platform_url = get_platform_url()


@pytest.mark.integration
def test_cli_decrypt_otdfctl_tdf(collect_server_logs, temp_credentials_file):
    """
    Test that the Python CLI can successfully decrypt TDF files created by otdfctl.
    """

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = "Hello, World! This is a test for decryption."
        with open(input_file, "w") as f:
            f.write(input_content)

        # Define TDF file created by otdfctl
        otdfctl_tdf_output = temp_path / "hello-world-otdfctl.txt.tdf"

        # Define decrypted output from our CLI
        cli_decrypt_output = temp_path / "decrypted-by-cli.txt"

        # Run otdfctl encrypt
        otdfctl_encrypt_cmd = build_otdfctl_encrypt_command(
            platform_url,
            temp_credentials_file,
            input_file,
            otdfctl_tdf_output,
            "text/plain",
        )

        otdfctl_result = subprocess.run(
            otdfctl_encrypt_cmd,
            capture_output=True,
            text=True,
            cwd=temp_path,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        # Verify the TDF file was created
        assert otdfctl_tdf_output.exists(), "otdfctl did not create TDF file"
        assert otdfctl_tdf_output.stat().st_size > 0, "otdfctl created empty TDF file"

        cli_decrypt_cmd = build_cli_decrypt_command(
            platform_url=platform_url,
            creds_file=temp_credentials_file,
            input_file=otdfctl_tdf_output,
            output_file=cli_decrypt_output,
        )

        # Run our Python CLI decrypt on the otdfctl-created TDF
        cli_decrypt_result = subprocess.run(
            cli_decrypt_cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt",
        )

        # Verify the decrypted file was created
        assert cli_decrypt_output.exists(), "Python CLI did not create decrypted file"
        assert cli_decrypt_output.stat().st_size > 0, (
            "Python CLI created empty decrypted file"
        )

        # Verify the content matches the original
        with open(cli_decrypt_output) as f:
            decrypted_content = f.read()

        assert decrypted_content == input_content, (
            f"Decrypted content does not match original. "
            f"Expected: '{input_content}', Got: '{decrypted_content}'"
        )


@pytest.mark.integration
def test_otdfctl_decrypt_comparison(collect_server_logs, temp_credentials_file):
    """
    Test comparative decryption between otdfctl and Python CLI on the same TDF.
    """

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
        otdfctl_encrypt_cmd = build_otdfctl_encrypt_command(
            platform_url,
            temp_credentials_file,
            input_file,
            otdfctl_tdf_output,
            "text/plain",
        )

        otdfctl_encrypt_result = subprocess.run(
            otdfctl_encrypt_cmd,
            capture_output=True,
            text=True,
            cwd=temp_path,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        # Verify the TDF file was created
        assert otdfctl_tdf_output.exists(), "otdfctl did not create TDF file"
        assert otdfctl_tdf_output.stat().st_size > 0, "otdfctl created empty TDF file"

        # Now run otdfctl decrypt (this is the reference implementation)
        otdfctl_decrypt_cmd = build_otdfctl_decrypt_command(
            platform_url,
            temp_credentials_file,
            otdfctl_tdf_output,
            otdfctl_decrypt_output,
        )

        otdfctl_decrypt_result = subprocess.run(
            otdfctl_decrypt_cmd,
            capture_output=True,
            text=True,
            cwd=temp_path,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl decrypt",
        )

        cli_decrypt_cmd = build_cli_decrypt_command(
            platform_url=platform_url,
            creds_file=temp_credentials_file,
            input_file=otdfctl_tdf_output,
            output_file=cli_decrypt_output,
        )

        # Run our Python CLI decrypt on the same TDF
        cli_decrypt_result = subprocess.run(
            cli_decrypt_cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt",
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
def test_otdfctl_encrypt_decrypt_roundtrip(collect_server_logs, temp_credentials_file):
    """
    Test complete encrypt-decrypt roundtrip using otdfctl to verify functionality.
    """

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
        otdfctl_encrypt_cmd = build_otdfctl_encrypt_command(
            platform_url,
            temp_credentials_file,
            input_file,
            otdfctl_tdf_output,
            "text/plain",
        )

        otdfctl_encrypt_result = subprocess.run(
            otdfctl_encrypt_cmd,
            capture_output=True,
            text=True,
            cwd=temp_path,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        # Verify the TDF file was created
        assert otdfctl_tdf_output.exists(), "otdfctl did not create TDF file"
        assert otdfctl_tdf_output.stat().st_size > 0, "otdfctl created empty TDF file"

        # Verify TDF file has correct ZIP signature
        with open(otdfctl_tdf_output, "rb") as f:
            tdf_header = f.read(4)
        assert tdf_header == b"PK\x03\x04", "otdfctl output is not a valid ZIP file"

        # Run otdfctl decrypt
        otdfctl_decrypt_cmd = build_otdfctl_decrypt_command(
            platform_url,
            temp_credentials_file,
            otdfctl_tdf_output,
            otdfctl_decrypt_output,
        )

        otdfctl_decrypt_result = subprocess.run(
            otdfctl_decrypt_cmd,
            capture_output=True,
            text=True,
            cwd=temp_path,
            env=get_testing_environ(),
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl decrypt",
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


@pytest.mark.integration
def test_cli_encrypt_integration(collect_server_logs, temp_credentials_file):
    """Integration test comparing our CLI with otdfctl"""

    # Create temporary directory for work
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "input.txt"
        input_content = "Hello, World"
        with open(input_file, "w") as f:
            f.write(input_content)

        # Define output files
        otdfctl_output = temp_path / "hello-world-otdfctl.txt.tdf"
        cli_output = temp_path / "hello-world-cli.txt.tdf"

        # Run otdfctl encrypt
        otdfctl_cmd = build_otdfctl_encrypt_command(
            platform_url,
            temp_credentials_file,
            input_file,
            otdfctl_output,
            "text/plain",
        )

        otdfctl_result = subprocess.run(
            otdfctl_cmd, capture_output=True, text=True, cwd=temp_path
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt",
        )

        cli_cmd = build_cli_encrypt_command(
            platform_url=platform_url,
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=cli_output,
            mime_type="text/plain",
            attributes=None,
        )

        # Run our Python CLI encrypt
        cli_result = subprocess.run(
            cli_cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI encrypt",
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
