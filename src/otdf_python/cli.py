#!/usr/bin/env python3
"""OpenTDF Python CLI.

A command-line interface for encrypting and decrypting files using OpenTDF.
Provides encrypt, decrypt, and inspect commands similar to the otdfctl CLI.
"""

import argparse
import contextlib
import json
import logging
import sys
from dataclasses import asdict
from importlib import metadata
from io import BytesIO
from pathlib import Path

from otdf_python.config import KASInfo, NanoTDFConfig, TDFConfig
from otdf_python.sdk import SDK
from otdf_python.sdk_builder import SDKBuilder
from otdf_python.sdk_exceptions import SDKException

try:
    __version__ = metadata.version("otdf-python")
except metadata.PackageNotFoundError:
    # package is not installed, e.g., in development
    __version__ = "0.0.0"


# Set up logging
logger = logging.getLogger(__name__)


class CLIError(Exception):
    """Custom exception for CLI errors."""

    def __init__(self, level: str, message: str, cause: Exception | None = None):
        """Initialize CLI error."""
        self.level = level
        self.message = message
        self.cause = cause
        super().__init__(message)


def setup_logging(level: str = "INFO", silent: bool = False):
    """Set up logging configuration."""
    if silent:
        level = "CRITICAL"

    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def validate_file_exists(file_path: str) -> Path:
    """Validate that a file exists and is readable."""
    path = Path(file_path)
    if not path.exists():
        raise CLIError("CRITICAL", f"File does not exist: {file_path}")
    if not path.is_file():
        raise CLIError("CRITICAL", f"Path is not a file: {file_path}")
    return path


def parse_attributes(attributes_str: str) -> list[str]:
    """Parse comma-separated attributes string."""
    if not attributes_str:
        return []
    return [attr.strip() for attr in attributes_str.split(",") if attr.strip()]


def parse_kas_endpoints(kas_str: str) -> list[str]:
    """Parse comma-separated KAS endpoints."""
    if not kas_str:
        return []
    return [kas.strip() for kas in kas_str.split(",") if kas.strip()]


def load_client_credentials(creds_file_path: str) -> tuple[str, str]:
    """Load client credentials from JSON file."""
    try:
        creds_path = Path(creds_file_path)
        if not creds_path.exists():
            raise CLIError(
                "CRITICAL", f"Credentials file does not exist: {creds_file_path}"
            )

        with creds_path.open() as f:
            creds = json.load(f)

        client_id = creds.get("clientId")
        client_secret = creds.get("clientSecret")

        if not client_id or not client_secret:
            raise CLIError(
                "CRITICAL",
                f"Credentials file must contain 'clientId' and 'clientSecret' fields: {creds_file_path}",
            )

        return client_id, client_secret

    except json.JSONDecodeError as e:
        raise CLIError(
            "CRITICAL", f"Invalid JSON in credentials file {creds_file_path}: {e}"
        ) from e
    except Exception as e:
        raise CLIError(
            "CRITICAL", f"Error reading credentials file {creds_file_path}: {e}"
        ) from e


def build_sdk(args) -> SDK:
    """Build SDK instance from CLI arguments."""
    builder = SDKBuilder()

    if args.platform_url:
        builder.set_platform_endpoint(args.platform_url)

        # Auto-detect HTTP URLs and enable plaintext mode
        if args.platform_url.startswith("http://") and (
            not hasattr(args, "plaintext") or not args.plaintext
        ):
            logger.debug(
                f"Auto-detected HTTP URL {args.platform_url}, enabling plaintext mode"
            )
            builder.use_insecure_plaintext_connection(True)

    if args.oidc_endpoint:
        builder.set_issuer_endpoint(args.oidc_endpoint)

    if args.client_id and args.client_secret:
        builder.client_secret(args.client_id, args.client_secret)
    elif hasattr(args, "with_client_creds_file") and args.with_client_creds_file:
        # Load credentials from file
        client_id, client_secret = load_client_credentials(args.with_client_creds_file)
        builder.client_secret(client_id, client_secret)
    elif hasattr(args, "auth") and args.auth:
        # Parse combined auth string (clientId:clientSecret) - legacy support
        auth_parts = args.auth.split(":")
        if len(auth_parts) != 2:
            raise CLIError(
                "CRITICAL",
                f"Auth expects <clientId>:<clientSecret>, received {args.auth}",
            )
        builder.client_secret(auth_parts[0], auth_parts[1])
    else:
        raise CLIError(
            "CRITICAL",
            "Authentication required: provide --with-client-creds-file OR --client-id and --client-secret",
        )

    if hasattr(args, "plaintext") and args.plaintext:
        builder.use_insecure_plaintext_connection(True)

    if args.insecure:
        builder.use_insecure_skip_verify(True)

    return builder.build()


