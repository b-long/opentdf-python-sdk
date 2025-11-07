from typing import ClassVar


class ECCMode:
    _CURVE_MAP: ClassVar[dict[str, int]] = {
        "secp256r1": 0,
        "secp384r1": 1,
        "secp521r1": 2,
        "secp256k1": 3,
    }

    def __init__(self, curve_mode: int = 0, use_ecdsa_binding: bool = False):
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
        """Get the curve name as a string (e.g., 'secp256r1')."""
        for name, mode in self._CURVE_MAP.items():
            if mode == self.curve_mode:
                return name
        # Default to secp256r1 if not found
        return "secp256r1"

    @staticmethod
    def get_ec_compressed_pubkey_size(curve_type: int) -> int:
        # 0: secp256r1, 1: secp384r1, 2: secp521r1, 3: secp256k1
        if curve_type == 0:
            return 33  # secp256r1
        elif curve_type == 1:
            return 49  # secp384r1
        elif curve_type == 2:
            return 67  # secp521r1
        elif curve_type == 3:
            return 33  # secp256k1 (same size as secp256r1)
        else:
            raise ValueError("Unsupported ECC algorithm.")

    def get_ecc_mode_as_byte(self) -> int:
        # Most significant bit: use_ecdsa_binding, lower 3 bits: curve_mode
        return ((1 if self.use_ecdsa_binding else 0) << 7) | (self.curve_mode & 0x07)

    @staticmethod
    def from_string(curve_str: str) -> "ECCMode":
        """Create ECCMode from curve string like 'secp256r1' or 'secp384r1', or policy binding type like 'gmac' or 'ecdsa'."""
        # Handle policy binding types
        if curve_str.lower() == "gmac":
            return ECCMode(0, False)  # GMAC binding with default secp256r1 curve
        elif curve_str.lower() == "ecdsa":
            return ECCMode(0, True)  # ECDSA binding with default secp256r1 curve

        # Handle curve names
        curve_mode = ECCMode._CURVE_MAP.get(curve_str.lower())
        if curve_mode is None:
            raise ValueError(f"Unsupported curve string: '{curve_str}'")
        return ECCMode(curve_mode, False)
