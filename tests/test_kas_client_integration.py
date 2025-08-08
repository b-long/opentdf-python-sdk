"""
Integration tests for KASClient.
"""

import pytest
from otdf_python.kas_client import KASClient


@pytest.mark.integration
def test_connect_rpc_public_key_retrieval():
    """Test Connect RPC public key retrieval using live backend server."""
    from tests.config_pydantic import CONFIG_TDF
    from otdf_python.config import KASInfo

    # Create KAS info from configuration
    kas_info = KASInfo(url=CONFIG_TDF.KAS_ENDPOINT)

    # Create KAS client with SSL verification disabled for testing
    client = KASClient(
        kas_url=CONFIG_TDF.KAS_ENDPOINT,
        verify_ssl=not CONFIG_TDF.INSECURE_SKIP_VERIFY,
        use_plaintext=bool(CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://")),
    )

    # Retrieve public key using Connect RPC
    result = client.get_public_key(kas_info)

    # Verify the result
    assert result is not None
    assert result.url == CONFIG_TDF.KAS_ENDPOINT
    assert result.public_key is not None
    assert len(result.public_key) > 0
    assert result.kid is not None
    assert len(result.kid) > 0

    # Verify the public key looks like a PEM format
    assert "-----BEGIN" in result.public_key
    assert "-----END" in result.public_key
