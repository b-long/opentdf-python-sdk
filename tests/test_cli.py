"""
Test CLI functionality
"""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path


def test_cli_help():
    """Test that CLI help command works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "OpenTDF CLI" in result.stdout
    assert "encrypt" in result.stdout
    assert "decrypt" in result.stdout
    assert "inspect" in result.stdout


def test_cli_version():
    """Test that CLI version command works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "--version"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "OpenTDF Python SDK" in result.stdout
    assert "0.3.0a9" in result.stdout


def test_cli_encrypt_help():
    """Test that CLI encrypt help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "encrypt", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Path to file to encrypt" in result.stdout
    assert "--attributes" in result.stdout
    assert "--container-type" in result.stdout


def test_cli_decrypt_help():
    """Test that CLI decrypt help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "decrypt", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Path to encrypted file" in result.stdout
    assert "--output" in result.stdout


def test_cli_inspect_help():
    """Test that CLI inspect help works"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "inspect", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Path to encrypted file" in result.stdout


def test_cli_encrypt_missing_auth():
    """Test that CLI encrypt fails gracefully without authentication"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("test content")
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, "-m", "otdf_python", "encrypt", temp_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "Authentication required" in result.stderr
        assert "--with-client-creds-file" in result.stderr
    finally:
        os.unlink(temp_file)


def test_cli_encrypt_missing_creds_file():
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
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "Credentials file does not exist" in result.stderr
    finally:
        os.unlink(temp_file)


def test_cli_encrypt_invalid_creds_file():
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
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "must contain 'clientId' and 'clientSecret' fields" in result.stderr
    finally:
        os.unlink(temp_file)
        os.unlink(creds_file)


def test_cli_decrypt_missing_file():
    """Test that CLI decrypt fails gracefully with missing file"""
    result = subprocess.run(
        [sys.executable, "-m", "otdf_python", "decrypt", "nonexistent.tdf"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 1
    assert "File does not exist" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__])
