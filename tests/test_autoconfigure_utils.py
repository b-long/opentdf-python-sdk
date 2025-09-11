import unittest

from otdf_python.autoconfigure_utils import (
    AttributeNameFQN,
    AttributeValueFQN,
    AutoConfigureException,
    KeySplitStep,
    RuleType,
)


class TestAutoconfigureUtils(unittest.TestCase):
    def test_rule_type(self):
        self.assertEqual(RuleType.HIERARCHY, "hierarchy")
        self.assertEqual(RuleType.ALL_OF, "allOf")

    def test_key_split_step(self):
        k1 = KeySplitStep("kas1", "split1")
        k2 = KeySplitStep("kas1", "split1")
        k3 = KeySplitStep("kas2", "split2")
        self.assertEqual(k1, k2)
        self.assertNotEqual(k1, k3)
        self.assertEqual(str(k1), "KeySplitStep{kas=kas1, splitID=split1}")
        self.assertEqual(len({k1, k2, k3}), 2)

    def test_attribute_name_fqn(self):
        url = "https://example.com/attr/department"
        fqn = AttributeNameFQN(url)
        self.assertEqual(fqn.prefix(), url)
        self.assertEqual(fqn.get_key(), url.lower())
        self.assertEqual(fqn.authority(), "https://example.com")
        self.assertEqual(fqn.name(), "department")
        val_fqn = fqn.select("HR")
        self.assertIsInstance(val_fqn, AttributeValueFQN)
        self.assertIn("/value/HR", str(val_fqn))
        with self.assertRaises(AutoConfigureException):
            AttributeNameFQN("badurl")

    def test_attribute_value_fqn(self):
        url = "https://example.com/attr/department/value/HR"
        fqn = AttributeValueFQN(url)
        self.assertEqual(str(fqn), url)
        self.assertEqual(fqn, AttributeValueFQN(url))
        self.assertEqual(len({fqn, AttributeValueFQN(url)}), 1)
        with self.assertRaises(AutoConfigureException):
            AttributeValueFQN("badurl")


if __name__ == "__main__":
    unittest.main()
