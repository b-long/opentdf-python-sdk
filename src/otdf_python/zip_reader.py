"""ZIP file reader for TDF operations."""

import io
import zipfile

from otdf_python.invalid_zip_exception import InvalidZipException


class ZipReader:
    """ZIP file reader for reading TDF packages."""

    class Entry:
        """ZIP file entry with data access."""

        def __init__(self, zipfile_obj, zipinfo):
            """Initialize ZIP entry."""
            self._zipfile = zipfile_obj
            self._zipinfo = zipinfo

        def get_name(self) -> str:
            return self._zipinfo.filename

        def get_data(self) -> bytes:
            try:
                return self._zipfile.read(self._zipinfo)
            except Exception as e:
                raise InvalidZipException(f"Error reading entry data: {e}") from e

    def __init__(self, in_stream: io.BytesIO | bytes | None = None):
        """Initialize ZIP reader."""
        try:
            if isinstance(in_stream, bytes):
                in_stream = io.BytesIO(in_stream)
            self.in_stream = in_stream or io.BytesIO()
            self.zipfile = zipfile.ZipFile(self.in_stream, mode="r")
            self.entries = [
                self.Entry(self.zipfile, zi) for zi in self.zipfile.infolist()
            ]
        except zipfile.BadZipFile as e:
            raise InvalidZipException(f"Invalid ZIP file: {e}") from e

    def get_entries(self) -> list:
        return self.entries

    def namelist(self) -> list[str]:
        return self.zipfile.namelist()

    def extract(self, name: str, path: str | None = None) -> str:
        return self.zipfile.extract(name, path)

    def read(self, name: str) -> bytes:
        return self.zipfile.read(name)

    def close(self):
        self.zipfile.close()
