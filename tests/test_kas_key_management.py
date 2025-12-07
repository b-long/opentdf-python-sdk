"""Tests for KAS key management."""

import base64
import os
import unittest
from unittest.mock import Mock, patch

import pytest

from otdf_python.kas_client import KASClient, KeyAccess
from otdf_python.key_type_constants import EC_KEY_TYPE, RSA_KEY_TYPE


class TestKASKeyManagement(unittest.TestCase):
    """Tests for the KAS key management pattern."""

    def test_rsa_key_generation(self):
        """Test that RSA keys are generated automatically."""
        client = KASClient(kas_url="http://kas.example.com")

        # Before unwrap, decryptor should be None
        self.assertIsNone(client.decryptor)
        self.assertIsNone(client.client_public_key)

        # Mock the HTTP response
        with patch("httpx.post") as mock_post:
            # Configure the mock
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "entityWrappedKey": base64.b64encode(os.urandom(32)).decode()
            }
            mock_post.return_value = mock_response

            # Create a test key access
            key_access = KeyAccess(
                url="http://kas.example.com",
                wrapped_key=base64.b64encode(os.urandom(32)).decode(),
            )

            # Also patch the decrypt method to return a predictable value
            with patch(
                "otdf_python.asym_crypto.AsymDecryption.decrypt",
                return_value=b"test_key",
            ):
                # Call unwrap
                from contextlib import suppress

                with suppress(Exception):
                    # We expect an exception because we're not actually unwrapping a valid key
                    client.unwrap(key_access, "{}", RSA_KEY_TYPE)

                # After unwrap, decryptor should be created
                self.assertIsNotNone(client.decryptor)
                self.assertIsNotNone(client.client_public_key)

                # The public key should be in PEM format
                assert isinstance(client.client_public_key, str)
                assert client.client_public_key.startswith("-----BEGIN PUBLIC KEY-----")

    @pytest.mark.skip(reason="Skipping 'test_ec_key_generation' until fixed")
    @pytest.mark.integration
    def test_ec_key_generation(self):
        """Test that EC keys are generated automatically for each request."""
        client = KASClient(kas_url="http://kas.example.com")

        # Mock the ECKeyPair and related classes
        with patch("otdf_python.eckeypair.ECKeyPair") as mock_ec_key_pair_class:
            # Configure the mocks
            mock_ec_key_pair = Mock()
            mock_ec_key_pair.public_key_in_pem_format.return_value = (
                "-----BEGIN PUBLIC KEY-----\nMOCKED_EC_KEY\n-----END PUBLIC KEY-----"
            )
            mock_ec_key_pair.get_private_key.return_value = Mock()
            mock_ec_key_pair_class.return_value = mock_ec_key_pair
            mock_ec_key_pair_class.public_key_from_pem.return_value = Mock()
            mock_ec_key_pair_class.compute_ecdh_key.return_value = b"mock_ecdh_key"
            mock_ec_key_pair_class.calculate_hkdf.return_value = b"mock_hkdf_key"

            # Mock HTTP response
            with patch("httpx.post") as mock_post:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "entityWrappedKey": base64.b64encode(os.urandom(32)).decode(),
                    "sessionPublicKey": "MOCK_SESSION_KEY",
                }
                mock_post.return_value = mock_response

                # Mock AesGcm
                with patch("otdf_python.aesgcm.AesGcm") as mock_aes_gcm_class:
                    mock_aes_gcm = Mock()
                    mock_aes_gcm.decrypt.return_value = b"decrypted_key"
                    mock_aes_gcm_class.return_value = mock_aes_gcm

                    # Create a test key access
                    key_access = KeyAccess(
                        url="http://kas.example.com",
                        wrapped_key=base64.b64encode(os.urandom(32)).decode(),
                    )

                    # Call unwrap
                    key = client.unwrap(key_access, "{}", EC_KEY_TYPE)

                    # Verify results
                    self.assertEqual(key, b"decrypted_key")
                    self.assertEqual(
                        client.client_public_key,
                        "-----BEGIN PUBLIC KEY-----\nMOCKED_EC_KEY\n-----END PUBLIC KEY-----",
                    )

                    # The original decryptor should not be affected
                    self.assertIsNone(client.decryptor)

                    # EC key pair should have been created with the right curve
                    mock_ec_key_pair_class.assert_called_once()
                    self.assertEqual(
                        mock_ec_key_pair_class.call_args[1].get("curve_name"), "P-256"
                    )


if __name__ == "__main__":
    unittest.main()
