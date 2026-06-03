"""TDF header parsing and serialization."""

from otdf_python.constants import MAGIC_NUMBER_AND_VERSION
from otdf_python.ecc_mode import ECCMode
from otdf_python.policy_info import PolicyInfo
from otdf_python.resource_locator import ResourceLocator
from otdf_python.symmetric_and_payload_config import SymmetricAndPayloadConfig


class Header:
    """TDF header with encryption and policy information."""

    # Size of GMAC (Galois Message Authentication Code) for policy binding
    GMAC_SIZE = 8

    def __init__(self):
        """Initialize TDF header."""
        self.kas_locator: ResourceLocator | None = None
        self.ecc_mode: ECCMode | None = None
        self.payload_config: SymmetricAndPayloadConfig | None = None
        self.policy_info: PolicyInfo | None = None
        self.policy_binding: bytes | None = None
        self.ephemeral_key: bytes | None = None

    @classmethod
    def from_bytes(cls, buffer: bytes):
        # Parse header from bytes, validate magic/version
        offset = 0
        magic = buffer[offset : offset + 3]
        if magic != MAGIC_NUMBER_AND_VERSION:
            raise ValueError("Invalid magic number and version in nano tdf.")
        offset += 3
        kas_locator, kas_size = ResourceLocator.from_bytes_with_size(buffer[offset:])
        offset += kas_size
        ecc_mode = ECCMode(buffer[offset])
        offset += 1
        payload_config = SymmetricAndPayloadConfig(buffer[offset])
        offset += 1
        policy_info, policy_size = PolicyInfo.from_bytes_with_size(
            buffer[offset:], ecc_mode
        )
        offset += policy_size

        # Read policy binding (GMAC - 8 bytes fixed size)
        # Note: ECDSA binding not yet supported in this implementation
        policy_binding = buffer[offset : offset + cls.GMAC_SIZE]
        if len(policy_binding) != cls.GMAC_SIZE:
            raise ValueError("Failed to read policy binding - invalid buffer size.")
        offset += cls.GMAC_SIZE

        compressed_pubkey_size = ECCMode.get_ec_compressed_pubkey_size(
            ecc_mode.get_elliptic_curve_type()
        )
        ephemeral_key = buffer[offset : offset + compressed_pubkey_size]
        if len(ephemeral_key) != compressed_pubkey_size:
            raise ValueError("Failed to read ephemeral key - invalid buffer size.")
        obj = cls()
        obj.kas_locator = kas_locator
        obj.ecc_mode = ecc_mode
        obj.payload_config = payload_config
        obj.policy_info = policy_info
        obj.policy_binding = policy_binding
        obj.ephemeral_key = ephemeral_key
        return obj

    @staticmethod
    def peek_length(buffer: bytes) -> int:
        offset = 0
        # MAGIC_NUMBER_AND_VERSION (3 bytes)
        offset += 3
        # ResourceLocator
        _kas_locator, kas_size = ResourceLocator.from_bytes_with_size(buffer[offset:])
        offset += kas_size
        # ECC mode (1 byte)
        ecc_mode = ECCMode(buffer[offset])
        offset += 1
        # Payload config (1 byte)
        offset += 1
        # PolicyInfo
        _policy_info, policy_size = PolicyInfo.from_bytes_with_size(
            buffer[offset:], ecc_mode
        )
        offset += policy_size
        # Policy binding (GMAC - 8 bytes)
        offset += Header.GMAC_SIZE
        # Ephemeral key (size depends on curve)
        compressed_pubkey_size = ECCMode.get_ec_compressed_pubkey_size(
            ecc_mode.get_elliptic_curve_type()
        )
        offset += compressed_pubkey_size
        return offset

    def set_kas_locator(self, kas_locator: ResourceLocator):
        self.kas_locator = kas_locator

    def get_kas_locator(self) -> ResourceLocator | None:
        return self.kas_locator

    def set_ecc_mode(self, ecc_mode: ECCMode):
        self.ecc_mode = ecc_mode

    def get_ecc_mode(self) -> ECCMode | None:
        return self.ecc_mode

    def set_payload_config(self, payload_config: SymmetricAndPayloadConfig):
        self.payload_config = payload_config

    def get_payload_config(self) -> SymmetricAndPayloadConfig | None:
        return self.payload_config

    def set_policy_info(self, policy_info: PolicyInfo):
        self.policy_info = policy_info

    def get_policy_info(self) -> PolicyInfo | None:
        return self.policy_info

    def set_policy_binding(self, policy_binding: bytes):
        if len(policy_binding) != self.GMAC_SIZE:
            raise ValueError(
                f"Policy binding must be exactly {self.GMAC_SIZE} bytes (GMAC), got {len(policy_binding)}"
            )
        self.policy_binding = policy_binding

    def get_policy_binding(self) -> bytes | None:
        return self.policy_binding

    def set_ephemeral_key(self, ephemeral_key: bytes):
        if self.ecc_mode is not None:
            expected_size = ECCMode.get_ec_compressed_pubkey_size(
                self.ecc_mode.get_elliptic_curve_type()
            )
            if len(ephemeral_key) != expected_size:
                raise ValueError("Failed to read ephemeral key - invalid buffer size.")
        self.ephemeral_key = ephemeral_key

    def get_ephemeral_key(self) -> bytes | None:
        return self.ephemeral_key

    def get_total_size(self) -> int:
        total = 0
        total += self.kas_locator.get_total_size() if self.kas_locator else 0
        total += 1  # ECC mode
        total += 1  # payload config
        total += self.policy_info.get_total_size() if self.policy_info else 0
        total += self.GMAC_SIZE  # policy binding (GMAC)
        total += len(self.ephemeral_key) if self.ephemeral_key else 0
        return total

    def write_into_buffer(self, buffer: bytearray) -> int:
        total_size = self.get_total_size()
        if len(buffer) < total_size:
            raise ValueError("Failed to write header - invalid buffer size.")
        offset = 0
        # ResourceLocator
        n = self.kas_locator.write_into_buffer(buffer, offset)
        offset += n
        # ECCMode (1 byte)
        buffer[offset] = self.ecc_mode.get_ecc_mode_as_byte()
        offset += 1
        # SymmetricAndPayloadConfig (1 byte)
        buffer[offset] = self.payload_config.get_symmetric_and_payload_config_as_byte()
        offset += 1
        # PolicyInfo
        n = self.policy_info.write_into_buffer(buffer, offset)
        offset += n
        # Policy binding (GMAC - 8 bytes)
        if self.policy_binding:
            if len(self.policy_binding) != self.GMAC_SIZE:
                raise ValueError(
                    f"Policy binding must be exactly {self.GMAC_SIZE} bytes (GMAC), got {len(self.policy_binding)}"
                )
            buffer[offset : offset + self.GMAC_SIZE] = self.policy_binding
            offset += self.GMAC_SIZE
        else:
            # Write zeros if no binding provided
            buffer[offset : offset + self.GMAC_SIZE] = b"\x00" * self.GMAC_SIZE
            offset += self.GMAC_SIZE
        # Ephemeral key
        buffer[offset : offset + len(self.ephemeral_key)] = self.ephemeral_key
        offset += len(self.ephemeral_key)
        return offset

    def to_bytes(self):
        buf = bytearray(self.get_total_size())
        self.write_into_buffer(buf)
        return bytes(buf)
