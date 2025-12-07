"""Integration tests for NanoTDF using otdfctl and Python CLI interoperability.

These tests verify that:
1. otdfctl can encrypt to NanoTDF and Python can decrypt
2. Python can encrypt to NanoTDF and otdfctl can decrypt
3. Both tools produce compatible NanoTDF files
"""

import logging
import tempfile
from pathlib import Path

import pytest

from tests.support_cli_args import run_cli_decrypt, run_cli_encrypt
from tests.support_common import (
    handle_subprocess_error,
    validate_plaintext_file_created,
)
from tests.support_otdfctl_args import (
    run_otdfctl_decrypt_command,
    run_otdfctl_encrypt_command,
)

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_otdfctl_encrypt_nano_python_decrypt(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test otdfctl encrypt with --tdf-type nano and Python CLI decrypt."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "nano_input.txt"
        input_content = "Hello NanoTDF! This is a test of nano format encryption."
        with input_file.open("w") as f:
            f.write(input_content)

        # Define NanoTDF file created by otdfctl
        nanotdf_output = temp_path / "test.tdf"

        # Define decrypted output from Python CLI
        python_decrypt_output = temp_path / "decrypted-by-python.txt"

        # Run otdfctl encrypt with --tdf-type nano
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=nanotdf_output,
            mime_type="text/plain",
            tdf_type="nano",
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt nano",
        )

        # Verify NanoTDF file was created
        assert nanotdf_output.exists(), "NanoTDF file should be created"
        assert nanotdf_output.stat().st_size > 0, "NanoTDF file should not be empty"

        # Log NanoTDF file info
        logger.info(f"✓ otdfctl created NanoTDF: {nanotdf_output.stat().st_size} bytes")

        # Run Python CLI decrypt on the NanoTDF
        python_decrypt_result = run_cli_decrypt(
            creds_file=temp_credentials_file,
            input_file=nanotdf_output,
            output_file=python_decrypt_output,
            cwd=project_root,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=python_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt nano",
        )

        # Validate decrypted content
        validate_plaintext_file_created(
            path=python_decrypt_output,
            scenario="Python CLI decrypt NanoTDF",
            expected_content=input_content,
        )

        logger.info(
            f"✓ Python CLI successfully decrypted NanoTDF: {python_decrypt_output.stat().st_size} bytes"
        )


