"""Test to verify that the use_plaintext parameter flows correctly from SDKBuilder to KASClient."""

from unittest.mock import MagicMock, patch

from otdf_python.sdk_builder import SDKBuilder


def test_use_plaintext_flows_through_sdk_builder_to_kas_client():
    """Test that use_plaintext parameter flows from SDKBuilder through to KASClient."""
    with patch("otdf_python.kas_client.KASClient") as mock_kas_client:
        # Mock the KASClient constructor to capture the arguments
        mock_kas_instance = MagicMock()
        mock_kas_client.return_value = mock_kas_instance

        # Create SDK with plaintext connection enabled
        builder = (
            SDKBuilder.new_builder()
            .set_platform_endpoint("platform.example.com")
            .use_insecure_plaintext_connection(True)
        )

        sdk = builder.build()

        # Access the KAS service to trigger KASClient creation
        sdk.get_services().kas()

        # Verify that KASClient was called with use_plaintext=True
        mock_kas_client.assert_called_once()
        call_args = mock_kas_client.call_args

        # Check that use_plaintext was passed as True
        assert call_args.kwargs.get("use_plaintext") is True

        # Also verify the platform URL was set correctly for plaintext
        assert call_args.kwargs.get("kas_url") == "http://platform.example.com"


def test_use_plaintext_false_flows_through_sdk_builder_to_kas_client():
    """Test that use_plaintext=False flows from SDKBuilder through to KASClient."""
    with patch("otdf_python.kas_client.KASClient") as mock_kas_client:
        # Mock the KASClient constructor to capture the arguments
        mock_kas_instance = MagicMock()
        mock_kas_client.return_value = mock_kas_instance

        # Create SDK with plaintext connection disabled (default)
        builder = (
            SDKBuilder.new_builder()
            .set_platform_endpoint("platform.example.com")
            .use_insecure_plaintext_connection(False)
        )

        sdk = builder.build()

        # Access the KAS service to trigger KASClient creation
        sdk.get_services().kas()

        # Verify that KASClient was called with use_plaintext=False
        mock_kas_client.assert_called_once()
        call_args = mock_kas_client.call_args

        # Check that use_plaintext was passed as False
        assert call_args.kwargs.get("use_plaintext") is False

        # Also verify the platform URL was set correctly for HTTPS
        assert call_args.kwargs.get("kas_url") == "https://platform.example.com"


def test_use_plaintext_default_value():
    """Test that the default use_plaintext value is False."""
    with patch("otdf_python.kas_client.KASClient") as mock_kas_client:
        # Mock the KASClient constructor to capture the arguments
        mock_kas_instance = MagicMock()
        mock_kas_client.return_value = mock_kas_instance

        # Create SDK without explicitly setting plaintext connection
        builder = SDKBuilder.new_builder().set_platform_endpoint("platform.example.com")

        sdk = builder.build()

        # Access the KAS service to trigger KASClient creation
        sdk.get_services().kas()

        # Verify that KASClient was called with use_plaintext=False by default
        mock_kas_client.assert_called_once()
        call_args = mock_kas_client.call_args

        # Check that use_plaintext defaults to False
        assert call_args.kwargs.get("use_plaintext") is False

        # Also verify the platform URL defaults to HTTPS
        assert call_args.kwargs.get("kas_url") == "https://platform.example.com"


if __name__ == "__main__":
    test_use_plaintext_flows_through_sdk_builder_to_kas_client()
    test_use_plaintext_false_flows_through_sdk_builder_to_kas_client()
    test_use_plaintext_default_value()
    print("All tests passed!")
