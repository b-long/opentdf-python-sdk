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
