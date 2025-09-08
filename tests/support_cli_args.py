from pathlib import Path

from tests.config_pydantic import CONFIG_TDF


def get_platform_url() -> str:
    # Get platform configuration
    platform_url = CONFIG_TDF.OPENTDF_PLATFORM_URL
    if not platform_url:
        # Fail fast if OPENTDF_PLATFORM_URL is not set
        raise Exception(
            "OPENTDF_PLATFORM_URL must be set in config for integration tests"
        )
    return platform_url


def get_otdfctl_flags() -> list:
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


def get_cli_flags() -> list:
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


def get_otdfctl_base_command(platform_url: str, creds_file: Path) -> list:
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
    input_file,
    output_file,
    mime_type: str = "text/plain",
    attributes: list | None = None,
) -> list:
    """Build otdfctl encrypt command."""
    cmd = get_otdfctl_base_command(platform_url, creds_file)
    cmd.extend(
        [
            "encrypt",
            "--mime-type",
            mime_type,
            str(input_file),
            "-o",
            str(output_file),
        ]
    )

    # Add attributes if provided
    if attributes:
        for attr in attributes:
            cmd.extend(["--attr", attr])

    return cmd


def build_otdfctl_decrypt_command(
    platform_url: str, creds_file: Path, tdf_file: Path, output_file: Path
) -> list:
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
