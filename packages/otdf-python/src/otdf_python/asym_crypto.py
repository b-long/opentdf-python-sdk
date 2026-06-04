"""Asymmetric encryption and decryption utilities for RSA keys in PEM format."""

import base64
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509 import load_pem_x509_certificate

from .sdk_exceptions import SDKException


class AsymDecryption:
    """Provides functionality for asymmetric decryption using an RSA private key.

    Supports both PEM string and key object initialization for flexibility.
    """

    CIPHER_TRANSFORM = "RSA/ECB/OAEPWithSHA-1AndMGF1Padding"
    PRIVATE_KEY_HEADER = "-----BEGIN PRIVATE KEY-----"
    PRIVATE_KEY_FOOTER = "-----END PRIVATE KEY-----"

    def __init__(self, private_key_pem: str | None = None, private_key_obj=None):
        """Initialize with either a PEM string or a key object.

        Args:
            private_key_pem: Private key in PEM format (with or without headers)
            private_key_obj: Pre-loaded private key object from cryptography library

        Raises:
            SDKException: If key loading fails

        """
        if private_key_obj is not None:
            self.private_key = private_key_obj
        elif private_key_pem is not None:
            try:
                # Try direct PEM loading first (most common case)
                try:
                    self.private_key = serialization.load_pem_private_key(
                        private_key_pem.encode(),
                        password=None,
                        backend=default_backend(),
                    )
                except Exception:
                    # Fallback: strip headers and load as DER (for base64-only keys)
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
                raise SDKException(f"Failed to load private key: {e}") from e
        else:
            self.private_key = None

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data using RSA OAEP with SHA-1.

        Args:
            data: Encrypted bytes to decrypt

        Returns:
            Decrypted bytes

        Raises:
            SDKException: If decryption fails or key is not set

        """
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
            raise SDKException(f"Error performing decryption: {e}") from e


class AsymEncryption:
    """Provides functionality for asymmetric encryption using an RSA public key or certificate in PEM format.

    Supports PEM public keys, X.509 certificates, and pre-loaded key objects.
    Also handles base64-encoded keys without PEM headers.
    """

    PUBLIC_KEY_HEADER = "-----BEGIN PUBLIC KEY-----"
    PUBLIC_KEY_FOOTER = "-----END PUBLIC KEY-----"
    CIPHER_TRANSFORM = "RSA/ECB/OAEPWithSHA-1AndMGF1Padding"

    def __init__(self, public_key_pem: str | None = None, public_key_obj=None):
        """Initialize with either a PEM string or a key object.

        Args:
            public_key_pem: Public key in PEM format, X.509 certificate, or base64 string
            public_key_obj: Pre-loaded public key object from cryptography library

        Raises:
            SDKException: If key loading fails or key is not RSA

        """
        if public_key_obj is not None:
            self.public_key = public_key_obj
        elif public_key_pem is not None:
            try:
                if "BEGIN CERTIFICATE" in public_key_pem:
                    # Load from X.509 certificate
                    cert = load_pem_x509_certificate(
                        public_key_pem.encode(), default_backend()
                    )
                    self.public_key = cert.public_key()
                else:
                    # Try direct PEM loading first (most common case)
                    try:
                        self.public_key = serialization.load_pem_public_key(
                            public_key_pem.encode(), backend=default_backend()
                        )
                    except Exception:
                        # Fallback: strip headers and load as DER (for base64-only keys)
                        pem_body = re.sub(r"-----BEGIN (.*)-----", "", public_key_pem)
                        pem_body = re.sub(r"-----END (.*)-----", "", pem_body)
                        pem_body = re.sub(r"\s", "", pem_body)
                        decoded = base64.b64decode(pem_body)
                        self.public_key = serialization.load_der_public_key(
                            decoded, backend=default_backend()
                        )
            except Exception as e:
                raise SDKException(f"Failed to load public key: {e}") from e
        else:
            self.public_key = None

        # Validate that it's an RSA key
        if self.public_key is not None and not isinstance(
            self.public_key, rsa.RSAPublicKey
        ):
            raise SDKException("Not an RSA PEM formatted public key")

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using RSA OAEP with SHA-1.

        Args:
            data: Plaintext bytes to encrypt

        Returns:
            Encrypted bytes

        Raises:
            SDKException: If encryption fails or key is not set

        """
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
            raise SDKException(f"Error performing encryption: {e}") from e

    def public_key_in_pem_format(self) -> str:
        """Export the public key to PEM format.

        Returns:
            Public key as PEM-encoded string

        Raises:
            SDKException: If export fails

        """
        try:
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            return pem.decode()
        except Exception as e:
            raise SDKException(f"Error exporting public key to PEM: {e}") from e
