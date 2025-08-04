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

import google.protobuf.wrappers_pb2
from . import kas_pb2

class AccessServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_public_key(
        self, req: kas_pb2.PublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[kas_pb2.PublicKeyResponse]:
        """Low-level method to call PublicKey, granting access to errors and metadata"""
        url = self.base_url + "/kas.AccessService/PublicKey"
        return self._connect_client.call_unary(url, req, kas_pb2.PublicKeyResponse,extra_headers, timeout_seconds)


    def public_key(
        self, req: kas_pb2.PublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> kas_pb2.PublicKeyResponse:
        response = self.call_public_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_legacy_public_key(
        self, req: kas_pb2.LegacyPublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[google.protobuf.wrappers_pb2.StringValue]:
        """Low-level method to call LegacyPublicKey, granting access to errors and metadata"""
        url = self.base_url + "/kas.AccessService/LegacyPublicKey"
        return self._connect_client.call_unary(url, req, google.protobuf.wrappers_pb2.StringValue,extra_headers, timeout_seconds)


    def legacy_public_key(
        self, req: kas_pb2.LegacyPublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> google.protobuf.wrappers_pb2.StringValue:
        response = self.call_legacy_public_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_rewrap(
        self, req: kas_pb2.RewrapRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[kas_pb2.RewrapResponse]:
        """Low-level method to call Rewrap, granting access to errors and metadata"""
        url = self.base_url + "/kas.AccessService/Rewrap"
        return self._connect_client.call_unary(url, req, kas_pb2.RewrapResponse,extra_headers, timeout_seconds)


    def rewrap(
        self, req: kas_pb2.RewrapRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> kas_pb2.RewrapResponse:
        response = self.call_rewrap(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncAccessServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_public_key(
        self, req: kas_pb2.PublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[kas_pb2.PublicKeyResponse]:
        """Low-level method to call PublicKey, granting access to errors and metadata"""
        url = self.base_url + "/kas.AccessService/PublicKey"
        return await self._connect_client.call_unary(url, req, kas_pb2.PublicKeyResponse,extra_headers, timeout_seconds)

    async def public_key(
        self, req: kas_pb2.PublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> kas_pb2.PublicKeyResponse:
        response = await self.call_public_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_legacy_public_key(
        self, req: kas_pb2.LegacyPublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[google.protobuf.wrappers_pb2.StringValue]:
        """Low-level method to call LegacyPublicKey, granting access to errors and metadata"""
        url = self.base_url + "/kas.AccessService/LegacyPublicKey"
        return await self._connect_client.call_unary(url, req, google.protobuf.wrappers_pb2.StringValue,extra_headers, timeout_seconds)

    async def legacy_public_key(
        self, req: kas_pb2.LegacyPublicKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> google.protobuf.wrappers_pb2.StringValue:
        response = await self.call_legacy_public_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_rewrap(
        self, req: kas_pb2.RewrapRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[kas_pb2.RewrapResponse]:
        """Low-level method to call Rewrap, granting access to errors and metadata"""
        url = self.base_url + "/kas.AccessService/Rewrap"
        return await self._connect_client.call_unary(url, req, kas_pb2.RewrapResponse,extra_headers, timeout_seconds)

    async def rewrap(
        self, req: kas_pb2.RewrapRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> kas_pb2.RewrapResponse:
        response = await self.call_rewrap(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class AccessServiceProtocol(typing.Protocol):
    def public_key(self, req: ClientRequest[kas_pb2.PublicKeyRequest]) -> ServerResponse[kas_pb2.PublicKeyResponse]:
        ...
    def legacy_public_key(self, req: ClientRequest[kas_pb2.LegacyPublicKeyRequest]) -> ServerResponse[google.protobuf.wrappers_pb2.StringValue]:
        ...
    def rewrap(self, req: ClientRequest[kas_pb2.RewrapRequest]) -> ServerResponse[kas_pb2.RewrapResponse]:
        ...

ACCESS_SERVICE_PATH_PREFIX = "/kas.AccessService"

def wsgi_access_service(implementation: AccessServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/kas.AccessService/PublicKey", implementation.public_key, kas_pb2.PublicKeyRequest)
    app.register_unary_rpc("/kas.AccessService/LegacyPublicKey", implementation.legacy_public_key, kas_pb2.LegacyPublicKeyRequest)
    app.register_unary_rpc("/kas.AccessService/Rewrap", implementation.rewrap, kas_pb2.RewrapRequest)
    return app