def create_tdf_config(sdk: SDK, args) -> TDFConfig:
    """Create TDF configuration from CLI arguments."""
    attributes = (
        parse_attributes(args.attributes)
        if hasattr(args, "attributes") and args.attributes
        else []
    )

    config = sdk.new_tdf_config(attributes=attributes)

    if hasattr(args, "kas_endpoint") and args.kas_endpoint:
        # Add KAS endpoints
        kas_endpoints = parse_kas_endpoints(args.kas_endpoint)
        kas_info_list = [KASInfo(url=kas_url) for kas_url in kas_endpoints]
        config.kas_info_list.extend(kas_info_list)

    if hasattr(args, "mime_type") and args.mime_type:
        config.mime_type = args.mime_type

    if hasattr(args, "autoconfigure") and args.autoconfigure is not None:
        config.autoconfigure = args.autoconfigure

    return config


def create_nano_tdf_config(sdk: SDK, args) -> NanoTDFConfig:
    """Create NanoTDF configuration from CLI arguments."""
    attributes = (
        parse_attributes(args.attributes)
        if hasattr(args, "attributes") and args.attributes
        else []
    )

    config = NanoTDFConfig(attributes=attributes)

    if hasattr(args, "kas_endpoint") and args.kas_endpoint:
        # Add KAS endpoints
        kas_endpoints = parse_kas_endpoints(args.kas_endpoint)
        kas_info_list = [KASInfo(url=kas_url) for kas_url in kas_endpoints]
        config.kas_info_list.extend(kas_info_list)
    elif args.platform_url:
        # If no explicit KAS endpoint provided, derive from platform URL
        # This matches the default KAS path convention
        kas_url = args.platform_url.rstrip("/") + "/kas"
        logger.debug(f"Deriving KAS endpoint from platform URL: {kas_url}")
        kas_info = KASInfo(url=kas_url)
        config.kas_info_list.append(kas_info)

    if hasattr(args, "policy_binding") and args.policy_binding:
        if args.policy_binding.lower() == "ecdsa":
            config.ecc_mode = "ecdsa"
        else:
            config.ecc_mode = "gmac"  # default

    return config


def cmd_encrypt(args):
    """Handle encrypt command."""
    logger.info("Running encrypt command")

    # Validate input file
    input_path = validate_file_exists(args.file)

    # Build SDK
    sdk = build_sdk(args)

    try:
        # Read input file
        with input_path.open("rb") as input_file:
            payload = input_file.read()

        # Determine output
        if args.output:
            output_path = Path(args.output)
            with output_path.open("wb") as output_file:
                try:
                    # Create appropriate config based on container type
                    container_type = getattr(args, "container_type", "tdf")

                    if container_type == "nano":
                        logger.debug("Creating NanoTDF")
                        config = create_nano_tdf_config(sdk, args)
                        output_stream = BytesIO()
                        size = sdk.create_nano_tdf(
                            BytesIO(payload), output_stream, config
                        )
                        output_file.write(output_stream.getvalue())
                        logger.info(f"Created NanoTDF of size {size} bytes")
                    else:
                        logger.debug("Creating TDF")
                        config = create_tdf_config(sdk, args)
                        output_stream = BytesIO()
                        _manifest, size, _ = sdk.create_tdf(
                            BytesIO(payload), config, output_stream
                        )
                        output_file.write(output_stream.getvalue())
                        logger.info(f"Created TDF of size {size} bytes")

                except Exception:
                    # Clean up the output file if there was an error
                    with contextlib.suppress(Exception):
                        output_path.unlink()
                    raise
        else:
            output_file = sys.stdout.buffer
            # Create appropriate config based on container type
            container_type = getattr(args, "container_type", "tdf")

            if container_type == "nano":
                logger.debug("Creating NanoTDF")
                config = create_nano_tdf_config(sdk, args)
                output_stream = BytesIO()
                size = sdk.create_nano_tdf(BytesIO(payload), output_stream, config)
                output_file.write(output_stream.getvalue())
                logger.info(f"Created NanoTDF of size {size} bytes")
            else:
                logger.debug("Creating TDF")
                config = create_tdf_config(sdk, args)
                output_stream = BytesIO()
                _manifest, size, _ = sdk.create_tdf(
                    BytesIO(payload), config, output_stream
                )
                output_file.write(output_stream.getvalue())
                logger.info(f"Created TDF of size {size} bytes")

    finally:
        sdk.close()


