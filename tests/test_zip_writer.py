"""Tests for ZipWriter."""

import io
import unittest
import zipfile

from otdf_python.zip_writer import ZipWriter


class TestZipWriter(unittest.TestCase):
    """Tests for ZipWriter class."""

    def test_data_and_stream(self):
        """Test writing data and streams to zip."""
        out = io.BytesIO()
        writer = ZipWriter(out)
        # Write using data
        writer.data("foo.txt", b"hello world")
        # Write using stream
        with writer.stream("bar.txt") as f:
            f.write(b"bar contents")
        size = writer.finish()
        self.assertGreater(size, 0)
        # Validate zip contents
        out.seek(0)
        with zipfile.ZipFile(out, "r") as z:
            self.assertEqual(z.read("foo.txt"), b"hello world")
            self.assertEqual(z.read("bar.txt"), b"bar contents")

    def test_getvalue(self):
        """Test getting writer value as bytes."""
        writer = ZipWriter()
        writer.data("a.txt", b"A")
        writer.finish()
        data = writer.getvalue()
        with zipfile.ZipFile(io.BytesIO(data), "r") as z:
            self.assertEqual(z.read("a.txt"), b"A")


if __name__ == "__main__":
    unittest.main()
