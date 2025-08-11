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

import policy.subjectmapping.subject_mapping_pb2

class SubjectMappingServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_match_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse]:
        """Low-level method to call MatchSubjectMappings, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/MatchSubjectMappings"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse,extra_headers, timeout_seconds)


    def match_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse:
        response = self.call_match_subject_mappings(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse]:
        """Low-level method to call ListSubjectMappings, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/ListSubjectMappings"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse,extra_headers, timeout_seconds)


    def list_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse:
        response = self.call_list_subject_mappings(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse]:
        """Low-level method to call GetSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/GetSubjectMapping"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse,extra_headers, timeout_seconds)


    def get_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse:
        response = self.call_get_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse]:
        """Low-level method to call CreateSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/CreateSubjectMapping"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse,extra_headers, timeout_seconds)


    def create_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse:
        response = self.call_create_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse]:
        """Low-level method to call UpdateSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/UpdateSubjectMapping"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse,extra_headers, timeout_seconds)


    def update_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse:
        response = self.call_update_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse]:
        """Low-level method to call DeleteSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/DeleteSubjectMapping"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse,extra_headers, timeout_seconds)


    def delete_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse:
        response = self.call_delete_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse]:
        """Low-level method to call ListSubjectConditionSets, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/ListSubjectConditionSets"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse,extra_headers, timeout_seconds)


    def list_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse:
        response = self.call_list_subject_condition_sets(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse]:
        """Low-level method to call GetSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/GetSubjectConditionSet"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse,extra_headers, timeout_seconds)


    def get_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse:
        response = self.call_get_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse]:
        """Low-level method to call CreateSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/CreateSubjectConditionSet"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse,extra_headers, timeout_seconds)


    def create_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse:
        response = self.call_create_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse]:
        """Low-level method to call UpdateSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/UpdateSubjectConditionSet"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse,extra_headers, timeout_seconds)


    def update_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse:
        response = self.call_update_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse]:
        """Low-level method to call DeleteSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/DeleteSubjectConditionSet"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse,extra_headers, timeout_seconds)


    def delete_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse:
        response = self.call_delete_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_all_unmapped_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse]:
        """Low-level method to call DeleteAllUnmappedSubjectConditionSets, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/DeleteAllUnmappedSubjectConditionSets"
        return self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse,extra_headers, timeout_seconds)


    def delete_all_unmapped_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse:
        response = self.call_delete_all_unmapped_subject_condition_sets(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncSubjectMappingServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_match_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse]:
        """Low-level method to call MatchSubjectMappings, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/MatchSubjectMappings"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse,extra_headers, timeout_seconds)

    async def match_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse:
        response = await self.call_match_subject_mappings(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse]:
        """Low-level method to call ListSubjectMappings, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/ListSubjectMappings"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse,extra_headers, timeout_seconds)

    async def list_subject_mappings(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse:
        response = await self.call_list_subject_mappings(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse]:
        """Low-level method to call GetSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/GetSubjectMapping"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse,extra_headers, timeout_seconds)

    async def get_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse:
        response = await self.call_get_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse]:
        """Low-level method to call CreateSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/CreateSubjectMapping"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse,extra_headers, timeout_seconds)

    async def create_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse:
        response = await self.call_create_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse]:
        """Low-level method to call UpdateSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/UpdateSubjectMapping"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse,extra_headers, timeout_seconds)

    async def update_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse:
        response = await self.call_update_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse]:
        """Low-level method to call DeleteSubjectMapping, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/DeleteSubjectMapping"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse,extra_headers, timeout_seconds)

    async def delete_subject_mapping(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse:
        response = await self.call_delete_subject_mapping(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse]:
        """Low-level method to call ListSubjectConditionSets, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/ListSubjectConditionSets"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse,extra_headers, timeout_seconds)

    async def list_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse:
        response = await self.call_list_subject_condition_sets(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse]:
        """Low-level method to call GetSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/GetSubjectConditionSet"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse,extra_headers, timeout_seconds)

    async def get_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse:
        response = await self.call_get_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse]:
        """Low-level method to call CreateSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/CreateSubjectConditionSet"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse,extra_headers, timeout_seconds)

    async def create_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse:
        response = await self.call_create_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse]:
        """Low-level method to call UpdateSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/UpdateSubjectConditionSet"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse,extra_headers, timeout_seconds)

    async def update_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse:
        response = await self.call_update_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse]:
        """Low-level method to call DeleteSubjectConditionSet, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/DeleteSubjectConditionSet"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse,extra_headers, timeout_seconds)

    async def delete_subject_condition_set(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse:
        response = await self.call_delete_subject_condition_set(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_all_unmapped_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse]:
        """Low-level method to call DeleteAllUnmappedSubjectConditionSets, granting access to errors and metadata"""
        url = self.base_url + "/policy.subjectmapping.SubjectMappingService/DeleteAllUnmappedSubjectConditionSets"
        return await self._connect_client.call_unary(url, req, policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse,extra_headers, timeout_seconds)

    async def delete_all_unmapped_subject_condition_sets(
        self, req: policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse:
        response = await self.call_delete_all_unmapped_subject_condition_sets(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class SubjectMappingServiceProtocol(typing.Protocol):
    def match_subject_mappings(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsResponse]:
        ...
    def list_subject_mappings(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsResponse]:
        ...
    def get_subject_mapping(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingResponse]:
        ...
    def create_subject_mapping(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingResponse]:
        ...
    def update_subject_mapping(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingResponse]:
        ...
    def delete_subject_mapping(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingResponse]:
        ...
    def list_subject_condition_sets(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsResponse]:
        ...
    def get_subject_condition_set(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetResponse]:
        ...
    def create_subject_condition_set(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetResponse]:
        ...
    def update_subject_condition_set(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetResponse]:
        ...
    def delete_subject_condition_set(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetResponse]:
        ...
    def delete_all_unmapped_subject_condition_sets(self, req: ClientRequest[policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsRequest]) -> ServerResponse[policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsResponse]:
        ...

SUBJECT_MAPPING_SERVICE_PATH_PREFIX = "/policy.subjectmapping.SubjectMappingService"

def wsgi_subject_mapping_service(implementation: SubjectMappingServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/MatchSubjectMappings", implementation.match_subject_mappings, policy.subjectmapping.subject_mapping_pb2.MatchSubjectMappingsRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/ListSubjectMappings", implementation.list_subject_mappings, policy.subjectmapping.subject_mapping_pb2.ListSubjectMappingsRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/GetSubjectMapping", implementation.get_subject_mapping, policy.subjectmapping.subject_mapping_pb2.GetSubjectMappingRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/CreateSubjectMapping", implementation.create_subject_mapping, policy.subjectmapping.subject_mapping_pb2.CreateSubjectMappingRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/UpdateSubjectMapping", implementation.update_subject_mapping, policy.subjectmapping.subject_mapping_pb2.UpdateSubjectMappingRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/DeleteSubjectMapping", implementation.delete_subject_mapping, policy.subjectmapping.subject_mapping_pb2.DeleteSubjectMappingRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/ListSubjectConditionSets", implementation.list_subject_condition_sets, policy.subjectmapping.subject_mapping_pb2.ListSubjectConditionSetsRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/GetSubjectConditionSet", implementation.get_subject_condition_set, policy.subjectmapping.subject_mapping_pb2.GetSubjectConditionSetRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/CreateSubjectConditionSet", implementation.create_subject_condition_set, policy.subjectmapping.subject_mapping_pb2.CreateSubjectConditionSetRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/UpdateSubjectConditionSet", implementation.update_subject_condition_set, policy.subjectmapping.subject_mapping_pb2.UpdateSubjectConditionSetRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/DeleteSubjectConditionSet", implementation.delete_subject_condition_set, policy.subjectmapping.subject_mapping_pb2.DeleteSubjectConditionSetRequest)
    app.register_unary_rpc("/policy.subjectmapping.SubjectMappingService/DeleteAllUnmappedSubjectConditionSets", implementation.delete_all_unmapped_subject_condition_sets, policy.subjectmapping.subject_mapping_pb2.DeleteAllUnmappedSubjectConditionSetsRequest)
    return app
