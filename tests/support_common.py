import logging
import subprocess
import zipfile
from pathlib import Path

import pytest

from tests.config_pydantic import CONFIG_TDF

logger = logging.getLogger(__name__)


def get_platform_url() -> str:
    # Get platform configuration
    platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
    if not platform_url:
        # Fail fast if OPENTDF_PLATFORM_URL is not set
        raise Exception(
            "OPENTDF_PLATFORM_URL must be set in config for integration tests"
        )
    return platform_url


def handle_subprocess_error(
    result: subprocess.CompletedProcess, collect_server_logs, scenario_name: str
) -> None:
    """Handle subprocess errors with proper server log collection and error reporting."""
    if result.returncode != 0:
        # Collect server logs for debugging
        logs = collect_server_logs()
        print(f"Server logs when '{scenario_name}' failed:\n{logs}")

        pytest.fail(
            f"Scenario failed: '{scenario_name}': "
            f"stdout={result.stdout}, stderr={result.stderr}"
        )


def get_testing_environ() -> dict | None:
    """Set up environment and configuration

    TODO: YAGNI: this is a hook we could use to modify all testing environments, e.g.
        env = os.environ.copy()
        env["GRPC_ENFORCE_ALPN_ENABLED"] = "false"
        return env
    """
    return None


def validate_tdf3_file(tdf_path: Path, tool_name: str) -> None:
    """Validate that a TDF file (tdf_type="tdf3") exists, is not empty, and has correct ZIP structure."""
    assert tdf_path.exists(), f"{tool_name} did not create TDF file"
    assert tdf_path.stat().st_size > 0, f"{tool_name} created empty TDF file"
    assert zipfile.is_zipfile(tdf_path), f"{tool_name} output is not a valid ZIP file"

    # Verify TDF file has correct ZIP signature
    with tdf_path.open("rb") as f:
        tdf_header = f.read(4)
    assert tdf_header == b"PK\x03\x04", f"{tool_name} output is not a valid ZIP file"
    assert tdf_path.suffix == ".tdf", f"File should have .tdf extension: {tdf_path}"


def validate_plaintext_file_created(
    path: Path, scenario: str, expected_content: str
) -> None:
    """Validate that a non-empty file was created, and contains the expected content"""
    assert path.exists(), f"{scenario=} did not create decrypted file"
    assert path.stat().st_size > 0, f"{scenario=} created empty decrypted file"
    # Verify scenario produces the expected decrypted content
    with path.open() as f:
        decrypted_content = f.read()

    assert decrypted_content == expected_content, (
        f"otdfctl decrypted content does not match original. "
        f"Expected: '{expected_content}', Got: '{decrypted_content}'"
    )


def compare_tdf3_file_size(otdfctl_tdf_path: Path, py_cli_tdf_path: Path) -> None:
    """Compare the file sizes of two TDF files (tdf_type="tdf3"), assert within 30% of each other."""
    size_otdfctl_tdf = otdfctl_tdf_path.stat().st_size
    size_py_cli_tdf = py_cli_tdf_path.stat().st_size
    size_diff_ratio = abs(size_otdfctl_tdf - size_py_cli_tdf) / max(
        size_otdfctl_tdf, size_py_cli_tdf
    )

    assert size_diff_ratio < 0.3, (
        f"File sizes too different: otdfctl={size_otdfctl_tdf}, cli={size_py_cli_tdf}"
    )
