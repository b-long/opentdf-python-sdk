"""
Asymmetric encryption and decryption utilities for RSA keys in PEM format.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509 import load_pem_x509_certificate

from .sdk_exceptions import SDKException


class AsymDecryption:
    """
    Provides functionality for asymmetric decryption using an RSA private key.
    """

    def __init__(self, private_key_pem: str):
        try:
            self.private_key = serialization.load_pem_private_key(
                private_key_pem.encode(), password=None, backend=default_backend()
            )
        except Exception as e:
            raise SDKException(f"Failed to load private key: {e}")

    def decrypt(self, data: bytes) -> bytes:
        if not self.private_key:
            raise SDKException("Failed to decrypt, private key is empty")
        try:
            return self.private_key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
            )
        except Exception as e:
            raise SDKException(f"Error performing decryption: {e}")


class AsymEncryption:
    """
    Provides functionality for asymmetric encryption using an RSA public key or certificate in PEM format.
    """

    def __init__(self, public_key_pem: str):
        try:
            if "BEGIN CERTIFICATE" in public_key_pem:
                cert = load_pem_x509_certificate(
                    public_key_pem.encode(), default_backend()
                )
                self.public_key = cert.public_key()
            else:
                self.public_key = serialization.load_pem_public_key(
                    public_key_pem.encode(), backend=default_backend()
                )
        except Exception as e:
            raise SDKException(f"Failed to load public key: {e}")

        if not isinstance(self.public_key, rsa.RSAPublicKey):
            raise SDKException("Not an RSA PEM formatted public key")

    def encrypt(self, data: bytes) -> bytes:
        try:
            return self.public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
            )
        except Exception as e:
            raise SDKException(f"Error performing encryption: {e}")

    def public_key_in_pem_format(self) -> str:
        try:
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            return pem.decode()
        except Exception as e:
            raise SDKException(f"Error exporting public key to PEM: {e}")
