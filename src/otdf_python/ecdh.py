"""ECDH (Elliptic Curve Diffie-Hellman) key exchange for NanoTDF.

This module implements the ECDH key exchange protocol with HKDF key derivation
as specified in the NanoTDF spec. It supports the following curves:
- secp256r1 (NIST P-256)
- secp384r1 (NIST P-384)
- secp521r1 (NIST P-521)
- secp256k1 (Bitcoin curve)

The protocol follows ECIES methodology similar to S/MIME and GPG:
1. Generate ephemeral keypair
2. Perform ECDH with recipient's public key to get shared secret
3. Use HKDF to derive symmetric encryption key from shared secret
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

from otdf_python.ecc_constants import ECCConstants

# HKDF salt for NanoTDF key derivation
# Per spec: "salt value derived from magic number/version"
# This is the SHA-256 hash of the NanoTDF magic number and version
NANOTDF_HKDF_SALT = bytes.fromhex(
    "3de3ca1e50cf62d8b6aba603a96fca6761387a7ac86c3d3afe85ae2d1812edfc"
)


class ECDHError(Exception):
    """Base exception for ECDH operations."""

    pass


class UnsupportedCurveError(ECDHError):
    """Raised when an unsupported curve is specified."""

    pass


class InvalidKeyError(ECDHError):
    """Raised when a key is invalid or malformed."""

    pass


def get_curve(curve_name: str) -> ec.EllipticCurve:
    """Get the cryptography curve object for a given curve name.

    Args:
        curve_name: Name of the curve (e.g., "secp256r1")

    Returns:
        ec.EllipticCurve: The curve object

    Raises:
        UnsupportedCurveError: If the curve is not supported

    """
    try:
        # Delegate to ECCConstants for the authoritative mapping
        return ECCConstants.get_curve_object(curve_name)
    except ValueError as e:
        raise UnsupportedCurveError(str(e)) from e


def get_compressed_key_size(curve_name: str) -> int:
    """Get the size of a compressed public key for a given curve.

    Args:
        curve_name: Name of the curve (e.g., "secp256r1")

    Returns:
        int: Size in bytes of the compressed public key

    Raises:
        UnsupportedCurveError: If the curve is not supported

    """
    try:
        # Delegate to ECCConstants for the authoritative mapping
        return ECCConstants.get_compressed_key_size_by_name(curve_name)
    except ValueError as e:
        raise UnsupportedCurveError(str(e)) from e


def generate_ephemeral_keypair(
    curve_name: str,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an ephemeral keypair for ECDH.

    Args:
        curve_name: Name of the curve (e.g., "secp256r1")

    Returns:
        tuple: (private_key, public_key)

    Raises:
        UnsupportedCurveError: If the curve is not supported

    """
    curve = get_curve(curve_name)
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def compress_public_key(public_key: ec.EllipticCurvePublicKey) -> bytes:
    """Compress an EC public key to compressed point format.

    Args:
        public_key: The EC public key to compress

    Returns:
        bytes: Compressed public key (33-67 bytes depending on curve)

    """
    return public_key.public_bytes(
        encoding=Encoding.X962, format=PublicFormat.CompressedPoint
    )


def decompress_public_key(
    compressed_key: bytes, curve_name: str
) -> ec.EllipticCurvePublicKey:
    """Decompress a public key from compressed point format.

    Args:
        compressed_key: The compressed public key bytes
        curve_name: Name of the curve (e.g., "secp256r1")

    Returns:
        ec.EllipticCurvePublicKey: The decompressed public key

    Raises:
        InvalidKeyError: If the key cannot be decompressed
        UnsupportedCurveError: If the curve is not supported

    """
    try:
        curve = get_curve(curve_name)
        # Verify the size matches expected compressed size
        expected_size = get_compressed_key_size(curve_name)
        if len(compressed_key) != expected_size:
            raise InvalidKeyError(
                f"Invalid compressed key size for {curve_name}: "
                f"expected {expected_size} bytes, got {len(compressed_key)} bytes"
            )

        return ec.EllipticCurvePublicKey.from_encoded_point(curve, compressed_key)
    except (ValueError, TypeError) as e:
        raise InvalidKeyError(f"Failed to decompress public key: {e}") from e


def derive_shared_secret(
    private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey
) -> bytes:
    """Derive a shared secret using ECDH.

    Args:
        private_key: The private key (can be ephemeral or recipient's key)
        public_key: The public key (recipient's or ephemeral key)

    Returns:
        bytes: The raw shared secret (x-coordinate of the ECDH point)

    Raises:
        ECDHError: If ECDH fails

    """
    try:
        shared_secret = private_key.exchange(ec.ECDH(), public_key)
        return shared_secret
    except Exception as e:
        raise ECDHError(f"Failed to derive shared secret: {e}") from e


