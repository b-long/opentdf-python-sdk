"""Tests for NanoTDF."""

import secrets

import pytest

from otdf_python.config import NanoTDFConfig
from otdf_python.nanotdf import InvalidNanoTDFConfig, NanoTDF, NanoTDFMaxSizeLimit


def test_nanotdf_roundtrip():
    """Test NanoTDF encrypt and decrypt roundtrip."""
    nanotdf = NanoTDF()
    key = secrets.token_bytes(32)
    data = b"nano tdf test payload"
    # Create config with key in cipher field
    config = NanoTDFConfig(cipher=key.hex())
    nanotdf_bytes = nanotdf.create_nanotdf(data, config)
    out = nanotdf.read_nanotdf(nanotdf_bytes, config)
    assert out == data


def test_nanotdf_too_large():
    """Test NanoTDF with payload exceeding size limit."""
    nanotdf = NanoTDF()
    key = secrets.token_bytes(32)
    data = b"x" * (NanoTDF.K_MAX_TDF_SIZE + 1)
    config = NanoTDFConfig(cipher=key.hex())
    with pytest.raises(NanoTDFMaxSizeLimit):
        nanotdf.create_nanotdf(data, config)


def test_nanotdf_invalid_magic():
    """Test NanoTDF with invalid magic bytes."""
    nanotdf = NanoTDF()
    key = secrets.token_bytes(32)
    config = NanoTDFConfig(cipher=key.hex())
    bad_bytes = b"BAD" + b"rest"
    with pytest.raises(InvalidNanoTDFConfig):
        nanotdf.read_nanotdf(bad_bytes, config)


@pytest.mark.integration
def test_nanotdf_integration_encrypt_decrypt():
    """Test NanoTDF integration with KAS."""
    # Load environment variables for integration
    from otdf_python.config import KASInfo
    from tests.config_pydantic import CONFIG_TDF

    # Create KAS info from configuration
    kas_info = KASInfo(url=CONFIG_TDF.KAS_ENDPOINT)

    nanotdf = NanoTDF()
    data = b"test data"

    # Generate a key and include it in config for both encrypt and decrypt
    # Note: In a real scenario with KAS integration, the key would be wrapped
    # and unwrapped via KAS. For now, we're testing the basic encrypt/decrypt flow.
    key = secrets.token_bytes(32)
    config = NanoTDFConfig(kas_info_list=[kas_info], cipher=key.hex())

    # Create and read NanoTDF
    nanotdf_bytes = nanotdf.create_nanotdf(data, config)
    decrypted = nanotdf.read_nanotdf(nanotdf_bytes, config)
    assert decrypted == data
