import unittest

from otdf_python.eckeypair import ECKeyPair


class TestECKeyPair(unittest.TestCase):
    def test_keypair_generation_and_pem(self):
        kp = ECKeyPair()
        pub_pem = kp.public_key_pem()
        priv_pem = kp.private_key_pem()
        self.assertIn("BEGIN PUBLIC KEY", pub_pem)
        self.assertIn("BEGIN PRIVATE KEY", priv_pem)

    def test_ecdh_and_hkdf(self):
        kp1 = ECKeyPair()
        kp2 = ECKeyPair()
        shared1 = ECKeyPair.compute_ecdh_key(kp2.public_key, kp1.private_key)
        shared2 = ECKeyPair.compute_ecdh_key(kp1.public_key, kp2.private_key)
        self.assertEqual(shared1, shared2)
        salt = b"salt"
        key1 = ECKeyPair.calculate_hkdf(salt, shared1)
        key2 = ECKeyPair.calculate_hkdf(salt, shared2)
        self.assertEqual(key1, key2)

    def test_sign_and_verify(self):
        kp = ECKeyPair()
        data = b"test data"
        sig = ECKeyPair.sign_ecdsa(data, kp.private_key)
        self.assertTrue(ECKeyPair.verify_ecdsa(data, sig, kp.public_key))
        self.assertFalse(ECKeyPair.verify_ecdsa(b"bad data", sig, kp.public_key))


if __name__ == "__main__":
    unittest.main()
