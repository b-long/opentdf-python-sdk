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

import policy.registeredresources.registered_resources_pb2

class RegisteredResourcesServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_create_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse]:
        """Low-level method to call CreateRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/CreateRegisteredResource"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse,extra_headers, timeout_seconds)


    def create_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse:
        response = self.call_create_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse]:
        """Low-level method to call GetRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/GetRegisteredResource"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse,extra_headers, timeout_seconds)


    def get_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse:
        response = self.call_get_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_registered_resources(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse]:
        """Low-level method to call ListRegisteredResources, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/ListRegisteredResources"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse,extra_headers, timeout_seconds)


    def list_registered_resources(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse:
        response = self.call_list_registered_resources(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse]:
        """Low-level method to call UpdateRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/UpdateRegisteredResource"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse,extra_headers, timeout_seconds)


    def update_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse:
        response = self.call_update_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse]:
        """Low-level method to call DeleteRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/DeleteRegisteredResource"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse,extra_headers, timeout_seconds)


    def delete_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse:
        response = self.call_delete_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse]:
        """Low-level method to call CreateRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/CreateRegisteredResourceValue"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse,extra_headers, timeout_seconds)


    def create_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse:
        response = self.call_create_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse]:
        """Low-level method to call GetRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/GetRegisteredResourceValue"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse,extra_headers, timeout_seconds)


    def get_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse:
        response = self.call_get_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_registered_resource_values_by_fq_ns(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse]:
        """Low-level method to call GetRegisteredResourceValuesByFQNs, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/GetRegisteredResourceValuesByFQNs"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse,extra_headers, timeout_seconds)


    def get_registered_resource_values_by_fq_ns(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse:
        response = self.call_get_registered_resource_values_by_fq_ns(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_registered_resource_values(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse]:
        """Low-level method to call ListRegisteredResourceValues, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/ListRegisteredResourceValues"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse,extra_headers, timeout_seconds)


    def list_registered_resource_values(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse:
        response = self.call_list_registered_resource_values(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse]:
        """Low-level method to call UpdateRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/UpdateRegisteredResourceValue"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse,extra_headers, timeout_seconds)


    def update_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse:
        response = self.call_update_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse]:
        """Low-level method to call DeleteRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/DeleteRegisteredResourceValue"
        return self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse,extra_headers, timeout_seconds)


    def delete_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse:
        response = self.call_delete_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncRegisteredResourcesServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_create_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse]:
        """Low-level method to call CreateRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/CreateRegisteredResource"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse,extra_headers, timeout_seconds)

    async def create_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse:
        response = await self.call_create_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse]:
        """Low-level method to call GetRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/GetRegisteredResource"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse,extra_headers, timeout_seconds)

    async def get_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse:
        response = await self.call_get_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_registered_resources(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse]:
        """Low-level method to call ListRegisteredResources, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/ListRegisteredResources"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse,extra_headers, timeout_seconds)

    async def list_registered_resources(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse:
        response = await self.call_list_registered_resources(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse]:
        """Low-level method to call UpdateRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/UpdateRegisteredResource"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse,extra_headers, timeout_seconds)

    async def update_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse:
        response = await self.call_update_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse]:
        """Low-level method to call DeleteRegisteredResource, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/DeleteRegisteredResource"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse,extra_headers, timeout_seconds)

    async def delete_registered_resource(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse:
        response = await self.call_delete_registered_resource(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse]:
        """Low-level method to call CreateRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/CreateRegisteredResourceValue"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse,extra_headers, timeout_seconds)

    async def create_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse:
        response = await self.call_create_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse]:
        """Low-level method to call GetRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/GetRegisteredResourceValue"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse,extra_headers, timeout_seconds)

    async def get_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse:
        response = await self.call_get_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_registered_resource_values_by_fq_ns(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse]:
        """Low-level method to call GetRegisteredResourceValuesByFQNs, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/GetRegisteredResourceValuesByFQNs"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse,extra_headers, timeout_seconds)

    async def get_registered_resource_values_by_fq_ns(
        self, req: policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse:
        response = await self.call_get_registered_resource_values_by_fq_ns(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_registered_resource_values(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse]:
        """Low-level method to call ListRegisteredResourceValues, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/ListRegisteredResourceValues"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse,extra_headers, timeout_seconds)

    async def list_registered_resource_values(
        self, req: policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse:
        response = await self.call_list_registered_resource_values(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse]:
        """Low-level method to call UpdateRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/UpdateRegisteredResourceValue"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse,extra_headers, timeout_seconds)

    async def update_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse:
        response = await self.call_update_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse]:
        """Low-level method to call DeleteRegisteredResourceValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.registeredresources.RegisteredResourcesService/DeleteRegisteredResourceValue"
        return await self._connect_client.call_unary(url, req, policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse,extra_headers, timeout_seconds)

    async def delete_registered_resource_value(
        self, req: policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse:
        response = await self.call_delete_registered_resource_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class RegisteredResourcesServiceProtocol(typing.Protocol):
    def create_registered_resource(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceResponse]:
        ...
    def get_registered_resource(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceResponse]:
        ...
    def list_registered_resources(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesResponse]:
        ...
    def update_registered_resource(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceResponse]:
        ...
    def delete_registered_resource(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceResponse]:
        ...
    def create_registered_resource_value(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueResponse]:
        ...
    def get_registered_resource_value(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueResponse]:
        ...
    def get_registered_resource_values_by_fq_ns(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsResponse]:
        ...
    def list_registered_resource_values(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesResponse]:
        ...
    def update_registered_resource_value(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueResponse]:
        ...
    def delete_registered_resource_value(self, req: ClientRequest[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueRequest]) -> ServerResponse[policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueResponse]:
        ...

REGISTERED_RESOURCES_SERVICE_PATH_PREFIX = "/policy.registeredresources.RegisteredResourcesService"

def wsgi_registered_resources_service(implementation: RegisteredResourcesServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/CreateRegisteredResource", implementation.create_registered_resource, policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/GetRegisteredResource", implementation.get_registered_resource, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/ListRegisteredResources", implementation.list_registered_resources, policy.registeredresources.registered_resources_pb2.ListRegisteredResourcesRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/UpdateRegisteredResource", implementation.update_registered_resource, policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/DeleteRegisteredResource", implementation.delete_registered_resource, policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/CreateRegisteredResourceValue", implementation.create_registered_resource_value, policy.registeredresources.registered_resources_pb2.CreateRegisteredResourceValueRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/GetRegisteredResourceValue", implementation.get_registered_resource_value, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValueRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/GetRegisteredResourceValuesByFQNs", implementation.get_registered_resource_values_by_fq_ns, policy.registeredresources.registered_resources_pb2.GetRegisteredResourceValuesByFQNsRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/ListRegisteredResourceValues", implementation.list_registered_resource_values, policy.registeredresources.registered_resources_pb2.ListRegisteredResourceValuesRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/UpdateRegisteredResourceValue", implementation.update_registered_resource_value, policy.registeredresources.registered_resources_pb2.UpdateRegisteredResourceValueRequest)
    app.register_unary_rpc("/policy.registeredresources.RegisteredResourcesService/DeleteRegisteredResourceValue", implementation.delete_registered_resource_value, policy.registeredresources.registered_resources_pb2.DeleteRegisteredResourceValueRequest)
    return app
