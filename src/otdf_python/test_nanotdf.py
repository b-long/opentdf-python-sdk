import os
import pytest
import secrets
from otdf_python.nanotdf import NanoTDF, NanoTDFMaxSizeLimit, InvalidNanoTDFConfig
from otdf_python.config import NanoTDFConfig

# Unit tests

def test_nanotdf_roundtrip():
    nanotdf = NanoTDF()
    key = secrets.token_bytes(32)
    data = b"nano tdf test payload"
    # Create config with key in cipher field
    config = NanoTDFConfig(cipher=key.hex())
    nanotdf_bytes = nanotdf.create_nanotdf(data, config)
    out = nanotdf.read_nanotdf(nanotdf_bytes, config)
    assert out == data

def test_nanotdf_too_large():
    nanotdf = NanoTDF()
    key = secrets.token_bytes(32)
    data = b"x" * (NanoTDF.K_MAX_TDF_SIZE + 1)
    config = NanoTDFConfig(cipher=key.hex())
    with pytest.raises(NanoTDFMaxSizeLimit):
        nanotdf.create_nanotdf(data, config)

def test_nanotdf_invalid_magic():
    nanotdf = NanoTDF()
    key = secrets.token_bytes(32)
    config = NanoTDFConfig(cipher=key.hex())
    bad_bytes = b"BAD" + b"rest"
    with pytest.raises(InvalidNanoTDFConfig):
        nanotdf.read_nanotdf(bad_bytes, config)

# Existing integration test
@pytest.mark.integration
@pytest.mark.skipif(not os.path.exists(".env.integration"), reason="Integration .env file not found")
def test_nanotdf_integration_encrypt_decrypt():
    # Load environment variables for integration
    from dotenv import load_dotenv
    load_dotenv(".env.integration")
    # Example: get KAS_URL or other config from env
    kas_url = os.getenv("KAS_URL")
    assert kas_url, "KAS_URL must be set in .env.integration"

    nanotdf = NanoTDF()
    data = b"test data"
    config = NanoTDFConfig(kas_info_list=[{"url": kas_url}])
    # These will raise NotImplementedError until implemented
    try:
        nanotdf_bytes = nanotdf.create_nanotdf(data, config)
    except NotImplementedError:
        pytest.skip("NanoTDF encryption not implemented yet.")
    try:
        decrypted = nanotdf.read_nanotdf(nanotdf_bytes, config)
    except NotImplementedError:
        pytest.skip("NanoTDF decryption not implemented yet.")
    assert decrypted == data
