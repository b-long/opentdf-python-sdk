import subprocess


def check_for_otdfctl():
    # TODO Consider setting GRPC_ENFORCE_ALPN_ENABLED to false if issues arise
    # original_env = os.environ.copy()
    # original_env["GRPC_ENFORCE_ALPN_ENABLED"] = "false"

    # Check if otdfctl is available
    try:
        subprocess.run(
            ["otdfctl", "--version"],
            capture_output=True,
            check=True,
            # env=original_env
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception(
            "otdfctl command not found on system. Please install otdfctl to run this test."
        )
