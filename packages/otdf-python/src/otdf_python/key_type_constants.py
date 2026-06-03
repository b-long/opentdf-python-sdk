"""Constants for session key types used in the KAS client.
This matches the Java SDK's KeyType enum pattern.
"""

from enum import Enum, auto


class KeyType(Enum):
    """Enum for key types used in the KAS client."""

    RSA2048 = auto()
    EC_P256 = auto()
    EC_P384 = auto()
    EC_P521 = auto()

    @property
    def is_ec(self):
        """Returns True if this key type is an EC key, False otherwise."""
        return self in [KeyType.EC_P256, KeyType.EC_P384, KeyType.EC_P521]

    @property
    def curve_name(self):
        """Returns the curve name for EC keys."""
        if self == KeyType.EC_P256:
            return "P-256"
        elif self == KeyType.EC_P384:
            return "P-384"
        elif self == KeyType.EC_P521:
            return "P-521"
        else:
            return None


# Constants for backward compatibility with string literals
RSA_KEY_TYPE = KeyType.RSA2048
EC_KEY_TYPE = KeyType.EC_P256  # Default EC curve
