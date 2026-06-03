"""Elliptic Curve Constants for NanoTDF.

This module defines shared constants for elliptic curve operations used across
the SDK, particularly for NanoTDF encryption/decryption.

All supported curves follow the NanoTDF specification which uses compressed
public key encoding (X9.62 format) to minimize header size.
"""

from typing import ClassVar

from cryptography.hazmat.primitives.asymmetric import ec


class ECCConstants:
    """Centralized constants for elliptic curve cryptography operations.

    This class provides mappings between curve names, curve type integers,
    cryptography curve objects, and compressed public key sizes.
    """

    # Mapping from curve names (strings) to curve type integers (per NanoTDF spec)
    # These integer values are encoded in the NanoTDF header's ECC mode byte
    CURVE_NAME_TO_TYPE: ClassVar[dict[str, int]] = {
        "secp256r1": 0,  # NIST P-256 (most common)
        "secp384r1": 1,  # NIST P-384
        "secp521r1": 2,  # NIST P-521
        "secp256k1": 3,  # Bitcoin curve (secp256k1)
    }

    # Mapping from curve type integers to curve names
    # Inverse of CURVE_NAME_TO_TYPE for reverse lookups
    CURVE_TYPE_TO_NAME: ClassVar[dict[int, str]] = {
        0: "secp256r1",
        1: "secp384r1",
        2: "secp521r1",
        3: "secp256k1",
    }

    # Compressed public key sizes (in bytes) for each curve
    # Format: 1 byte prefix (0x02 or 0x03) + x-coordinate bytes
    # Used by both ecc_mode.py (indexed by int) and ecdh.py (indexed by string)
    COMPRESSED_KEY_SIZE_BY_TYPE: ClassVar[dict[int, int]] = {
        0: 33,  # secp256r1: 1 byte prefix + 32 bytes x-coordinate
        1: 49,  # secp384r1: 1 byte prefix + 48 bytes x-coordinate
        2: 67,  # secp521r1: 1 byte prefix + 66 bytes x-coordinate
        3: 33,  # secp256k1: 1 byte prefix + 32 bytes x-coordinate (same as secp256r1)
    }

    COMPRESSED_KEY_SIZE_BY_NAME: ClassVar[dict[str, int]] = {
        "secp256r1": 33,  # 1 byte prefix + 32 bytes
        "secp384r1": 49,  # 1 byte prefix + 48 bytes
        "secp521r1": 67,  # 1 byte prefix + 66 bytes
        "secp256k1": 33,  # 1 byte prefix + 32 bytes
    }

    # Mapping from curve names to cryptography library curve objects
    # Used by ecdh.py for key generation and ECDH operations
    CURVE_OBJECTS: ClassVar[dict[str, ec.EllipticCurve]] = {
        "secp256r1": ec.SECP256R1(),
        "secp384r1": ec.SECP384R1(),
        "secp521r1": ec.SECP521R1(),
        "secp256k1": ec.SECP256K1(),
    }

    @classmethod
    def get_curve_name(cls, curve_type: int) -> str:
        """Get curve name from curve type integer.

        Args:
            curve_type: Curve type (0=secp256r1, 1=secp384r1, 2=secp521r1, 3=secp256k1)

        Returns:
            Curve name as string (e.g., "secp256r1")

        Raises:
            ValueError: If curve_type is not supported

        """
        name = cls.CURVE_TYPE_TO_NAME.get(curve_type)
        if name is None:
            raise ValueError(
                f"Unsupported curve type: {curve_type}. "
                f"Supported types: {list(cls.CURVE_TYPE_TO_NAME.keys())}"
            )
        return name

    @classmethod
    def get_curve_type(cls, curve_name: str) -> int:
        """Get curve type integer from curve name.

        Args:
            curve_name: Curve name (e.g., "secp256r1")

        Returns:
            Curve type as integer (0-3)

        Raises:
            ValueError: If curve_name is not supported

        """
        curve_type = cls.CURVE_NAME_TO_TYPE.get(curve_name.lower())
        if curve_type is None:
            raise ValueError(
                f"Unsupported curve name: '{curve_name}'. "
                f"Supported curves: {list(cls.CURVE_NAME_TO_TYPE.keys())}"
            )
        return curve_type

    @classmethod
    def get_compressed_key_size_by_type(cls, curve_type: int) -> int:
        """Get compressed public key size from curve type integer.

        Args:
            curve_type: Curve type (0=secp256r1, 1=secp384r1, 2=secp521r1, 3=secp256k1)

        Returns:
            Size in bytes of the compressed public key

        Raises:
            ValueError: If curve_type is not supported

        """
        size = cls.COMPRESSED_KEY_SIZE_BY_TYPE.get(curve_type)
        if size is None:
            raise ValueError(
                f"Unsupported curve type: {curve_type}. "
                f"Supported types: {list(cls.COMPRESSED_KEY_SIZE_BY_TYPE.keys())}"
            )
        return size

    @classmethod
    def get_compressed_key_size_by_name(cls, curve_name: str) -> int:
        """Get compressed public key size from curve name.

        Args:
            curve_name: Curve name (e.g., "secp256r1")

        Returns:
            Size in bytes of the compressed public key

        Raises:
            ValueError: If curve_name is not supported

        """
        size = cls.COMPRESSED_KEY_SIZE_BY_NAME.get(curve_name.lower())
        if size is None:
            raise ValueError(
                f"Unsupported curve name: '{curve_name}'. "
                f"Supported curves: {list(cls.COMPRESSED_KEY_SIZE_BY_NAME.keys())}"
            )
        return size

    @classmethod
    def get_curve_object(cls, curve_name: str) -> ec.EllipticCurve:
        """Get cryptography library curve object from curve name.

        Args:
            curve_name: Curve name (e.g., "secp256r1")

        Returns:
            Cryptography library EllipticCurve object

        Raises:
            ValueError: If curve_name is not supported

        """
        curve = cls.CURVE_OBJECTS.get(curve_name.lower())
        if curve is None:
            raise ValueError(
                f"Unsupported curve name: '{curve_name}'. "
                f"Supported curves: {list(cls.CURVE_OBJECTS.keys())}"
            )
        return curve
