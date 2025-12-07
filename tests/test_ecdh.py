"""Unit tests for ECDH key exchange module."""

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from otdf_python.ecc_constants import ECCConstants
from otdf_python.ecdh import (
    InvalidKeyError,
    UnsupportedCurveError,
    compress_public_key,
    decompress_public_key,
    decrypt_key_with_ecdh,
    derive_key_from_shared_secret,
    derive_shared_secret,
    encrypt_key_with_ecdh,
    generate_ephemeral_keypair,
    get_compressed_key_size,
    get_curve,
)


class TestCurveOperations:
    """Test basic curve operations."""

    def test_get_curve_secp256r1(self):
        """Test getting secp256r1 curve."""
        curve = get_curve("secp256r1")
        assert isinstance(curve, ec.SECP256R1)

    def test_get_curve_secp384r1(self):
        """Test getting secp384r1 curve."""
        curve = get_curve("secp384r1")
        assert isinstance(curve, ec.SECP384R1)

    def test_get_curve_secp521r1(self):
        """Test getting secp521r1 curve."""
        curve = get_curve("secp521r1")
        assert isinstance(curve, ec.SECP521R1)

    def test_get_curve_secp256k1(self):
        """Test getting secp256k1 curve."""
        curve = get_curve("secp256k1")
        assert isinstance(curve, ec.SECP256K1)

    def test_get_curve_case_insensitive(self):
        """Test that curve names are case-insensitive."""
        curve1 = get_curve("SECP256R1")
        curve2 = get_curve("secp256r1")
        assert type(curve1) is type(curve2)

    def test_get_curve_unsupported(self):
        """Test that unsupported curves raise an error."""
        with pytest.raises(UnsupportedCurveError):
            get_curve("unsupported_curve")

    def test_get_compressed_key_size(self):
        """Test getting compressed key sizes for all curves."""
        assert get_compressed_key_size("secp256r1") == 33
        assert get_compressed_key_size("secp384r1") == 49
        assert get_compressed_key_size("secp521r1") == 67
        assert get_compressed_key_size("secp256k1") == 33

    def test_get_compressed_key_size_unsupported(self):
        """Test that unsupported curves raise an error."""
        with pytest.raises(UnsupportedCurveError):
            get_compressed_key_size("unsupported")


class TestKeypairGeneration:
    """Test ephemeral keypair generation."""

    def test_generate_keypair_secp256r1(self):
        """Test generating a keypair for secp256r1."""
        private_key, public_key = generate_ephemeral_keypair("secp256r1")
        assert isinstance(private_key, ec.EllipticCurvePrivateKey)
        assert isinstance(public_key, ec.EllipticCurvePublicKey)
        assert isinstance(private_key.curve, ec.SECP256R1)

    def test_generate_keypair_all_curves(self):
        """Test generating keypairs for all supported curves."""
        for curve_name in ["secp256r1", "secp384r1", "secp521r1", "secp256k1"]:
            private_key, public_key = generate_ephemeral_keypair(curve_name)
            assert isinstance(private_key, ec.EllipticCurvePrivateKey)
            assert isinstance(public_key, ec.EllipticCurvePublicKey)

    def test_generate_keypair_unique(self):
        """Test that generated keypairs are unique."""
        _, pub1 = generate_ephemeral_keypair("secp256r1")
        _, pub2 = generate_ephemeral_keypair("secp256r1")

        # Compress and compare - should be different
        compressed1 = compress_public_key(pub1)
        compressed2 = compress_public_key(pub2)
        assert compressed1 != compressed2


class TestPublicKeyCompression:
    """Test public key compression and decompression."""

    def test_compress_public_key(self):
        """Test compressing a public key."""
        _, public_key = generate_ephemeral_keypair("secp256r1")
        compressed = compress_public_key(public_key)

        # Should be 33 bytes for secp256r1
        assert len(compressed) == 33
        # First byte should be 0x02 or 0x03 (compressed point format)
        assert compressed[0] in (0x02, 0x03)

    def test_compress_all_curves(self):
        """Test compressing public keys for all curves."""
        for (
            curve_name,
            expected_size,
        ) in ECCConstants.COMPRESSED_KEY_SIZE_BY_NAME.items():
            _, public_key = generate_ephemeral_keypair(curve_name)
            compressed = compress_public_key(public_key)
            assert len(compressed) == expected_size

    def test_decompress_public_key(self):
        """Test decompressing a public key."""
        _, original_public_key = generate_ephemeral_keypair("secp256r1")
        compressed = compress_public_key(original_public_key)

        # Decompress
        decompressed = decompress_public_key(compressed, "secp256r1")

        # Should be able to get the same bytes back
        compressed_again = compress_public_key(decompressed)
        assert compressed == compressed_again

    def test_decompress_all_curves(self):
        """Test decompressing public keys for all curves."""
        for curve_name in ["secp256r1", "secp384r1", "secp521r1", "secp256k1"]:
            _, original_public_key = generate_ephemeral_keypair(curve_name)
            compressed = compress_public_key(original_public_key)

            decompressed = decompress_public_key(compressed, curve_name)
            compressed_again = compress_public_key(decompressed)
            assert compressed == compressed_again

    def test_decompress_invalid_size(self):
        """Test that decompressing with wrong size raises an error."""
        with pytest.raises(InvalidKeyError):
            # Too short for secp256r1
            decompress_public_key(b"\x02" + b"\x00" * 31, "secp256r1")

    def test_decompress_invalid_data(self):
        """Test that decompressing invalid data raises an error."""
        with pytest.raises(InvalidKeyError):
            # Invalid compressed point (wrong prefix)
            decompress_public_key(b"\xff" + b"\x00" * 32, "secp256r1")


