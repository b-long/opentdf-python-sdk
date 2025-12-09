"""Integration tests for NanoTDF with ECDH key exchange."""

import io

import pytest
from cryptography.hazmat.primitives import serialization

from otdf_python.config import KASInfo, NanoTDFConfig
from otdf_python.ecdh import generate_ephemeral_keypair
from otdf_python.nanotdf import NanoTDF


class TestNanoTDFWithECDH:
    """Test NanoTDF encryption/decryption using ECDH key exchange."""

    def test_nanotdf_ecdh_roundtrip_secp256r1(self):
        """Test NanoTDF roundtrip with ECDH using secp256r1 curve."""
        # Generate a keypair for the recipient (e.g., KAS)
        recipient_private_key, recipient_public_key = generate_ephemeral_keypair(
            "secp256r1"
        )

        # Convert to PEM format
        recipient_public_pem = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        recipient_private_pem = recipient_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Create NanoTDF instance
        nanotdf = NanoTDF()

        # Test payload
        payload = b"Hello NanoTDF with ECDH!"

        # Create configuration with KAS public key
        kas_info = KASInfo(
            url="https://kas.example.com", public_key=recipient_public_pem
        )
        config_encrypt = NanoTDFConfig(kas_info_list=[kas_info], ecc_mode="secp256r1")

        # Encrypt
        encrypted_stream = io.BytesIO()
        size = nanotdf.create_nano_tdf(payload, encrypted_stream, config_encrypt)
        encrypted_data = encrypted_stream.getvalue()

        # Verify encryption worked
        assert size > 0
        assert len(encrypted_data) > len(
            payload
        )  # Should be larger due to header + IV + MAC

        # Decrypt with recipient's private key
        config_decrypt = NanoTDFConfig(cipher=recipient_private_pem)
        decrypted_stream = io.BytesIO()
        nanotdf.read_nano_tdf(encrypted_data, decrypted_stream, config_decrypt)
        decrypted_data = decrypted_stream.getvalue()

        # Verify decryption worked
        assert decrypted_data == payload

    def test_nanotdf_ecdh_roundtrip_all_curves(self):
        """Test NanoTDF roundtrip with ECDH using all supported curves."""
        curves = ["secp256r1", "secp384r1", "secp521r1", "secp256k1"]

        for curve_name in curves:
            # Generate keypair
            recipient_private_key, recipient_public_key = generate_ephemeral_keypair(
                curve_name
            )

            recipient_public_pem = recipient_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()

            recipient_private_pem = recipient_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode()

            # Create NanoTDF
            nanotdf = NanoTDF()
            payload = f"Testing {curve_name}".encode()

            # Encrypt
            kas_info = KASInfo(
                url="https://kas.example.com", public_key=recipient_public_pem
            )
            config_encrypt = NanoTDFConfig(
                kas_info_list=[kas_info], ecc_mode=curve_name
            )
            encrypted_stream = io.BytesIO()
            nanotdf.create_nano_tdf(payload, encrypted_stream, config_encrypt)
            encrypted_data = encrypted_stream.getvalue()

            # Decrypt
            config_decrypt = NanoTDFConfig(cipher=recipient_private_pem)
            decrypted_stream = io.BytesIO()
            nanotdf.read_nano_tdf(encrypted_data, decrypted_stream, config_decrypt)
            decrypted_data = decrypted_stream.getvalue()

            # Verify
            assert decrypted_data == payload, f"Failed for curve {curve_name}"

    def test_nanotdf_ecdh_with_attributes(self):
        """Test NanoTDF with ECDH and policy attributes."""
        # Generate keypair
        recipient_private_key, recipient_public_key = generate_ephemeral_keypair(
            "secp256r1"
        )

        recipient_public_pem = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        recipient_private_pem = recipient_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Create NanoTDF with attributes
        nanotdf = NanoTDF()
        payload = b"Sensitive data with attributes"

        kas_info = KASInfo(
            url="https://kas.example.com", public_key=recipient_public_pem
        )
        attributes = [
            "https://example.com/attr/classification/secret",
            "https://example.com/attr/country/us",
        ]
        config_encrypt = NanoTDFConfig(
            kas_info_list=[kas_info], attributes=attributes, ecc_mode="secp256r1"
        )

        # Encrypt
        encrypted_stream = io.BytesIO()
        nanotdf.create_nano_tdf(payload, encrypted_stream, config_encrypt)
        encrypted_data = encrypted_stream.getvalue()

        # Decrypt
        config_decrypt = NanoTDFConfig(cipher=recipient_private_pem)
        decrypted_stream = io.BytesIO()
        nanotdf.read_nano_tdf(encrypted_data, decrypted_stream, config_decrypt)
        decrypted_data = decrypted_stream.getvalue()

        # Verify
        assert decrypted_data == payload

    def test_nanotdf_ecdh_multiple_encryptions_different_keys(self):
        """Test that multiple encryptions produce different ephemeral keys."""
        # Generate recipient keypair
        recipient_private_key, recipient_public_key = generate_ephemeral_keypair(
            "secp256r1"
        )

        recipient_public_pem = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        recipient_private_pem = recipient_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Encrypt same payload twice
        nanotdf = NanoTDF()
        payload = b"Same payload"

        kas_info = KASInfo(
            url="https://kas.example.com", public_key=recipient_public_pem
        )
        config_encrypt = NanoTDFConfig(kas_info_list=[kas_info], ecc_mode="secp256r1")

        # First encryption
        encrypted_stream1 = io.BytesIO()
        nanotdf.create_nano_tdf(payload, encrypted_stream1, config_encrypt)
        encrypted_data1 = encrypted_stream1.getvalue()

        # Second encryption
        encrypted_stream2 = io.BytesIO()
        nanotdf.create_nano_tdf(payload, encrypted_stream2, config_encrypt)
        encrypted_data2 = encrypted_stream2.getvalue()

        # Encrypted data should be different (different ephemeral keys)
        assert encrypted_data1 != encrypted_data2

        # But both should decrypt to the same payload
        config_decrypt = NanoTDFConfig(cipher=recipient_private_pem)

        decrypted_stream1 = io.BytesIO()
        nanotdf.read_nano_tdf(encrypted_data1, decrypted_stream1, config_decrypt)
        assert decrypted_stream1.getvalue() == payload

        decrypted_stream2 = io.BytesIO()
        nanotdf.read_nano_tdf(encrypted_data2, decrypted_stream2, config_decrypt)
        assert decrypted_stream2.getvalue() == payload

    def test_nanotdf_ecdh_wrong_private_key_fails(self):
        """Test that decryption with wrong private key fails."""
        # Generate recipient keypair
        _, recipient_public_key = generate_ephemeral_keypair("secp256r1")

        recipient_public_pem = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        # Generate a different private key (wrong key)
        wrong_private_key, _ = generate_ephemeral_keypair("secp256r1")
        wrong_private_pem = wrong_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Encrypt
        nanotdf = NanoTDF()
        payload = b"Secret message"

        kas_info = KASInfo(
            url="https://kas.example.com", public_key=recipient_public_pem
        )
        config_encrypt = NanoTDFConfig(kas_info_list=[kas_info], ecc_mode="secp256r1")

        encrypted_stream = io.BytesIO()
        nanotdf.create_nano_tdf(payload, encrypted_stream, config_encrypt)
        encrypted_data = encrypted_stream.getvalue()

        # Try to decrypt with wrong private key
        config_decrypt = NanoTDFConfig(cipher=wrong_private_pem)
        decrypted_stream = io.BytesIO()

        # Should fail (authentication error from AES-GCM)
        # Will be cryptography.exceptions.InvalidTag
        with pytest.raises(Exception):  # noqa: B017
            nanotdf.read_nano_tdf(encrypted_data, decrypted_stream, config_decrypt)

    def test_nanotdf_ecdh_large_payload(self):
        """Test NanoTDF with ECDH for a large payload."""
        # Generate keypair
        recipient_private_key, recipient_public_key = generate_ephemeral_keypair(
            "secp256r1"
        )

        recipient_public_pem = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        recipient_private_pem = recipient_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Large payload (1MB)
        nanotdf = NanoTDF()
        payload = b"X" * (1024 * 1024)

        kas_info = KASInfo(
            url="https://kas.example.com", public_key=recipient_public_pem
        )
        config_encrypt = NanoTDFConfig(kas_info_list=[kas_info], ecc_mode="secp256r1")

        # Encrypt
        encrypted_stream = io.BytesIO()
        nanotdf.create_nano_tdf(payload, encrypted_stream, config_encrypt)
        encrypted_data = encrypted_stream.getvalue()

        # Decrypt
        config_decrypt = NanoTDFConfig(cipher=recipient_private_pem)
        decrypted_stream = io.BytesIO()
        nanotdf.read_nano_tdf(encrypted_data, decrypted_stream, config_decrypt)
        decrypted_data = decrypted_stream.getvalue()

        # Verify
        assert decrypted_data == payload
        assert len(decrypted_data) == 1024 * 1024

    def test_nanotdf_backward_compat_symmetric_key(self):
        """Test that symmetric key encryption still works (backward compatibility)."""
        nanotdf = NanoTDF()
        payload = b"Testing symmetric key backward compat"

        # Use symmetric key (no ECDH)
        import secrets

        key = secrets.token_bytes(32)
        config_encrypt = NanoTDFConfig(cipher=key.hex())

        # Encrypt
        encrypted_stream = io.BytesIO()
        nanotdf.create_nano_tdf(payload, encrypted_stream, config_encrypt)
        encrypted_data = encrypted_stream.getvalue()

        # Decrypt with same symmetric key
        config_decrypt = NanoTDFConfig(cipher=key.hex())
        decrypted_stream = io.BytesIO()
        nanotdf.read_nano_tdf(encrypted_data, decrypted_stream, config_decrypt)
        decrypted_data = decrypted_stream.getvalue()

        # Verify
        assert decrypted_data == payload


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
