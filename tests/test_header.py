import unittest

from otdf_python.ecc_mode import ECCMode
from otdf_python.header import Header
from otdf_python.policy_info import PolicyInfo
from otdf_python.resource_locator import ResourceLocator
from otdf_python.symmetric_and_payload_config import SymmetricAndPayloadConfig


class TestHeader(unittest.TestCase):
    def test_header_fields(self):
        header = Header()
        kas_locator = ResourceLocator("https://kas.example.com", "id1")
        ecc_mode = ECCMode(curve_mode=1, use_ecdsa_binding=True)
        payload_config = SymmetricAndPayloadConfig(
            cipher_type=2, signature_ecc_mode=1, has_signature=False
        )
        # PolicyInfo now only has policy_type and body (binding is separate in Header)
        policy_info = PolicyInfo(policy_type=1, body=b"body")
        # Binding is now a separate field in Header
        policy_binding = b"bind1234"  # GMAC is 8 bytes
        # Use correct ephemeral key length for curve_mode=1 (secp384r1): 49 bytes
        ephemeral_key = b"e" * 49

        header.set_kas_locator(kas_locator)
        header.set_ecc_mode(ecc_mode)
        header.set_payload_config(payload_config)
        header.set_policy_info(policy_info)
        header.policy_binding = policy_binding
        header.set_ephemeral_key(ephemeral_key)

        self.assertEqual(header.get_kas_locator(), kas_locator)
        self.assertEqual(header.get_ecc_mode(), ecc_mode)
        self.assertEqual(header.get_payload_config(), payload_config)
        self.assertEqual(header.get_policy_info(), policy_info)
        self.assertEqual(header.policy_binding, policy_binding)
        self.assertEqual(header.get_ephemeral_key(), ephemeral_key)


if __name__ == "__main__":
    unittest.main()
