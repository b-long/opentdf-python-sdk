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

import policy.kasregistry.key_access_server_registry_pb2

class KeyAccessServerRegistryServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_list_key_access_servers(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse]:
        """Low-level method to call ListKeyAccessServers, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/ListKeyAccessServers"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse,extra_headers, timeout_seconds)


    def list_key_access_servers(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse:
        response = self.call_list_key_access_servers(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse]:
        """Low-level method to call GetKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/GetKeyAccessServer"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse,extra_headers, timeout_seconds)


    def get_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse:
        response = self.call_get_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse]:
        """Low-level method to call CreateKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/CreateKeyAccessServer"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse,extra_headers, timeout_seconds)


    def create_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse:
        response = self.call_create_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse]:
        """Low-level method to call UpdateKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/UpdateKeyAccessServer"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse,extra_headers, timeout_seconds)


    def update_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse:
        response = self.call_update_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse]:
        """Low-level method to call DeleteKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/DeleteKeyAccessServer"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse,extra_headers, timeout_seconds)


    def delete_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse:
        response = self.call_delete_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_key_access_server_grants(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse]:
        """Low-level method to call ListKeyAccessServerGrants, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/ListKeyAccessServerGrants"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse,extra_headers, timeout_seconds)


    def list_key_access_server_grants(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse:
        response = self.call_list_key_access_server_grants(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse]:
        """Low-level method to call CreateKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/CreateKey"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse,extra_headers, timeout_seconds)


    def create_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse:
        response = self.call_create_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse]:
        """Low-level method to call GetKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/GetKey"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse,extra_headers, timeout_seconds)


    def get_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse:
        response = self.call_get_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_keys(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeysRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse]:
        """Low-level method to call ListKeys, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/ListKeys"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse,extra_headers, timeout_seconds)


    def list_keys(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeysRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse:
        response = self.call_list_keys(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse]:
        """Low-level method to call UpdateKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/UpdateKey"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse,extra_headers, timeout_seconds)


    def update_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse:
        response = self.call_update_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_rotate_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.RotateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse]:
        """Low-level method to call RotateKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/RotateKey"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse,extra_headers, timeout_seconds)


    def rotate_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.RotateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse:
        response = self.call_rotate_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_set_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse]:
        """Low-level method to call SetBaseKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/SetBaseKey"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse,extra_headers, timeout_seconds)


    def set_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse:
        response = self.call_set_base_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse]:
        """Low-level method to call GetBaseKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/GetBaseKey"
        return self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse,extra_headers, timeout_seconds)


    def get_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse:
        response = self.call_get_base_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncKeyAccessServerRegistryServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_list_key_access_servers(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse]:
        """Low-level method to call ListKeyAccessServers, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/ListKeyAccessServers"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse,extra_headers, timeout_seconds)

    async def list_key_access_servers(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse:
        response = await self.call_list_key_access_servers(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse]:
        """Low-level method to call GetKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/GetKeyAccessServer"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse,extra_headers, timeout_seconds)

    async def get_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse:
        response = await self.call_get_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse]:
        """Low-level method to call CreateKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/CreateKeyAccessServer"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse,extra_headers, timeout_seconds)

    async def create_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse:
        response = await self.call_create_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse]:
        """Low-level method to call UpdateKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/UpdateKeyAccessServer"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse,extra_headers, timeout_seconds)

    async def update_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse:
        response = await self.call_update_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse]:
        """Low-level method to call DeleteKeyAccessServer, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/DeleteKeyAccessServer"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse,extra_headers, timeout_seconds)

    async def delete_key_access_server(
        self, req: policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse:
        response = await self.call_delete_key_access_server(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_key_access_server_grants(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse]:
        """Low-level method to call ListKeyAccessServerGrants, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/ListKeyAccessServerGrants"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse,extra_headers, timeout_seconds)

    async def list_key_access_server_grants(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse:
        response = await self.call_list_key_access_server_grants(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse]:
        """Low-level method to call CreateKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/CreateKey"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse,extra_headers, timeout_seconds)

    async def create_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.CreateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse:
        response = await self.call_create_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse]:
        """Low-level method to call GetKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/GetKey"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse,extra_headers, timeout_seconds)

    async def get_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse:
        response = await self.call_get_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_keys(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeysRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse]:
        """Low-level method to call ListKeys, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/ListKeys"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse,extra_headers, timeout_seconds)

    async def list_keys(
        self, req: policy.kasregistry.key_access_server_registry_pb2.ListKeysRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse:
        response = await self.call_list_keys(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse]:
        """Low-level method to call UpdateKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/UpdateKey"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse,extra_headers, timeout_seconds)

    async def update_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.UpdateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse:
        response = await self.call_update_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_rotate_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.RotateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse]:
        """Low-level method to call RotateKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/RotateKey"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse,extra_headers, timeout_seconds)

    async def rotate_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.RotateKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse:
        response = await self.call_rotate_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_set_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse]:
        """Low-level method to call SetBaseKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/SetBaseKey"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse,extra_headers, timeout_seconds)

    async def set_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse:
        response = await self.call_set_base_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse]:
        """Low-level method to call GetBaseKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.kasregistry.KeyAccessServerRegistryService/GetBaseKey"
        return await self._connect_client.call_unary(url, req, policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse,extra_headers, timeout_seconds)

    async def get_base_key(
        self, req: policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse:
        response = await self.call_get_base_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class KeyAccessServerRegistryServiceProtocol(typing.Protocol):
    def list_key_access_servers(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersResponse]:
        ...
    def get_key_access_server(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerResponse]:
        ...
    def create_key_access_server(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerResponse]:
        ...
    def update_key_access_server(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerResponse]:
        ...
    def delete_key_access_server(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerResponse]:
        ...
    def list_key_access_server_grants(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsResponse]:
        ...
    def create_key(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.CreateKeyRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.CreateKeyResponse]:
        ...
    def get_key(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.GetKeyRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.GetKeyResponse]:
        ...
    def list_keys(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.ListKeysRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.ListKeysResponse]:
        ...
    def update_key(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.UpdateKeyResponse]:
        ...
    def rotate_key(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.RotateKeyRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.RotateKeyResponse]:
        ...
    def set_base_key(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyResponse]:
        ...
    def get_base_key(self, req: ClientRequest[policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyRequest]) -> ServerResponse[policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyResponse]:
        ...

KEY_ACCESS_SERVER_REGISTRY_SERVICE_PATH_PREFIX = "/policy.kasregistry.KeyAccessServerRegistryService"

def wsgi_key_access_server_registry_service(implementation: KeyAccessServerRegistryServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/ListKeyAccessServers", implementation.list_key_access_servers, policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServersRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/GetKeyAccessServer", implementation.get_key_access_server, policy.kasregistry.key_access_server_registry_pb2.GetKeyAccessServerRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/CreateKeyAccessServer", implementation.create_key_access_server, policy.kasregistry.key_access_server_registry_pb2.CreateKeyAccessServerRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/UpdateKeyAccessServer", implementation.update_key_access_server, policy.kasregistry.key_access_server_registry_pb2.UpdateKeyAccessServerRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/DeleteKeyAccessServer", implementation.delete_key_access_server, policy.kasregistry.key_access_server_registry_pb2.DeleteKeyAccessServerRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/ListKeyAccessServerGrants", implementation.list_key_access_server_grants, policy.kasregistry.key_access_server_registry_pb2.ListKeyAccessServerGrantsRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/CreateKey", implementation.create_key, policy.kasregistry.key_access_server_registry_pb2.CreateKeyRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/GetKey", implementation.get_key, policy.kasregistry.key_access_server_registry_pb2.GetKeyRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/ListKeys", implementation.list_keys, policy.kasregistry.key_access_server_registry_pb2.ListKeysRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/UpdateKey", implementation.update_key, policy.kasregistry.key_access_server_registry_pb2.UpdateKeyRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/RotateKey", implementation.rotate_key, policy.kasregistry.key_access_server_registry_pb2.RotateKeyRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/SetBaseKey", implementation.set_base_key, policy.kasregistry.key_access_server_registry_pb2.SetBaseKeyRequest)
    app.register_unary_rpc("/policy.kasregistry.KeyAccessServerRegistryService/GetBaseKey", implementation.get_base_key, policy.kasregistry.key_access_server_registry_pb2.GetBaseKeyRequest)
    return app
