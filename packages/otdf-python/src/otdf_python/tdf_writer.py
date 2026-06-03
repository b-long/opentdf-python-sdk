"""TDF writer for creating encrypted TDF files."""

import io

from otdf_python.zip_writer import ZipWriter


class TDFWriter:
    """TDF file writer for creating encrypted TDF packages."""

    TDF_PAYLOAD_FILE_NAME = "0.payload"
    TDF_MANIFEST_FILE_NAME = "0.manifest.json"

    def __init__(self, out_stream: io.BytesIO | None = None):
        """Initialize TDF writer."""
        self._zip_writer = ZipWriter(out_stream)

    def append_manifest(self, manifest: str):
        self._zip_writer.data(self.TDF_MANIFEST_FILE_NAME, manifest.encode("utf-8"))

    def payload(self):
        return self._zip_writer.stream(self.TDF_PAYLOAD_FILE_NAME)

    def finish(self) -> int:
        return self._zip_writer.finish()

    def getvalue(self) -> bytes:
        return self._zip_writer.getvalue()
