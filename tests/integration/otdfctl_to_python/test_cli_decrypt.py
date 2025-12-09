"""Tests using target mode fixtures, for CLI integration testing."""

import logging
import subprocess
import tempfile
from pathlib import Path

import pytest

from tests.support_cli_args import (
    run_cli_decrypt,
)
from tests.support_common import handle_subprocess_error

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_cli_decrypt_v4_2_2_vs_v4_3_1(
    all_target_mode_tdf_files, temp_credentials_file, collect_server_logs, project_root
):
    """Test Python CLI decrypt with various TDF versions created by otdfctl."""
    v4_2_2_files = all_target_mode_tdf_files["v4.2.2"]
    v4_3_1_files = all_target_mode_tdf_files["v4.3.1"]

    # Test decrypt on both versions of the same file type
    for file_type in ["text", "binary"]:
        v4_2_2_tdf = v4_2_2_files[file_type]
        v4_3_1_tdf = v4_3_1_files[file_type]

        # Decrypt v4.2.2 TDF
        v4_2_2_output = _run_cli_decrypt(
            v4_2_2_tdf, temp_credentials_file, project_root, collect_server_logs
        )

        # Decrypt v4.3.1 TDF
        v4_3_1_output = _run_cli_decrypt(
            v4_3_1_tdf, temp_credentials_file, project_root, collect_server_logs
        )

        # Both should succeed and produce output files
        assert v4_2_2_output is not None, f"Failed to decrypt v4.2.2 {file_type} TDF"
        assert v4_3_1_output is not None, f"Failed to decrypt v4.3.1 {file_type} TDF"

        assert v4_2_2_output.exists(), (
            f"v4.2.2 {file_type} decrypt output file not created"
        )
        assert v4_3_1_output.exists(), (
            f"v4.3.1 {file_type} decrypt output file not created"
        )

        # Both output files should have content (not empty)
        assert v4_2_2_output.stat().st_size > 0, (
            f"v4.2.2 {file_type} decrypt produced empty file"
        )
        assert v4_3_1_output.stat().st_size > 0, (
            f"v4.3.1 {file_type} decrypt produced empty file"
        )

        # Log the decryption results for comparison
        logger.info(f"\n=== {file_type.upper()} TDF Decryption Comparison ===")
        logger.info(f"v4.2.2 output size: {v4_2_2_output.stat().st_size} bytes")
        logger.info(f"v4.3.1 output size: {v4_3_1_output.stat().st_size} bytes")

        # For text files, we can compare the content directly
        if file_type == "text":
            v4_2_2_content = v4_2_2_output.read_text()
            v4_3_1_content = v4_3_1_output.read_text()

            logger.info(f"v4.2.2 content preview: {v4_2_2_content[:50]}...")
            logger.info(f"v4.3.1 content preview: {v4_3_1_content[:50]}...")

        # Clean up output files
        v4_2_2_output.unlink()
        v4_3_1_output.unlink()


@pytest.mark.integration
def test_cli_decrypt_different_file_types(
    all_target_mode_tdf_files,
    temp_credentials_file,
    collect_server_logs,
    project_root,
    known_target_modes,
):
    """Test CLI decrypt with different file types."""
    assert "v4.2.2" in all_target_mode_tdf_files
    assert "v4.3.1" in all_target_mode_tdf_files

    # Check each version has the expected file types
    for target_mode in known_target_modes:
        tdf_files = all_target_mode_tdf_files[target_mode]

        file_types_to_test = [
            "text",
            "binary",
            "with_attributes",
        ]  # TODO: Consider adding "empty" file type as well

        for file_type in file_types_to_test:
            tdf_path = tdf_files[file_type]

            # Decrypt the TDF
            output_file = _run_cli_decrypt(
                tdf_path, temp_credentials_file, project_root, collect_server_logs
            )

            assert output_file is not None, f"Failed to decrypt {file_type} TDF"
            assert output_file.exists(), (
                f"{file_type} TDF decrypt output file not created"
            )

            # Check file-type specific expectations
            if file_type == "empty":
                # Empty files should produce empty output files
                assert output_file.stat().st_size == 0, (
                    f"{file_type} TDF should produce empty output"
                )
            else:
                # Non-empty files should produce non-empty output
                assert output_file.stat().st_size > 0, (
                    f"{file_type} TDF produced empty decrypt output"
                )

            # For attributed files, just ensure they decrypt successfully
            if file_type == "with_attributes":
                logger.info(
                    f"Successfully decrypted attributed TDF, output size: {output_file.stat().st_size}"
                )

            # For text files, verify the content is readable
            if file_type == "text":
                try:
                    content = output_file.read_text()
                    assert len(content) > 0, "Text file should have readable content"
                    logger.info(f"Text content preview: {content[:100]}...")
                except UnicodeDecodeError:
                    pytest.fail(f"Decrypted {file_type} file should be valid text")

            # Clean up output file
            output_file.unlink()


def _run_cli_decrypt(
    tdf_path: Path, creds_file: Path, cwd: Path, collect_server_logs
) -> Path | None:
    """Helper function to run Python CLI decrypt command and return the output file path.

    Returns the Path to the decrypted output file if successful, None if failed.
    """
    # Create a temporary output file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".decrypted") as temp_file:
        output_path = Path(temp_file.name)

    try:
        # Build CLI command
        cli_decrypt_result = run_cli_decrypt(
            creds_file=creds_file,
            input_file=tdf_path,
            output_file=output_path,
            cwd=cwd,
        )

        # Fail fast on errors
        handle_subprocess_error(
            result=cli_decrypt_result,
            collect_server_logs=collect_server_logs,
            scenario_name="Python CLI decrypt",
        )

        return output_path

    except subprocess.CalledProcessError as e:
        logger.error(f"CLI decrypt failed for {tdf_path}: {e}")
        logger.error(f"CLI stderr: {e.stderr}")
        logger.error(f"CLI stdout: {e.stdout}")

        # Clean up the output file if it was created but command failed
        if output_path.exists():
            output_path.unlink()

        raise Exception(f"Failed to decrypt TDF {tdf_path}: {e}") from e
