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

import policy.keymanagement.key_management_pb2

class KeyManagementServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_create_provider_config(
        self, req: policy.keymanagement.key_management_pb2.CreateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.CreateProviderConfigResponse]:
        """Low-level method to call CreateProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/CreateProviderConfig"
        return self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.CreateProviderConfigResponse,extra_headers, timeout_seconds)


    def create_provider_config(
        self, req: policy.keymanagement.key_management_pb2.CreateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.CreateProviderConfigResponse:
        response = self.call_create_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_provider_config(
        self, req: policy.keymanagement.key_management_pb2.GetProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.GetProviderConfigResponse]:
        """Low-level method to call GetProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/GetProviderConfig"
        return self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.GetProviderConfigResponse,extra_headers, timeout_seconds)


    def get_provider_config(
        self, req: policy.keymanagement.key_management_pb2.GetProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.GetProviderConfigResponse:
        response = self.call_get_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_provider_configs(
        self, req: policy.keymanagement.key_management_pb2.ListProviderConfigsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.ListProviderConfigsResponse]:
        """Low-level method to call ListProviderConfigs, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/ListProviderConfigs"
        return self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.ListProviderConfigsResponse,extra_headers, timeout_seconds)


    def list_provider_configs(
        self, req: policy.keymanagement.key_management_pb2.ListProviderConfigsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.ListProviderConfigsResponse:
        response = self.call_list_provider_configs(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_provider_config(
        self, req: policy.keymanagement.key_management_pb2.UpdateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse]:
        """Low-level method to call UpdateProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/UpdateProviderConfig"
        return self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse,extra_headers, timeout_seconds)


    def update_provider_config(
        self, req: policy.keymanagement.key_management_pb2.UpdateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse:
        response = self.call_update_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_provider_config(
        self, req: policy.keymanagement.key_management_pb2.DeleteProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse]:
        """Low-level method to call DeleteProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/DeleteProviderConfig"
        return self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse,extra_headers, timeout_seconds)


    def delete_provider_config(
        self, req: policy.keymanagement.key_management_pb2.DeleteProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse:
        response = self.call_delete_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncKeyManagementServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_create_provider_config(
        self, req: policy.keymanagement.key_management_pb2.CreateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.CreateProviderConfigResponse]:
        """Low-level method to call CreateProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/CreateProviderConfig"
        return await self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.CreateProviderConfigResponse,extra_headers, timeout_seconds)

    async def create_provider_config(
        self, req: policy.keymanagement.key_management_pb2.CreateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.CreateProviderConfigResponse:
        response = await self.call_create_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_provider_config(
        self, req: policy.keymanagement.key_management_pb2.GetProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.GetProviderConfigResponse]:
        """Low-level method to call GetProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/GetProviderConfig"
        return await self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.GetProviderConfigResponse,extra_headers, timeout_seconds)

    async def get_provider_config(
        self, req: policy.keymanagement.key_management_pb2.GetProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.GetProviderConfigResponse:
        response = await self.call_get_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_provider_configs(
        self, req: policy.keymanagement.key_management_pb2.ListProviderConfigsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.ListProviderConfigsResponse]:
        """Low-level method to call ListProviderConfigs, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/ListProviderConfigs"
        return await self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.ListProviderConfigsResponse,extra_headers, timeout_seconds)

    async def list_provider_configs(
        self, req: policy.keymanagement.key_management_pb2.ListProviderConfigsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.ListProviderConfigsResponse:
        response = await self.call_list_provider_configs(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_provider_config(
        self, req: policy.keymanagement.key_management_pb2.UpdateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse]:
        """Low-level method to call UpdateProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/UpdateProviderConfig"
        return await self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse,extra_headers, timeout_seconds)

    async def update_provider_config(
        self, req: policy.keymanagement.key_management_pb2.UpdateProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse:
        response = await self.call_update_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_provider_config(
        self, req: policy.keymanagement.key_management_pb2.DeleteProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse]:
        """Low-level method to call DeleteProviderConfig, granting access to errors and metadata"""
        url = self.base_url + "/policy.keymanagement.KeyManagementService/DeleteProviderConfig"
        return await self._connect_client.call_unary(url, req, policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse,extra_headers, timeout_seconds)

    async def delete_provider_config(
        self, req: policy.keymanagement.key_management_pb2.DeleteProviderConfigRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse:
        response = await self.call_delete_provider_config(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class KeyManagementServiceProtocol(typing.Protocol):
    def create_provider_config(self, req: ClientRequest[policy.keymanagement.key_management_pb2.CreateProviderConfigRequest]) -> ServerResponse[policy.keymanagement.key_management_pb2.CreateProviderConfigResponse]:
        ...
    def get_provider_config(self, req: ClientRequest[policy.keymanagement.key_management_pb2.GetProviderConfigRequest]) -> ServerResponse[policy.keymanagement.key_management_pb2.GetProviderConfigResponse]:
        ...
    def list_provider_configs(self, req: ClientRequest[policy.keymanagement.key_management_pb2.ListProviderConfigsRequest]) -> ServerResponse[policy.keymanagement.key_management_pb2.ListProviderConfigsResponse]:
        ...
    def update_provider_config(self, req: ClientRequest[policy.keymanagement.key_management_pb2.UpdateProviderConfigRequest]) -> ServerResponse[policy.keymanagement.key_management_pb2.UpdateProviderConfigResponse]:
        ...
    def delete_provider_config(self, req: ClientRequest[policy.keymanagement.key_management_pb2.DeleteProviderConfigRequest]) -> ServerResponse[policy.keymanagement.key_management_pb2.DeleteProviderConfigResponse]:
        ...

KEY_MANAGEMENT_SERVICE_PATH_PREFIX = "/policy.keymanagement.KeyManagementService"

def wsgi_key_management_service(implementation: KeyManagementServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.keymanagement.KeyManagementService/CreateProviderConfig", implementation.create_provider_config, policy.keymanagement.key_management_pb2.CreateProviderConfigRequest)
    app.register_unary_rpc("/policy.keymanagement.KeyManagementService/GetProviderConfig", implementation.get_provider_config, policy.keymanagement.key_management_pb2.GetProviderConfigRequest)
    app.register_unary_rpc("/policy.keymanagement.KeyManagementService/ListProviderConfigs", implementation.list_provider_configs, policy.keymanagement.key_management_pb2.ListProviderConfigsRequest)
    app.register_unary_rpc("/policy.keymanagement.KeyManagementService/UpdateProviderConfig", implementation.update_provider_config, policy.keymanagement.key_management_pb2.UpdateProviderConfigRequest)
    app.register_unary_rpc("/policy.keymanagement.KeyManagementService/DeleteProviderConfig", implementation.delete_provider_config, policy.keymanagement.key_management_pb2.DeleteProviderConfigRequest)
    return app