class TestSharedSecret:
    """Test ECDH shared secret derivation."""

    def test_derive_shared_secret(self):
        """Test deriving a shared secret."""
        # Alice's keypair
        alice_private, alice_public = generate_ephemeral_keypair("secp256r1")
        # Bob's keypair
        bob_private, bob_public = generate_ephemeral_keypair("secp256r1")

        # Alice computes shared secret with Bob's public key
        secret_alice = derive_shared_secret(alice_private, bob_public)
        # Bob computes shared secret with Alice's public key
        secret_bob = derive_shared_secret(bob_private, alice_public)

        # Should be the same
        assert secret_alice == secret_bob
        # Should be 32 bytes for secp256r1
        assert len(secret_alice) == 32

    def test_derive_shared_secret_all_curves(self):
        """Test deriving shared secrets for all curves."""
        for curve_name in ["secp256r1", "secp384r1", "secp521r1", "secp256k1"]:
            alice_private, alice_public = generate_ephemeral_keypair(curve_name)
            bob_private, bob_public = generate_ephemeral_keypair(curve_name)

            secret_alice = derive_shared_secret(alice_private, bob_public)
            secret_bob = derive_shared_secret(bob_private, alice_public)

            assert secret_alice == secret_bob
            assert len(secret_alice) > 0


class TestKeyDerivation:
    """Test HKDF key derivation from shared secret."""

    def test_derive_key_default(self):
        """Test deriving a key with default parameters."""
        # Use a dummy shared secret
        shared_secret = b"test_shared_secret_32_bytes!!!!!"

        key = derive_key_from_shared_secret(shared_secret)

        # Should be 32 bytes (default for AES-256)
        assert len(key) == 32
        # Should be deterministic
        key2 = derive_key_from_shared_secret(shared_secret)
        assert key == key2

    def test_derive_key_custom_length(self):
        """Test deriving keys of different lengths."""
        shared_secret = b"test_shared_secret"

        key_16 = derive_key_from_shared_secret(shared_secret, key_length=16)
        key_32 = derive_key_from_shared_secret(shared_secret, key_length=32)
        key_64 = derive_key_from_shared_secret(shared_secret, key_length=64)

        assert len(key_16) == 16
        assert len(key_32) == 32
        assert len(key_64) == 64

    def test_derive_key_custom_salt(self):
        """Test deriving keys with custom salt."""
        shared_secret = b"test_shared_secret"

        key1 = derive_key_from_shared_secret(shared_secret, salt=b"salt1")
        key2 = derive_key_from_shared_secret(shared_secret, salt=b"salt2")

        # Different salts should produce different keys
        assert key1 != key2

    def test_derive_key_custom_info(self):
        """Test deriving keys with custom info."""
        shared_secret = b"test_shared_secret"

        key1 = derive_key_from_shared_secret(shared_secret, info=b"info1")
        key2 = derive_key_from_shared_secret(shared_secret, info=b"info2")

        # Different info should produce different keys
        assert key1 != key2


class TestHighLevelEncryption:
    """Test high-level encrypt_key_with_ecdh function."""

    def test_encrypt_key_with_ecdh(self):
        """Test the high-level encryption function."""
        # Generate a recipient keypair (e.g., KAS)
        _recipient_private, recipient_public = generate_ephemeral_keypair("secp256r1")

        # Get PEM format
        recipient_public_pem = recipient_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        # Encrypt (generate ephemeral key and derive encryption key)
        derived_key, compressed_ephemeral_key = encrypt_key_with_ecdh(
            recipient_public_pem, curve_name="secp256r1"
        )

        # Verify results
        assert len(derived_key) == 32  # AES-256 key
        assert len(compressed_ephemeral_key) == 33  # Compressed secp256r1 key

    def test_encrypt_key_all_curves(self):
        """Test encryption with all supported curves."""
        for curve_name in ["secp256r1", "secp384r1", "secp521r1", "secp256k1"]:
            _recipient_private, recipient_public = generate_ephemeral_keypair(
                curve_name
            )
            recipient_public_pem = recipient_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()

            derived_key, compressed_ephemeral_key = encrypt_key_with_ecdh(
                recipient_public_pem, curve_name=curve_name
            )

            assert len(derived_key) == 32
            expected_size = ECCConstants.COMPRESSED_KEY_SIZE_BY_NAME[curve_name]
            assert len(compressed_ephemeral_key) == expected_size

    def test_encrypt_key_invalid_recipient_key(self):
        """Test that invalid recipient keys raise an error."""
        with pytest.raises(InvalidKeyError):
            encrypt_key_with_ecdh("not a valid pem key")


