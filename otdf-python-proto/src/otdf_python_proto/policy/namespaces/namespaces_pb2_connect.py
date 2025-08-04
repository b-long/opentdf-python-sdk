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

import policy.namespaces.namespaces_pb2

class NamespaceServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_get_namespace(
        self, req: policy.namespaces.namespaces_pb2.GetNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.GetNamespaceResponse]:
        """Low-level method to call GetNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/GetNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.GetNamespaceResponse,extra_headers, timeout_seconds)


    def get_namespace(
        self, req: policy.namespaces.namespaces_pb2.GetNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.GetNamespaceResponse:
        response = self.call_get_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_namespaces(
        self, req: policy.namespaces.namespaces_pb2.ListNamespacesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.ListNamespacesResponse]:
        """Low-level method to call ListNamespaces, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/ListNamespaces"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.ListNamespacesResponse,extra_headers, timeout_seconds)


    def list_namespaces(
        self, req: policy.namespaces.namespaces_pb2.ListNamespacesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.ListNamespacesResponse:
        response = self.call_list_namespaces(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_namespace(
        self, req: policy.namespaces.namespaces_pb2.CreateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.CreateNamespaceResponse]:
        """Low-level method to call CreateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/CreateNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.CreateNamespaceResponse,extra_headers, timeout_seconds)


    def create_namespace(
        self, req: policy.namespaces.namespaces_pb2.CreateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.CreateNamespaceResponse:
        response = self.call_create_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_namespace(
        self, req: policy.namespaces.namespaces_pb2.UpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.UpdateNamespaceResponse]:
        """Low-level method to call UpdateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/UpdateNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.UpdateNamespaceResponse,extra_headers, timeout_seconds)


    def update_namespace(
        self, req: policy.namespaces.namespaces_pb2.UpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.UpdateNamespaceResponse:
        response = self.call_update_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_deactivate_namespace(
        self, req: policy.namespaces.namespaces_pb2.DeactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse]:
        """Low-level method to call DeactivateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/DeactivateNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse,extra_headers, timeout_seconds)


    def deactivate_namespace(
        self, req: policy.namespaces.namespaces_pb2.DeactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse:
        response = self.call_deactivate_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_assign_key_access_server_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse]:
        """Low-level method to call AssignKeyAccessServerToNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/AssignKeyAccessServerToNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse,extra_headers, timeout_seconds)


    def assign_key_access_server_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse:
        response = self.call_assign_key_access_server_to_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_remove_key_access_server_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse]:
        """Low-level method to call RemoveKeyAccessServerFromNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/RemoveKeyAccessServerFromNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse,extra_headers, timeout_seconds)


    def remove_key_access_server_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse:
        response = self.call_remove_key_access_server_from_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_assign_public_key_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse]:
        """Low-level method to call AssignPublicKeyToNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/AssignPublicKeyToNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse,extra_headers, timeout_seconds)


    def assign_public_key_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse:
        response = self.call_assign_public_key_to_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_remove_public_key_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse]:
        """Low-level method to call RemovePublicKeyFromNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/RemovePublicKeyFromNamespace"
        return self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse,extra_headers, timeout_seconds)


    def remove_public_key_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse:
        response = self.call_remove_public_key_from_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncNamespaceServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_get_namespace(
        self, req: policy.namespaces.namespaces_pb2.GetNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.GetNamespaceResponse]:
        """Low-level method to call GetNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/GetNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.GetNamespaceResponse,extra_headers, timeout_seconds)

    async def get_namespace(
        self, req: policy.namespaces.namespaces_pb2.GetNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.GetNamespaceResponse:
        response = await self.call_get_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_namespaces(
        self, req: policy.namespaces.namespaces_pb2.ListNamespacesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.ListNamespacesResponse]:
        """Low-level method to call ListNamespaces, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/ListNamespaces"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.ListNamespacesResponse,extra_headers, timeout_seconds)

    async def list_namespaces(
        self, req: policy.namespaces.namespaces_pb2.ListNamespacesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.ListNamespacesResponse:
        response = await self.call_list_namespaces(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_namespace(
        self, req: policy.namespaces.namespaces_pb2.CreateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.CreateNamespaceResponse]:
        """Low-level method to call CreateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/CreateNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.CreateNamespaceResponse,extra_headers, timeout_seconds)

    async def create_namespace(
        self, req: policy.namespaces.namespaces_pb2.CreateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.CreateNamespaceResponse:
        response = await self.call_create_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_namespace(
        self, req: policy.namespaces.namespaces_pb2.UpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.UpdateNamespaceResponse]:
        """Low-level method to call UpdateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/UpdateNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.UpdateNamespaceResponse,extra_headers, timeout_seconds)

    async def update_namespace(
        self, req: policy.namespaces.namespaces_pb2.UpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.UpdateNamespaceResponse:
        response = await self.call_update_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_deactivate_namespace(
        self, req: policy.namespaces.namespaces_pb2.DeactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse]:
        """Low-level method to call DeactivateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/DeactivateNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse,extra_headers, timeout_seconds)

    async def deactivate_namespace(
        self, req: policy.namespaces.namespaces_pb2.DeactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse:
        response = await self.call_deactivate_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_assign_key_access_server_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse]:
        """Low-level method to call AssignKeyAccessServerToNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/AssignKeyAccessServerToNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse,extra_headers, timeout_seconds)

    async def assign_key_access_server_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse:
        response = await self.call_assign_key_access_server_to_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_remove_key_access_server_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse]:
        """Low-level method to call RemoveKeyAccessServerFromNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/RemoveKeyAccessServerFromNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse,extra_headers, timeout_seconds)

    async def remove_key_access_server_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse:
        response = await self.call_remove_key_access_server_from_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_assign_public_key_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse]:
        """Low-level method to call AssignPublicKeyToNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/AssignPublicKeyToNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse,extra_headers, timeout_seconds)

    async def assign_public_key_to_namespace(
        self, req: policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse:
        response = await self.call_assign_public_key_to_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_remove_public_key_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse]:
        """Low-level method to call RemovePublicKeyFromNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.namespaces.NamespaceService/RemovePublicKeyFromNamespace"
        return await self._connect_client.call_unary(url, req, policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse,extra_headers, timeout_seconds)

    async def remove_public_key_from_namespace(
        self, req: policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse:
        response = await self.call_remove_public_key_from_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class NamespaceServiceProtocol(typing.Protocol):
    def get_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.GetNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.GetNamespaceResponse]:
        ...
    def list_namespaces(self, req: ClientRequest[policy.namespaces.namespaces_pb2.ListNamespacesRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.ListNamespacesResponse]:
        ...
    def create_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.CreateNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.CreateNamespaceResponse]:
        ...
    def update_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.UpdateNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.UpdateNamespaceResponse]:
        ...
    def deactivate_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.DeactivateNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.DeactivateNamespaceResponse]:
        ...
    def assign_key_access_server_to_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceResponse]:
        ...
    def remove_key_access_server_from_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceResponse]:
        ...
    def assign_public_key_to_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceResponse]:
        ...
    def remove_public_key_from_namespace(self, req: ClientRequest[policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceRequest]) -> ServerResponse[policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceResponse]:
        ...

