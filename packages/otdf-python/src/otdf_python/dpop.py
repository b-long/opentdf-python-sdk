"""DPoP (Demonstration of Proof-of-Possession) token generation utilities."""

import base64
import hashlib
import time

import jwt

from .crypto_utils import CryptoUtils


def create_dpop_token(
    private_key_pem: str,
    public_key_pem: str,
    url: str,
    method: str = "POST",
    access_token: str | None = None,
) -> str:
    """Create a DPoP (Demonstration of Proof-of-Possession) token.

    Args:
        private_key_pem: RSA private key in PEM format for signing
        public_key_pem: RSA public key in PEM format for JWK
        url: The URL being accessed
        method: HTTP method (default: POST)
        access_token: Optional access token for ath claim

    Returns:
        DPoP token as a string

    """
    # Parse the RSA public key to extract modulus and exponent
    public_key_obj = CryptoUtils.get_rsa_public_key_from_pem(public_key_pem)
    public_numbers = public_key_obj.public_numbers()

    # Convert to base64url encoded values
    def int_to_base64url(value):
        # Convert integer to bytes, then to base64url
        byte_length = (value.bit_length() + 7) // 8
        value_bytes = value.to_bytes(byte_length, byteorder="big")
        return base64.urlsafe_b64encode(value_bytes).decode("ascii").rstrip("=")

    # Create JWK (JSON Web Key) representation
    jwk = {
        "kty": "RSA",
        "n": int_to_base64url(public_numbers.n),
        "e": int_to_base64url(public_numbers.e),
    }

    # Create DPoP header
    now = int(time.time())

    # Create JWT header with JWK
    header = {"typ": "dpop+jwt", "alg": "RS256", "jwk": jwk}

    # Create JWT payload
    payload = {
        "jti": base64.urlsafe_b64encode(
            hashlib.sha256(f"{url}{method}{now}".encode()).digest()
        )
        .decode("ascii")
        .rstrip("="),
        "htm": method,
        "htu": url,
        "iat": now,
    }

    # Add access token hash if provided
    if access_token:
        # Create SHA-256 hash of access token
        token_hash = hashlib.sha256(access_token.encode()).digest()
        payload["ath"] = (
            base64.urlsafe_b64encode(token_hash).decode("ascii").rstrip("=")
        )

    # Sign the DPoP token
    dpop_token = jwt.encode(payload, private_key_pem, algorithm="RS256", headers=header)

    return dpop_token
