"""Elliptic Curve key pair management."""

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)


class ECKeyPair:
    """Elliptic Curve key pair for cryptographic operations."""

    def __init__(self, curve=None):
        """Initialize EC key pair."""
        if curve is None:
            curve = ec.SECP256R1()
        self.private_key = ec.generate_private_key(curve, default_backend())
        self.public_key = self.private_key.public_key()
        self.curve = curve

    def public_key_pem(self):
        return self.public_key.public_bytes(
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def private_key_pem(self):
        return self.private_key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
        ).decode()

    def key_size(self):
        return self.private_key.key_size

    def compress_public_key(self):
        return self.public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    @staticmethod
    def public_key_from_pem(pem):
        return serialization.load_pem_public_key(
            pem.encode(), backend=default_backend()
        )

    @staticmethod
    def private_key_from_pem(pem):
        return serialization.load_pem_private_key(
            pem.encode(), password=None, backend=default_backend()
        )

    @staticmethod
    def compute_ecdh_key(public_key, private_key):
        return private_key.exchange(ec.ECDH(), public_key)

    @staticmethod
    def calculate_hkdf(salt, secret, length=32):
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            info=None,
            backend=default_backend(),
        )
        return hkdf.derive(secret)

    @staticmethod
    def sign_ecdsa(data, private_key):
        return private_key.sign(data, ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify_ecdsa(data, signature, public_key):
        try:
            public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
