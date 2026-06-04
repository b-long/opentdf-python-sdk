"""Key type constants for RSA and EC encryption."""

from enum import Enum


class KeyType(Enum):
    """Key type enumeration for encryption algorithms."""

    RSA2048Key = "rsa:2048"
    EC256Key = "ec:secp256r1"
    EC384Key = "ec:secp384r1"
    EC521Key = "ec:secp521r1"

    def __str__(self):
        return self.value

    def get_curve_name(self):
        if self == KeyType.EC256Key:
            return "secp256r1"
        elif self == KeyType.EC384Key:
            return "secp384r1"
        elif self == KeyType.EC521Key:
            return "secp521r1"
        else:
            raise ValueError(f"Unsupported key type: {self}")

    @staticmethod
    def from_string(key_type):
        for t in KeyType:
            if t.value.lower() == key_type.lower():
                return t
        raise ValueError(f"No enum constant for key type: {key_type}")

    def is_ec(self):
        return self != KeyType.RSA2048Key
