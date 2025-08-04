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

import wellknownconfiguration.wellknown_configuration_pb2

class WellKnownServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_get_well_known_configuration(
        self, req: wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse]:
        """Low-level method to call GetWellKnownConfiguration, granting access to errors and metadata"""
        url = self.base_url + "/wellknownconfiguration.WellKnownService/GetWellKnownConfiguration"
        return self._connect_client.call_unary(url, req, wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse,extra_headers, timeout_seconds)


    def get_well_known_configuration(
        self, req: wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse:
        response = self.call_get_well_known_configuration(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncWellKnownServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_get_well_known_configuration(
        self, req: wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse]:
        """Low-level method to call GetWellKnownConfiguration, granting access to errors and metadata"""
        url = self.base_url + "/wellknownconfiguration.WellKnownService/GetWellKnownConfiguration"
        return await self._connect_client.call_unary(url, req, wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse,extra_headers, timeout_seconds)

    async def get_well_known_configuration(
        self, req: wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse:
        response = await self.call_get_well_known_configuration(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class WellKnownServiceProtocol(typing.Protocol):
    def get_well_known_configuration(self, req: ClientRequest[wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationRequest]) -> ServerResponse[wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationResponse]:
        ...

WELL_KNOWN_SERVICE_PATH_PREFIX = "/wellknownconfiguration.WellKnownService"

def wsgi_well_known_service(implementation: WellKnownServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/wellknownconfiguration.WellKnownService/GetWellKnownConfiguration", implementation.get_well_known_configuration, wellknownconfiguration.wellknown_configuration_pb2.GetWellKnownConfigurationRequest)
    return app
