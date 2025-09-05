"""
Shared fixtures and utilities for integration tests.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from tests.config_pydantic import CONFIG_TDF
from tests.support_cli_args import get_otdfctl_flags, get_platform_url

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
        "empty": test_data_dir / "empty_file.txt",
        "binary": test_data_dir / "sample_binary.png",
        "with_attributes": test_data_dir / "sample_with_attributes.txt",
    }


@pytest.fixture(scope="session")
def tdf_v4_2_2_files(temp_credentials_file, test_data_dir, sample_input_files):
    """Generate TDF files with target mode v4.2.2."""

    output_dir = test_data_dir / "v4.2.2"
    tdf_files = {}

    try:
        # Generate text TDF
        text_tdf = output_dir / "sample_text.txt.tdf"
        _generate_target_mode_tdf(
            sample_input_files["text"],
            text_tdf,
            "v4.2.2",
            temp_credentials_file,
            mime_type="text/plain",
        )
        tdf_files["text"] = text_tdf

        # Generate empty file TDF
        # empty_tdf = output_dir / "empty_file.txt.tdf"
        # _generate_target_mode_tdf(
        #     sample_input_files["empty"],
        #     empty_tdf,
        #     "v4.2.2",
        #     temp_credentials_file,
        #     mime_type="text/plain",
        # )
        # tdf_files["empty"] = empty_tdf

        # Generate binary TDF
        binary_tdf = output_dir / "sample_binary.png.tdf"
        _generate_target_mode_tdf(
            sample_input_files["binary"],
            binary_tdf,
            "v4.2.2",
            temp_credentials_file,
            mime_type="image/png",
        )
        tdf_files["binary"] = binary_tdf

        # Generate TDF with attributes
        attr_tdf = output_dir / "sample_with_attributes.txt.tdf"
        _generate_target_mode_tdf(
            sample_input_files["with_attributes"],
            attr_tdf,
            "v4.2.2",
            temp_credentials_file,
            attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1],
            mime_type="text/plain",
        )
        tdf_files["with_attributes"] = attr_tdf

        yield tdf_files

    except Exception as e:
        raise Exception(f"Failed to generate v4.2.2 TDF files: {e}") from e


@pytest.fixture(scope="session")
def tdf_v4_3_1_files(temp_credentials_file, test_data_dir, sample_input_files):
    """Generate TDF files with target mode v4.3.1."""

    output_dir = test_data_dir / "v4.3.1"
    tdf_files = {}

    try:
        # Generate text TDF
        text_tdf = output_dir / "sample_text.txt.tdf"
        _generate_target_mode_tdf(
            sample_input_files["text"],
            text_tdf,
            "v4.3.1",
            temp_credentials_file,
            mime_type="text/plain",
        )
        tdf_files["text"] = text_tdf

        # Generate empty file TDF
        # empty_tdf = output_dir / "empty_file.txt.tdf"
        # _generate_target_mode_tdf(
        #     sample_input_files["empty"],
        #     empty_tdf,
        #     "v4.3.1",
        #     temp_credentials_file,
        #     mime_type="text/plain",
        # )
        # tdf_files["empty"] = empty_tdf

        # Generate binary TDF
        binary_tdf = output_dir / "sample_binary.png.tdf"
        _generate_target_mode_tdf(
            sample_input_files["binary"],
            binary_tdf,
            "v4.3.1",
            temp_credentials_file,
            mime_type="image/png",
        )
        tdf_files["binary"] = binary_tdf

        # Generate TDF with attributes
        attr_tdf = output_dir / "sample_with_attributes.txt.tdf"
        _generate_target_mode_tdf(
            sample_input_files["with_attributes"],
            attr_tdf,
            "v4.3.1",
            temp_credentials_file,
            attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1],
            mime_type="text/plain",
        )
        tdf_files["with_attributes"] = attr_tdf

        yield tdf_files

    except Exception as e:
        raise Exception(f"Failed to generate v4.3.1 TDF files: {e}") from e


@pytest.fixture(scope="session")
def all_target_mode_tdf_files(tdf_v4_2_2_files, tdf_v4_3_1_files):
    """Combine all target mode TDF files into a single fixture."""
    return {
        "v4.2.2": tdf_v4_2_2_files,
        "v4.3.1": tdf_v4_3_1_files,
    }
