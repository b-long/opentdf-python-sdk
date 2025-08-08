class ResourceLocator:
    def __init__(self, resource_url: str | None = None, identifier: str | None = None):
        self.resource_url = resource_url
        self.identifier = identifier

    def get_resource_url(self):
        return self.resource_url

    def get_identifier(self):
        return self.identifier

    def to_bytes(self):
        # Based on Java implementation: [url_len][url_bytes][id_len][id_bytes], each len is 1 byte
        url_bytes = (self.resource_url or "").encode()
        id_bytes = (self.identifier or "").encode()
        if len(url_bytes) > 255 or len(id_bytes) > 255:
            raise ValueError("ResourceLocator fields too long for 1-byte length prefix")
        return bytes([len(url_bytes)]) + url_bytes + bytes([len(id_bytes)]) + id_bytes

    def get_total_size(self) -> int:
        return len(self.to_bytes())

    def write_into_buffer(self, buffer: bytearray, offset: int = 0) -> int:
        data = self.to_bytes()
        buffer[offset : offset + len(data)] = data
        return len(data)

    @staticmethod
    def from_bytes_with_size(buffer: bytes):
        # Based on Java implementation: [url_len][url_bytes][id_len][id_bytes]
        if len(buffer) < 2:
            raise ValueError("Buffer too short for ResourceLocator")
        url_len = buffer[0]
        if len(buffer) < 1 + url_len + 1:
            raise ValueError("Buffer too short for ResourceLocator url")
        url_bytes = buffer[1 : 1 + url_len]
        id_len = buffer[1 + url_len]
        if len(buffer) < 1 + url_len + 1 + id_len:
            raise ValueError("Buffer too short for ResourceLocator id")
        id_bytes = buffer[1 + url_len + 1 : 1 + url_len + 1 + id_len]
        resource_url = url_bytes.decode()
        identifier = id_bytes.decode()
        size = 1 + url_len + 1 + id_len
        return ResourceLocator(resource_url, identifier), size
