"""
Tests using target mode fixtures, for CLI integration testing.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.config_pydantic import CONFIG_TDF


@pytest.mark.integration
def test_cli_inspect_v4_2_2_vs_v4_3_1(all_target_mode_tdf_files, temp_credentials_file):
    """
    Test CLI inspect with various TDF versions.
    """

    v4_2_2_files = all_target_mode_tdf_files["v4.2.2"]
    v4_3_1_files = all_target_mode_tdf_files["v4.3.1"]

    # Test inspect on both versions of the same file type
    for file_type in ["text", "binary"]:
        v4_2_2_tdf = v4_2_2_files[file_type]
        v4_3_1_tdf = v4_3_1_files[file_type]

        # Inspect v4.2.2 TDF
        v4_2_2_result = _run_cli_inspect(v4_2_2_tdf, temp_credentials_file)

        # Inspect v4.3.1 TDF
        v4_3_1_result = _run_cli_inspect(v4_3_1_tdf, temp_credentials_file)

        # Both should succeed
        assert v4_2_2_result is not None, f"Failed to inspect v4.2.2 {file_type} TDF"
        assert v4_3_1_result is not None, f"Failed to inspect v4.3.1 {file_type} TDF"

        # Both should have manifest data
        assert "manifest" in v4_2_2_result, (
            f"v4.2.2 {file_type} inspection missing manifest"
        )
        assert "manifest" in v4_3_1_result, (
            f"v4.3.1 {file_type} inspection missing manifest"
        )

        # Compare manifest versions (this is where version differences would show)
        print(f"\\n=== {file_type.upper()} TDF Comparison ===")
        print(f"v4.2.2 manifest keys: {list(v4_2_2_result['manifest'].keys())}")
        print(f"v4.3.1 manifest keys: {list(v4_3_1_result['manifest'].keys())}")


@pytest.mark.integration
def test_cli_inspect_different_file_types(tdf_v4_3_1_files, temp_credentials_file):
    """
    Test CLI inspect with different file types.
    """

    file_types_to_test = ["text", "empty", "binary", "with_attributes"]

    for file_type in file_types_to_test:
        tdf_path = tdf_v4_3_1_files[file_type]

        # Inspect the TDF
        result = _run_cli_inspect(tdf_path, temp_credentials_file)

        assert result is not None, f"Failed to inspect {file_type} TDF"
        assert "manifest" in result, f"{file_type} TDF inspection missing manifest"

        # Check file-type specific expectations
        if file_type == "empty":
            # Empty files should still have valid manifests
            assert "encryptionInformation" in result["manifest"]
        elif file_type == "with_attributes":
            # Attributed files should have keyAccess information
            assert (
                "keyAccess" in result["manifest"]
                or "encryptionInformation" in result["manifest"]
            )


def _run_cli_inspect(tdf_path: Path, creds_file: Path) -> dict | None:
    """
    Helper function to run CLI inspect command and return parsed JSON result.

    This demonstrates how the CLI inspect functionality could be tested
    with the new fixtures.
    """
    # Determine platform flags
    platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
    cli_flags = []

    if platform_url.startswith("http://"):
        cli_flags = ["--plaintext"]
    elif CONFIG_TDF.INSECURE_SKIP_VERIFY:
        cli_flags = ["--insecure"]

    # Build CLI command
    cmd = [
        sys.executable,
        "-m",
        "otdf_python.cli",
        "inspect",
        str(tdf_path),
        "--platform-url",
        platform_url,
        "--with-client-creds-file",
        str(creds_file),
        *cli_flags,
    ]

    try:
        # Run the CLI command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=Path(__file__).parent.parent.parent,  # Project root
        )

        # Parse JSON output
        return json.loads(result.stdout)

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"CLI inspect failed for {tdf_path}: {e}")
        return None
