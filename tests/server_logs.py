"""
Server log collection utility for debugging test failures.
"""

import subprocess
import logging

from tests.config_pydantic import CONFIG_TESTING

logger = logging.getLogger(__name__)


def collect_server_logs(
    pod_name: str = CONFIG_TESTING.POD_NAME,
    namespace: str = CONFIG_TESTING.NAMESPACE,
    ssh_target: str = CONFIG_TESTING.SSH_TARGET,
    lines: int = CONFIG_TESTING.LOG_LINES,
) -> str | None:
    """
    Collect server logs from a Kubernetes pod via SSH.

    Args:
        pod_name: Name of the Kubernetes pod
        namespace: Kubernetes namespace
        ssh_target: SSH target (hostname/alias)
        lines: Number of log lines to retrieve

    Returns:
        Log output as string, or None if collection failed
    """
    cmd = ["ssh", ssh_target, f"kubectl logs -n {lines} {pod_name} -n {namespace}"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
        )

        if result.returncode == 0:
            return result.stdout
        else:
            logger.error(f"Failed to collect logs: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        logger.error("Timeout while collecting server logs")
        return None
    except Exception as e:
        logger.error(f"Error collecting server logs: {e}")
        return None


def log_server_logs_on_failure(
    test_name: str,
    pod_name: str = CONFIG_TESTING.POD_NAME,
    namespace: str = CONFIG_TESTING.NAMESPACE,
    ssh_target: str = CONFIG_TESTING.SSH_TARGET,
    lines: int = CONFIG_TESTING.LOG_LINES,
) -> None:
    """
    Collect and log server logs when a test fails.

    Args:
        test_name: Name of the failed test
        pod_name: Name of the Kubernetes pod
        namespace: Kubernetes namespace
        ssh_target: SSH target (hostname/alias)
        lines: Number of log lines to retrieve
    """
    print(f"\n{'=' * 60}")
    print(f"COLLECTING SERVER LOGS FOR FAILED TEST: {test_name}")
    print(f"{'=' * 60}")

    logs = collect_server_logs(pod_name, namespace, ssh_target, lines)

    if logs:
        print(f"\nServer logs (last {lines} lines):")
        print("-" * 40)
        print(logs)
        print("-" * 40)
    else:
        print("\nFailed to collect server logs")

    print(f"{'=' * 60}\n")
