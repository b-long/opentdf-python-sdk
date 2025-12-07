"""Tests for the integration between SDK and TDF classes."""

import io

from otdf_python.sdk_builder import SDKBuilder
from tests.config_pydantic import CONFIG_TDF
from tests.mock_crypto import generate_rsa_keypair


def test_sdk_create_tdf_with_builder():
    """Test that SDK.create_tdf works with TDFConfig created from new_tdf_config."""
    from otdf_python.kas_info import KASInfo

    # Generate key pair for testing
    _kas_private_key, kas_public_key = generate_rsa_keypair()

    # Create SDK with builder
    sdk = SDKBuilder().set_platform_endpoint("https://example.kas.com").build()

    # Create KASInfo with public key
    kas_info = KASInfo(
        url="https://example.kas.com", public_key=kas_public_key, kid="test-kid"
    )

    # Use the SDK to create a TDFConfig with the KASInfo
    config = sdk.new_tdf_config(
        attributes=[
            CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1,
            CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_2,
        ],
        kas_info_list=[kas_info],
    )
    # Use BytesIO to mimic file-like API
    payload = b"Hello from test"
    output = io.BytesIO()

    # This should not raise an AttributeError or ValueError
    _manifest, size, out_stream = sdk.create_tdf(payload, config, output_stream=output)

    # Basic validations
    assert size > 0
    assert out_stream.getvalue() == output.getvalue()
    assert len(output.getvalue()) > 0


def test_validate_otdf_python_script():
    """Test that simulates the validate_otdf_python.py script's usage patterns."""
    from otdf_python.kas_info import KASInfo

    # Generate key pair for testing
    _kas_private_key, kas_public_key = generate_rsa_keypair()

    # Create SDK with builder
    sdk = SDKBuilder().set_platform_endpoint("https://default.kas.example.com").build()

    # Create KASInfo with public key
    kas_info = KASInfo(
        url="https://default.kas.example.com", public_key=kas_public_key, kid="test-kid"
    )

    # Use the SDK to create a TDFConfig with the KASInfo
    config = sdk.new_tdf_config(
        attributes=[
            CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1,
            CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_2,
        ],
        kas_info_list=[kas_info],
    )

    # Use BytesIO to mimic file-like API
    payload = b"Hello from Python"
    output = io.BytesIO()

    # This should not raise an AttributeError or ValueError
    _manifest, size, out_stream = sdk.create_tdf(payload, config, output_stream=output)

    # Basic validations
    assert size > 0
    assert out_stream.getvalue() == output.getvalue()
    assert len(output.getvalue()) > 0


def test_new_tdf_config_with_https_platform():
    """Test that new_tdf_config correctly handles HTTPS platform URLs."""
    # Create SDK with HTTPS platform
    sdk = (
        SDKBuilder()
        .set_platform_endpoint("https://secure.platform.example.com")
        .build()
    )

    # Create config without overriding kas_info_list
    config = sdk.new_tdf_config(attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1])

    # Verify the default KAS info was created with HTTPS URL
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]
    assert kas_info.url == "https://secure.platform.example.com:443/kas"
    assert kas_info.default is True


def test_new_tdf_config_with_http_platform_using_plaintext():
    """Test that new_tdf_config correctly handles HTTP platform URLs when using plaintext."""
    # Create SDK with HTTP platform and plaintext enabled
    sdk = (
        SDKBuilder()
        .set_platform_endpoint("http://localhost:8080")
        .use_insecure_plaintext_connection(True)
        .build()
    )

    # Create config without overriding kas_info_list
    config = sdk.new_tdf_config(attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1])

    # Verify the default KAS info was created with HTTP URL
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]
    assert kas_info.url == "http://localhost:8080/kas"
    assert kas_info.default is True


def test_new_tdf_config_with_custom_port_https():
    """Test that new_tdf_config correctly handles HTTPS URLs with custom ports."""
    # Create SDK with HTTPS platform with custom port
    sdk = (
        SDKBuilder().set_platform_endpoint("https://platform.example.com:9443").build()
    )

    # Create config without overriding kas_info_list
    config = sdk.new_tdf_config(attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1])

    # Verify the default KAS info preserves the custom port
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]
    assert kas_info.url == "https://platform.example.com:9443/kas"
    assert kas_info.default is True


