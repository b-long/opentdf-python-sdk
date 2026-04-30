#!/usr/bin/env python3
"""Setup script for Connect RPC dependencies.

Run this script once to install the required tools before generating proto files:

    uv run python scripts/setup_connect_rpc.py
"""

import subprocess
import sys


def main():
    """Install Connect RPC compiler dependencies."""
    print("Installing Connect RPC dependencies...")
    subprocess.run(
        ["uv", "sync"],
        check=True,
    )
    print("✓ Connect RPC dependencies installed.")
    print("  Run 'uv run python scripts/generate_connect_proto.py' to generate files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
