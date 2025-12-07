"""Shared fixtures and utilities for integration tests."""

import json
import logging
import tempfile
from pathlib import Path

import pytest

from tests.support_otdfctl_args import otdfctl_generate_tdf_files_for_target_mode

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def temp_credentials_file():
    """Create a temporary credentials file for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        creds_file = Path(temp_dir) / "creds.json"
        creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
        with creds_file.open("w") as f:
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


@pytest.fixture(scope="session")
def tdf_v4_2_2_files(temp_credentials_file, test_data_dir, sample_input_files):
    """Generate TDF files with target mode v4.2.2."""
    tdf_files = otdfctl_generate_tdf_files_for_target_mode(
        "v4.2.2", temp_credentials_file, test_data_dir, sample_input_files
    )
    yield tdf_files


@pytest.fixture(scope="session")
def tdf_v4_3_1_files(temp_credentials_file, test_data_dir, sample_input_files):
    """Generate TDF files with target mode v4.3.1."""
    tdf_files = otdfctl_generate_tdf_files_for_target_mode(
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


@pytest.fixture(scope="session")
def known_target_modes():
    return ["v4.2.2", "v4.3.1"]
