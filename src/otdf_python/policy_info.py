class PolicyInfo:
    def __init__(
        self,
        policy_type: int = 0,
        has_ecdsa_binding: bool = False,
        body: bytes | None = None,
        binding: bytes | None = None,
    ):
        self.policy_type = policy_type
        self.has_ecdsa_binding = has_ecdsa_binding
        self.body = body
        self.binding = binding

    def set_embedded_plain_text_policy(self, body: bytes):
        self.body = body
        self.policy_type = 1  # Placeholder for EMBEDDED_POLICY_PLAIN_TEXT

    def set_embedded_encrypted_text_policy(self, body: bytes):
        self.body = body
        self.policy_type = 2  # Placeholder for EMBEDDED_POLICY_ENCRYPTED

    def set_policy_binding(self, binding: bytes):
        self.binding = binding

    def get_body(self) -> bytes | None:
        return self.body

    def get_binding(self) -> bytes | None:
        return self.binding

    def get_total_size(self) -> int:
        size = 1  # policy_type
        size += 2  # body_len
        size += len(self.body) if self.body else 0
        size += 1  # binding_len
        size += len(self.binding) if self.binding else 0
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
        binding_len = len(self.binding) if self.binding else 0
        buffer[offset] = binding_len
        offset += 1
        if self.binding:
            buffer[offset : offset + binding_len] = self.binding
            offset += binding_len
        return offset - start

    @staticmethod
    def from_bytes_with_size(buffer: bytes, ecc_mode):
        # Based on Java implementation: parse policy_type (1 byte), body_len (2 bytes), body, binding_len (1 byte), binding
        offset = 0
        if len(buffer) < 4:
            raise ValueError("Buffer too short for PolicyInfo header")
        policy_type = buffer[offset]
        offset += 1
        body_len = int.from_bytes(buffer[offset : offset + 2], "big")
        offset += 2
        if len(buffer) < offset + body_len + 1:
            raise ValueError("Buffer too short for PolicyInfo body")
        body = buffer[offset : offset + body_len]
        offset += body_len
        binding_len = buffer[offset]
        offset += 1
        if len(buffer) < offset + binding_len:
            raise ValueError("Buffer too short for PolicyInfo binding")
        binding = buffer[offset : offset + binding_len]
        offset += binding_len
        pi = PolicyInfo(policy_type=policy_type, body=body, binding=binding)
        return pi, offset
