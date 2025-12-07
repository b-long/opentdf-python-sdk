"""Support functions for constructing CLI arguments for otdfctl CLI."""

import logging
import subprocess
from pathlib import Path

from tests.config_pydantic import CONFIG_TDF
from tests.support_common import get_platform_url, get_testing_environ

logger = logging.getLogger(__name__)


def get_otdfctl_flags() -> list[str]:
    """Determine otdfctl flags based on platform URL"""
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


def get_otdfctl_base_command(
    creds_file: Path, platform_url: str | None = None
) -> list[str]:
    """Get base otdfctl command with common flags."""
    base_cmd = [
        "otdfctl",
        "--host",
        platform_url if platform_url is not None else get_platform_url(),
        "--with-client-creds-file",
        str(creds_file),
    ]

    # Add platform-specific flags
    base_cmd.extend(get_otdfctl_flags())

    return base_cmd


def _build_otdfctl_encrypt_command(
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    platform_url: str | None = None,
    mime_type: str = "text/plain",
    attributes: list[str] | None = None,
    tdf_type: str | None = None,
    target_mode: str | None = None,
) -> list[str]:
    """Build otdfctl encrypt command.

    Args:
        platform_url: Platform URL like "http://localhost:8080"
        creds_file: Path to credentials file
        input_file: Path to the input file to encrypt
        output_file: Path where the TDF file should be created
        mime_type: Optional MIME type for the input file
        attributes: Optional list of attributes to apply
        tdf_type: TDF type (e.g., "tdf3", "nano")
        target_mode: Target TDF spec version (e.g., "v4.2.2", "v4.3.1")

    """
    cmd = get_otdfctl_base_command(creds_file, platform_url)
    cmd.append("encrypt")
    cmd.extend(["--mime-type", mime_type])

    # Add attributes if provided
    if attributes:
        for attr in attributes:
            cmd.extend(["--attr", attr])

    if tdf_type:
        cmd.extend(
            [
                "--tdf-type",
                tdf_type,
            ]
        )

    if target_mode:
        cmd.extend(["--target-mode", target_mode])

    cmd.extend(
        [
            str(input_file),
            "-o",
            str(output_file),
        ]
    )
    return cmd


def run_otdfctl_encrypt_command(
    creds_file: Path,
    input_file: Path,
    output_file: Path,
    cwd: Path,
    platform_url: str | None = None,
    mime_type: str = "text/plain",
    attributes: list[str] | None = None,
    tdf_type: str | None = None,
    target_mode: str | None = None,
) -> subprocess.CompletedProcess:
    otdfctl_encrypt_cmd = _build_otdfctl_encrypt_command(
        creds_file=creds_file,
        input_file=input_file,
        output_file=output_file,
        platform_url=platform_url,
        mime_type=mime_type,
        attributes=attributes,
        tdf_type=tdf_type,
        target_mode=target_mode,
    )
    return subprocess.run(
        otdfctl_encrypt_cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=get_testing_environ(),
    )


def _build_otdfctl_decrypt_command(
    creds_file: Path, tdf_file: Path, output_file: Path, platform_url: str | None = None
) -> list[str]:
    """Build otdfctl decrypt command."""
    cmd = get_otdfctl_base_command(creds_file, platform_url)
    cmd.extend(
        [
            "decrypt",
            str(tdf_file),
            "-o",
            str(output_file),
        ]
    )

    return cmd


def run_otdfctl_decrypt_command(
    creds_file: Path,
    tdf_file: Path,
    output_file: Path,
    cwd: Path,
    platform_url: str | None = None,
) -> subprocess.CompletedProcess:
    otdfctl_decrypt_cmd = _build_otdfctl_decrypt_command(
        creds_file=creds_file,
        tdf_file=tdf_file,
        output_file=output_file,
        platform_url=platform_url,
    )

    return subprocess.run(
        otdfctl_decrypt_cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=get_testing_environ(),
    )


def _generate_target_mode_tdf(
    input_file: Path,
    output_file: Path,
    target_mode: str,
    creds_file: Path,
    attributes: list[str] | None = None,
    mime_type: str | None = None,
) -> None:
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Build otdfctl command
    cmd = _build_otdfctl_encrypt_command(
        platform_url=get_platform_url(),
        creds_file=creds_file,
        input_file=input_file,
        output_file=output_file,
        mime_type=mime_type if mime_type else "text/plain",
        attributes=attributes if attributes else None,
        tdf_type="tdf3",
        target_mode=target_mode,
    )

    # Run otdfctl command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=get_testing_environ(),
    )

    if result.returncode != 0:
        logger.error(f"otdfctl command failed: {result.stderr}")
        raise Exception(
            f"Failed to generate TDF with target mode {target_mode}: "
            f"stdout={result.stdout}, stderr={result.stderr}"
        )


def otdfctl_generate_tdf_files_for_target_mode(
    target_mode: str,
    temp_credentials_file: Path,
    test_data_dir: Path,
    sample_input_files: dict[str, Path],
) -> dict[str, Path]:
    """Factory function to generate TDF files for a specific target mode.

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
                attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1]
                if config["key"] == "with_attributes"
                else None,
                mime_type=config["mime_type"],
            )
            tdf_files[config["key"]] = tdf_path

        return tdf_files

    except Exception as e:
        logger.error(f"Error generating {target_mode} TDF files: {e}")
        raise Exception(f"Failed to generate {target_mode} TDF files: {e}") from e
