"""Tests for NanoTDF types."""

import unittest

from otdf_python.nanotdf_type import (
    Cipher,
    ECCurve,
    IdentifierType,
    PolicyType,
    Protocol,
)


class TestNanoTDFType(unittest.TestCase):
    """Tests for NanoTDF type enums."""

    def test_eccurve(self):
        """Test ECCurve enum values."""
        self.assertEqual(str(ECCurve.SECP256R1), "secp256r1")
        self.assertEqual(str(ECCurve.SECP384R1), "secp384r1")
        self.assertEqual(str(ECCurve.SECP521R1), "secp384r1")
        self.assertEqual(str(ECCurve.SECP256K1), "secp256k1")

    def test_protocol(self):
        """Test Protocol enum values."""
        self.assertEqual(Protocol.HTTP.value, "HTTP")
        self.assertEqual(Protocol.HTTPS.value, "HTTPS")

    def test_identifier_type(self):
        """Test IdentifierType enum values."""
        self.assertEqual(IdentifierType.NONE.get_length(), 0)
        self.assertEqual(IdentifierType.TWO_BYTES.get_length(), 2)
        self.assertEqual(IdentifierType.EIGHT_BYTES.get_length(), 8)
        self.assertEqual(IdentifierType.THIRTY_TWO_BYTES.get_length(), 32)

    def test_policy_type(self):
        """Test PolicyType enum values."""
        self.assertEqual(PolicyType.REMOTE_POLICY.value, 0)
        self.assertEqual(PolicyType.EMBEDDED_POLICY_PLAIN_TEXT.value, 1)
        self.assertEqual(PolicyType.EMBEDDED_POLICY_ENCRYPTED.value, 2)
        self.assertEqual(
            PolicyType.EMBEDDED_POLICY_ENCRYPTED_POLICY_KEY_ACCESS.value, 3
        )

    def test_cipher(self):
        """Test Cipher enum values."""
        self.assertEqual(Cipher.AES_256_GCM_64_TAG.value, 0)
        self.assertEqual(Cipher.AES_256_GCM_128_TAG.value, 5)
        self.assertEqual(Cipher.EAD_AES_256_HMAC_SHA_256.value, 6)


if __name__ == "__main__":
    unittest.main()
