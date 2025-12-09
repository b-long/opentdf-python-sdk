"""Tests for policy objects."""

import unittest

from otdf_python.policy_object import AttributeObject, PolicyBody, PolicyObject


class TestPolicyObject(unittest.TestCase):
    """Tests for policy object classes."""

    def test_attribute_object(self):
        """Test AttributeObject creation and properties."""
        attr = AttributeObject(
            attribute="attr1",
            display_name="Attribute 1",
            is_default=True,
            pub_key="pubkey123",
            kas_url="https://kas.example.com",
        )
        self.assertEqual(attr.attribute, "attr1")
        self.assertEqual(attr.display_name, "Attribute 1")
        self.assertTrue(attr.is_default)
        self.assertEqual(attr.pub_key, "pubkey123")
        self.assertEqual(attr.kas_url, "https://kas.example.com")

    def test_policy_body(self):
        """Test PolicyBody creation and properties."""
        attr1 = AttributeObject(attribute="attr1")
        attr2 = AttributeObject(attribute="attr2")
        body = PolicyBody(data_attributes=[attr1, attr2], dissem=["user1", "user2"])
        self.assertEqual(len(body.data_attributes), 2)
        self.assertIn("user1", body.dissem)
        self.assertIn("user2", body.dissem)

    def test_policy_object(self):
        """Test PolicyObject creation and properties."""
        attr = AttributeObject(attribute="attr1")
        body = PolicyBody(data_attributes=[attr], dissem=["user1"])
        policy = PolicyObject(uuid="uuid-1234", body=body)
        self.assertEqual(policy.uuid, "uuid-1234")
        self.assertEqual(policy.body, body)


if __name__ == "__main__":
    unittest.main()
