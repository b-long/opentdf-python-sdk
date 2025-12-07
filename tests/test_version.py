"""Tests for Version."""

import unittest

from otdf_python.version import Version


class TestVersion(unittest.TestCase):
    """Tests for Version class."""

    def test_parse_and_str(self):
        """Test Version parsing and string representation."""
        v = Version("1.2.3-alpha")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertEqual(v.prerelease_and_metadata, "-alpha")
        self.assertIn("Version{major=1, minor=2, patch=3", str(v))

    def test_compare(self):
        """Test Version comparison."""
        v1 = Version("1.2.3")
        v2 = Version("1.2.4")
        v3 = Version("1.3.0")
        v4 = Version("2.0.0")
        self.assertTrue(v1 < v2)
        self.assertTrue(v2 < v3)
        self.assertTrue(v3 < v4)
        self.assertTrue(v4 > v1)
        self.assertEqual(v1, Version(1, 2, 3))

    def test_hash(self):
        """Test Version hashing."""
        v1 = Version("1.2.3")
        v2 = Version(1, 2, 3)
        self.assertEqual(hash(v1), hash(v2))
        s = {v1, v2}
        self.assertEqual(len(s), 1)

    def test_invalid(self):
        """Test invalid Version string."""
        with self.assertRaises(ValueError):
            Version("not.a.version")


if __name__ == "__main__":
    unittest.main()
