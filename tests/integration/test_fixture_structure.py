"""
Test the basic structure of target mode fixtures without requiring otdfctl/platform.
"""

from pathlib import Path


def test_test_data_directory_structure():
    """Test that the test data directory has the correct structure."""
    test_data_dir = Path(__file__).parent / "test_data"

    # Check main directory exists
    assert test_data_dir.exists(), "Test data directory should exist"

    # Check subdirectories exist
    v4_2_2_dir = test_data_dir / "v4.2.2"
    v4_3_1_dir = test_data_dir / "v4.3.1"
    assert v4_2_2_dir.exists(), "v4.2.2 directory should exist"
    assert v4_3_1_dir.exists(), "v4.3.1 directory should exist"

    # Check sample input files exist
    expected_files = [
        "sample_text.txt",
        "empty_file.txt",
        "sample_binary.png",
        "sample_with_attributes.txt",
    ]

    for filename in expected_files:
        file_path = test_data_dir / filename
        assert file_path.exists(), f"Sample file should exist: {filename}"


def test_sample_file_contents():
    """Test that sample files have expected content."""
    test_data_dir = Path(__file__).parent / "test_data"

    # Check text file has content
    text_file = test_data_dir / "sample_text.txt"
    with open(text_file) as f:
        content = f.read()
    assert "Hello, World!" in content
    assert len(content) > 0

    # Check empty file is empty
    empty_file = test_data_dir / "empty_file.txt"
    assert empty_file.stat().st_size == 0

    # Check binary file exists and has content
    binary_file = test_data_dir / "sample_binary.png"
    assert binary_file.stat().st_size > 0

    # Check attributes file has content
    attr_file = test_data_dir / "sample_with_attributes.txt"
    with open(attr_file) as f:
        content = f.read()
    assert "Classification: SECRET" in content
