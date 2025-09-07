import secrets

import pytest

from otdf_python.config import NanoTDFConfig
from otdf_python.nanotdf import InvalidNanoTDFConfig, NanoTDF, NanoTDFMaxSizeLimit


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


@pytest.mark.skip(
    "This test is skipped because NanoTDF encryption/decryption is not implemented yet."
)
@pytest.mark.integration
def test_nanotdf_integration_encrypt_decrypt():
    # Load environment variables for integration
    from otdf_python.config import KASInfo
    from tests.config_pydantic import CONFIG_TDF

    # Create KAS info from configuration
    kas_info = KASInfo(url=CONFIG_TDF.KAS_ENDPOINT)

    # Create KAS client with SSL verification disabled for testing
    # from otdf_python.kas_client import KASClient
    # client = KASClient(
    #     kas_url=CONFIG_TDF.KAS_ENDPOINT,
    #     verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
    #     use_plaintext=bool(CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://")),
    # )

    nanotdf = NanoTDF()
    data = b"test data"
    config = NanoTDFConfig(kas_info_list=[kas_info])
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
