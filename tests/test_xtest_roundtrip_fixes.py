"""Regression tests for the community xtest Stage-1 roundtrip failures.

Covers the three bugs observed in arkavo-org/opentdf-tests run 29210974140:

1. Encrypt emitted two key access objects for the same KAS (the platform-
   derived default plus the explicit --kas-endpoint), where the manifest
   should carry one.
2. OIDC discovery doubled the realm path when --oidc-endpoint already named
   a realm (…/auth/realms/opentdf/realms/opentdf/…) and failed with 404.
3. After a token-acquisition failure, rewrap proceeded without an
   Authorization header instead of failing fast, so KAS rejected it with a
   misleading "missing authorization header".
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from otdf_python.cli import create_tdf_config
from otdf_python.config import KASInfo, TDFConfig
from otdf_python.kas_client import KASClient, KeyAccess
from otdf_python.sdk_builder import OAuthConfig, SDKBuilder
from otdf_python.sdk_exceptions import SDKException
from otdf_python.tdf import TDF


def _stub_sdk_with_default_kas(default_url: str):
    return SimpleNamespace(
        new_tdf_config=lambda attributes: TDFConfig(
            kas_info_list=[KASInfo(url=default_url, default=True)],
            attributes=attributes,
        )
    )


def test_explicit_kas_endpoint_replaces_platform_default():
    sdk = _stub_sdk_with_default_kas("http://localhost:8080/kas")
    args = SimpleNamespace(kas_endpoint="http://localhost:8080/kas")
    config = create_tdf_config(sdk, args)
    assert [k.url for k in config.kas_info_list] == ["http://localhost:8080/kas"]


def test_explicit_kas_endpoint_wins_over_different_default():
    sdk = _stub_sdk_with_default_kas("http://localhost:8080/kas")
    args = SimpleNamespace(kas_endpoint="http://alpha:8181/kas")
    config = create_tdf_config(sdk, args)
    assert [k.url for k in config.kas_info_list] == ["http://alpha:8181/kas"]


def test_validate_kas_infos_dedupes_same_url():
    tdf = TDF(services=None)
    kas_infos = [
        KASInfo(url="http://localhost:8080/kas", public_key="PK", kid="r1"),
        KASInfo(url="http://localhost:8080/kas/", public_key="PK", kid="r1"),
    ]
    validated = tdf._validate_kas_infos(kas_infos)
    assert len(validated) == 1


def _builder_with_issuer(issuer: str) -> SDKBuilder:
    builder = SDKBuilder()
    builder.issuer_endpoint = issuer
    builder.oauth_config = OAuthConfig(client_id="c", client_secret="s")
    return builder


def test_issuer_naming_realm_is_used_verbatim():
    builder = _builder_with_issuer("http://localhost:8888/auth/realms/opentdf")
    assert builder._candidate_issuer_urls() == [
        "http://localhost:8888/auth/realms/opentdf"
    ]


def test_bare_issuer_tries_default_realm_first():
    builder = _builder_with_issuer("http://localhost:8888")
    assert builder._candidate_issuer_urls() == [
        "http://localhost:8888/realms/opentdf",
        "http://localhost:8888",
    ]


def test_discovery_hits_realm_issuer_without_doubling_path():
    builder = _builder_with_issuer("http://localhost:8888/auth/realms/opentdf")
    response = MagicMock(status_code=200)
    response.json.return_value = {"token_endpoint": "http://localhost:8888/token"}
    with patch("otdf_python.sdk_builder.httpx.get", return_value=response) as get:
        builder._discover_token_endpoint_from_issuer_endpoint()
    get.assert_called_once_with(
        "http://localhost:8888/auth/realms/opentdf/.well-known/openid-configuration",
        verify=True,
    )
    assert builder.oauth_config is not None
    assert builder.oauth_config.token_endpoint == "http://localhost:8888/token"


def test_unwrap_fails_fast_when_token_unavailable():
    def broken_token_source():
        raise RuntimeError("no token endpoint")

    client = KASClient(
        kas_url="http://localhost:8080", token_source=broken_token_source
    )
    client.connect_rpc_client = MagicMock()
    key_access = KeyAccess(url="http://localhost:8080/kas", wrapped_key="d3Jh")

    with pytest.raises(SDKException, match="access token"):
        client._unwrap_with_connect_rpc(key_access, signed_token="jwt")
    client.connect_rpc_client.unwrap_key.assert_not_called()
