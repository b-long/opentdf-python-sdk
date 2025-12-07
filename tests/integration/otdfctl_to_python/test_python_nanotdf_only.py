"""Simple NanoTDF integration test focusing on Python CLI only.

This tests the Python implementation without otdfctl dependency.
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

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_python_nanotdf_roundtrip(
    collect_server_logs, temp_credentials_file, project_root
):
    """Test Python CLI NanoTDF encryption and decryption roundtrip."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input file
        input_file = temp_path / "test.txt"
        input_content = "Hello NanoTDF from Python!"
        with input_file.open("w") as f:
            f.write(input_content)

        # Define NanoTDF and output files
        nanotdf_file = temp_path / "test.ntdf"
        decrypted_file = temp_path / "decrypted.txt"

        # Step 1: Encrypt with Python CLI using --container-type nano
        logger.info(f"\n=== Encrypting {input_file} to {nanotdf_file} ===")
        encrypt_result = run_cli_encrypt(
            creds_file=temp_credentials_file,
            input_file=input_file,
            output_file=nanotdf_file,
            mime_type="text/plain",
            container_type="nano",
            cwd=project_root,
        )

        # Log results for debugging
        logger.info(f"Encrypt returncode: {encrypt_result.returncode}")
        logger.info(f"Encrypt stdout: {encrypt_result.stdout}")
        logger.info(f"Encrypt stderr: {encrypt_result.stderr}")

        # Check for errors
        handle_subprocess_error(
            result=encrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI encrypt nano",
        )

        # Verify NanoTDF was created
        assert nanotdf_file.exists(), f"NanoTDF file should exist at {nanotdf_file}"
        nanotdf_size = nanotdf_file.stat().st_size
        assert nanotdf_size > 0, "NanoTDF file should not be empty"
        logger.info(f"✓ Created NanoTDF: {nanotdf_size} bytes")

        # Step 2: Decrypt with Python CLI
        logger.info(f"\n=== Decrypting {nanotdf_file} to {decrypted_file} ===")
        decrypt_result = run_cli_decrypt(
            creds_file=temp_credentials_file,
            input_file=nanotdf_file,
            output_file=decrypted_file,
            cwd=project_root,
        )

        # Log results
        logger.info(f"Decrypt returncode: {decrypt_result.returncode}")
        logger.info(f"Decrypt stdout: {decrypt_result.stdout}")
        logger.info(f"Decrypt stderr: {decrypt_result.stderr}")

        # Check for errors
        handle_subprocess_error(
            result=decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt nano",
        )

        # Validate content
        validate_plaintext_file_created(
            path=decrypted_file,
            scenario="Python CLI NanoTDF roundtrip",
            expected_content=input_content,
        )

        logger.info("✓ Successfully decrypted NanoTDF roundtrip!")
        logger.info(f"  Input: {input_file.stat().st_size} bytes")
        logger.info(f"  NanoTDF: {nanotdf_size} bytes")
        logger.info(f"  Decrypted: {decrypted_file.stat().st_size} bytes")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
