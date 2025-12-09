"""Policy information handling for NanoTDF."""


class PolicyInfo:
    """Policy information."""

    def __init__(
        self,
        policy_type: int = 0,
        body: bytes | None = None,
    ):
        """Initialize policy information."""
        self.policy_type = policy_type
        self.body = body

    def set_embedded_plain_text_policy(self, body: bytes):
        self.body = body
        self.policy_type = 1  # Placeholder for EMBEDDED_POLICY_PLAIN_TEXT

    def set_embedded_encrypted_text_policy(self, body: bytes):
        self.body = body
        self.policy_type = 2  # Placeholder for EMBEDDED_POLICY_ENCRYPTED

    def get_body(self) -> bytes | None:
        return self.body

    def get_total_size(self) -> int:
        size = 1  # policy_type
        size += 2  # body_len
        size += len(self.body) if self.body else 0
        return size

    def write_into_buffer(self, buffer: bytearray, offset: int = 0) -> int:
        start = offset
        buffer[offset] = self.policy_type
        offset += 1
        body_len = len(self.body) if self.body else 0
        buffer[offset : offset + 2] = body_len.to_bytes(2, "big")
        offset += 2
        if self.body:
            buffer[offset : offset + body_len] = self.body
            offset += body_len
        return offset - start

    @staticmethod
    def from_bytes_with_size(buffer: bytes, ecc_mode):
        # Parse policy_type (1 byte), body_len (2 bytes), body
        # Note: binding is NOT part of PolicyInfo - it's read separately in Header
        offset = 0
        if len(buffer) < 3:
            raise ValueError("Buffer too short for PolicyInfo header")
        policy_type = buffer[offset]
        offset += 1
        body_len = int.from_bytes(buffer[offset : offset + 2], "big")
        offset += 2
        if len(buffer) < offset + body_len:
            raise ValueError("Buffer too short for PolicyInfo body")
        body = buffer[offset : offset + body_len]
        offset += body_len
        pi = PolicyInfo(policy_type=policy_type, body=body)
        return pi, offset