class TestHighLevelDecryption:
    """Test high-level decrypt_key_with_ecdh function."""

    def test_decrypt_key_with_ecdh(self):
        """Test the high-level decryption function."""
        # Generate a recipient keypair (e.g., KAS)
        recipient_private, recipient_public = generate_ephemeral_keypair("secp256r1")

        # Get PEM formats
        recipient_public_pem = recipient_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        recipient_private_pem = recipient_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Encrypt (sender side)
        derived_key_encrypt, compressed_ephemeral_key = encrypt_key_with_ecdh(
            recipient_public_pem, curve_name="secp256r1"
        )

        # Decrypt (recipient side)
        derived_key_decrypt = decrypt_key_with_ecdh(
            recipient_private_pem, compressed_ephemeral_key, curve_name="secp256r1"
        )

        # Keys should match
        assert derived_key_encrypt == derived_key_decrypt

    def test_decrypt_key_all_curves(self):
        """Test decryption with all supported curves."""
        for curve_name in ["secp256r1", "secp384r1", "secp521r1", "secp256k1"]:
            recipient_private, recipient_public = generate_ephemeral_keypair(curve_name)

            recipient_public_pem = recipient_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()
            recipient_private_pem = recipient_private.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode()

            # Encrypt
            derived_key_encrypt, compressed_ephemeral_key = encrypt_key_with_ecdh(
                recipient_public_pem, curve_name=curve_name
            )

            # Decrypt
            derived_key_decrypt = decrypt_key_with_ecdh(
                recipient_private_pem, compressed_ephemeral_key, curve_name=curve_name
            )

            # Should match
            assert derived_key_encrypt == derived_key_decrypt

    def test_decrypt_key_invalid_private_key(self):
        """Test that invalid private keys raise an error."""
        _, pub = generate_ephemeral_keypair("secp256r1")
        compressed = compress_public_key(pub)

        with pytest.raises(InvalidKeyError):
            decrypt_key_with_ecdh("not a valid pem key", compressed)

    def test_decrypt_key_invalid_ephemeral_key(self):
        """Test that invalid ephemeral keys raise an error."""
        priv, _ = generate_ephemeral_keypair("secp256r1")
        priv_pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        with pytest.raises(InvalidKeyError):
            decrypt_key_with_ecdh(priv_pem, b"invalid_compressed_key")


class TestRoundtrip:
    """Test complete ECDH roundtrip scenarios."""

    def test_full_roundtrip(self):
        """Test a complete encrypt/decrypt roundtrip."""
        # Scenario: Alice wants to send encrypted data to Bob

        # Bob generates a keypair and shares his public key
        bob_private, bob_public = generate_ephemeral_keypair("secp256r1")
        bob_public_pem = bob_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        bob_private_pem = bob_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Alice encrypts: generates ephemeral keypair and derives key
        encryption_key, ephemeral_public_compressed = encrypt_key_with_ecdh(
            bob_public_pem
        )

        # Alice would use encryption_key to encrypt data with AES-256-GCM
        # and include ephemeral_public_compressed in the NanoTDF header

        # Bob receives the NanoTDF and extracts ephemeral_public_compressed from header
        # Bob decrypts: uses his private key with the ephemeral public key
        decryption_key = decrypt_key_with_ecdh(
            bob_private_pem, ephemeral_public_compressed
        )

        # Bob would use decryption_key to decrypt the data

        # The keys should match
        assert encryption_key == decryption_key

    def test_multiple_roundtrips_same_recipient(self):
        """Test multiple encryptions to the same recipient produce different ephemeral keys."""
        # Bob's keypair
        bob_private, bob_public = generate_ephemeral_keypair("secp256r1")
        bob_public_pem = bob_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        bob_private_pem = bob_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Alice encrypts twice
        key1, ephemeral1 = encrypt_key_with_ecdh(bob_public_pem)
        key2, ephemeral2 = encrypt_key_with_ecdh(bob_public_pem)

        # Ephemeral keys should be different (new keypair each time)
        assert ephemeral1 != ephemeral2
        # Derived keys should be different
        assert key1 != key2

        # But Bob should be able to decrypt both
        decrypted_key1 = decrypt_key_with_ecdh(bob_private_pem, ephemeral1)
        decrypted_key2 = decrypt_key_with_ecdh(bob_private_pem, ephemeral2)

        assert key1 == decrypted_key1
        assert key2 == decrypted_key2
