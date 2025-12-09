"""NanoTDF ECDSA Signature Structure."""

from dataclasses import dataclass, field


class IncorrectNanoTDFECDSASignatureSize(Exception):
    """Exception raised when the signature size is incorrect."""

    pass


@dataclass
class NanoTDFECDSAStruct:
    """Class to handle ECDSA signature structure for NanoTDF.

    This structure represents an ECDSA signature as required by the NanoTDF format.
    It consists of r and s values along with their lengths.
    """

    r_length: bytearray = field(default_factory=lambda: bytearray(1))
    r_value: bytearray = None
    s_length: bytearray = field(default_factory=lambda: bytearray(1))
    s_value: bytearray = None

    @classmethod
    def from_bytes(
        cls, ecdsa_signature_value: bytes, key_size: int
    ) -> "NanoTDFECDSAStruct":
        """Create a NanoTDFECDSAStruct from a byte array.

        Args:
            ecdsa_signature_value: The signature value as bytes
            key_size: The size of the key in bytes

        Returns:
            A new NanoTDFECDSAStruct

        Raises:
            IncorrectNanoTDFECDSASignatureSize: If the signature buffer size is invalid

        """
        if len(ecdsa_signature_value) != (2 * key_size) + 2:
            raise IncorrectNanoTDFECDSASignatureSize(
                f"Invalid signature buffer size. Expected {(2 * key_size) + 2}, got {len(ecdsa_signature_value)}"
            )

        struct_obj = cls()

        # Copy value of r_length to signature struct
        index = 0
        struct_obj.r_length[0] = ecdsa_signature_value[index]

        # Copy the contents of r_value to signature struct
        index += 1
        r_len = struct_obj.r_length[0]
        struct_obj.r_value = bytearray(key_size)
        struct_obj.r_value[:r_len] = ecdsa_signature_value[index : index + r_len]

        # Copy value of s_length to signature struct
        index += key_size
        struct_obj.s_length[0] = ecdsa_signature_value[index]

        # Copy value of s_value
        index += 1
        s_len = struct_obj.s_length[0]
        struct_obj.s_value = bytearray(key_size)
        struct_obj.s_value[:s_len] = ecdsa_signature_value[index : index + s_len]

        return struct_obj

    def as_bytes(self) -> bytes:
        """Convert the signature structure to bytes.
        Raises ValueError if r_value or s_value is None.
        """
        if self.r_value is None or self.s_value is None:
            raise ValueError("r_value and s_value must not be None")
        total_size = 1 + len(self.r_value) + 1 + len(self.s_value)
        signature = bytearray(total_size)

        # Copy value of r_length
        index = 0
        signature[index] = self.r_length[0]

        # Copy the contents of r_value
        index += 1
        signature[index : index + len(self.r_value)] = self.r_value

        # Copy value of s_length
        index += len(self.r_value)
        signature[index] = self.s_length[0]

        # Copy value of s_value
        index += 1
        signature[index : index + len(self.s_value)] = self.s_value

        return bytes(signature)

    def get_s_value(self) -> bytearray:
        """Get the s value of the signature."""
        return self.s_value

    def set_s_value(self, s_value: bytearray) -> None:
        """Set the s value of the signature."""
        self.s_value = s_value

    def get_s_length(self) -> int:
        """Get the length of the s value."""
        return self.s_length[0]

    def set_s_length(self, s_length: int) -> None:
        """Set the length of the s value."""
        self.s_length[0] = s_length

    def get_r_value(self) -> bytearray:
        """Get the r value of the signature."""
        return self.r_value

    def set_r_value(self, r_value: bytearray) -> None:
        """Set the r value of the signature."""
        self.r_value = r_value

    def get_r_length(self) -> int:
        """Get the length of the r value."""
        return self.r_length[0]

    def set_r_length(self, r_length: int) -> None:
        """Set the length of the r value."""
        self.r_length[0] = r_length
