"""
Test target mode TDF fixtures.
"""

from pathlib import Path

import pytest


@pytest.mark.integration
def test_target_mode_fixtures_exist(all_target_mode_tdf_files):
    """Test that target mode fixtures generate TDF files correctly."""
    # Check that we have both versions
    assert "v4.2.2" in all_target_mode_tdf_files
    assert "v4.3.1" in all_target_mode_tdf_files

    # Check each version has the expected file types
    for version in ["v4.2.2", "v4.3.1"]:
        tdf_files = all_target_mode_tdf_files[version]

        # Check all expected file types exist
        expected_types = ["text", "empty", "binary", "with_attributes"]
        for file_type in expected_types:
            assert file_type in tdf_files, f"Missing {file_type} TDF for {version}"

            # Check the TDF file exists and is not empty
            tdf_path = tdf_files[file_type]
            assert isinstance(tdf_path, Path)
            assert tdf_path.exists(), f"TDF file does not exist: {tdf_path}"
            assert tdf_path.stat().st_size > 0, f"TDF file is empty: {tdf_path}"

            # Check it's a valid ZIP file (TDF format)
            with open(tdf_path, "rb") as f:
                header = f.read(4)
            assert header == b"PK\x03\x04", f"TDF file is not a valid ZIP: {tdf_path}"


@pytest.mark.integration
def test_v4_2_2_tdf_files(tdf_v4_2_2_files):
    """Test that v4.2.2 TDF fixtures work independently."""
    assert "text" in tdf_v4_2_2_files
    assert tdf_v4_2_2_files["text"].exists()


@pytest.mark.integration
def test_v4_3_1_tdf_files(tdf_v4_3_1_files):
    """Test that v4.3.1 TDF fixtures work independently."""
    assert "text" in tdf_v4_3_1_files
    assert tdf_v4_3_1_files["text"].exists()
