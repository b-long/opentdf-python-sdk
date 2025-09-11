import unittest

from otdf_python.assertion_config import (
    AppliesToState,
    AssertionConfig,
    AssertionKey,
    AssertionKeyAlg,
    BindingMethod,
    Scope,
    Statement,
    Type,
)


class TestAssertionConfig(unittest.TestCase):
    def test_enums(self):
        self.assertEqual(str(Type.HANDLING_ASSERTION), "handling")
        self.assertEqual(str(Scope.PAYLOAD), "payload")
        self.assertEqual(str(AppliesToState.ENCRYPTED), "encrypted")
        self.assertEqual(str(BindingMethod.JWS), "jws")

    def test_assertion_key(self):
        key = AssertionKey(AssertionKeyAlg.RS256, "keydata")
        self.assertTrue(key.is_defined())
        key2 = AssertionKey(AssertionKeyAlg.NOT_DEFINED, None)
        self.assertFalse(key2.is_defined())

    def test_statement_equality_and_hash(self):
        s1 = Statement("fmt", "schema", "val")
        s2 = Statement("fmt", "schema", "val")
        s3 = Statement("fmt2", "schema", "val")
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertEqual(hash(s1), hash(s2))

    def test_assertion_config(self):
        statement = Statement("fmt", "schema", "val")
        key = AssertionKey(AssertionKeyAlg.HS256, "keydata")
        config = AssertionConfig(
            id="id1",
            type=Type.BASE_ASSERTION,
            scope=Scope.TRUSTED_DATA_OBJ,
            applies_to_state=AppliesToState.UNENCRYPTED,
            statement=statement,
            signing_key=key,
        )
        self.assertEqual(config.id, "id1")
        self.assertEqual(config.type, Type.BASE_ASSERTION)
        self.assertEqual(config.scope, Scope.TRUSTED_DATA_OBJ)
        self.assertEqual(config.applies_to_state, AppliesToState.UNENCRYPTED)
        self.assertEqual(config.statement, statement)
        self.assertEqual(config.signing_key, key)


if __name__ == "__main__":
    unittest.main()
