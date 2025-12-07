"""Tests for TDF."""

import io
import json
import zipfile

import pytest

from otdf_python.config import KASInfo, TDFConfig
from otdf_python.manifest import Manifest
from otdf_python.tdf import TDF, TDFReaderConfig
from tests.mock_crypto import generate_rsa_keypair


def test_tdf_create_and_load():
    """Test TDF creation and loading roundtrip."""
    tdf = TDF()
    payload = b"test payload"
    kas_private_key, kas_public_key = generate_rsa_keypair()
    kas_info = KASInfo(
        url="https://kas.example.com", public_key=kas_public_key, kid="test-kid"
    )

    config = TDFConfig(kas_info_list=[kas_info], tdf_private_key=kas_private_key)
    manifest, size, out = tdf.create_tdf(payload, config)
    assert isinstance(manifest, Manifest)
    assert size > 0
    data = out.getvalue() if hasattr(out, "getvalue") else out.read()
    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        files = z.namelist()
        assert "0.manifest.json" in files
        assert "0.payload" in files
        manifest_json = json.loads(z.read("0.manifest.json").decode())
        assert manifest_json["schemaVersion"] == TDF.TDF_VERSION
        encrypted_payload = z.read("0.payload")
        assert encrypted_payload != payload  # Should be encrypted
        assert len(encrypted_payload) > 0
    # Test round-trip decryption
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key)
    decrypted = tdf.load_tdf(data, reader_config)
    assert decrypted.payload == payload


@pytest.mark.integration
def test_tdf_multi_kas_roundtrip():
    """Test TDF with multiple KAS roundtrip."""
    tdf = TDF()
    payload = b"multi-kas test payload"
    # Generate two KAS keypairs
    priv1, pub1 = generate_rsa_keypair()
    priv2, pub2 = generate_rsa_keypair()
    kas1 = KASInfo(url="https://kas1.example.com", public_key=pub1, kid="kas1")
    kas2 = KASInfo(url="https://kas2.example.com", public_key=pub2, kid="kas2")

    config = TDFConfig(kas_info_list=[kas1, kas2])
    _manifest, _size, out = tdf.create_tdf(payload, config)
    data = out.getvalue() if hasattr(out, "getvalue") else out.read()
    # Should be able to decrypt with either KAS private key
    for priv in (priv1, priv2):
        reader_config = TDFReaderConfig(kas_private_key=priv)
        dec = tdf.load_tdf(data, reader_config)
        assert dec.payload == payload