@pytest.mark.integration
def test_python_encrypt_nano_otdfctl_decrypt(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test Python CLI encrypt with --container-type nano and otdfctl decrypt."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "nano_input.txt"
        input_content = "Hello from Python! Testing nano format encryption."
        with input_file.open("w") as f:
            f.write(input_content)

        # Define NanoTDF file created by Python CLI
        nanotdf_output = temp_path / "python_created.tdf"

        # Define decrypted output from otdfctl
        otdfctl_decrypt_output = temp_path / "decrypted-by-otdfctl.txt"

        # Run Python CLI encrypt with --container-type nano
        python_encrypt_result = run_cli_encrypt(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=nanotdf_output,
            mime_type="text/plain",
            container_type="nano",
            cwd=project_root,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=python_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI encrypt nano",
        )

        # Verify NanoTDF file was created
        assert nanotdf_output.exists(), "NanoTDF file should be created"
        assert nanotdf_output.stat().st_size > 0, "NanoTDF file should not be empty"

        # Log NanoTDF file info
        logger.info(
            f"✓ Python CLI created NanoTDF: {nanotdf_output.stat().st_size} bytes"
        )

        # Run otdfctl decrypt on the NanoTDF
        otdfctl_decrypt_result = run_otdfctl_decrypt_command(
            creds_file=temp_credentials_file,
            tdf_file=nanotdf_output,
            output_file=otdfctl_decrypt_output,
            cwd=temp_path,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=otdfctl_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl decrypt nano",
        )

        # Validate decrypted content
        validate_plaintext_file_created(
            path=otdfctl_decrypt_output,
            scenario="otdfctl decrypt NanoTDF",
            expected_content=input_content,
        )

        logger.info(
            f"✓ otdfctl successfully decrypted Python NanoTDF: {otdfctl_decrypt_output.stat().st_size} bytes"
        )


@pytest.mark.integration
def test_nanotdf_roundtrip_comparison(
    collect_server_logs, temp_credentials_file, project_root
):
    """Compare NanoTDF files created by otdfctl and Python CLI.

    Tests both tools' roundtrip encryption/decryption.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "roundtrip_input.txt"
        input_content = "NanoTDF roundtrip test with both tools!"
        with input_file.open("w") as f:
            f.write(input_content)

        # Define NanoTDF files from both tools
        otdfctl_nanotdf = temp_path / "otdfctl.tdf"
        python_nanotdf = temp_path / "python.tdf"

        # Define decrypted outputs
        otdfctl_encrypted_python_decrypted = temp_path / "otdfctl_enc_python_dec.txt"
        python_encrypted_otdfctl_decrypted = temp_path / "python_enc_otdfctl_dec.txt"

        # 1. Create NanoTDF with otdfctl
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=otdfctl_nanotdf,
            mime_type="text/plain",
            tdf_type="nano",
            cwd=temp_path,
        )

        handle_subprocess_error(
            result=otdfctl_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt nano (roundtrip)",
        )

        # 2. Create NanoTDF with Python CLI
        python_encrypt_result = run_cli_encrypt(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=python_nanotdf,
            mime_type="text/plain",
            container_type="nano",
            cwd=project_root,
        )

        handle_subprocess_error(
            result=python_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI encrypt nano (roundtrip)",
        )

        # Verify both NanoTDF files were created
        assert otdfctl_nanotdf.exists(), "otdfctl NanoTDF should exist"
        assert python_nanotdf.exists(), "Python NanoTDF should exist"

        otdfctl_size = otdfctl_nanotdf.stat().st_size
        python_size = python_nanotdf.stat().st_size

        logger.info("\n=== NanoTDF File Size Comparison ===")
        logger.info(f"otdfctl NanoTDF: {otdfctl_size} bytes")
        logger.info(f"Python NanoTDF:  {python_size} bytes")

        # Both should be reasonable sizes (not empty, not too large)
        assert otdfctl_size > 0, "otdfctl NanoTDF should not be empty"
        assert python_size > 0, "Python NanoTDF should not be empty"
        assert otdfctl_size < 10000, "otdfctl NanoTDF should be compact"
        assert python_size < 10000, "Python NanoTDF should be compact"

        # 3. Cross-decrypt: Python decrypts otdfctl NanoTDF
        python_decrypt_result = run_cli_decrypt(
            creds_file=temp_credentials_file,
            input_file=otdfctl_nanotdf,
            output_file=otdfctl_encrypted_python_decrypted,
            cwd=project_root,
        )

        handle_subprocess_error(
            result=python_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt otdfctl nano",
        )

        # 4. Cross-decrypt: otdfctl decrypts Python NanoTDF
        otdfctl_decrypt_result = run_otdfctl_decrypt_command(
            creds_file=temp_credentials_file,
            tdf_file=python_nanotdf,
            output_file=python_encrypted_otdfctl_decrypted,
            cwd=temp_path,
        )

        handle_subprocess_error(
            result=otdfctl_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl decrypt Python nano",
        )

        # Validate both cross-decryptions
        validate_plaintext_file_created(
            path=otdfctl_encrypted_python_decrypted,
            scenario="Python decrypt otdfctl NanoTDF",
            expected_content=input_content,
        )

        validate_plaintext_file_created(
            path=python_encrypted_otdfctl_decrypted,
            scenario="otdfctl decrypt Python NanoTDF",
            expected_content=input_content,
        )

        logger.info("\n=== Cross-Decryption Success ===")
        logger.info(
            f"✓ Python successfully decrypted otdfctl NanoTDF: {otdfctl_encrypted_python_decrypted.stat().st_size} bytes"
        )
        logger.info(
            f"✓ otdfctl successfully decrypted Python NanoTDF: {python_encrypted_otdfctl_decrypted.stat().st_size} bytes"
        )
        logger.info("✓ Both tools are interoperable for NanoTDF format!")


@pytest.mark.integration
def test_nanotdf_with_attributes(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test NanoTDF encryption/decryption with attributes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Import attribute for testing
        from tests.config_pydantic import CONFIG_TDF

        test_attribute = CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1

        # Create input file
        input_file = temp_path / "attributed_nano.txt"
        input_content = "NanoTDF with attributes test"
        with input_file.open("w") as f:
            f.write(input_content)

        # Define NanoTDF file with attributes
        nanotdf_with_attrs = temp_path / "attributed.tdf"
        decrypted_output = temp_path / "decrypted_attributed.txt"

        # Encrypt with otdfctl using attributes
        otdfctl_encrypt_result = run_otdfctl_encrypt_command(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=nanotdf_with_attrs,
            mime_type="text/plain",
            tdf_type="nano",
            attributes=[test_attribute],
            cwd=temp_path,
        )

        handle_subprocess_error(
            result=otdfctl_encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="otdfctl encrypt nano with attributes",
        )

        # Verify NanoTDF was created
        assert nanotdf_with_attrs.exists(), "Attributed NanoTDF should be created"
        logger.info(
            f"✓ Created attributed NanoTDF: {nanotdf_with_attrs.stat().st_size} bytes"
        )

        # Decrypt with Python CLI
        python_decrypt_result = run_cli_decrypt(
            creds_file=temp_credentials_file,
            input_file=nanotdf_with_attrs,
            output_file=decrypted_output,
            cwd=project_root,
        )

        handle_subprocess_error(
            result=python_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt attributed nano",
        )

        # Validate decrypted content
        validate_plaintext_file_created(
            path=decrypted_output,
            scenario="Python decrypt attributed NanoTDF",
            expected_content=input_content,
        )

        logger.info(
            f"✓ Successfully decrypted attributed NanoTDF: {decrypted_output.stat().st_size} bytes"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
