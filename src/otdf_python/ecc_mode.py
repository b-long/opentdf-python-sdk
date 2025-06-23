class ECCMode:
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

    @staticmethod
    def get_ec_compressed_pubkey_size(curve_type: int) -> int:
        # 0: secp256r1, 1: secp384r1, 2: secp521r1
        if curve_type == 0:
            return 33
        elif curve_type == 1:
            return 49
        elif curve_type == 2:
            return 67
        else:
            raise ValueError("Unsupported ECC algorithm.")

    def get_ecc_mode_as_byte(self) -> int:
        # Most significant bit: use_ecdsa_binding, lower 3 bits: curve_mode
        return ((1 if self.use_ecdsa_binding else 0) << 7) | (self.curve_mode & 0x07)
