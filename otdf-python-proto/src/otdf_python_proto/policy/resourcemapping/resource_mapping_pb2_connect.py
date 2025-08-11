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

import policy.resourcemapping.resource_mapping_pb2

class ResourceMappingServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_list_resource_mapping_groups(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse]:
        """Low-level method to call ListResourceMappingGroups, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/ListResourceMappingGroups"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse,extra_headers, timeout_seconds)


    def list_resource_mapping_groups(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse:
        response = self.call_list_resource_mapping_groups(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse]:
        """Low-level method to call GetResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/GetResourceMappingGroup"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse,extra_headers, timeout_seconds)


    def get_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse:
        response = self.call_get_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse]:
        """Low-level method to call CreateResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/CreateResourceMappingGroup"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse,extra_headers, timeout_seconds)


    def create_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse:
        response = self.call_create_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse]:
        """Low-level method to call UpdateResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/UpdateResourceMappingGroup"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse,extra_headers, timeout_seconds)


    def update_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse:
        response = self.call_update_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse]:
        """Low-level method to call DeleteResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/DeleteResourceMappingGroup"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse,extra_headers, timeout_seconds)


    def delete_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse:
        response = self.call_delete_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_resource_mappings(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse]:
        """Low-level method to call ListResourceMappings, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/ListResourceMappings"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse,extra_headers, timeout_seconds)


    def list_resource_mappings(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse:
        response = self.call_list_resource_mappings(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_resource_mappings_by_group_fqns(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse]:
        """Low-level method to call ListResourceMappingsByGroupFqns, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/ListResourceMappingsByGroupFqns"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse,extra_headers, timeout_seconds)


    def list_resource_mappings_by_group_fqns(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse:
        response = self.call_list_resource_mappings_by_group_fqns(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse]:
        """Low-level method to call GetResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/GetResourceMapping"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse,extra_headers, timeout_seconds)


    def get_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse:
        response = self.call_get_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse]:
        """Low-level method to call CreateResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/CreateResourceMapping"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse,extra_headers, timeout_seconds)


    def create_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse:
        response = self.call_create_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse]:
        """Low-level method to call UpdateResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/UpdateResourceMapping"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse,extra_headers, timeout_seconds)


    def update_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse:
        response = self.call_update_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse]:
        """Low-level method to call DeleteResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/DeleteResourceMapping"
        return self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse,extra_headers, timeout_seconds)


    def delete_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse:
        response = self.call_delete_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncResourceMappingServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_list_resource_mapping_groups(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse]:
        """Low-level method to call ListResourceMappingGroups, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/ListResourceMappingGroups"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse,extra_headers, timeout_seconds)

    async def list_resource_mapping_groups(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse:
        response = await self.call_list_resource_mapping_groups(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse]:
        """Low-level method to call GetResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/GetResourceMappingGroup"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse,extra_headers, timeout_seconds)

    async def get_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse:
        response = await self.call_get_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse]:
        """Low-level method to call CreateResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/CreateResourceMappingGroup"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse,extra_headers, timeout_seconds)

    async def create_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse:
        response = await self.call_create_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse]:
        """Low-level method to call UpdateResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/UpdateResourceMappingGroup"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse,extra_headers, timeout_seconds)

    async def update_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse:
        response = await self.call_update_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse]:
        """Low-level method to call DeleteResourceMappingGroup, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/DeleteResourceMappingGroup"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse,extra_headers, timeout_seconds)

    async def delete_resource_mapping_group(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse:
        response = await self.call_delete_resource_mapping_group(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_resource_mappings(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse]:
        """Low-level method to call ListResourceMappings, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/ListResourceMappings"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse,extra_headers, timeout_seconds)

    async def list_resource_mappings(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse:
        response = await self.call_list_resource_mappings(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_resource_mappings_by_group_fqns(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse]:
        """Low-level method to call ListResourceMappingsByGroupFqns, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/ListResourceMappingsByGroupFqns"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse,extra_headers, timeout_seconds)

    async def list_resource_mappings_by_group_fqns(
        self, req: policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse:
        response = await self.call_list_resource_mappings_by_group_fqns(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse]:
        """Low-level method to call GetResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/GetResourceMapping"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse,extra_headers, timeout_seconds)

    async def get_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.GetResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse:
        response = await self.call_get_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse]:
        """Low-level method to call CreateResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/CreateResourceMapping"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse,extra_headers, timeout_seconds)

    async def create_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse:
        response = await self.call_create_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse]:
        """Low-level method to call UpdateResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/UpdateResourceMapping"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse,extra_headers, timeout_seconds)

    async def update_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse:
        response = await self.call_update_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse]:
        """Low-level method to call DeleteResourceMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.resourcemapping.ResourceMappingService/DeleteResourceMapping"
        return await self._connect_client.call_unary(url, req, policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse,extra_headers, timeout_seconds)

    async def delete_resource_mapping(
        self, req: policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse:
        response = await self.call_delete_resource_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class ResourceMappingServiceProtocol(typing.Protocol):
    def list_resource_mapping_groups(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsResponse]:
        ...
    def get_resource_mapping_group(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupResponse]:
        ...
    def create_resource_mapping_group(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupResponse]:
        ...
    def update_resource_mapping_group(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupResponse]:
        ...
    def delete_resource_mapping_group(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupResponse]:
        ...
    def list_resource_mappings(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsResponse]:
        ...
    def list_resource_mappings_by_group_fqns(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsResponse]:
        ...
    def get_resource_mapping(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.GetResourceMappingResponse]:
        ...
    def create_resource_mapping(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingResponse]:
        ...
    def update_resource_mapping(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingResponse]:
        ...
    def delete_resource_mapping(self, req: ClientRequest[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingRequest]) -> ServerResponse[policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingResponse]:
        ...

RESOURCE_MAPPING_SERVICE_PATH_PREFIX = "/policy.resourcemapping.ResourceMappingService"

def wsgi_resource_mapping_service(implementation: ResourceMappingServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/ListResourceMappingGroups", implementation.list_resource_mapping_groups, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingGroupsRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/GetResourceMappingGroup", implementation.get_resource_mapping_group, policy.resourcemapping.resource_mapping_pb2.GetResourceMappingGroupRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/CreateResourceMappingGroup", implementation.create_resource_mapping_group, policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingGroupRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/UpdateResourceMappingGroup", implementation.update_resource_mapping_group, policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingGroupRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/DeleteResourceMappingGroup", implementation.delete_resource_mapping_group, policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingGroupRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/ListResourceMappings", implementation.list_resource_mappings, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/ListResourceMappingsByGroupFqns", implementation.list_resource_mappings_by_group_fqns, policy.resourcemapping.resource_mapping_pb2.ListResourceMappingsByGroupFqnsRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/GetResourceMapping", implementation.get_resource_mapping, policy.resourcemapping.resource_mapping_pb2.GetResourceMappingRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/CreateResourceMapping", implementation.create_resource_mapping, policy.resourcemapping.resource_mapping_pb2.CreateResourceMappingRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/UpdateResourceMapping", implementation.update_resource_mapping, policy.resourcemapping.resource_mapping_pb2.UpdateResourceMappingRequest)
    app.register_unary_rpc("/policy.resourcemapping.ResourceMappingService/DeleteResourceMapping", implementation.delete_resource_mapping, policy.resourcemapping.resource_mapping_pb2.DeleteResourceMappingRequest)
    return app
