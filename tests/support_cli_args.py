"""Support functions for constructing CLI arguments for this project's (Python) CLI."""

import json
import logging
import subprocess
import sys
from pathlib import Path

from tests.config_pydantic import CONFIG_TDF
from tests.support_common import get_platform_url, get_testing_environ

logger = logging.getLogger(__name__)


def _get_cli_flags() -> list[str]:
    """Determine (Python) CLI flags based on platform URL"""
    platform_url = get_platform_url()
    cli_flags = []

    if platform_url.startswith("http://"):
        cli_flags = ["--plaintext"]
    else:
        # For HTTPS, skip TLS verification if INSECURE_SKIP_VERIFY is True
        if CONFIG_TDF.INSECURE_SKIP_VERIFY:
            cli_flags = ["--insecure"]

    return cli_flags


def run_cli_inspect(tdf_path: Path, creds_file: Path, cwd: Path) -> dict:
    """Helper function to run Python CLI inspect command and return parsed JSON result.

    This demonstrates how the CLI inspect functionality could be tested
    with the new fixtures.
    """
    # Build CLI command
    cmd = [
        sys.executable,
        "-m",
        "otdf_python",
        "--platform-url",
        get_platform_url(),
        "--with-client-creds-file",
        str(creds_file),
        *_get_cli_flags(),
        "inspect",
        str(tdf_path),
    ]

    try:
        # Run the CLI command
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, cwd=cwd
        )

        # Parse JSON output
        return json.loads(result.stdout)

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        logger.error(f"CLI inspect failed for {tdf_path}: {e}")
        raise Exception(f"Failed to inspect TDF {tdf_path}: {e}") from e


def _build_cli_decrypt_command(
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    platform_url: str | None = None,
) -> list[str]:
    """Build CLI decrypt command."""
    cmd = [
        sys.executable,
        "-m",
        "otdf_python",
        "--platform-url",
        platform_url if platform_url is not None else get_platform_url(),
        "--with-client-creds-file",
        str(creds_file),
        *_get_cli_flags(),
        "decrypt",
        str(input_file),
        "-o",
        str(output_file),
    ]
    return cmd


def run_cli_decrypt(
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    cwd: Path,
    platform_url: str | None = None,
) -> subprocess.CompletedProcess:
    python_decrypt_cmd = _build_cli_decrypt_command(
        creds_file=creds_file,
        input_file=input_file,
        output_file=output_file,
        platform_url=platform_url,
    )
    return subprocess.run(
        python_decrypt_cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=get_testing_environ(),
    )


def _build_cli_encrypt_command(
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    platform_url: str | None = None,
    mime_type: str = "text/plain",
    attributes: list[str] | None = None,
    container_type: str = "tdf",
) -> list[str]:
    cmd = [
        sys.executable,
        "-m",
        "otdf_python",
        "--platform-url",
        platform_url if platform_url is not None else get_platform_url(),
        "--with-client-creds-file",
        str(creds_file),
        *_get_cli_flags(),
        "encrypt",
        "--mime-type",
        mime_type,
        "--container-type",
        container_type,
    ]

    # Add attributes if provided
    if attributes:
        for attr in attributes:
            cmd.extend(["--attr", attr])

    cmd.extend(
        [
            str(input_file),
            "-o",
            str(output_file),
        ]
    )

    return cmd


def run_cli_encrypt(
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    cwd: Path,
    platform_url: str | None = None,
    mime_type: str = "text/plain",
    attributes: list[str] | None = None,
    container_type: str = "tdf",
) -> subprocess.CompletedProcess:
    python_encrypt_cmd = _build_cli_encrypt_command(
        creds_file=creds_file,
        input_file=input_file,
        output_file=output_file,
        platform_url=platform_url,
        mime_type=mime_type,
        attributes=attributes,
        container_type=container_type,
    )

    return subprocess.run(
        python_encrypt_cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=get_testing_environ(),
    )
