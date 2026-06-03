"""AES-GCM encryption and decryption functionality."""

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AesGcm:
    """AES-GCM encryption and decryption operations."""

    GCM_NONCE_LENGTH = 12
    GCM_TAG_LENGTH = 16

    def __init__(self, key: bytes):
        """Initialize AES-GCM cipher with key."""
        if not key or len(key) not in (16, 24, 32):
            raise ValueError("Invalid key size for GCM encryption")
        self.key = key
        self.aesgcm = AESGCM(key)

    def get_key(self) -> bytes:
        return self.key

    class Encrypted:
        """Encrypted data with initialization vector and ciphertext."""

        def __init__(self, iv: bytes, ciphertext: bytes):
            """Initialize encrypted data."""
            self.iv = iv
            self.ciphertext = ciphertext

        def as_bytes(self) -> bytes:
            return self.iv + self.ciphertext

    def encrypt(
        self, plaintext: bytes, offset: int = 0, length: int | None = None
    ) -> "AesGcm.Encrypted":
        if length is None:
            length = len(plaintext) - offset
        iv = os.urandom(self.GCM_NONCE_LENGTH)
        ct = self.aesgcm.encrypt(iv, plaintext[offset : offset + length], None)
        return self.Encrypted(iv, ct)

    def encrypt_with_iv(
        self,
        iv: bytes,
        auth_tag_len: int,
        plaintext: bytes,
        offset: int = 0,
        length: int | None = None,
    ) -> bytes:
        if length is None:
            length = len(plaintext) - offset
        ct = self.aesgcm.encrypt(iv, plaintext[offset : offset + length], None)
        return iv + ct

    def decrypt(self, encrypted: "AesGcm.Encrypted") -> bytes:
        return self.aesgcm.decrypt(encrypted.iv, encrypted.ciphertext, None)

    def decrypt_with_iv(
        self, iv: bytes, auth_tag_len: int, cipher_data: bytes
    ) -> bytes:
        return self.aesgcm.decrypt(iv, cipher_data, None)
