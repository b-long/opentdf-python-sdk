"""OpenTDF Python SDK.

A Python implementation of the OpenTDF SDK for working with Trusted Data Format (TDF) files.
Provides both programmatic APIs and command-line interface for encryption and decryption.
"""

from .cli import main as cli_main
from .config import KASInfo, NanoTDFConfig, TDFConfig
from .sdk import SDK
from .sdk_builder import SDKBuilder

__all__ = [
    "SDK",
    "KASInfo",
    "NanoTDFConfig",
    "SDKBuilder",
    "TDFConfig",
    "cli_main",
]


def main() -> None:
    """Entry point for the CLI."""
    cli_main()
