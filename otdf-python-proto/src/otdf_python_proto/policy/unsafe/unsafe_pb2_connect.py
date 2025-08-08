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

import policy.unsafe.unsafe_pb2

class UnsafeServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_unsafe_update_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse]:
        """Low-level method to call UnsafeUpdateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeUpdateNamespace"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse,extra_headers, timeout_seconds)


    def unsafe_update_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse:
        response = self.call_unsafe_update_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_reactivate_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse]:
        """Low-level method to call UnsafeReactivateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeReactivateNamespace"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse,extra_headers, timeout_seconds)


    def unsafe_reactivate_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse:
        response = self.call_unsafe_reactivate_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_delete_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse]:
        """Low-level method to call UnsafeDeleteNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteNamespace"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse,extra_headers, timeout_seconds)


    def unsafe_delete_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse:
        response = self.call_unsafe_delete_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_update_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse]:
        """Low-level method to call UnsafeUpdateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeUpdateAttribute"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse,extra_headers, timeout_seconds)


    def unsafe_update_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse:
        response = self.call_unsafe_update_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_reactivate_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse]:
        """Low-level method to call UnsafeReactivateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeReactivateAttribute"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse,extra_headers, timeout_seconds)


    def unsafe_reactivate_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse:
        response = self.call_unsafe_reactivate_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_delete_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse]:
        """Low-level method to call UnsafeDeleteAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteAttribute"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse,extra_headers, timeout_seconds)


    def unsafe_delete_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse:
        response = self.call_unsafe_delete_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_update_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse]:
        """Low-level method to call UnsafeUpdateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeUpdateAttributeValue"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse,extra_headers, timeout_seconds)


    def unsafe_update_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse:
        response = self.call_unsafe_update_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_reactivate_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse]:
        """Low-level method to call UnsafeReactivateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeReactivateAttributeValue"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse,extra_headers, timeout_seconds)


    def unsafe_reactivate_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse:
        response = self.call_unsafe_reactivate_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_delete_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse]:
        """Low-level method to call UnsafeDeleteAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteAttributeValue"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse,extra_headers, timeout_seconds)


    def unsafe_delete_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse:
        response = self.call_unsafe_delete_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_unsafe_delete_kas_key(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse]:
        """Low-level method to call UnsafeDeleteKasKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteKasKey"
        return self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse,extra_headers, timeout_seconds)


    def unsafe_delete_kas_key(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse:
        response = self.call_unsafe_delete_kas_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncUnsafeServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_unsafe_update_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse]:
        """Low-level method to call UnsafeUpdateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeUpdateNamespace"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse,extra_headers, timeout_seconds)

    async def unsafe_update_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse:
        response = await self.call_unsafe_update_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_reactivate_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse]:
        """Low-level method to call UnsafeReactivateNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeReactivateNamespace"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse,extra_headers, timeout_seconds)

    async def unsafe_reactivate_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse:
        response = await self.call_unsafe_reactivate_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_delete_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse]:
        """Low-level method to call UnsafeDeleteNamespace, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteNamespace"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse,extra_headers, timeout_seconds)

    async def unsafe_delete_namespace(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse:
        response = await self.call_unsafe_delete_namespace(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_update_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse]:
        """Low-level method to call UnsafeUpdateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeUpdateAttribute"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse,extra_headers, timeout_seconds)

    async def unsafe_update_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse:
        response = await self.call_unsafe_update_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_reactivate_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse]:
        """Low-level method to call UnsafeReactivateAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeReactivateAttribute"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse,extra_headers, timeout_seconds)

    async def unsafe_reactivate_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse:
        response = await self.call_unsafe_reactivate_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_delete_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse]:
        """Low-level method to call UnsafeDeleteAttribute, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteAttribute"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse,extra_headers, timeout_seconds)

    async def unsafe_delete_attribute(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse:
        response = await self.call_unsafe_delete_attribute(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_update_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse]:
        """Low-level method to call UnsafeUpdateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeUpdateAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse,extra_headers, timeout_seconds)

    async def unsafe_update_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse:
        response = await self.call_unsafe_update_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_reactivate_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse]:
        """Low-level method to call UnsafeReactivateAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeReactivateAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse,extra_headers, timeout_seconds)

    async def unsafe_reactivate_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse:
        response = await self.call_unsafe_reactivate_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_delete_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse]:
        """Low-level method to call UnsafeDeleteAttributeValue, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteAttributeValue"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse,extra_headers, timeout_seconds)

    async def unsafe_delete_attribute_value(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse:
        response = await self.call_unsafe_delete_attribute_value(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_unsafe_delete_kas_key(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse]:
        """Low-level method to call UnsafeDeleteKasKey, granting access to errors and metadata"""
        url = self.base_url + "/policy.unsafe.UnsafeService/UnsafeDeleteKasKey"
        return await self._connect_client.call_unary(url, req, policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse,extra_headers, timeout_seconds)

    async def unsafe_delete_kas_key(
        self, req: policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse:
        response = await self.call_unsafe_delete_kas_key(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class UnsafeServiceProtocol(typing.Protocol):
    def unsafe_update_namespace(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceResponse]:
        ...
    def unsafe_reactivate_namespace(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceResponse]:
        ...
    def unsafe_delete_namespace(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceResponse]:
        ...
    def unsafe_update_attribute(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeResponse]:
        ...
    def unsafe_reactivate_attribute(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeResponse]:
        ...
    def unsafe_delete_attribute(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeResponse]:
        ...
    def unsafe_update_attribute_value(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueResponse]:
        ...
    def unsafe_reactivate_attribute_value(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueResponse]:
        ...
    def unsafe_delete_attribute_value(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueResponse]:
        ...
    def unsafe_delete_kas_key(self, req: ClientRequest[policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyRequest]) -> ServerResponse[policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyResponse]:
        ...

UNSAFE_SERVICE_PATH_PREFIX = "/policy.unsafe.UnsafeService"

def wsgi_unsafe_service(implementation: UnsafeServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeUpdateNamespace", implementation.unsafe_update_namespace, policy.unsafe.unsafe_pb2.UnsafeUpdateNamespaceRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeReactivateNamespace", implementation.unsafe_reactivate_namespace, policy.unsafe.unsafe_pb2.UnsafeReactivateNamespaceRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeDeleteNamespace", implementation.unsafe_delete_namespace, policy.unsafe.unsafe_pb2.UnsafeDeleteNamespaceRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeUpdateAttribute", implementation.unsafe_update_attribute, policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeReactivateAttribute", implementation.unsafe_reactivate_attribute, policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeDeleteAttribute", implementation.unsafe_delete_attribute, policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeUpdateAttributeValue", implementation.unsafe_update_attribute_value, policy.unsafe.unsafe_pb2.UnsafeUpdateAttributeValueRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeReactivateAttributeValue", implementation.unsafe_reactivate_attribute_value, policy.unsafe.unsafe_pb2.UnsafeReactivateAttributeValueRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeDeleteAttributeValue", implementation.unsafe_delete_attribute_value, policy.unsafe.unsafe_pb2.UnsafeDeleteAttributeValueRequest)
    app.register_unary_rpc("/policy.unsafe.UnsafeService/UnsafeDeleteKasKey", implementation.unsafe_delete_kas_key, policy.unsafe.unsafe_pb2.UnsafeDeleteKasKeyRequest)
    return app
