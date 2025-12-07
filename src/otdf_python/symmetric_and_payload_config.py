"""Symmetric encryption and payload configuration."""


class SymmetricAndPayloadConfig:
    """Symmetric and payload configuration."""

    def __init__(
        self,
        cipher_type: int = 0,
        signature_ecc_mode: int = 0,
        has_signature: bool = True,
    ):
        """Initialize symmetric and payload configuration."""
        self.cipher_type = cipher_type
        self.signature_ecc_mode = signature_ecc_mode
        self.has_signature = has_signature

    def set_has_signature(self, flag: bool):
        self.has_signature = flag

    def set_signature_ecc_mode(self, mode: int):
        self.signature_ecc_mode = mode

    def set_symmetric_cipher_type(self, cipher_type: int):
        self.cipher_type = cipher_type

    def get_cipher_type(self) -> int:
        return self.cipher_type

    def get_symmetric_and_payload_config_as_byte(self) -> int:
        # Most significant bit: has_signature, next 3 bits: signature_ecc_mode, lower 4 bits: cipher_type
        return (
            ((1 if self.has_signature else 0) << 7)
            | ((self.signature_ecc_mode & 0x07) << 4)
            | (self.cipher_type & 0x0F)
        )
