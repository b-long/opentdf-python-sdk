"""Cryptographic utility functions."""

import hashlib
import hmac

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa


class CryptoUtils:
    """Cryptographic utility functions and helpers."""

    KEYPAIR_SIZE = 2048

    @staticmethod
    def calculate_sha256_hmac(key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, hashlib.sha256).digest()

    @staticmethod
    def generate_rsa_keypair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=CryptoUtils.KEYPAIR_SIZE,
            backend=default_backend(),
        )
        return private_key, private_key.public_key()

    @staticmethod
    def generate_ec_keypair(
        curve=None,
    ) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
        if curve is None:
            curve = ec.SECP256R1()
        private_key = ec.generate_private_key(curve, default_backend())
        return private_key, private_key.public_key()

    @staticmethod
    def get_public_key_pem(public_key) -> str:
        return public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    @staticmethod
    def get_private_key_pem(private_key) -> str:
        return private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

    @staticmethod
    def get_rsa_public_key_pem(public_key) -> str:
        if public_key.__class__.__name__ != "RSAPublicKey":
            raise ValueError("Not an RSA public key")
        return CryptoUtils.get_public_key_pem(public_key)

    @staticmethod
    def get_rsa_private_key_pem(private_key) -> str:
        if private_key.__class__.__name__ != "RSAPrivateKey":
            raise ValueError("Not an RSA private key")
        return CryptoUtils.get_private_key_pem(private_key)

    @staticmethod
    def get_rsa_public_key_from_pem(pem_data: str) -> rsa.RSAPublicKey:
        """Load RSA public key from PEM string."""
        public_key = serialization.load_pem_public_key(
            pem_data.encode(), backend=default_backend()
        )
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise ValueError("Not an RSA public key")
        return public_key

    @staticmethod
    def get_rsa_private_key_from_pem(pem_data: str) -> rsa.RSAPrivateKey:
        """Load RSA private key from PEM string."""
        private_key = serialization.load_pem_private_key(
            pem_data.encode(), password=None, backend=default_backend()
        )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise ValueError("Not an RSA private key")
        return private_key
