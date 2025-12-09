"""ZIP file writer for TDF operations."""

import io
import zipfile
import zlib


class FileInfo:
    """ZIP file metadata information."""

    def __init__(self, name: str, crc: int, size: int, offset: int):
        """Initialize file info."""
        self.name = name
        self.crc = crc
        self.size = size
        self.offset = offset


class ZipWriter:
    """ZIP file writer for creating TDF packages."""

    def __init__(self, out_stream: io.BytesIO | None = None):
        """Initialize ZIP writer."""
        self.out_stream = out_stream or io.BytesIO()
        self.zipfile = zipfile.ZipFile(
            self.out_stream, mode="w", compression=zipfile.ZIP_STORED
        )
        self._file_infos: list[FileInfo] = []
        self._offsets: dict[str, int] = {}

    def stream(self, name: str):
        # Returns a writable file-like object for the given name, tracks offset
        offset = self.out_stream.tell()
        self._offsets[name] = offset
        return _TrackingWriter(self, name, offset)

    def data(self, name: str, content: bytes):
        offset = self.out_stream.tell()
        crc = zlib.crc32(content)
        self.zipfile.writestr(name, content)
        self._file_infos.append(FileInfo(name, crc, len(content), offset))

    def finish(self) -> int:
        self.zipfile.close()
        return self.out_stream.tell()

    def getvalue(self) -> bytes:
        self.zipfile.close()
        return self.out_stream.getvalue()

    def get_file_infos(self) -> list[FileInfo]:
        return self._file_infos


class _TrackingWriter(io.RawIOBase):
    """Internal ZIP stream writer with offset tracking."""

    def __init__(self, zip_writer: ZipWriter, name: str, offset: int):
        """Initialize tracking writer."""
        self._zip_writer = zip_writer
        self._name = name
        self._offset = offset
        self._buffer = io.BytesIO()
        self._closed = False

    def write(self, b):
        return self._buffer.write(b)

    def close(self):
        if not self._closed:
            data = self._buffer.getvalue()
            crc = zlib.crc32(data)
            self._zip_writer.zipfile.writestr(self._name, data)
            self._zip_writer._file_infos.append(
                FileInfo(self._name, crc, len(data), self._offset)
            )
            self._closed = True
        super().close()

    def writable(self):
        return True