NAMESPACE_SERVICE_PATH_PREFIX = "/policy.namespaces.NamespaceService"

def wsgi_namespace_service(implementation: NamespaceServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.namespaces.NamespaceService/GetNamespace", implementation.get_namespace, policy.namespaces.namespaces_pb2.GetNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/ListNamespaces", implementation.list_namespaces, policy.namespaces.namespaces_pb2.ListNamespacesRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/CreateNamespace", implementation.create_namespace, policy.namespaces.namespaces_pb2.CreateNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/UpdateNamespace", implementation.update_namespace, policy.namespaces.namespaces_pb2.UpdateNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/DeactivateNamespace", implementation.deactivate_namespace, policy.namespaces.namespaces_pb2.DeactivateNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/AssignKeyAccessServerToNamespace", implementation.assign_key_access_server_to_namespace, policy.namespaces.namespaces_pb2.AssignKeyAccessServerToNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/RemoveKeyAccessServerFromNamespace", implementation.remove_key_access_server_from_namespace, policy.namespaces.namespaces_pb2.RemoveKeyAccessServerFromNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/AssignPublicKeyToNamespace", implementation.assign_public_key_to_namespace, policy.namespaces.namespaces_pb2.AssignPublicKeyToNamespaceRequest)
    app.register_unary_rpc("/policy.namespaces.NamespaceService/RemovePublicKeyFromNamespace", implementation.remove_public_key_from_namespace, policy.namespaces.namespaces_pb2.RemovePublicKeyFromNamespaceRequest)
    return app
