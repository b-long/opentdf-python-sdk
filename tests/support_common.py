import logging
import subprocess

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
