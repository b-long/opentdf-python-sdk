"""Tests for TDFWriter."""

import io
import unittest
import zipfile

from otdf_python.tdf_writer import TDFWriter


class TestTDFWriter(unittest.TestCase):
    """Tests for TDFWriter class."""

    def test_append_manifest_and_payload(self):
        """Test appending manifest and payload."""
        out = io.BytesIO()
        writer = TDFWriter(out)
        manifest = '{"foo": "bar"}'
        writer.append_manifest(manifest)
        with writer.payload() as f:
            f.write(b"payload data")
        size = writer.finish()
        self.assertGreater(size, 0)
        out.seek(0)
        with zipfile.ZipFile(out, "r") as z:
            self.assertEqual(z.read("0.manifest.json"), manifest.encode("utf-8"))
            self.assertEqual(z.read("0.payload"), b"payload data")

    def test_getvalue(self):
        """Test getting writer value as bytes."""
        writer = TDFWriter()
        writer.append_manifest("{}")
        with writer.payload() as f:
            f.write(b"abc")
        writer.finish()
        data = writer.getvalue()
        with zipfile.ZipFile(io.BytesIO(data), "r") as z:
            self.assertEqual(z.read("0.manifest.json"), b"{}")
            self.assertEqual(z.read("0.payload"), b"abc")

    def test_large_payload_chunks(self):
        """Test writing large payload in chunks."""
        out = io.BytesIO()
        writer = TDFWriter(out)
        writer.append_manifest('{"test": true}')
        chunk = b"x" * 1024 * 1024  # 1MB
        with writer.payload() as f:
            for _ in range(5):
                f.write(chunk)
        writer.finish()
        out.seek(0)
        with zipfile.ZipFile(out, "r") as z:
            self.assertEqual(z.read("0.payload"), chunk * 5)

    def test_error_on_write_after_finish(self):
        """Test error when writing after finish."""
        out = io.BytesIO()
        writer = TDFWriter(out)
        writer.append_manifest("{}")
        with writer.payload() as f:
            f.write(b"abc")
        writer.finish()
        # After finish, writing should raise ValueError
        with self.assertRaises(ValueError), writer.payload() as f:
            f.write(b"should fail")


if __name__ == "__main__":
    unittest.main()
