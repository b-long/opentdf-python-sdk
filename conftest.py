"""Pytest configuration and fixtures for the OpenTDF Python SDK tests.

This module contains pytest hooks and fixtures that will be automatically
loaded by pytest when running tests.
"""

from pathlib import Path

import pytest

from tests.server_logs import log_server_logs_on_failure


@pytest.fixture(scope="session")
def project_root(request) -> Path:
    """Get project root directory."""
    return request.config.rootpath  # Project root


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect server logs when test fails after each test phase.

    This hook automatically collects server logs when a test fails.
    """
    # Execute the test and get the report
    outcome = yield
    rep = outcome.get_result()

    # Only collect logs on test failure during the 'call' phase
    # (not during setup or teardown failures)
    if rep.when == "call" and rep.failed:
        # Get the test name from the item
        test_name = item.nodeid

        # Check if this is an integration test that might need server logs
        if hasattr(item, "pytestmark"):
            markers = [mark.name for mark in item.pytestmark]
            if "integration" in markers:
                log_server_logs_on_failure(test_name)
        else:
            # For tests without explicit markers, check if it's likely an integration test
            # by looking at the test name or if it involves network operations
            if (
                "integration" in test_name.lower()
                or "encrypt" in test_name.lower()
                or "decrypt" in test_name.lower()
                or "cli" in test_name.lower()
            ):
                log_server_logs_on_failure(test_name)


@pytest.fixture
def collect_server_logs():
    """Fixture that provides a function to manually collect server logs.

    Usage:
        def test_something(collect_server_logs):
            # ... test code ...
            if some_condition:
                logs = collect_server_logs()
                print(logs)
    """
    from tests.server_logs import collect_server_logs

    return collect_server_logs
