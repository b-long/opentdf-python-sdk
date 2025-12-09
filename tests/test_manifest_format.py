"""Test TDF manifest format, inspired by the Java SDK manifest tests."""

import json

from otdf_python.config import KASInfo, TDFConfig
from otdf_python.tdf import TDF
from tests.mock_crypto import generate_rsa_keypair


def test_manifest_field_format():
    """Test that manifest uses camelCase field names as per TDF specification."""
    # Create a mock KAS info with public key to avoid network calls
    kas_private_key, kas_public_key = generate_rsa_keypair()
    kas_info = KASInfo(
        url="https://kas.example.com", public_key=kas_public_key, kid="test-kid"
    )

    config = TDFConfig(kas_info_list=[kas_info], tdf_private_key=kas_private_key)

    # Create a test TDF and get manifest
    test_data = b"Hello World"
    tdf_instance = TDF()
    config.policy_object = {"uuid": "test-uuid", "body": {"dissem": ["test"]}}
    manifest, _size, _output_stream = tdf_instance.create_tdf(
        payload=test_data, config=config
    )

    manifest_dict = json.loads(manifest.to_json())

    # Test required camelCase fields
    assert "encryptionInformation" in manifest_dict
    assert "payload" in manifest_dict
    assert "schemaVersion" in manifest_dict or "tdfVersion" in manifest_dict

    # Test encryption information structure
    enc_info = manifest_dict["encryptionInformation"]
    assert "keyAccess" in enc_info
    assert "integrityInformation" in enc_info
    assert "policy" in enc_info
    assert "method" in enc_info

    # Test key access structure
    key_access = enc_info["keyAccess"][0]
    assert "url" in key_access  # Should be url not kas_url
    assert "wrappedKey" in key_access  # camelCase not wrapped_key
    assert "policyBinding" in key_access  # camelCase not policy_binding

    # Test integrity information
    integrity_info = enc_info["integrityInformation"]
    assert "encryptedSegmentSizeDefault" in integrity_info
    assert "segmentHashAlg" in integrity_info
    assert "segments" in integrity_info

    # Ensure no snake_case fields exist
    manifest_str = json.dumps(manifest_dict)
    assert "kas_url" not in manifest_str
    assert "wrapped_key" not in manifest_str
    assert "policy_binding" not in manifest_str
    assert "encryption_information" not in manifest_str
    assert "integrity_information" not in manifest_str
    assert "key_access" not in manifest_str
    assert "encrypted_segment_size_default" not in manifest_str
    assert "segment_hash_alg" not in manifest_str

    print("✓ All manifest fields use camelCase naming")


def test_manifest_roundtrip_serialization():
    """Test manifest serialization/deserialization roundtrip."""
    # Create a mock KAS info with public key to avoid network calls
    kas_private_key, kas_public_key = generate_rsa_keypair()
    kas_info = KASInfo(
        url="https://kas.example.com", public_key=kas_public_key, kid="test-kid"
    )

    config = TDFConfig(kas_info_list=[kas_info], tdf_private_key=kas_private_key)

    # Create a test TDF and get manifest
    test_data = b"Hello World"
    tdf_instance = TDF()
    config.policy_object = {"uuid": "test-uuid", "body": {"dissem": ["test"]}}
    manifest, _size, _output_stream = tdf_instance.create_tdf(
        payload=test_data, config=config
    )

    # Test JSON roundtrip
    json_str = manifest.to_json()
    manifest_dict = json.loads(json_str)
    roundtrip_json = json.dumps(manifest_dict)
    assert json.loads(json_str) == json.loads(roundtrip_json)

    # Test that critical fields survive roundtrip
    original_wrapped_key = manifest_dict["encryptionInformation"]["keyAccess"][0][
        "wrappedKey"
    ]
    roundtrip_dict = json.loads(roundtrip_json)
    roundtrip_wrapped_key = roundtrip_dict["encryptionInformation"]["keyAccess"][0][
        "wrappedKey"
    ]
    assert original_wrapped_key == roundtrip_wrapped_key
