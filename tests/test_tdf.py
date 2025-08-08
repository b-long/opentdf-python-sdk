from otdf_python.tdf import TDF, TDFReaderConfig
from otdf_python.config import TDFConfig, KASInfo
from otdf_python.manifest import Manifest
import io
import zipfile
import json
import pytest

from tests.mock_crypto import generate_rsa_keypair


def test_tdf_create_and_load():
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
    tdf = TDF()
    payload = b"multi-kas test payload"
    # Generate two KAS keypairs
    priv1, pub1 = generate_rsa_keypair()
    priv2, pub2 = generate_rsa_keypair()
    kas1 = KASInfo(url="https://kas1.example.com", public_key=pub1, kid="kas1")
    kas2 = KASInfo(url="https://kas2.example.com", public_key=pub2, kid="kas2")

    config = TDFConfig(kas_info_list=[kas1, kas2])
    manifest, size, out = tdf.create_tdf(payload, config)
    data = out.getvalue() if hasattr(out, "getvalue") else out.read()
    # Should be able to decrypt with either KAS private key
    for priv in (priv1, priv2):
        reader_config = TDFReaderConfig(kas_private_key=priv)
        dec = tdf.load_tdf(data, reader_config)
        assert dec.payload == payload


def test_tdf_abac_policy_enforcement():
    tdf = TDF()
    payload = b"abac test payload"
    kas_private_key, kas_public_key = generate_rsa_keypair()
    kas_info = KASInfo(
        url="https://kas.example.com", public_key=kas_public_key, kid="test-kid"
    )
    # Policy: require attribute 'foo'
    from otdf_python.policy_object import AttributeObject, PolicyBody, PolicyObject
    import uuid

    attr = AttributeObject(attribute="foo")
    body = PolicyBody(data_attributes=[attr], dissem=[])
    policy = PolicyObject(uuid=str(uuid.uuid4()), body=body)
    config = TDFConfig(
        kas_info_list=[kas_info], tdf_private_key=kas_private_key, policy_object=policy
    )
    manifest, size, out = tdf.create_tdf(payload, config)
    data = out.getvalue() if hasattr(out, "getvalue") else out.read()
    import pytest

    # Should fail if no attributes provided
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key)
    with pytest.raises(
        ValueError, match="ABAC policy enforcement: user attributes required"
    ):
        tdf.load_tdf(data, reader_config)
    # Should fail if wrong attribute provided
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key, attributes=["bar"])
    with pytest.raises(ValueError, match="missing required attributes"):
        tdf.load_tdf(data, reader_config)
    # Should succeed if required attribute provided
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key, attributes=["foo"])
    dec = tdf.load_tdf(data, reader_config)
    assert dec.payload == payload
