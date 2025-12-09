"""Test CLI functionality"""

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


def test_cli_help(project_root):
    """Test that CLI help command works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result.returncode == 0
    assert "OpenTDF CLI" in result.stdout
    assert "encrypt" in result.stdout
    assert "decrypt" in result.stdout
    assert "inspect" in result.stdout


def test_cli_version(project_root):
    """Test that CLI version command works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "--version"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result.returncode == 0
    assert "OpenTDF Python SDK" in result.stdout

    with (Path(__file__).parent.parent / "pyproject.toml").open("rb") as f:
        # Use tomli for Python < 3.11, tomllib for 3.11+
        if sys.version_info < (3, 11):
            import tomli

            pyproject = tomli.load(f)
        else:
            import tomllib

            pyproject = tomllib.load(f)
        expected_version = pyproject["project"]["version"]

    assert (
        expected_version in result.stdout or "0.0.0" in result.stdout
    )  # allow for dev version


def test_cli_encrypt_help(project_root):
    """Test that CLI encrypt help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "encrypt", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result.returncode == 0
    assert "Path to file to encrypt" in result.stdout
    assert "--attributes" in result.stdout
    assert "--container-type" in result.stdout


def test_cli_decrypt_help(project_root):
    """Test that CLI decrypt help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "decrypt", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result.returncode == 0
    assert "Path to encrypted file" in result.stdout
    assert "--output" in result.stdout


def test_cli_inspect_help(project_root):
    """Test that CLI inspect help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "inspect", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result.returncode == 0
    assert "Path to encrypted file" in result.stdout


def test_cli_encrypt_missing_auth(project_root):
    """Test that CLI encrypt fails gracefully without authentication"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, "-m", "otdf_python", "encrypt", temp_file],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 1
        assert "Authentication required" in result.stderr
        assert "--with-client-creds-file" in result.stderr
    finally:
        Path(temp_file).unlink()


def test_cli_encrypt_missing_creds_file(project_root):
    """Test that CLI encrypt fails gracefully with missing credentials file"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "otdf_python",
                "--with-client-creds-file",
                "nonexistent.json",
                "encrypt",
                temp_file,
            ],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 1
        assert "Credentials file does not exist" in result.stderr
    finally:
        Path(temp_file).unlink()


def test_cli_encrypt_invalid_creds_file(project_root):
    """Test that CLI encrypt fails gracefully with invalid credentials file"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as creds_f:
        creds_f.write('{"invalid": "format"}')
        creds_file = creds_f.name

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "otdf_python",
                "--with-client-creds-file",
                creds_file,
                "encrypt",
                temp_file,
            ],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 1
        assert "must contain 'clientId' and 'clientSecret' fields" in result.stderr
    finally:
        Path(temp_file).unlink()
        Path(creds_file).unlink()


def test_cli_decrypt_missing_file(project_root):
    """Test that CLI decrypt fails gracefully with missing file"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "decrypt", "nonexistent.tdf"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result.returncode == 1
    assert "File does not exist" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__])
