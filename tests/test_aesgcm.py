import os
import unittest

from otdf_python.aesgcm import AesGcm


class TestAesGcm(unittest.TestCase):
    def test_encrypt_decrypt(self):
        key = os.urandom(32)
        aes = AesGcm(key)
        data = b"test data"
        encrypted = aes.encrypt(data)
        decrypted = aes.decrypt(encrypted)
        self.assertEqual(decrypted, data)

    def test_encrypt_decrypt_with_iv(self):
        key = os.urandom(32)
        aes = AesGcm(key)
        data = b"test data"
        iv = os.urandom(AesGcm.GCM_NONCE_LENGTH)
        ct = aes.encrypt_with_iv(iv, AesGcm.GCM_TAG_LENGTH, data)
        decrypted = aes.decrypt_with_iv(
            iv, AesGcm.GCM_TAG_LENGTH, ct[AesGcm.GCM_NONCE_LENGTH :]
        )
        self.assertEqual(decrypted, data)

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            AesGcm(b"")
        with self.assertRaises(ValueError):
            AesGcm(b"short")


if __name__ == "__main__":
    unittest.main()
