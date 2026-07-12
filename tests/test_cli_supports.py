"""Unit tests for the CLI `supports` subcommand (community xtest contract)."""

import subprocess
import sys


def test_supports_autoconfigure_exit_0():
    r = subprocess.run(
        [sys.executable, "-m", "otdf_python", "supports", "autoconfigure"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr


def test_supports_ecwrap_exit_1():
    r = subprocess.run(
        [sys.executable, "-m", "otdf_python", "supports", "ecwrap"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 1, r.stderr


def test_supports_unknown_exit_2():
    r = subprocess.run(
        [sys.executable, "-m", "otdf_python", "supports", "not-a-real-feature"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 2
