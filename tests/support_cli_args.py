import json
import logging
import subprocess
import sys
from pathlib import Path

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


def get_otdfctl_flags() -> list[str]:
    """
    Determine otdfctl flags based on platform URL
    """
    platform_url = get_platform_url()
    otdfctl_flags = []
    if platform_url.startswith("http://"):
        # otdfctl doesn't have a --plaintext flag, just omit --tls-no-verify for HTTP
        pass
    else:
        # For HTTPS, skip TLS verification if INSECURE_SKIP_VERIFY is True
        if CONFIG_TDF.INSECURE_SKIP_VERIFY:
            otdfctl_flags = ["--tls-no-verify"]

    return otdfctl_flags


def get_cli_flags() -> list[str]:
    """
    Determine Python (cli) flags based on platform URL
    """
    platform_url = get_platform_url()
    cli_flags = []

    if platform_url.startswith("http://"):
        cli_flags = ["--plaintext"]
        # otdfctl doesn't have a --plaintext flag, just omit --tls-no-verify for HTTP
    else:
        # For HTTPS, skip TLS verification if INSECURE_SKIP_VERIFY is True
        if CONFIG_TDF.INSECURE_SKIP_VERIFY:
            cli_flags = ["--insecure"]  # equivalent to --tls-no-verify

    return cli_flags


def get_otdfctl_base_command(platform_url: str, creds_file: Path) -> list[str]:
    """Get base otdfctl command with common flags."""
    base_cmd = [
        "otdfctl",
        "--host",
        platform_url,
        "--with-client-creds-file",
        str(creds_file),
    ]

    # Add platform-specific flags
    base_cmd.extend(get_otdfctl_flags())

    return base_cmd


def build_otdfctl_encrypt_command(
    platform_url: str,
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    mime_type: str = "text/plain",
    attributes: list[str] | None = None,
) -> list[str]:
    """Build otdfctl encrypt command."""
    cmd = get_otdfctl_base_command(platform_url, creds_file)
    cmd.append("encrypt")
    cmd.extend(["--mime-type", mime_type])

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


def build_otdfctl_decrypt_command(
    platform_url: str, creds_file: Path, tdf_file: Path, output_file: Path
) -> list[str]:
    """Build otdfctl decrypt command."""
    cmd = get_otdfctl_base_command(platform_url, creds_file)
    cmd.extend(
        [
            "decrypt",
            str(tdf_file),
            "-o",
            str(output_file),
        ]
    )

    return cmd


def run_cli_inspect(tdf_path: Path, creds_file: Path) -> dict:
    """
    Helper function to run Python CLI inspect command and return parsed JSON result.

    This demonstrates how the CLI inspect functionality could be tested
    with the new fixtures.
    """
    # Determine platform flags
    platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
    cli_flags = get_cli_flags()

    # Build CLI command
    cmd = [
        sys.executable,
        "-m",
        "otdf_python.cli",
        "--platform-url",
        platform_url,
        "--with-client-creds-file",
        str(creds_file),
        *cli_flags,
        "inspect",
        str(tdf_path),
    ]

    try:
        # Run the CLI command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=Path(__file__).parent.parent,  # Project root
        )

        # Parse JSON output
        return json.loads(result.stdout)

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        logger.error(f"CLI inspect failed for {tdf_path}: {e}")
        raise Exception(f"Failed to inspect TDF {tdf_path}: {e}") from e
