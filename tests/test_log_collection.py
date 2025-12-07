#!/usr/bin/env python3
"""Test script to verify server log collection functionality.

This script tests the server log collection without running full pytest.
"""

from tests.config_pydantic import CONFIG_TESTING
from tests.server_logs import collect_server_logs, log_server_logs_on_failure


def test_log_collection():
    """Test that we can collect server logs."""
    print("Testing server log collection...")

    # Test with a command that should work (basic SSH test)
    print("\n1. Testing SSH connectivity...")
    logs = collect_server_logs(
        pod_name=CONFIG_TESTING.POD_NAME,
        namespace=CONFIG_TESTING.NAMESPACE,
        ssh_target=CONFIG_TESTING.SSH_TARGET,
        lines=CONFIG_TESTING.LOG_LINES,
    )

    if logs:
        print("✓ Successfully collected logs")
        print(f"Log preview (first 200 chars): {logs[:200]}...")
    else:
        print("✗ Failed to collect logs")

    # Test the failure logging function
    print("\n2. Testing failure log collection...")
    log_server_logs_on_failure("test_function_name")

    print("\nTest completed!")


if __name__ == "__main__":
    test_log_collection()