def cmd_decrypt(args):
    """Handle decrypt command."""
    logger.info("Running decrypt command")

    # Validate input file
    input_path = validate_file_exists(args.file)

    # Build SDK
    sdk = build_sdk(args)

    try:
        # Read encrypted file
        with input_path.open("rb") as input_file:
            encrypted_data = input_file.read()

        # Determine output
        if args.output:
            output_path = Path(args.output)
            with output_path.open("wb") as output_file:
                try:
                    # Try to determine if it's a NanoTDF or regular TDF
                    # NanoTDFs have a specific header format, regular TDFs are ZIP files
                    if encrypted_data.startswith(b"PK"):
                        # Regular TDF (ZIP format)
                        logger.debug("Decrypting TDF")
                        tdf_reader = sdk.load_tdf(encrypted_data)
                        # Access payload directly from TDFReader
                        payload_bytes = tdf_reader.payload
                        output_file.write(payload_bytes)
                        logger.info("Successfully decrypted TDF")
                    else:
                        # Assume NanoTDF
                        logger.debug("Decrypting NanoTDF")
                        config = create_nano_tdf_config(sdk, args)
                        sdk.read_nano_tdf(BytesIO(encrypted_data), output_file, config)
                        logger.info("Successfully decrypted NanoTDF")

                except Exception:
                    # Clean up the output file if there was an error
                    output_path.unlink(missing_ok=True)
                    raise
        else:
            output_file = sys.stdout.buffer
            # Try to determine if it's a NanoTDF or regular TDF
            # NanoTDFs have a specific header format, regular TDFs are ZIP files
            if encrypted_data.startswith(b"PK"):
                # Regular TDF (ZIP format)
                logger.debug("Decrypting TDF")
                tdf_reader = sdk.load_tdf(encrypted_data)
                payload_bytes = tdf_reader.payload
                output_file.write(payload_bytes)
                logger.info("Successfully decrypted TDF")
            else:
                # Assume NanoTDF
                logger.debug("Decrypting NanoTDF")
                config = create_nano_tdf_config(sdk, args)
                sdk.read_nano_tdf(BytesIO(encrypted_data), output_file, config)
                logger.info("Successfully decrypted NanoTDF")

    finally:
        sdk.close()


def cmd_inspect(args):
    """Handle inspect command."""
    logger.info("Running inspect command")

    # Validate input file
    input_path = validate_file_exists(args.file)

    try:
        sdk = build_sdk(args)

        try:
            # Read encrypted file
            with input_path.open("rb") as input_file:
                encrypted_data = input_file.read()

            if encrypted_data.startswith(b"PK"):
                # Regular TDF
                logger.debug("Inspecting TDF")
                tdf_reader = sdk.load_tdf(BytesIO(encrypted_data))
                manifest = tdf_reader.manifest

                # Try to get data attributes
                try:
                    data_attributes = []  # This would need to be implemented in the SDK
                    inspection_result = {
                        "manifest": asdict(manifest),
                        "dataAttributes": data_attributes,
                    }
                except Exception as e:
                    logger.warning(f"Could not retrieve data attributes: {e}")
                    inspection_result = {"manifest": asdict(manifest)}

                print(json.dumps(inspection_result, indent=2, default=str))
            else:
                # NanoTDF - for now just show basic info
                logger.debug("Inspecting NanoTDF")
                print(
                    json.dumps(
                        {
                            "type": "NanoTDF",
                            "size": len(encrypted_data),
                            "note": "NanoTDF inspection not fully implemented",
                        },
                        indent=2,
                    )
                )

        finally:
            sdk.close()

    except Exception as e:
        # If we can't inspect due to auth issues, show what we can
        logger.warning(f"Limited inspection due to: {e}")
        with input_path.open("rb") as input_file:
            encrypted_data = input_file.read()

        file_type = "TDF" if encrypted_data.startswith(b"PK") else "NanoTDF"
        print(
            json.dumps(
                {
                    "type": file_type,
                    "size": len(encrypted_data),
                    "note": "Full inspection requires authentication",
                },
                indent=2,
            )
        )


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="OpenTDF CLI - Encrypt and decrypt files using OpenTDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encrypt --file plain.txt --with-client-creds-file creds.json --platform-url https://platform.example.com
  %(prog)s decrypt --file encrypted.tdf --with-client-creds-file creds.json --platform-url https://platform.example.com
  %(prog)s inspect --file encrypted.tdf

