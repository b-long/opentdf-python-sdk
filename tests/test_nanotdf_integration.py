import io

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from otdf_python.config import KASInfo, NanoTDFConfig
from otdf_python.nanotdf import NanoTDF


@pytest.mark.integration
def test_nanotdf_kas_roundtrip():
    # Generate RSA keypair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    public_pem = (
        private_key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode()
    )
    # Prepare NanoTDF
    nanotdf = NanoTDF()
    payload = b"nano test payload"
    # Create KASInfo with public key
    kas_info = KASInfo(url="https://mock-kas", public_key=public_pem)
    # Configure NanoTDFConfig for encryption
    config = NanoTDFConfig(kas_info_list=[kas_info])
    out = io.BytesIO()
    nanotdf.create_nano_tdf(payload, out, config)
    nanotdf_bytes = out.getvalue()
    # Read/decrypt NanoTDF with private key
    config_read = NanoTDFConfig(cipher=private_pem, config="mock_unwrap=true")
    out_dec = io.BytesIO()
    nanotdf.read_nano_tdf(nanotdf_bytes, out_dec, config_read)
    assert out_dec.getvalue() == payload
