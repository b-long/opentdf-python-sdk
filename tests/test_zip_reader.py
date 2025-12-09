"""Tests for ZipReader."""

import io
import random
import unittest
from pathlib import Path

from otdf_python.zip_reader import ZipReader
from otdf_python.zip_writer import ZipWriter


class TestZipReader(unittest.TestCase):
    """Tests for ZipReader class."""

    def test_read_and_namelist(self):
        """Test reading zip and listing files."""
        # Create a zip in memory
        writer = ZipWriter()
        writer.data("foo.txt", b"foo")
        writer.data("bar.txt", b"bar")
        writer.finish()
        data = writer.getvalue()
        # Read it back
        reader = ZipReader(io.BytesIO(data))
        names = reader.namelist()
        self.assertIn("foo.txt", names)
        self.assertIn("bar.txt", names)
        self.assertEqual(reader.read("foo.txt"), b"foo")
        self.assertEqual(reader.read("bar.txt"), b"bar")
        reader.close()

    def test_extract(self):
        """Test extracting files from zip."""
        import tempfile

        writer = ZipWriter()
        writer.data("baz.txt", b"baz")
        writer.finish()
        data = writer.getvalue()
        reader = ZipReader(io.BytesIO(data))
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = reader.extract("baz.txt", tmpdir)
            with Path(out_path).open("rb") as f:
                self.assertEqual(f.read(), b"baz")
        reader.close()

    def test_entry_interface_and_random_files(self):
        """Test zip entry interface with random files."""
        # Create a zip with many random files
        r = random.Random(42)
        num_entries = r.randint(10, 20)  # Use a smaller number for test speed
        test_data = []
        for _ in range(num_entries):
            file_name = "".join(
                r.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=r.randint(5, 15))
            )
            file_content = bytes(r.getrandbits(8) for _ in range(r.randint(10, 100)))
            test_data.append((file_name, file_content))
        writer = ZipWriter()
        for name, content in test_data:
            writer.data(name, content)
        writer.finish()
        data = writer.getvalue()
        # Read back using the Entry interface
        reader = ZipReader(io.BytesIO(data))
        names_to_data = dict(test_data)
        found_names = set()
        for entry in reader.get_entries():
            name = entry.get_name()
            self.assertIn(name, names_to_data)
            self.assertEqual(entry.get_data(), names_to_data[name])
            found_names.add(name)
        self.assertEqual(found_names, set(names_to_data.keys()))
        reader.close()


if __name__ == "__main__":
    unittest.main()
