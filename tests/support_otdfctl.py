import subprocess
import pytest


@pytest.mark.integration
@pytest.fixture(scope="session", autouse=True)
def check_for_otdfctl():
    """
    Ensure that the otdfctl command is available on the system.

    This fixture runs once per test session (for integration tests) and raises
    an exception if the otdfctl command is not found.
    """

    # TODO Consider setting GRPC_ENFORCE_ALPN_ENABLED to false as needed
    # test_env = os.environ.copy()
    # test_env["GRPC_ENFORCE_ALPN_ENABLED"] = "false"

    # Check if otdfctl is available
    try:
        subprocess.run(
            ["otdfctl", "--version"],
            capture_output=True,
            check=True,
            # env=test_env
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception(
            "otdfctl command not found on system. Please install otdfctl to run this test."
        )
