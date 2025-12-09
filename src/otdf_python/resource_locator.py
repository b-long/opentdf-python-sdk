"""NanoTDF resource locator handling."""


class ResourceLocator:
    """Represent NanoTDF Resource Locator per specification.

    See https://github.com/opentdf/spec/blob/main/schema/nanotdf/README.md

    Format:
        - Byte 0: Protocol Enum (bits 0-3) + Identifier Length (bits 4-7)
          - Protocol: 0x0=HTTP, 0x1=HTTPS, 0xF=Shared Resource Directory
          - Identifier: 0x0=None, 0x1=2 bytes, 0x2=8 bytes, 0x3=32 bytes
        - Byte 1: Body Length (1-255 bytes)
        - Bytes 2-N: Body (URL path)
        - Bytes N+1-M: Identifier (optional, 0/2/8/32 bytes)

    """

    # Protocol enum values
    PROTOCOL_HTTP = 0x0
    PROTOCOL_HTTPS = 0x1
    PROTOCOL_SHARED_RESOURCE_DIR = 0xF

    # Identifier length enum values (in bits 4-7)
    IDENTIFIER_NONE = 0x0
    IDENTIFIER_2_BYTES = 0x1
    IDENTIFIER_8_BYTES = 0x2
    IDENTIFIER_32_BYTES = 0x3

    def __init__(self, resource_url: str | None = None, identifier: str | None = None):
        """Initialize resource locator.

        Args:
            resource_url: URL of the resource
            identifier: Optional identifier for the resource

        """
        self.resource_url = resource_url or ""
        self.identifier = identifier or ""

    def get_resource_url(self):
        return self.resource_url

    def get_identifier(self):
        return self.identifier

    def _parse_url(self):
        """Parse URL to extract protocol and body (path)."""
        url = self.resource_url
        if url.startswith("https://"):
            protocol = self.PROTOCOL_HTTPS
            body = url[8:]  # Remove "https://"
        elif url.startswith("http://"):
            protocol = self.PROTOCOL_HTTP
            body = url[7:]  # Remove "http://"
        else:
            # Default to HTTP
            protocol = self.PROTOCOL_HTTP
            body = url
        return protocol, body.encode()

    def _get_identifier_bytes(self):
        """Get identifier bytes and determine identifier length enum."""
        if not self.identifier:
            return self.IDENTIFIER_NONE, b""

        id_bytes = self.identifier.encode()
        id_len = len(id_bytes)

        if id_len == 0:
            return self.IDENTIFIER_NONE, b""
        elif id_len <= 2:
            # Pad to 2 bytes
            return self.IDENTIFIER_2_BYTES, id_bytes.ljust(2, b"\x00")
        elif id_len <= 8:
            # Pad to 8 bytes
            return self.IDENTIFIER_8_BYTES, id_bytes.ljust(8, b"\x00")
        elif id_len <= 32:
            # Pad to 32 bytes
            return self.IDENTIFIER_32_BYTES, id_bytes.ljust(32, b"\x00")
        else:
            raise ValueError(f"Identifier too long: {id_len} bytes (max 32)")

    def to_bytes(self):
        """Convert to NanoTDF Resource Locator format per spec.

        Format:
        - Byte 0: Protocol Enum (bits 0-3) + Identifier Length (bits 4-7)
        - Byte 1: Body Length
        - Bytes 2-N: Body (URL path)
        - Bytes N+1-M: Identifier (0/2/8/32 bytes)
        """
        protocol, body_bytes = self._parse_url()
        identifier_enum, identifier_bytes = self._get_identifier_bytes()

        if len(body_bytes) > 255:
            raise ValueError(
                f"Resource Locator body too long: {len(body_bytes)} bytes (max 255)"
            )

        # Byte 0: protocol in bits 0-3, identifier length in bits 4-7
        protocol_and_id = (identifier_enum << 4) | protocol

        # Byte 1: body length
        body_len = len(body_bytes)

        return bytes([protocol_and_id, body_len]) + body_bytes + identifier_bytes

    def get_total_size(self) -> int:
        return len(self.to_bytes())

    def write_into_buffer(self, buffer: bytearray, offset: int = 0) -> int:
        data = self.to_bytes()
        buffer[offset : offset + len(data)] = data
        return len(data)

    @staticmethod
    def from_bytes_with_size(buffer: bytes):  # noqa: C901
        """Parse NanoTDF Resource Locator from bytes per spec.

        Format:
        - Byte 0: Protocol Enum (bits 0-3) + Identifier Length (bits 4-7)
        - Byte 1: Body Length
        - Bytes 2-N: Body (URL path)
        - Bytes N+1-M: Identifier (0/2/8/32 bytes)
        """
        if len(buffer) < 2:
            raise ValueError("Buffer too short for ResourceLocator")

        # Parse byte 0: protocol and identifier length
        protocol_and_id = buffer[0]
        protocol = protocol_and_id & 0x0F  # Bits 0-3
        identifier_enum = (protocol_and_id >> 4) & 0x0F  # Bits 4-7

        # Parse byte 1: body length
        body_len = buffer[1]

        if len(buffer) < 2 + body_len:
            raise ValueError(
                f"Buffer too short for ResourceLocator body (need {2 + body_len}, have {len(buffer)})"
            )

        # Parse body (URL path)
        body_bytes = buffer[2 : 2 + body_len]
        body = body_bytes.decode()

        # Reconstruct full URL with protocol
        if protocol == ResourceLocator.PROTOCOL_HTTPS:
            resource_url = f"https://{body}"
        elif protocol == ResourceLocator.PROTOCOL_HTTP:
            resource_url = f"http://{body}"
        else:
            resource_url = body

        # Parse identifier based on identifier_enum
        offset = 2 + body_len
        if identifier_enum == ResourceLocator.IDENTIFIER_NONE:
            identifier_len = 0
        elif identifier_enum == ResourceLocator.IDENTIFIER_2_BYTES:
            identifier_len = 2
        elif identifier_enum == ResourceLocator.IDENTIFIER_8_BYTES:
            identifier_len = 8
        elif identifier_enum == ResourceLocator.IDENTIFIER_32_BYTES:
            identifier_len = 32
        else:
            raise ValueError(f"Invalid identifier length enum: {identifier_enum}")

        if len(buffer) < offset + identifier_len:
            raise ValueError(
                f"Buffer too short for ResourceLocator identifier (need {offset + identifier_len}, have {len(buffer)})"
            )

        if identifier_len > 0:
            identifier_bytes = buffer[offset : offset + identifier_len]
            # Remove padding
            identifier = identifier_bytes.rstrip(b"\x00").decode()
        else:
            identifier = ""

        size = 2 + body_len + identifier_len
        return ResourceLocator(resource_url, identifier), size
