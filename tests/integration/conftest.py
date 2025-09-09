"""
Shared fixtures and utilities for integration tests.
"""

import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from tests.support_cli_args import get_otdfctl_flags
from tests.support_common import get_platform_url

logger = logging.getLogger(__name__)
# from tests.config_pydantic import CONFIG_TDF

# Set up environment and configuration
original_env = os.environ.copy()
original_env["GRPC_ENFORCE_ALPN_ENABLED"] = "false"

platform_url = get_platform_url()
otdfctl_flags = get_otdfctl_flags()


def _generate_target_mode_tdf(
    input_file: Path,
    output_file: Path,
    target_mode: str,
    creds_file: Path,
    attributes: list[str] | None = None,
    mime_type: str | None = None,
) -> None:
    """
    Generate a TDF file using otdfctl with a specific target mode.

    Args:
        input_file: Path to the input file to encrypt
        output_file: Path where the TDF file should be created
        target_mode: Target TDF spec version (e.g., "v4.2.2", "v4.3.1")
        creds_file: Path to credentials file
        attributes: Optional list of attributes to apply
        mime_type: Optional MIME type for the input file
    """
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Build otdfctl command
    cmd = [
        "otdfctl",
        "encrypt",
        "--host",
        platform_url,
        "--with-client-creds-file",
        str(creds_file),
        *otdfctl_flags,
        "--tdf-type",
        "tdf3",
        "--target-mode",
        target_mode,
        "-o",
        str(output_file),
    ]

    # Add optional parameters
    if attributes:
        for attr in attributes:
            cmd.extend(["--attr", attr])

    if mime_type:
        cmd.extend(["--mime-type", mime_type])

    # Add input file
    cmd.append(str(input_file))

    # Run otdfctl command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=original_env,
    )

    if result.returncode != 0:
        logger.error(f"otdfctl command failed: {result.stderr}")
        raise Exception(
            f"Failed to generate TDF with target mode {target_mode}: "
            f"stdout={result.stdout}, stderr={result.stderr}"
        )


@pytest.fixture(scope="session")
def temp_credentials_file():
    """Create a temporary credentials file for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        creds_file = Path(temp_dir) / "creds.json"
        creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
        with open(creds_file, "w") as f:
            json.dump(creds_data, f)
        yield creds_file


@pytest.fixture(scope="session")
def test_data_dir():
    """Get the path to the test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def sample_input_files(test_data_dir):
    """Provide paths to sample input files for TDF generation."""
    return {
        "text": test_data_dir / "sample_text.txt",
        # "empty": test_data_dir / "empty_file.txt",
        "binary": test_data_dir / "sample_binary.png",
        "with_attributes": test_data_dir / "sample_with_attributes.txt",
    }


def _generate_tdf_files_for_target_mode(
    target_mode: str,
    temp_credentials_file: Path,
    test_data_dir: Path,
    sample_input_files: dict[str, Path],
) -> dict[str, Path]:
    """
    Factory function to generate TDF files for a specific target mode.

    Args:
        target_mode: Target TDF spec version (e.g., "v4.2.2", "v4.3.1")
        temp_credentials_file: Path to credentials file
        test_data_dir: Base test data directory
        sample_input_files: Dictionary of sample input files

    Returns:
        Dictionary mapping file types to their TDF file paths
    """
    output_dir = test_data_dir / target_mode
    tdf_files = {}

    # Define the file generation configurations
    file_configs = [
        {
            "key": "text",
            "input_key": "text",
            "output_name": "sample_text.txt.tdf",
            "mime_type": "text/plain",
        },
        # {
        #     "key": "empty",
        #     "input_key": "empty",
        #     "output_name": "empty_file.txt.tdf",
        #     "mime_type": "text/plain",
        # },
        {
            "key": "binary",
            "input_key": "binary",
            "output_name": "sample_binary.png.tdf",
            "mime_type": "image/png",
        },
        {
            "key": "with_attributes",
            "input_key": "with_attributes",
            "output_name": "sample_with_attributes.txt.tdf",
            "mime_type": "text/plain",
        },
    ]

    try:
        for config in file_configs:
            tdf_path = output_dir / config["output_name"]
            _generate_target_mode_tdf(
                sample_input_files[config["input_key"]],
                tdf_path,
                target_mode,
                temp_credentials_file,
                # attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1] if config["key"] == "with_attributes" else None,  # Temporarily disabled due to external KAS dependency
                mime_type=config["mime_type"],
            )
            tdf_files[config["key"]] = tdf_path

        return tdf_files

    except Exception as e:
        logger.error(f"Error generating {target_mode} TDF files: {e}")
        raise Exception(f"Failed to generate {target_mode} TDF files: {e}") from e


@pytest.fixture(scope="session")
def tdf_v4_2_2_files(temp_credentials_file, test_data_dir, sample_input_files):
    """Generate TDF files with target mode v4.2.2."""
    tdf_files = _generate_tdf_files_for_target_mode(
        "v4.2.2", temp_credentials_file, test_data_dir, sample_input_files
    )
    yield tdf_files


@pytest.fixture(scope="session")
def tdf_v4_3_1_files(temp_credentials_file, test_data_dir, sample_input_files):
    """Generate TDF files with target mode v4.3.1."""
    tdf_files = _generate_tdf_files_for_target_mode(
        "v4.3.1", temp_credentials_file, test_data_dir, sample_input_files
    )
    yield tdf_files


@pytest.fixture(scope="session")
def all_target_mode_tdf_files(tdf_v4_2_2_files, tdf_v4_3_1_files):
    """Combine all target mode TDF files into a single fixture."""
    return {
        "v4.2.2": tdf_v4_2_2_files,
        "v4.3.1": tdf_v4_3_1_files,
    }
