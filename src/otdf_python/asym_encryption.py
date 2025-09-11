import base64
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate

from .sdk_exceptions import SDKException


class AsymEncryption:
    """
    Provides methods for asymmetric encryption and handling public keys in PEM format.
    """

    PUBLIC_KEY_HEADER = "-----BEGIN PUBLIC KEY-----"
    PUBLIC_KEY_FOOTER = "-----END PUBLIC KEY-----"
    CIPHER_TRANSFORM = "RSA/ECB/OAEPWithSHA-1AndMGF1Padding"

    def __init__(self, public_key_pem: str | None = None, public_key_obj=None):
        if public_key_obj is not None:
            self.public_key = public_key_obj
        elif public_key_pem is not None:
            try:
                if "BEGIN CERTIFICATE" in public_key_pem:
                    cert = load_pem_x509_certificate(
                        public_key_pem.encode(), default_backend()
                    )
                    self.public_key = cert.public_key()
                else:
                    # Remove PEM headers/footers and whitespace
                    pem_body = re.sub(r"-----BEGIN (.*)-----", "", public_key_pem)
                    pem_body = re.sub(r"-----END (.*)-----", "", pem_body)
                    pem_body = re.sub(r"\s", "", pem_body)
                    decoded = base64.b64decode(pem_body)
                    self.public_key = serialization.load_der_public_key(
                        decoded, backend=default_backend()
                    )
            except Exception as e:
                raise SDKException(f"Failed to load public key: {e}")
        else:
            self.public_key = None

        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

        if self.public_key is not None and not isinstance(
            self.public_key, RSAPublicKey
        ):
            raise SDKException("Not an RSA PEM formatted public key")

    def encrypt(self, data: bytes) -> bytes:
        if self.public_key is None:
            raise SDKException("Failed to encrypt, public key is empty")
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
