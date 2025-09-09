"""
Support functions for constructing CLI arguments for otdfctl CLI.
"""

from pathlib import Path

from tests.config_pydantic import CONFIG_TDF
from tests.support_common import get_platform_url


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
    tdf_type: str | None = None,
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
    """

    # FIXME: Add target_mode: Target TDF spec version (e.g., "v4.2.2", "v4.3.1")

    cmd = get_otdfctl_base_command(platform_url, creds_file)
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
