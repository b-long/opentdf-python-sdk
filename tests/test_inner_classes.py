import unittest

from otdf_python.auth_headers import AuthHeaders
from otdf_python.kas_info import KASInfo
from otdf_python.policy_binding_serializer import PolicyBinding, PolicyBindingSerializer


class TestAuthHeaders(unittest.TestCase):
    def test_auth_headers(self):
        headers = AuthHeaders("Bearer token123", "dpop456")
        self.assertEqual(headers.auth_header, "Bearer token123")
        self.assertEqual(headers.dpop_header, "dpop456")
        self.assertEqual(headers.get_auth_header(), "Bearer token123")
        self.assertEqual(headers.get_dpop_header(), "dpop456")

    def test_auth_headers_to_dict_with_dpop(self):
        headers = AuthHeaders("Bearer token123", "dpop456")
        headers_dict = headers.to_dict()
        self.assertEqual(headers_dict["Authorization"], "Bearer token123")
        self.assertEqual(headers_dict["DPoP"], "dpop456")
        self.assertEqual(len(headers_dict), 2)

    def test_auth_headers_to_dict_without_dpop(self):
        headers = AuthHeaders("Bearer token123", "")
        headers_dict = headers.to_dict()
        self.assertEqual(headers_dict["Authorization"], "Bearer token123")
        self.assertNotIn("DPoP", headers_dict)
        self.assertEqual(len(headers_dict), 1)

    def test_auth_headers_default_dpop(self):
        headers = AuthHeaders("Bearer token123")
        self.assertEqual(headers.dpop_header, "")
        headers_dict = headers.to_dict()
        self.assertEqual(headers_dict["Authorization"], "Bearer token123")
        self.assertNotIn("DPoP", headers_dict)


class TestKASInfo(unittest.TestCase):
    def test_kas_info_clone(self):
        kas_info = KASInfo(url="https://kas.example.com", public_key="pubkey")
        clone = kas_info.clone()
        assert clone == kas_info
        assert clone is not kas_info

    def test_string_representation(self):
        kas_info = KASInfo(
            url="https://kas.example.com",
            public_key="pubkey",
            kid="kid1",
            default=True,
            algorithm="RSA",
        )
        s = str(kas_info)
        assert "KASInfo" in s
        assert "url=https://kas.example.com" in s
        assert "kid=kid1" in s
        assert "default=True" in s
        assert "algorithm=RSA" in s


class TestPolicyBindingSerializer(unittest.TestCase):
    def test_deserialize_dict(self):
        json_data = {"attr": "value", "number": 42}
        result = PolicyBindingSerializer.deserialize(json_data)
        self.assertEqual(result.attr, "value")
        self.assertEqual(result.number, 42)

    def test_deserialize_string(self):
        json_data = "policy_string"
        result = PolicyBindingSerializer.deserialize(json_data)
        self.assertEqual(result, "policy_string")

    def test_deserialize_invalid(self):
        with self.assertRaises(ValueError):
            PolicyBindingSerializer.deserialize(123)

    def test_serialize_policy_binding(self):
        policy = PolicyBinding(name="test_policy", value="test_value")
        result = PolicyBindingSerializer.serialize(policy)
        self.assertEqual(result, {"name": "test_policy", "value": "test_value"})

    def test_serialize_string(self):
        result = PolicyBindingSerializer.serialize("policy_string")
        self.assertEqual(result, "policy_string")


if __name__ == "__main__":
    unittest.main()