Where creds.json contains:
  {"clientId": "your-client-id", "clientSecret": "your-client-secret"}
        """,
    )

    # Global options
    parser.add_argument(
        "--version", action="version", version=f"OpenTDF Python SDK {__version__}"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level",
    )
    parser.add_argument("--silent", action="store_true", help="Disable logging")

    # Server endpoints
    server_group = parser.add_argument_group("Server Endpoints")
    server_group.add_argument("--platform-url", help="OpenTDF platform URL")
    server_group.add_argument(
        "--kas-endpoint", help="KAS endpoint URL (comma-separated for multiple)"
    )
    server_group.add_argument("--oidc-endpoint", help="OIDC endpoint URL")

    # Authentication
    auth_group = parser.add_argument_group("Authentication")
    auth_group.add_argument(
        "--with-client-creds-file",
        help="Path to JSON file containing OAuth credentials (clientId and clientSecret)",
    )
    auth_group.add_argument("--client-id", help="OAuth client ID")
    auth_group.add_argument("--client-secret", help="OAuth client secret")

    # Security options
    security_group = parser.add_argument_group("Security")
    security_group.add_argument(
        "--plaintext", action="store_true", help="Use HTTP instead of HTTPS"
    )
    security_group.add_argument(
        "--insecure", action="store_true", help="Skip TLS verification"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("file", help="Path to file to encrypt")
    encrypt_parser.add_argument(
        "--output", "-o", help="Output file path (default: stdout)"
    )
    encrypt_parser.add_argument(
        "--attributes", help="Data attributes (comma-separated)"
    )
    encrypt_parser.add_argument(
        "--container-type",
        choices=["tdf", "nano"],
        default="tdf",
        help="Container format",
    )
    encrypt_parser.add_argument("--mime-type", help="MIME type of the input file")
    encrypt_parser.add_argument(
        "--autoconfigure",
        action="store_true",
        help="Enable automatic configuration from attributes",
    )
    encrypt_parser.add_argument(
        "--policy-binding",
        choices=["ecdsa", "gmac"],
        default="gmac",
        help="Policy binding type (nano only)",
    )

    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("file", help="Path to encrypted file")
    decrypt_parser.add_argument(
        "--output", "-o", help="Output file path (default: stdout)"
    )

    # Inspect command
    inspect_parser = subparsers.add_parser(
        "inspect", help="Inspect encrypted file metadata"
    )
    inspect_parser.add_argument("file", help="Path to encrypted file")

    return parser


def main():
    """Execute the CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.log_level, args.silent)

    # Validate command
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "encrypt":
            cmd_encrypt(args)
        elif args.command == "decrypt":
            cmd_decrypt(args)
        elif args.command == "inspect":
            cmd_inspect(args)
        else:
            parser.print_help()
            sys.exit(1)

    except CLIError as e:
        logger.error(f"{e.level}: {e.message}")
        if e.cause:
            logger.debug(f"Caused by: {e.cause}")
        sys.exit(1)
    except SDKException as e:
        logger.error(f"SDK Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error("", exc_info=True)  # Always print traceback for unexpected errors
        sys.exit(1)


if __name__ == "__main__":
    main()
