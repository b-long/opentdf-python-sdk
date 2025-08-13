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

import entityresolution.entity_resolution_pb2

class EntityResolutionServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_resolve_entities(
        self, req: entityresolution.entity_resolution_pb2.ResolveEntitiesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[entityresolution.entity_resolution_pb2.ResolveEntitiesResponse]:
        """Low-level method to call ResolveEntities, granting access to errors and metadata"""
        url = self.base_url + "/entityresolution.EntityResolutionService/ResolveEntities"
        return self._connect_client.call_unary(url, req, entityresolution.entity_resolution_pb2.ResolveEntitiesResponse,extra_headers, timeout_seconds)


    def resolve_entities(
        self, req: entityresolution.entity_resolution_pb2.ResolveEntitiesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> entityresolution.entity_resolution_pb2.ResolveEntitiesResponse:
        response = self.call_resolve_entities(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_entity_chain_from_jwt(
        self, req: entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse]:
        """Low-level method to call CreateEntityChainFromJwt, granting access to errors and metadata"""
        url = self.base_url + "/entityresolution.EntityResolutionService/CreateEntityChainFromJwt"
        return self._connect_client.call_unary(url, req, entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse,extra_headers, timeout_seconds)


    def create_entity_chain_from_jwt(
        self, req: entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse:
        response = self.call_create_entity_chain_from_jwt(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncEntityResolutionServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_resolve_entities(
        self, req: entityresolution.entity_resolution_pb2.ResolveEntitiesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[entityresolution.entity_resolution_pb2.ResolveEntitiesResponse]:
        """Low-level method to call ResolveEntities, granting access to errors and metadata"""
        url = self.base_url + "/entityresolution.EntityResolutionService/ResolveEntities"
        return await self._connect_client.call_unary(url, req, entityresolution.entity_resolution_pb2.ResolveEntitiesResponse,extra_headers, timeout_seconds)

    async def resolve_entities(
        self, req: entityresolution.entity_resolution_pb2.ResolveEntitiesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> entityresolution.entity_resolution_pb2.ResolveEntitiesResponse:
        response = await self.call_resolve_entities(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_entity_chain_from_jwt(
        self, req: entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse]:
        """Low-level method to call CreateEntityChainFromJwt, granting access to errors and metadata"""
        url = self.base_url + "/entityresolution.EntityResolutionService/CreateEntityChainFromJwt"
        return await self._connect_client.call_unary(url, req, entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse,extra_headers, timeout_seconds)

    async def create_entity_chain_from_jwt(
        self, req: entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse:
        response = await self.call_create_entity_chain_from_jwt(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class EntityResolutionServiceProtocol(typing.Protocol):
    def resolve_entities(self, req: ClientRequest[entityresolution.entity_resolution_pb2.ResolveEntitiesRequest]) -> ServerResponse[entityresolution.entity_resolution_pb2.ResolveEntitiesResponse]:
        ...
    def create_entity_chain_from_jwt(self, req: ClientRequest[entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtRequest]) -> ServerResponse[entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtResponse]:
        ...

ENTITY_RESOLUTION_SERVICE_PATH_PREFIX = "/entityresolution.EntityResolutionService"

def wsgi_entity_resolution_service(implementation: EntityResolutionServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/entityresolution.EntityResolutionService/ResolveEntities", implementation.resolve_entities, entityresolution.entity_resolution_pb2.ResolveEntitiesRequest)
    app.register_unary_rpc("/entityresolution.EntityResolutionService/CreateEntityChainFromJwt", implementation.create_entity_chain_from_jwt, entityresolution.entity_resolution_pb2.CreateEntityChainFromJwtRequest)
    return app
