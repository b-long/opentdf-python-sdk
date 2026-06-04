"""Verify httpx/httpx2 client compatibility with connect-python (connectrpc).

connectrpc passes httpx.USE_CLIENT_DEFAULT as a timeout sentinel to the session
client. httpx.Client handles it natively; httpx2.Client raises TypeError because
it cannot interpret the foreign sentinel as an integer.
"""

import httpx
import httpx2
import pytest
from otdf_python_proto.kas import kas_pb2
from otdf_python_proto.kas.kas_connect import AccessServiceClientSync


def _make_svc(session):
    return AccessServiceClientSync(address="http://localhost:19999", session=session)


def test_httpx_client_is_compatible():
    """httpx.Client passes USE_CLIENT_DEFAULT through its own transport without error.

    We expect a connection error (no server), not a TypeError.
    """
    with httpx.Client() as client:
        svc = _make_svc(client)
        with pytest.raises(Exception) as exc_info:
            svc.public_key(kas_pb2.PublicKeyRequest())
        assert "UseClientDefault" not in str(exc_info.value)


def test_httpx2_client_is_incompatible():
    """httpx2.Client receives httpx.USE_CLIENT_DEFAULT as timeout and raises TypeError.

    This confirms kas_connect_rpc_client.py must use httpx, not httpx2.
    """
    with httpx2.Client() as client:
        svc = _make_svc(client)
        with pytest.raises(Exception, match="UseClientDefault"):
            svc.public_key(kas_pb2.PublicKeyRequest())
