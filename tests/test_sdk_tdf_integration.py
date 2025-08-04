"""
Tests for the integration between SDK and TDF classes.
"""

import io

from otdf_python.sdk_builder import SDKBuilder
from tests.mock_crypto import generate_rsa_keypair


def test_sdk_create_tdf_with_builder():
    """Test that SDK.create_tdf works with TDFConfig created from new_tdf_config."""
    from otdf_python.kas_info import KASInfo

    # Generate key pair for testing
    kas_private_key, kas_public_key = generate_rsa_keypair()

    # Create SDK with builder
    sdk = SDKBuilder().set_platform_endpoint("https://example.kas.com").build()

    # Create KASInfo with public key
    kas_info = KASInfo(
        url="https://example.kas.com", public_key=kas_public_key, kid="test-kid"
    )

    # Use the SDK to create a TDFConfig with the KASInfo
    config = sdk.new_tdf_config(attributes=["attr1", "attr2"], kas_info_list=[kas_info])

    # Use BytesIO to mimic file-like API
    payload = b"Hello from test"
    output = io.BytesIO()

    # This should not raise an AttributeError or ValueError
    manifest, size, out_stream = sdk.create_tdf(payload, config, output_stream=output)

    # Basic validations
    assert size > 0
    assert out_stream.getvalue() == output.getvalue()
    assert len(output.getvalue()) > 0


def test_validate_otdf_python_script():
    """Test that simulates the validate_otdf_python.py script's usage patterns."""
    from otdf_python.kas_info import KASInfo

    # Generate key pair for testing
    kas_private_key, kas_public_key = generate_rsa_keypair()

    # Create SDK with builder
    sdk = SDKBuilder().set_platform_endpoint("https://default.kas.example.com").build()

    # Create KASInfo with public key
    kas_info = KASInfo(
        url="https://default.kas.example.com", public_key=kas_public_key, kid="test-kid"
    )

    # Use the SDK to create a TDFConfig with the KASInfo
    config = sdk.new_tdf_config(attributes=["attr1", "attr2"], kas_info_list=[kas_info])

    # Use BytesIO to mimic file-like API
    payload = b"Hello from Python"
    output = io.BytesIO()

    # This should not raise an AttributeError or ValueError
    manifest, size, out_stream = sdk.create_tdf(payload, config, output_stream=output)

    # Basic validations
    assert size > 0
    assert out_stream.getvalue() == output.getvalue()
    assert len(output.getvalue()) > 0
