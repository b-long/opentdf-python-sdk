from otdf_python.manifest import (
    Manifest, ManifestEncryptionInformation, ManifestPayload, ManifestAssertion,
    ManifestMethod, ManifestKeyAccess, ManifestIntegrityInformation, ManifestRootSignature, ManifestSegment
)

def test_manifest_serialization():
    # Create a minimal manifest
    seg = ManifestSegment(hash="abc", segment_size=100, encrypted_segment_size=120)
    root_sig = ManifestRootSignature(algorithm="alg", signature="sig")
    integrity = ManifestIntegrityInformation(
        root_signature=root_sig,
        segment_hash_alg="sha256",
        segment_size_default=100,
        encrypted_segment_size_default=120,
        segments=[seg],
    )
    method = ManifestMethod(algorithm="AES", iv="iv123", is_streamable=True)
    key_access = ManifestKeyAccess(
        key_type="split", url="https://kas", protocol="kas", wrapped_key="key", policy_binding=None
    )
    enc_info = ManifestEncryptionInformation(
        key_access_type="split",
        policy="cG9saWN5",  # base64 for 'policy'
        key_access_obj=[key_access],
        method=method,
        integrity_information=integrity,
    )
    payload = ManifestPayload(
        type="file", url="https://file", protocol="https", mime_type="text/plain", is_encrypted=True
    )
    assertion = ManifestAssertion(
        id="id1", type="type1", scope="scope1", applies_to_state="state1", statement={}
    )
    manifest = Manifest(
        tdf_version="4.3.0",
        encryption_information=enc_info,
        payload=payload,
        assertions=[assertion],
    )
    js = manifest.to_json()
    loaded = Manifest.from_json(js)
    assert loaded.tdf_version == manifest.tdf_version
    assert loaded.payload.type == manifest.payload.type
    assert loaded.encryption_information.key_access_type == manifest.encryption_information.key_access_type
    assert loaded.assertions[0].id == manifest.assertions[0].id
