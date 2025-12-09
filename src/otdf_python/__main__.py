#!/usr/bin/env python3
"""Main entry point for running otdf_python as a module.

This allows the package to be run with `python -m otdf_python` and properly
handles the CLI interface without import conflicts.
"""

from .cli import main

if __name__ == "__main__":
    main()
