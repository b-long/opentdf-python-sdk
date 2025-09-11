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

import policy.attributes.attributes_pb2

class AttributesServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_list_attributes(
        self, req: policy.attributes.attributes_pb2.ListAttributesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.ListAttributesResponse]:
        """Low-level method to call ListAttributes, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/ListAttributes"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.ListAttributesResponse,extra_headers, timeout_seconds)


    def list_attributes(
        self, req: policy.attributes.attributes_pb2.ListAttributesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.ListAttributesResponse:
        response = self.call_list_attributes(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_attribute_values(
        self, req: policy.attributes.attributes_pb2.ListAttributeValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.ListAttributeValuesResponse]:
        """Low-level method to call ListAttributeValues, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/ListAttributeValues"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.ListAttributeValuesResponse,extra_headers, timeout_seconds)


    def list_attribute_values(
        self, req: policy.attributes.attributes_pb2.ListAttributeValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.ListAttributeValuesResponse:
        response = self.call_list_attribute_values(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_attribute(
        self, req: policy.attributes.attributes_pb2.GetAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.GetAttributeResponse]:
        """Low-level method to call GetAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/GetAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.GetAttributeResponse,extra_headers, timeout_seconds)


    def get_attribute(
        self, req: policy.attributes.attributes_pb2.GetAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.GetAttributeResponse:
        response = self.call_get_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_attribute_values_by_fqns(
        self, req: policy.attributes.attributes_pb2.GetAttributeValuesByFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse]:
        """Low-level method to call GetAttributeValuesByFqns, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/GetAttributeValuesByFqns"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse,extra_headers, timeout_seconds)


    def get_attribute_values_by_fqns(
        self, req: policy.attributes.attributes_pb2.GetAttributeValuesByFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse:
        response = self.call_get_attribute_values_by_fqns(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_attribute(
        self, req: policy.attributes.attributes_pb2.CreateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.CreateAttributeResponse]:
        """Low-level method to call CreateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/CreateAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.CreateAttributeResponse,extra_headers, timeout_seconds)


    def create_attribute(
        self, req: policy.attributes.attributes_pb2.CreateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.CreateAttributeResponse:
        response = self.call_create_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_attribute(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.UpdateAttributeResponse]:
        """Low-level method to call UpdateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/UpdateAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.UpdateAttributeResponse,extra_headers, timeout_seconds)


    def update_attribute(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.UpdateAttributeResponse:
        response = self.call_update_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_deactivate_attribute(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.DeactivateAttributeResponse]:
        """Low-level method to call DeactivateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/DeactivateAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.DeactivateAttributeResponse,extra_headers, timeout_seconds)


    def deactivate_attribute(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.DeactivateAttributeResponse:
        response = self.call_deactivate_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_get_attribute_value(
        self, req: policy.attributes.attributes_pb2.GetAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.GetAttributeValueResponse]:
        """Low-level method to call GetAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/GetAttributeValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.GetAttributeValueResponse,extra_headers, timeout_seconds)


    def get_attribute_value(
        self, req: policy.attributes.attributes_pb2.GetAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.GetAttributeValueResponse:
        response = self.call_get_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_attribute_value(
        self, req: policy.attributes.attributes_pb2.CreateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.CreateAttributeValueResponse]:
        """Low-level method to call CreateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/CreateAttributeValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.CreateAttributeValueResponse,extra_headers, timeout_seconds)


    def create_attribute_value(
        self, req: policy.attributes.attributes_pb2.CreateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.CreateAttributeValueResponse:
        response = self.call_create_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_attribute_value(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.UpdateAttributeValueResponse]:
        """Low-level method to call UpdateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/UpdateAttributeValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.UpdateAttributeValueResponse,extra_headers, timeout_seconds)


    def update_attribute_value(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.UpdateAttributeValueResponse:
        response = self.call_update_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_deactivate_attribute_value(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.DeactivateAttributeValueResponse]:
        """Low-level method to call DeactivateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/DeactivateAttributeValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.DeactivateAttributeValueResponse,extra_headers, timeout_seconds)


    def deactivate_attribute_value(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.DeactivateAttributeValueResponse:
        response = self.call_deactivate_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_assign_key_access_server_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse]:
        """Low-level method to call AssignKeyAccessServerToAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignKeyAccessServerToAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse,extra_headers, timeout_seconds)


    def assign_key_access_server_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse:
        response = self.call_assign_key_access_server_to_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_remove_key_access_server_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse]:
        """Low-level method to call RemoveKeyAccessServerFromAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemoveKeyAccessServerFromAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse,extra_headers, timeout_seconds)


    def remove_key_access_server_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse:
        response = self.call_remove_key_access_server_from_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_assign_key_access_server_to_value(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse]:
        """Low-level method to call AssignKeyAccessServerToValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignKeyAccessServerToValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse,extra_headers, timeout_seconds)


    def assign_key_access_server_to_value(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse:
        response = self.call_assign_key_access_server_to_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_remove_key_access_server_from_value(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse]:
        """Low-level method to call RemoveKeyAccessServerFromValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemoveKeyAccessServerFromValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse,extra_headers, timeout_seconds)


    def remove_key_access_server_from_value(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse:
        response = self.call_remove_key_access_server_from_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_assign_public_key_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse]:
        """Low-level method to call AssignPublicKeyToAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignPublicKeyToAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse,extra_headers, timeout_seconds)


    def assign_public_key_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse:
        response = self.call_assign_public_key_to_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_remove_public_key_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse]:
        """Low-level method to call RemovePublicKeyFromAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemovePublicKeyFromAttribute"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse,extra_headers, timeout_seconds)


    def remove_public_key_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse:
        response = self.call_remove_public_key_from_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_assign_public_key_to_value(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse]:
        """Low-level method to call AssignPublicKeyToValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignPublicKeyToValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse,extra_headers, timeout_seconds)


    def assign_public_key_to_value(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse:
        response = self.call_assign_public_key_to_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_remove_public_key_from_value(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse]:
        """Low-level method to call RemovePublicKeyFromValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemovePublicKeyFromValue"
        return self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse,extra_headers, timeout_seconds)


    def remove_public_key_from_value(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse:
        response = self.call_remove_public_key_from_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncAttributesServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_list_attributes(
        self, req: policy.attributes.attributes_pb2.ListAttributesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.ListAttributesResponse]:
        """Low-level method to call ListAttributes, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/ListAttributes"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.ListAttributesResponse,extra_headers, timeout_seconds)

    async def list_attributes(
        self, req: policy.attributes.attributes_pb2.ListAttributesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.ListAttributesResponse:
        response = await self.call_list_attributes(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_attribute_values(
        self, req: policy.attributes.attributes_pb2.ListAttributeValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.ListAttributeValuesResponse]:
        """Low-level method to call ListAttributeValues, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/ListAttributeValues"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.ListAttributeValuesResponse,extra_headers, timeout_seconds)

    async def list_attribute_values(
        self, req: policy.attributes.attributes_pb2.ListAttributeValuesRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.ListAttributeValuesResponse:
        response = await self.call_list_attribute_values(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_attribute(
        self, req: policy.attributes.attributes_pb2.GetAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.GetAttributeResponse]:
        """Low-level method to call GetAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/GetAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.GetAttributeResponse,extra_headers, timeout_seconds)

    async def get_attribute(
        self, req: policy.attributes.attributes_pb2.GetAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.GetAttributeResponse:
        response = await self.call_get_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_attribute_values_by_fqns(
        self, req: policy.attributes.attributes_pb2.GetAttributeValuesByFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse]:
        """Low-level method to call GetAttributeValuesByFqns, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/GetAttributeValuesByFqns"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse,extra_headers, timeout_seconds)

    async def get_attribute_values_by_fqns(
        self, req: policy.attributes.attributes_pb2.GetAttributeValuesByFqnsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse:
        response = await self.call_get_attribute_values_by_fqns(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_attribute(
        self, req: policy.attributes.attributes_pb2.CreateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.CreateAttributeResponse]:
        """Low-level method to call CreateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/CreateAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.CreateAttributeResponse,extra_headers, timeout_seconds)

    async def create_attribute(
        self, req: policy.attributes.attributes_pb2.CreateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.CreateAttributeResponse:
        response = await self.call_create_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_attribute(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.UpdateAttributeResponse]:
        """Low-level method to call UpdateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/UpdateAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.UpdateAttributeResponse,extra_headers, timeout_seconds)

    async def update_attribute(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.UpdateAttributeResponse:
        response = await self.call_update_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_deactivate_attribute(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.DeactivateAttributeResponse]:
        """Low-level method to call DeactivateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/DeactivateAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.DeactivateAttributeResponse,extra_headers, timeout_seconds)

    async def deactivate_attribute(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.DeactivateAttributeResponse:
        response = await self.call_deactivate_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_get_attribute_value(
        self, req: policy.attributes.attributes_pb2.GetAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.GetAttributeValueResponse]:
        """Low-level method to call GetAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/GetAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.GetAttributeValueResponse,extra_headers, timeout_seconds)

    async def get_attribute_value(
        self, req: policy.attributes.attributes_pb2.GetAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.GetAttributeValueResponse:
        response = await self.call_get_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_attribute_value(
        self, req: policy.attributes.attributes_pb2.CreateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.CreateAttributeValueResponse]:
        """Low-level method to call CreateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/CreateAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.CreateAttributeValueResponse,extra_headers, timeout_seconds)

    async def create_attribute_value(
        self, req: policy.attributes.attributes_pb2.CreateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.CreateAttributeValueResponse:
        response = await self.call_create_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_attribute_value(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.UpdateAttributeValueResponse]:
        """Low-level method to call UpdateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/UpdateAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.UpdateAttributeValueResponse,extra_headers, timeout_seconds)

    async def update_attribute_value(
        self, req: policy.attributes.attributes_pb2.UpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.UpdateAttributeValueResponse:
        response = await self.call_update_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_deactivate_attribute_value(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.DeactivateAttributeValueResponse]:
        """Low-level method to call DeactivateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/DeactivateAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.DeactivateAttributeValueResponse,extra_headers, timeout_seconds)

    async def deactivate_attribute_value(
        self, req: policy.attributes.attributes_pb2.DeactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.DeactivateAttributeValueResponse:
        response = await self.call_deactivate_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_assign_key_access_server_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse]:
        """Low-level method to call AssignKeyAccessServerToAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignKeyAccessServerToAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse,extra_headers, timeout_seconds)

    async def assign_key_access_server_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse:
        response = await self.call_assign_key_access_server_to_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_remove_key_access_server_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse]:
        """Low-level method to call RemoveKeyAccessServerFromAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemoveKeyAccessServerFromAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse,extra_headers, timeout_seconds)

    async def remove_key_access_server_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse:
        response = await self.call_remove_key_access_server_from_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_assign_key_access_server_to_value(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse]:
        """Low-level method to call AssignKeyAccessServerToValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignKeyAccessServerToValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse,extra_headers, timeout_seconds)

    async def assign_key_access_server_to_value(
        self, req: policy.attributes.attributes_pb2.AssignKeyAccessServerToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse:
        response = await self.call_assign_key_access_server_to_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_remove_key_access_server_from_value(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse]:
        """Low-level method to call RemoveKeyAccessServerFromValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemoveKeyAccessServerFromValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse,extra_headers, timeout_seconds)

    async def remove_key_access_server_from_value(
        self, req: policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse:
        response = await self.call_remove_key_access_server_from_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_assign_public_key_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse]:
        """Low-level method to call AssignPublicKeyToAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignPublicKeyToAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse,extra_headers, timeout_seconds)

    async def assign_public_key_to_attribute(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse:
        response = await self.call_assign_public_key_to_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_remove_public_key_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse]:
        """Low-level method to call RemovePublicKeyFromAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemovePublicKeyFromAttribute"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse,extra_headers, timeout_seconds)

    async def remove_public_key_from_attribute(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse:
        response = await self.call_remove_public_key_from_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_assign_public_key_to_value(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse]:
        """Low-level method to call AssignPublicKeyToValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/AssignPublicKeyToValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse,extra_headers, timeout_seconds)

    async def assign_public_key_to_value(
        self, req: policy.attributes.attributes_pb2.AssignPublicKeyToValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse:
        response = await self.call_assign_public_key_to_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_remove_public_key_from_value(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse]:
        """Low-level method to call RemovePublicKeyFromValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.attributes.AttributesService/RemovePublicKeyFromValue"
        return await self._connect_client.call_unary(url, req, policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse,extra_headers, timeout_seconds)

    async def remove_public_key_from_value(
        self, req: policy.attributes.attributes_pb2.RemovePublicKeyFromValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse:
        response = await self.call_remove_public_key_from_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class AttributesServiceProtocol(typing.Protocol):
    def list_attributes(self, req: ClientRequest[policy.attributes.attributes_pb2.ListAttributesRequest]) -> ServerResponse[policy.attributes.attributes_pb2.ListAttributesResponse]:
        ...
    def list_attribute_values(self, req: ClientRequest[policy.attributes.attributes_pb2.ListAttributeValuesRequest]) -> ServerResponse[policy.attributes.attributes_pb2.ListAttributeValuesResponse]:
        ...
    def get_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.GetAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.GetAttributeResponse]:
        ...
    def get_attribute_values_by_fqns(self, req: ClientRequest[policy.attributes.attributes_pb2.GetAttributeValuesByFqnsRequest]) -> ServerResponse[policy.attributes.attributes_pb2.GetAttributeValuesByFqnsResponse]:
        ...
    def create_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.CreateAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.CreateAttributeResponse]:
        ...
    def update_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.UpdateAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.UpdateAttributeResponse]:
        ...
    def deactivate_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.DeactivateAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.DeactivateAttributeResponse]:
        ...
    def get_attribute_value(self, req: ClientRequest[policy.attributes.attributes_pb2.GetAttributeValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.GetAttributeValueResponse]:
        ...
    def create_attribute_value(self, req: ClientRequest[policy.attributes.attributes_pb2.CreateAttributeValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.CreateAttributeValueResponse]:
        ...
    def update_attribute_value(self, req: ClientRequest[policy.attributes.attributes_pb2.UpdateAttributeValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.UpdateAttributeValueResponse]:
        ...
    def deactivate_attribute_value(self, req: ClientRequest[policy.attributes.attributes_pb2.DeactivateAttributeValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.DeactivateAttributeValueResponse]:
        ...
    def assign_key_access_server_to_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeResponse]:
        ...
    def remove_key_access_server_from_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeResponse]:
        ...
    def assign_key_access_server_to_value(self, req: ClientRequest[policy.attributes.attributes_pb2.AssignKeyAccessServerToValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.AssignKeyAccessServerToValueResponse]:
        ...
    def remove_key_access_server_from_value(self, req: ClientRequest[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueResponse]:
        ...
    def assign_public_key_to_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.AssignPublicKeyToAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.AssignPublicKeyToAttributeResponse]:
        ...
    def remove_public_key_from_attribute(self, req: ClientRequest[policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeRequest]) -> ServerResponse[policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeResponse]:
        ...
    def assign_public_key_to_value(self, req: ClientRequest[policy.attributes.attributes_pb2.AssignPublicKeyToValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.AssignPublicKeyToValueResponse]:
        ...
    def remove_public_key_from_value(self, req: ClientRequest[policy.attributes.attributes_pb2.RemovePublicKeyFromValueRequest]) -> ServerResponse[policy.attributes.attributes_pb2.RemovePublicKeyFromValueResponse]:
        ...

ATTRIBUTES_SERVICE_PATH_PREFIX = "/policy.attributes.AttributesService"

def wsgi_attributes_service(implementation: AttributesServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.attributes.AttributesService/ListAttributes", implementation.list_attributes, policy.attributes.attributes_pb2.ListAttributesRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/ListAttributeValues", implementation.list_attribute_values, policy.attributes.attributes_pb2.ListAttributeValuesRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/GetAttribute", implementation.get_attribute, policy.attributes.attributes_pb2.GetAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/GetAttributeValuesByFqns", implementation.get_attribute_values_by_fqns, policy.attributes.attributes_pb2.GetAttributeValuesByFqnsRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/CreateAttribute", implementation.create_attribute, policy.attributes.attributes_pb2.CreateAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/UpdateAttribute", implementation.update_attribute, policy.attributes.attributes_pb2.UpdateAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/DeactivateAttribute", implementation.deactivate_attribute, policy.attributes.attributes_pb2.DeactivateAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/GetAttributeValue", implementation.get_attribute_value, policy.attributes.attributes_pb2.GetAttributeValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/CreateAttributeValue", implementation.create_attribute_value, policy.attributes.attributes_pb2.CreateAttributeValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/UpdateAttributeValue", implementation.update_attribute_value, policy.attributes.attributes_pb2.UpdateAttributeValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/DeactivateAttributeValue", implementation.deactivate_attribute_value, policy.attributes.attributes_pb2.DeactivateAttributeValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/AssignKeyAccessServerToAttribute", implementation.assign_key_access_server_to_attribute, policy.attributes.attributes_pb2.AssignKeyAccessServerToAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/RemoveKeyAccessServerFromAttribute", implementation.remove_key_access_server_from_attribute, policy.attributes.attributes_pb2.RemoveKeyAccessServerFromAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/AssignKeyAccessServerToValue", implementation.assign_key_access_server_to_value, policy.attributes.attributes_pb2.AssignKeyAccessServerToValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/RemoveKeyAccessServerFromValue", implementation.remove_key_access_server_from_value, policy.attributes.attributes_pb2.RemoveKeyAccessServerFromValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/AssignPublicKeyToAttribute", implementation.assign_public_key_to_attribute, policy.attributes.attributes_pb2.AssignPublicKeyToAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/RemovePublicKeyFromAttribute", implementation.remove_public_key_from_attribute, policy.attributes.attributes_pb2.RemovePublicKeyFromAttributeRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/AssignPublicKeyToValue", implementation.assign_public_key_to_value, policy.attributes.attributes_pb2.AssignPublicKeyToValueRequest)
    app.register_unary_rpc("/policy.attributes.AttributesService/RemovePublicKeyFromValue", implementation.remove_public_key_from_value, policy.attributes.attributes_pb2.RemovePublicKeyFromValueRequest)
    return app