def derive_key_from_shared_secret(
    shared_secret: bytes,
    key_length: int = 32,
    salt: bytes | None = None,
    info: bytes = b"",
) -> bytes:
    """Derive a symmetric encryption key from the ECDH shared secret using HKDF.

    Args:
        shared_secret: The raw ECDH shared secret
        key_length: Length of the derived key in bytes (default: 32 for AES-256)
        salt: Optional salt for HKDF (default: NANOTDF_HKDF_SALT)
        info: Optional context/application-specific info (default: empty)

    Returns:
        bytes: Derived symmetric encryption key

    Raises:
        ECDHError: If key derivation fails

    """
    if salt is None:
        salt = NANOTDF_HKDF_SALT

    try:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=salt,
            info=info,
            backend=default_backend(),
        )
        return hkdf.derive(shared_secret)
    except Exception as e:
        raise ECDHError(f"Failed to derive key from shared secret: {e}") from e


def encrypt_key_with_ecdh(
    recipient_public_key_pem: str, curve_name: str = "secp256r1"
) -> tuple[bytes, bytes]:
    """High-level function: Generate ephemeral keypair and derive encryption key.

    This is used during NanoTDF encryption to derive the key that will be used
    to encrypt the payload. The ephemeral public key must be stored in the
    NanoTDF header so the recipient can derive the same key.

    Args:
        recipient_public_key_pem: Recipient's public key in PEM format (e.g., KAS public key)
        curve_name: Name of the curve to use (default: "secp256r1")

    Returns:
        tuple: (derived_key, compressed_ephemeral_public_key)
            - derived_key: 32-byte AES-256 key for encrypting the payload
            - compressed_ephemeral_public_key: Ephemeral public key to store in header

    Raises:
        ECDHError: If key derivation fails
        InvalidKeyError: If recipient's public key is invalid
        UnsupportedCurveError: If the curve is not supported

    """
    # Load recipient's public key
    try:
        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key_pem.encode(), backend=default_backend()
        )
        if not isinstance(recipient_public_key, ec.EllipticCurvePublicKey):
            raise InvalidKeyError("Recipient's public key is not an EC key")
    except Exception as e:
        raise InvalidKeyError(f"Failed to load recipient's public key: {e}") from e

    # Generate ephemeral keypair
    ephemeral_private_key, ephemeral_public_key = generate_ephemeral_keypair(curve_name)

    # Derive shared secret
    shared_secret = derive_shared_secret(ephemeral_private_key, recipient_public_key)

    # Derive encryption key from shared secret
    derived_key = derive_key_from_shared_secret(shared_secret, key_length=32)

    # Compress ephemeral public key for storage in header
    compressed_ephemeral_key = compress_public_key(ephemeral_public_key)

    return derived_key, compressed_ephemeral_key


def decrypt_key_with_ecdh(
    recipient_private_key_pem: str,
    compressed_ephemeral_public_key: bytes,
    curve_name: str = "secp256r1",
) -> bytes:
    """High-level function: Derive decryption key from ephemeral public key and recipient's private key.

    This is used during NanoTDF decryption to derive the same key that was used
    to encrypt the payload. The ephemeral public key is extracted from the
    NanoTDF header.

    Args:
        recipient_private_key_pem: Recipient's private key in PEM format (e.g., KAS private key)
        compressed_ephemeral_public_key: Ephemeral public key from NanoTDF header
        curve_name: Name of the curve (default: "secp256r1")

    Returns:
        bytes: 32-byte AES-256 key for decrypting the payload

    Raises:
        ECDHError: If key derivation fails
        InvalidKeyError: If keys are invalid
        UnsupportedCurveError: If the curve is not supported

    """
    # Load recipient's private key
    try:
        recipient_private_key = serialization.load_pem_private_key(
            recipient_private_key_pem.encode(), password=None, backend=default_backend()
        )
        if not isinstance(recipient_private_key, ec.EllipticCurvePrivateKey):
            raise InvalidKeyError("Recipient's private key is not an EC key")
    except Exception as e:
        raise InvalidKeyError(f"Failed to load recipient's private key: {e}") from e

    # Decompress ephemeral public key
    ephemeral_public_key = decompress_public_key(
        compressed_ephemeral_public_key, curve_name
    )

    # Derive shared secret
    shared_secret = derive_shared_secret(recipient_private_key, ephemeral_public_key)

    # Derive decryption key from shared secret
    derived_key = derive_key_from_shared_secret(shared_secret, key_length=32)

    return derived_key