def test_new_tdf_config_with_custom_port_http():
    """Test that new_tdf_config correctly handles HTTP URLs with custom ports."""
    # Create SDK with HTTP platform with custom port and plaintext enabled
    sdk = (
        SDKBuilder()
        .set_platform_endpoint("http://localhost:9080")
        .use_insecure_plaintext_connection(True)
        .build()
    )

    # Create config without overriding kas_info_list
    config = sdk.new_tdf_config(attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1])

    # Verify the default KAS info preserves the custom port
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]
    assert kas_info.url == "http://localhost:9080/kas"
    assert kas_info.default is True


def test_new_tdf_config_with_path_preservation():
    """Test that new_tdf_config correctly preserves paths in platform URLs."""
    # Create SDK with platform URL that has a path
    sdk = (
        SDKBuilder().set_platform_endpoint("https://api.example.com/v1/opentdf").build()
    )

    # Create config without overriding kas_info_list
    config = sdk.new_tdf_config(attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1])

    # Verify the default KAS info preserves the path
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]
    assert kas_info.url == "https://api.example.com:443/v1/opentdf/kas"
    assert kas_info.default is True


def test_new_tdf_config_use_plaintext_parameter_validation():
    """Test that use_plaintext parameter in new_tdf_config works correctly."""
    # Test with HTTPS platform but override to use plaintext
    sdk = SDKBuilder().set_platform_endpoint("https://platform.example.com").build()

    # Create config with use_plaintext parameter
    config = sdk.new_tdf_config(
        attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1], use_plaintext=True
    )

    # Verify the config was created successfully
    assert config is not None
    # The use_plaintext parameter should affect KAS URL construction, converting to HTTP
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]

    # With use_plaintext=True, the KAS URL should use HTTP scheme and port 80
    assert kas_info.url.startswith("http://"), f"Expected HTTP URL, got: {kas_info.url}"
    assert "80" in kas_info.url, f"Expected port 80 for HTTP, got: {kas_info.url}"
    assert "/kas" in kas_info.url, f"Expected /kas path, got: {kas_info.url}"


def test_new_tdf_config_kas_info_list_override():
    """Test that kas_info_list parameter overrides default KAS info creation."""
    from otdf_python.kas_info import KASInfo

    # Create SDK
    sdk = SDKBuilder().set_platform_endpoint("https://platform.example.com").build()

    # Create custom KAS info
    custom_kas = KASInfo(
        url="https://custom.kas.example.com/kas",
        public_key="custom-key",
        kid="custom-kid",
        default=False,
    )

    # Create config with custom kas_info_list
    config = sdk.new_tdf_config(
        attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1], kas_info_list=[custom_kas]
    )

    # Verify the custom KAS info was used instead of default
    assert len(config.kas_info_list) == 1
    kas_info = config.kas_info_list[0]
    assert kas_info.url == "https://custom.kas.example.com/kas"
    assert kas_info.public_key == "custom-key"
    assert kas_info.kid == "custom-kid"
    assert kas_info.default is False


def test_new_tdf_config_empty_attributes():
    """Test that new_tdf_config handles empty or None attributes correctly."""
    # Create SDK
    sdk = SDKBuilder().set_platform_endpoint("https://platform.example.com").build()

    # Test with None attributes
    config1 = sdk.new_tdf_config(attributes=None)
    assert config1.attributes == []

    # Test with empty attributes list
    config2 = sdk.new_tdf_config(attributes=[])
    assert config2.attributes == []

    # Test with no attributes parameter
    config3 = sdk.new_tdf_config()
    assert config3.attributes == []


def test_new_tdf_config_kwargs_passthrough():
    """Test that additional kwargs are passed through to TDFConfig."""
    # Create SDK
    sdk = SDKBuilder().set_platform_endpoint("https://platform.example.com").build()

    # Create config with additional kwargs that should be passed to TDFConfig
    config = sdk.new_tdf_config(
        attributes=[CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1],
        default_segment_size=1024 * 1024,
        mime_type="application/json",
        render_version_info_in_manifest=False,
    )

    # Verify kwargs were passed through
    assert config.default_segment_size == 1024 * 1024
    assert config.mime_type == "application/json"
    assert config.render_version_info_in_manifest is False
