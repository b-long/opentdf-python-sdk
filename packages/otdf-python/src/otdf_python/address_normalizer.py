"""Address normalization utilities for OpenTDF."""

import logging
import re
from urllib.parse import urlparse

from .sdk_exceptions import SDKException

logger = logging.getLogger(__name__)


def normalize_address(url_string: str, use_plaintext: bool) -> str:
    """Normalize a URL address to ensure it has the correct scheme and port.

    Args:
        url_string: The URL string to normalize
        use_plaintext: If True, use http scheme, otherwise use https

    Returns:
        The normalized URL string

    Raises:
        SDKException: If there's an error parsing or creating the URL

    """
    scheme = "http" if use_plaintext else "https"

    # Check if we have a host:port format without scheme (with non-digit port)
    host_port_pattern = re.match(r"^([^/:]+):([^/]+)$", url_string)
    if host_port_pattern:
        host = host_port_pattern.group(1)
        port_str = host_port_pattern.group(2)
        try:
            port = int(port_str)
        except ValueError as err:
            raise SDKException(f"Invalid port in URL [{url_string}]") from err

        normalized_url = f"{scheme}://{host}:{port}"
        logger.debug(f"normalized url [{url_string}] to [{normalized_url}]")
        return normalized_url

    try:
        # Check if we just have a hostname without scheme and port
        if "://" not in url_string and "/" not in url_string and ":" not in url_string:
            port = 80 if use_plaintext else 443
            normalized_url = f"{scheme}://{url_string}:{port}"
            logger.debug(f"normalized url [{url_string}] to [{normalized_url}]")
            return normalized_url

        # Parse the URL
        parsed_url = urlparse(url_string)

        # If no scheme, add one
        if not parsed_url.scheme:
            url_string = f"{scheme}://{url_string}"
            parsed_url = urlparse(url_string)

        # Extract host and port
        host = parsed_url.netloc.split(":")[0] if parsed_url.netloc else parsed_url.path

        # If there's a port in the URL, try to extract it
        port = None
        if ":" in parsed_url.netloc:
            _, port_str = parsed_url.netloc.split(":", 1)
            try:
                port = int(port_str)
            except ValueError as err:
                raise SDKException(f"Invalid port in URL [{url_string}]") from err

        # If no port was found or extracted, use the default
        if port is None:
            port = 80 if use_plaintext else 443

        # Reconstruct the URL with the desired scheme
        normalized_url = f"{scheme}://{host}:{port}"
        logger.debug(f"normalized url [{url_string}] to [{normalized_url}]")
        return normalized_url

    except Exception as e:
        if isinstance(e, SDKException):
            raise e
        raise SDKException(f"Error normalizing URL [{url_string}]: {e}") from e
