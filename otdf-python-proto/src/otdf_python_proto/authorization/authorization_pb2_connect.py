# Generated Connect client code

from __future__ import annotations
from collections.abc import AsyncIterator
from collections.abc import Iterator
from collections.abc import Iterable
import aiohttp
import urllib3
import typing
import sys

from connectrpc.client_async import AsyncConnectClient
from connectrpc.client_sync import ConnectClient
from connectrpc.client_protocol import ConnectProtocol
from connectrpc.client_connect import ConnectProtocolError
from connectrpc.headers import HeaderInput
from connectrpc.server import ClientRequest
from connectrpc.server import ClientStream
from connectrpc.server import ServerResponse
from connectrpc.server import ServerStream
from connectrpc.server_sync import ConnectWSGI
from connectrpc.streams import StreamInput
from connectrpc.streams import AsyncStreamOutput
from connectrpc.streams import StreamOutput
from connectrpc.unary import UnaryOutput
from connectrpc.unary import ClientStreamingOutput

if typing.TYPE_CHECKING:
    # wsgiref.types was added in Python 3.11.
    if sys.version_info >= (3, 11):
        from wsgiref.types import WSGIApplication
    else:
        from _typeshed.wsgi import WSGIApplication

import authorization.authorization_pb2

class AuthorizationServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_get_decisions(
        self, req: authorization.authorization_pb2.GetDecisionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.authorization_pb2.GetDecisionsResponse]:
        """Low-level method to call GetDecisions, granting access to errors and metadata"""
        url = self.base_url + "/authorization.AuthorizationService/GetDecisions"
        return self._connect_client.call_unary(url, req, authorization.authorization_pb2.GetDecisionsResponse,extra_headers, timeout_seconds)


    def get_decisions(
        self, req: authorization.authorization_pb2.GetDecisionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.authorization_pb2.GetDecisionsResponse:
        response = self.call_get_decisions(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_decisions_by_token(
        self, req: authorization.authorization_pb2.GetDecisionsByTokenRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.authorization_pb2.GetDecisionsByTokenResponse]:
        """Low-level method to call GetDecisionsByToken, granting access to errors and metadata"""
        url = self.base_url + "/authorization.AuthorizationService/GetDecisionsByToken"
        return self._connect_client.call_unary(url, req, authorization.authorization_pb2.GetDecisionsByTokenResponse,extra_headers, timeout_seconds)


    def get_decisions_by_token(
        self, req: authorization.authorization_pb2.GetDecisionsByTokenRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.authorization_pb2.GetDecisionsByTokenResponse:
        response = self.call_get_decisions_by_token(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_entitlements(
        self, req: authorization.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.authorization_pb2.GetEntitlementsResponse]:
        """Low-level method to call GetEntitlements, granting access to errors and metadata"""
        url = self.base_url + "/authorization.AuthorizationService/GetEntitlements"
        return self._connect_client.call_unary(url, req, authorization.authorization_pb2.GetEntitlementsResponse,extra_headers, timeout_seconds)


    def get_entitlements(
        self, req: authorization.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.authorization_pb2.GetEntitlementsResponse:
        response = self.call_get_entitlements(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncAuthorizationServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_get_decisions(
        self, req: authorization.authorization_pb2.GetDecisionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.authorization_pb2.GetDecisionsResponse]:
        """Low-level method to call GetDecisions, granting access to errors and metadata"""
        url = self.base_url + "/authorization.AuthorizationService/GetDecisions"
        return await self._connect_client.call_unary(url, req, authorization.authorization_pb2.GetDecisionsResponse,extra_headers, timeout_seconds)

    async def get_decisions(
        self, req: authorization.authorization_pb2.GetDecisionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.authorization_pb2.GetDecisionsResponse:
        response = await self.call_get_decisions(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_decisions_by_token(
        self, req: authorization.authorization_pb2.GetDecisionsByTokenRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.authorization_pb2.GetDecisionsByTokenResponse]:
        """Low-level method to call GetDecisionsByToken, granting access to errors and metadata"""
        url = self.base_url + "/authorization.AuthorizationService/GetDecisionsByToken"
        return await self._connect_client.call_unary(url, req, authorization.authorization_pb2.GetDecisionsByTokenResponse,extra_headers, timeout_seconds)

    async def get_decisions_by_token(
        self, req: authorization.authorization_pb2.GetDecisionsByTokenRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.authorization_pb2.GetDecisionsByTokenResponse:
        response = await self.call_get_decisions_by_token(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_entitlements(
        self, req: authorization.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.authorization_pb2.GetEntitlementsResponse]:
        """Low-level method to call GetEntitlements, granting access to errors and metadata"""
        url = self.base_url + "/authorization.AuthorizationService/GetEntitlements"
        return await self._connect_client.call_unary(url, req, authorization.authorization_pb2.GetEntitlementsResponse,extra_headers, timeout_seconds)

    async def get_entitlements(
        self, req: authorization.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.authorization_pb2.GetEntitlementsResponse:
        response = await self.call_get_entitlements(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class AuthorizationServiceProtocol(typing.Protocol):
    def get_decisions(self, req: ClientRequest[authorization.authorization_pb2.GetDecisionsRequest]) -> ServerResponse[authorization.authorization_pb2.GetDecisionsResponse]:
        ...
    def get_decisions_by_token(self, req: ClientRequest[authorization.authorization_pb2.GetDecisionsByTokenRequest]) -> ServerResponse[authorization.authorization_pb2.GetDecisionsByTokenResponse]:
        ...
    def get_entitlements(self, req: ClientRequest[authorization.authorization_pb2.GetEntitlementsRequest]) -> ServerResponse[authorization.authorization_pb2.GetEntitlementsResponse]:
        ...

AUTHORIZATION_SERVICE_PATH_PREFIX = "/authorization.AuthorizationService"

def wsgi_authorization_service(implementation: AuthorizationServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/authorization.AuthorizationService/GetDecisions", implementation.get_decisions, authorization.authorization_pb2.GetDecisionsRequest)
    app.register_unary_rpc("/authorization.AuthorizationService/GetDecisionsByToken", implementation.get_decisions_by_token, authorization.authorization_pb2.GetDecisionsByTokenRequest)
    app.register_unary_rpc("/authorization.AuthorizationService/GetEntitlements", implementation.get_entitlements, authorization.authorization_pb2.GetEntitlementsRequest)
    return app
