"""Tests for TDF manifest."""

from otdf_python.manifest import (
    Manifest,
    ManifestAssertion,
    ManifestEncryptionInformation,
    ManifestIntegrityInformation,
    ManifestKeyAccess,
    ManifestMethod,
    ManifestPayload,
    ManifestRootSignature,
    ManifestSegment,
)


def test_manifest_serialization():
    # Create a minimal manifest
    seg = ManifestSegment(hash="abc", segmentSize=100, encryptedSegmentSize=120)
    root_sig = ManifestRootSignature(alg="alg", sig="sig")
    integrity = ManifestIntegrityInformation(
        rootSignature=root_sig,
        segmentHashAlg="sha256",
        segmentSizeDefault=100,
        encryptedSegmentSizeDefault=120,
        segments=[seg],
    )
    method = ManifestMethod(algorithm="AES", iv="iv123", isStreamable=True)
    key_access = ManifestKeyAccess(
        type="split",
        url="https://kas",
        protocol="kas",
        wrappedKey="key",
        policyBinding=None,
    )
    enc_info = ManifestEncryptionInformation(
        type="split",
        policy="cG9saWN5",  # base64 for 'policy'
        keyAccess=[key_access],
        method=method,
        integrityInformation=integrity,
    )
    payload = ManifestPayload(
        type="file",
        url="https://file",
        protocol="https",
        mimeType="text/plain",
        isEncrypted=True,
    )
    assertion = ManifestAssertion(
        id="id1", type="type1", scope="scope1", appliesTo_state="state1", statement={}
    )
    manifest = Manifest(
        schemaVersion="4.3.0",
        encryptionInformation=enc_info,
        payload=payload,
        assertions=[assertion],
    )
    js = manifest.to_json()
    loaded = Manifest.from_json(js)
    assert loaded.schemaVersion == manifest.schemaVersion
    assert isinstance(loaded.payload, ManifestPayload)
    assert isinstance(manifest.payload, ManifestPayload)
    assert loaded.payload.type == manifest.payload.type
    assert isinstance(loaded.encryptionInformation, ManifestEncryptionInformation)
    assert isinstance(manifest.encryptionInformation, ManifestEncryptionInformation)
    assert loaded.encryptionInformation.type == manifest.encryptionInformation.type
    assert loaded.assertions[0].id == manifest.assertions[0].id
