import unittest

from cryptography.hazmat.primitives.asymmetric import ec

from otdf_python.crypto_utils import CryptoUtils


class TestCryptoUtils(unittest.TestCase):
    def test_hmac(self):
        key = b"key"
        data = b"data"
        h = CryptoUtils.calculate_sha256_hmac(key, data)
        self.assertEqual(len(h), 32)

    def test_rsa_keypair(self):
        priv, pub = CryptoUtils.generate_rsa_keypair()
        pub_pem = CryptoUtils.get_rsa_public_key_pem(pub)
        priv_pem = CryptoUtils.get_rsa_private_key_pem(priv)
        self.assertIn("BEGIN PUBLIC KEY", pub_pem)
        self.assertIn("BEGIN PRIVATE KEY", priv_pem)

    def test_ec_keypair(self):
        priv, pub = CryptoUtils.generate_ec_keypair(ec.SECP384R1())
        pub_pem = CryptoUtils.get_public_key_pem(pub)
        priv_pem = CryptoUtils.get_private_key_pem(priv)
        self.assertIn("BEGIN PUBLIC KEY", pub_pem)
        self.assertIn("BEGIN PRIVATE KEY", priv_pem)

    def test_rsa_key_type_check(self):
        _priv, _pub = CryptoUtils.generate_rsa_keypair()
        with self.assertRaises(ValueError):
            CryptoUtils.get_rsa_public_key_pem("notakey")
        with self.assertRaises(ValueError):
            CryptoUtils.get_rsa_private_key_pem("notakey")


if __name__ == "__main__":
    unittest.main()
