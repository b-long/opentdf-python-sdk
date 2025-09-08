import unittest

from otdf_python.key_type import KeyType


class TestKeyType(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(KeyType.RSA2048Key), "rsa:2048")
        self.assertEqual(str(KeyType.EC256Key), "ec:secp256r1")

    def test_get_curve_name(self):
        self.assertEqual(KeyType.EC256Key.get_curve_name(), "secp256r1")
        self.assertEqual(KeyType.EC384Key.get_curve_name(), "secp384r1")
        self.assertEqual(KeyType.EC521Key.get_curve_name(), "secp521r1")
        with self.assertRaises(ValueError):
            KeyType.RSA2048Key.get_curve_name()

    def test_from_string(self):
        self.assertEqual(KeyType.from_string("rsa:2048"), KeyType.RSA2048Key)
        self.assertEqual(KeyType.from_string("ec:secp256r1"), KeyType.EC256Key)
        with self.assertRaises(ValueError):
            KeyType.from_string("notakey")

    def test_is_ec(self):
        self.assertTrue(KeyType.EC256Key.is_ec())
        self.assertFalse(KeyType.RSA2048Key.is_ec())


if __name__ == "__main__":
    unittest.main()
