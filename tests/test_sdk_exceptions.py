"""Tests for SDK exceptions."""

import unittest

from otdf_python.sdk_exceptions import AutoConfigureException, SDKException


class TestSDKExceptions(unittest.TestCase):
    """Tests for SDK exception classes."""

    def test_sdk_exception(self):
        """Test SDKException creation and properties."""
        e = SDKException("msg", Exception("reason"))
        self.assertEqual(str(e), "msg")
        self.assertIsInstance(e.reason, Exception)

    def test_auto_configure_exception(self):
        """Test AutoConfigureException creation and properties."""
        e = AutoConfigureException("fail", Exception("cause"))
        self.assertEqual(str(e), "fail")
        self.assertIsInstance(e.reason, Exception)
        e2 = AutoConfigureException("fail2")
        self.assertEqual(str(e2), "fail2")
        self.assertIsNone(e2.reason)


if __name__ == "__main__":
    unittest.main()
