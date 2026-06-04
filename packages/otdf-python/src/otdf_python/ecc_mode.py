"""Elliptic Curve Cryptography mode enumeration."""

from otdf_python.ecc_constants import ECCConstants


class ECCMode:
    """ECC (Elliptic Curve Cryptography) mode configuration for NanoTDF.

    This class encapsulates the curve type and policy binding mode (GMAC vs ECDSA)
    that are encoded in the NanoTDF header. It delegates to ECCConstants for
    curve-related lookups to maintain a single source of truth.
    """

    def __init__(self, curve_mode: int = 0, use_ecdsa_binding: bool = False):
        """Initialize ECC mode."""
        self.curve_mode = curve_mode
        self.use_ecdsa_binding = use_ecdsa_binding

    def set_ecdsa_binding(self, flag: bool):
        self.use_ecdsa_binding = flag

    def is_ecdsa_binding_enabled(self) -> bool:
        return self.use_ecdsa_binding

    def set_elliptic_curve(self, curve_mode: int):
        self.curve_mode = curve_mode

    def get_elliptic_curve_type(self) -> int:
        return self.curve_mode

    def get_curve_name(self) -> str:
        """Get the curve name as a string (e.g., 'secp256r1').

        Returns:
            Curve name corresponding to the current curve_mode

        Raises:
            ValueError: If curve_mode is not supported

        """
        # Delegate to ECCConstants for the authoritative mapping
        return ECCConstants.get_curve_name(self.curve_mode)

    @staticmethod
    def get_ec_compressed_pubkey_size(curve_type: int) -> int:
        """Get the compressed public key size for a given curve type.

        Args:
            curve_type: Curve type identifier (0=secp256r1, 1=secp384r1, 2=secp521r1, 3=secp256k1)

        Returns:
            Size in bytes of the compressed public key

        Raises:
            ValueError: If curve_type is not supported

        """
        # Delegate to ECCConstants for the authoritative mapping
        return ECCConstants.get_compressed_key_size_by_type(curve_type)

    def get_ecc_mode_as_byte(self) -> int:
        # Most significant bit: use_ecdsa_binding, lower 3 bits: curve_mode
        return ((1 if self.use_ecdsa_binding else 0) << 7) | (self.curve_mode & 0x07)

    @staticmethod
    def from_string(curve_str: str) -> "ECCMode":
        """Create ECCMode from curve string or policy binding type.

        Args:
            curve_str: Either a curve name ('secp256r1', 'secp384r1', 'secp521r1', 'secp256k1')
                      or a policy binding type ('gmac', 'ecdsa')

        Returns:
            ECCMode instance configured with the appropriate curve and binding mode

        Raises:
            ValueError: If curve_str is not a supported curve or binding type

        """
        # Handle policy binding types (always use secp256r1 as default curve)
        if curve_str.lower() == "gmac":
            return ECCMode(0, False)  # GMAC binding with default secp256r1 curve
        elif curve_str.lower() == "ecdsa":
            return ECCMode(0, True)  # ECDSA binding with default secp256r1 curve

        # Handle curve names - delegate to ECCConstants for the authoritative mapping
        curve_mode = ECCConstants.get_curve_type(curve_str)
        return ECCMode(curve_mode, False)
