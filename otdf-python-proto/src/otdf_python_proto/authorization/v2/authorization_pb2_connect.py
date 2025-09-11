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

import authorization.v2.authorization_pb2

class AuthorizationServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_get_decision(
        self, req: authorization.v2.authorization_pb2.GetDecisionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetDecisionResponse]:
        """Low-level method to call GetDecision, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetDecision"
        return self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetDecisionResponse,extra_headers, timeout_seconds)


    def get_decision(
        self, req: authorization.v2.authorization_pb2.GetDecisionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetDecisionResponse:
        response = self.call_get_decision(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_decision_multi_resource(
        self, req: authorization.v2.authorization_pb2.GetDecisionMultiResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse]:
        """Low-level method to call GetDecisionMultiResource, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetDecisionMultiResource"
        return self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse,extra_headers, timeout_seconds)


    def get_decision_multi_resource(
        self, req: authorization.v2.authorization_pb2.GetDecisionMultiResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse:
        response = self.call_get_decision_multi_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_decision_bulk(
        self, req: authorization.v2.authorization_pb2.GetDecisionBulkRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetDecisionBulkResponse]:
        """Low-level method to call GetDecisionBulk, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetDecisionBulk"
        return self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetDecisionBulkResponse,extra_headers, timeout_seconds)


    def get_decision_bulk(
        self, req: authorization.v2.authorization_pb2.GetDecisionBulkRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetDecisionBulkResponse:
        response = self.call_get_decision_bulk(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_entitlements(
        self, req: authorization.v2.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetEntitlementsResponse]:
        """Low-level method to call GetEntitlements, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetEntitlements"
        return self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetEntitlementsResponse,extra_headers, timeout_seconds)


    def get_entitlements(
        self, req: authorization.v2.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetEntitlementsResponse:
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

    async def call_get_decision(
        self, req: authorization.v2.authorization_pb2.GetDecisionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetDecisionResponse]:
        """Low-level method to call GetDecision, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetDecision"
        return await self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetDecisionResponse,extra_headers, timeout_seconds)

    async def get_decision(
        self, req: authorization.v2.authorization_pb2.GetDecisionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetDecisionResponse:
        response = await self.call_get_decision(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_decision_multi_resource(
        self, req: authorization.v2.authorization_pb2.GetDecisionMultiResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse]:
        """Low-level method to call GetDecisionMultiResource, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetDecisionMultiResource"
        return await self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse,extra_headers, timeout_seconds)

    async def get_decision_multi_resource(
        self, req: authorization.v2.authorization_pb2.GetDecisionMultiResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse:
        response = await self.call_get_decision_multi_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_decision_bulk(
        self, req: authorization.v2.authorization_pb2.GetDecisionBulkRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetDecisionBulkResponse]:
        """Low-level method to call GetDecisionBulk, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetDecisionBulk"
        return await self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetDecisionBulkResponse,extra_headers, timeout_seconds)

    async def get_decision_bulk(
        self, req: authorization.v2.authorization_pb2.GetDecisionBulkRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetDecisionBulkResponse:
        response = await self.call_get_decision_bulk(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_entitlements(
        self, req: authorization.v2.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[authorization.v2.authorization_pb2.GetEntitlementsResponse]:
        """Low-level method to call GetEntitlements, granting access to errors and metadata"""
        url = self.base_url + "/authorization.v2.AuthorizationService/GetEntitlements"
        return await self._connect_client.call_unary(url, req, authorization.v2.authorization_pb2.GetEntitlementsResponse,extra_headers, timeout_seconds)

    async def get_entitlements(
        self, req: authorization.v2.authorization_pb2.GetEntitlementsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> authorization.v2.authorization_pb2.GetEntitlementsResponse:
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
    def get_decision(self, req: ClientRequest[authorization.v2.authorization_pb2.GetDecisionRequest]) -> ServerResponse[authorization.v2.authorization_pb2.GetDecisionResponse]:
        ...
    def get_decision_multi_resource(self, req: ClientRequest[authorization.v2.authorization_pb2.GetDecisionMultiResourceRequest]) -> ServerResponse[authorization.v2.authorization_pb2.GetDecisionMultiResourceResponse]:
        ...
    def get_decision_bulk(self, req: ClientRequest[authorization.v2.authorization_pb2.GetDecisionBulkRequest]) -> ServerResponse[authorization.v2.authorization_pb2.GetDecisionBulkResponse]:
        ...
    def get_entitlements(self, req: ClientRequest[authorization.v2.authorization_pb2.GetEntitlementsRequest]) -> ServerResponse[authorization.v2.authorization_pb2.GetEntitlementsResponse]:
        ...

AUTHORIZATION_SERVICE_PATH_PREFIX = "/authorization.v2.AuthorizationService"

def wsgi_authorization_service(implementation: AuthorizationServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/authorization.v2.AuthorizationService/GetDecision", implementation.get_decision, authorization.v2.authorization_pb2.GetDecisionRequest)
    app.register_unary_rpc("/authorization.v2.AuthorizationService/GetDecisionMultiResource", implementation.get_decision_multi_resource, authorization.v2.authorization_pb2.GetDecisionMultiResourceRequest)
    app.register_unary_rpc("/authorization.v2.AuthorizationService/GetDecisionBulk", implementation.get_decision_bulk, authorization.v2.authorization_pb2.GetDecisionBulkRequest)
    app.register_unary_rpc("/authorization.v2.AuthorizationService/GetEntitlements", implementation.get_entitlements, authorization.v2.authorization_pb2.GetEntitlementsRequest)
    return app
