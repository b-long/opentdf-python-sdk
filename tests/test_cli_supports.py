"""Unit tests for the CLI `supports` subcommand (community xtest contract)."""

import subprocess
import sys
from types import SimpleNamespace

from otdf_python.cli import cmd_supports


def test_cmd_supports_returns_codes_in_process():
    """cmd_supports returns exit codes without calling sys.exit (review feedback)."""
    assert cmd_supports(SimpleNamespace(feature="autoconfigure")) == 0
    assert cmd_supports(SimpleNamespace(feature="ecwrap")) == 1
    assert cmd_supports(SimpleNamespace(feature="not-a-real-feature")) == 2


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
