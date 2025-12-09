"""Tests for NanoTDFECDSAStruct."""

import pytest

from otdf_python.nanotdf_ecdsa_struct import (
    IncorrectNanoTDFECDSASignatureSize,
    NanoTDFECDSAStruct,
)


def test_from_bytes():
    """Test creating a NanoTDFECDSAStruct from bytes."""
    # Create a simple test signature (r_length=1, r_value=0x01, s_length=1, s_value=0x02)
    key_size = 1
    signature = bytes([1, 1, 1, 2])  # r_length, r_value, s_length, s_value

    # Create the struct
    struct = NanoTDFECDSAStruct.from_bytes(signature, key_size)

    # Check values
    assert struct.get_r_length() == 1
    assert struct.get_r_value()[0] == 1
    assert struct.get_s_length() == 1
    assert struct.get_s_value()[0] == 2


def test_from_bytes_incorrect_size():
    """Test creating a NanoTDFECDSAStruct with incorrect signature size."""
    # Create an invalid signature (too short)
    key_size = 2
    signature = bytes([1, 1, 1, 2])  # Should be 6 bytes for key_size=2

    # Should raise an exception
    with pytest.raises(IncorrectNanoTDFECDSASignatureSize):
        NanoTDFECDSAStruct.from_bytes(signature, key_size)


def test_as_bytes():
    """Test converting a NanoTDFECDSAStruct to bytes."""
    # Create a struct
    struct = NanoTDFECDSAStruct()
    struct.set_r_length(1)
    struct.set_r_value(bytearray([1]))
    struct.set_s_length(1)
    struct.set_s_value(bytearray([2]))

    # Convert to bytes
    signature = struct.as_bytes()

    # Check values
    assert len(signature) == 4
    assert signature == bytes([1, 1, 1, 2])


def test_as_bytes_missing_values():
    """Test that an exception is raised when r_value or s_value is not set."""
    # Create an incomplete struct
    struct = NanoTDFECDSAStruct()
    struct.set_r_length(1)
    # Missing r_value
    struct.set_s_length(1)
    struct.set_s_value(bytearray([2]))

    # Should raise an exception
    with pytest.raises(ValueError):
        struct.as_bytes()


def test_getters_setters():
    """Test all getters and setters."""
    struct = NanoTDFECDSAStruct()

    # Test r_length
    struct.set_r_length(5)
    assert struct.get_r_length() == 5

    # Test r_value
    r_value = bytearray([1, 2, 3])
    struct.set_r_value(r_value)
    assert struct.get_r_value() == r_value

    # Test s_length
    struct.set_s_length(3)
    assert struct.get_s_length() == 3

    # Test s_value
    s_value = bytearray([4, 5, 6])
    struct.set_s_value(s_value)
    assert struct.get_s_value() == s_value
