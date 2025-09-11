import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .sdk_exceptions import SDKException


class AsymDecryption:
    """
    Class providing functionality for asymmetric decryption using an RSA private key.
    """

    CIPHER_TRANSFORM = "RSA/ECB/OAEPWithSHA-1AndMGF1Padding"
    PRIVATE_KEY_HEADER = "-----BEGIN PRIVATE KEY-----"
    PRIVATE_KEY_FOOTER = "-----END PRIVATE KEY-----"

    def __init__(self, private_key_pem: str | None = None, private_key_obj=None):
        if private_key_obj is not None:
            self.private_key = private_key_obj
        elif private_key_pem is not None:
            try:
                private_key_pem = (
                    private_key_pem.replace(self.PRIVATE_KEY_HEADER, "")
                    .replace(self.PRIVATE_KEY_FOOTER, "")
                    .replace("\n", "")
                    .replace("\r", "")
                    .replace(" ", "")
                )
                decoded = base64.b64decode(private_key_pem)
                self.private_key = serialization.load_der_private_key(
                    decoded, password=None, backend=default_backend()
                )
            except Exception as e:
                raise SDKException(f"Failed to load private key: {e}")
        else:
            self.private_key = None

    def decrypt(self, data: bytes) -> bytes:
        if self.private_key is None:
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
