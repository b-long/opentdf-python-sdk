"""NanoTDF type enumeration."""

from enum import Enum


class ECCurve(Enum):
    """Elliptic curve enumeration for NanoTDF."""

    SECP256R1 = "secp256r1"
    SECP384R1 = "secp384r1"
    SECP521R1 = "secp384r1"
    SECP256K1 = "secp256k1"

    def __str__(self):
        return self.value


class Protocol(Enum):
    """Protocol enumeration for KAS communication."""

    HTTP = "HTTP"
    HTTPS = "HTTPS"


class IdentifierType(Enum):
    """Identifier type enumeration for NanoTDF."""

    NONE = 0
    TWO_BYTES = 2
    EIGHT_BYTES = 8
    THIRTY_TWO_BYTES = 32

    def get_length(self):
        return self.value


class PolicyType(Enum):
    """Policy type enumeration for NanoTDF."""

    REMOTE_POLICY = 0
    EMBEDDED_POLICY_PLAIN_TEXT = 1
    EMBEDDED_POLICY_ENCRYPTED = 2
    EMBEDDED_POLICY_ENCRYPTED_POLICY_KEY_ACCESS = 3


class Cipher(Enum):
    """Cipher enumeration for NanoTDF encryption."""

    AES_256_GCM_64_TAG = 0
    AES_256_GCM_96_TAG = 1
    AES_256_GCM_104_TAG = 2
    AES_256_GCM_112_TAG = 3
    AES_256_GCM_120_TAG = 4
    AES_256_GCM_128_TAG = 5
    EAD_AES_256_HMAC_SHA_256 = 6
