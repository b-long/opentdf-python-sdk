from otdf_python.tdf import TDF
from otdf_python.manifest import Manifest
import io
import zipfile
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from otdf_python.config import KASInfo
import pytest

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return private_pem, public_pem

def test_tdf_create_and_load():
    tdf = TDF()
    payload = b"test payload"
    kas_private_key, kas_public_key = generate_rsa_keypair()
    kas_info = KASInfo(url="https://kas.example.com", public_key=kas_public_key, kid="test-kid")
    from otdf_python.tdf import TDFConfig, TDFReaderConfig
    config = TDFConfig(kas_info=kas_info, kas_private_key=kas_private_key)
    manifest, size, out = tdf.create_tdf(payload, config)
    assert isinstance(manifest, Manifest)
    assert size > 0
    data = out.getvalue() if hasattr(out, 'getvalue') else out.read()
    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        files = z.namelist()
        assert "0.manifest.json" in files
        assert "0.payload" in files
        manifest_json = json.loads(z.read("0.manifest.json").decode())
        assert manifest_json["tdf_version"] == TDF.TDF_VERSION
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
    from otdf_python.tdf import TDFConfig, TDFReaderConfig
    config = TDFConfig(kas_info=[kas1, kas2])
    manifest, size, out = tdf.create_tdf(payload, config)
    data = out.getvalue() if hasattr(out, 'getvalue') else out.read()
    # Should be able to decrypt with either KAS private key
    for priv in (priv1, priv2):
        reader_config = TDFReaderConfig(kas_private_key=priv)
        dec = tdf.load_tdf(data, reader_config)
        assert dec.payload == payload

def test_tdf_abac_policy_enforcement():
    tdf = TDF()
    payload = b"abac test payload"
    kas_private_key, kas_public_key = generate_rsa_keypair()
    kas_info = KASInfo(url="https://kas.example.com", public_key=kas_public_key, kid="test-kid")
    # Policy: require attribute 'foo'
    from otdf_python.policy_object import AttributeObject, PolicyBody, PolicyObject
    from otdf_python.tdf import TDFConfig, TDFReaderConfig
    attr = AttributeObject(attribute="foo")
    body = PolicyBody(data_attributes=[attr], dissem=[])
    import uuid
    policy = PolicyObject(uuid=str(uuid.uuid4()), body=body)
    config = TDFConfig(kas_info=kas_info, kas_private_key=kas_private_key, policy_object=policy)
    manifest, size, out = tdf.create_tdf(payload, config)
    data = out.getvalue() if hasattr(out, 'getvalue') else out.read()
    import pytest
    # Should fail if no attributes provided
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key)
    with pytest.raises(ValueError, match="ABAC policy enforcement: user attributes required"):
        tdf.load_tdf(data, reader_config)
    # Should fail if wrong attribute provided
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key, attributes=["bar"])
    with pytest.raises(ValueError, match="missing required attributes"):
        tdf.load_tdf(data, reader_config)
    # Should succeed if required attribute provided
    reader_config = TDFReaderConfig(kas_private_key=kas_private_key, attributes=["foo"])
    dec = tdf.load_tdf(data, reader_config)
    assert dec.payload == payload
