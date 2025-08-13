"""
Shared fixtures and utilities for integration tests.
"""

import json
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def temp_credentials_file():
    """Create a temporary credentials file for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        creds_file = Path(temp_dir) / "creds.json"
        creds_data = {"clientId": "opentdf", "clientSecret": "secret"}
        with open(creds_file, "w") as f:
            json.dump(creds_data, f)
        yield creds_file
