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

import policy.actions.actions_pb2

class ActionServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: urllib3.PoolManager | None = None,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = ConnectClient(http_client, protocol)
    def call_get_action(
        self, req: policy.actions.actions_pb2.GetActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.GetActionResponse]:
        """Low-level method to call GetAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/GetAction"
        return self._connect_client.call_unary(url, req, policy.actions.actions_pb2.GetActionResponse,extra_headers, timeout_seconds)


    def get_action(
        self, req: policy.actions.actions_pb2.GetActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.GetActionResponse:
        response = self.call_get_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_list_actions(
        self, req: policy.actions.actions_pb2.ListActionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.ListActionsResponse]:
        """Low-level method to call ListActions, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/ListActions"
        return self._connect_client.call_unary(url, req, policy.actions.actions_pb2.ListActionsResponse,extra_headers, timeout_seconds)


    def list_actions(
        self, req: policy.actions.actions_pb2.ListActionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.ListActionsResponse:
        response = self.call_list_actions(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_create_action(
        self, req: policy.actions.actions_pb2.CreateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.CreateActionResponse]:
        """Low-level method to call CreateAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/CreateAction"
        return self._connect_client.call_unary(url, req, policy.actions.actions_pb2.CreateActionResponse,extra_headers, timeout_seconds)


    def create_action(
        self, req: policy.actions.actions_pb2.CreateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.CreateActionResponse:
        response = self.call_create_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_update_action(
        self, req: policy.actions.actions_pb2.UpdateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.UpdateActionResponse]:
        """Low-level method to call UpdateAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/UpdateAction"
        return self._connect_client.call_unary(url, req, policy.actions.actions_pb2.UpdateActionResponse,extra_headers, timeout_seconds)


    def update_action(
        self, req: policy.actions.actions_pb2.UpdateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.UpdateActionResponse:
        response = self.call_update_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    def call_delete_action(
        self, req: policy.actions.actions_pb2.DeleteActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.DeleteActionResponse]:
        """Low-level method to call DeleteAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/DeleteAction"
        return self._connect_client.call_unary(url, req, policy.actions.actions_pb2.DeleteActionResponse,extra_headers, timeout_seconds)


    def delete_action(
        self, req: policy.actions.actions_pb2.DeleteActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.DeleteActionResponse:
        response = self.call_delete_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


class AsyncActionServiceClient:
    def __init__(
        self,
        base_url: str,
        http_client: aiohttp.ClientSession,
        protocol: ConnectProtocol = ConnectProtocol.CONNECT_PROTOBUF,
    ):
        self.base_url = base_url
        self._connect_client = AsyncConnectClient(http_client, protocol)

    async def call_get_action(
        self, req: policy.actions.actions_pb2.GetActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.GetActionResponse]:
        """Low-level method to call GetAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/GetAction"
        return await self._connect_client.call_unary(url, req, policy.actions.actions_pb2.GetActionResponse,extra_headers, timeout_seconds)

    async def get_action(
        self, req: policy.actions.actions_pb2.GetActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.GetActionResponse:
        response = await self.call_get_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_list_actions(
        self, req: policy.actions.actions_pb2.ListActionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.ListActionsResponse]:
        """Low-level method to call ListActions, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/ListActions"
        return await self._connect_client.call_unary(url, req, policy.actions.actions_pb2.ListActionsResponse,extra_headers, timeout_seconds)

    async def list_actions(
        self, req: policy.actions.actions_pb2.ListActionsRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.ListActionsResponse:
        response = await self.call_list_actions(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_create_action(
        self, req: policy.actions.actions_pb2.CreateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.CreateActionResponse]:
        """Low-level method to call CreateAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/CreateAction"
        return await self._connect_client.call_unary(url, req, policy.actions.actions_pb2.CreateActionResponse,extra_headers, timeout_seconds)

    async def create_action(
        self, req: policy.actions.actions_pb2.CreateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.CreateActionResponse:
        response = await self.call_create_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_update_action(
        self, req: policy.actions.actions_pb2.UpdateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.UpdateActionResponse]:
        """Low-level method to call UpdateAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/UpdateAction"
        return await self._connect_client.call_unary(url, req, policy.actions.actions_pb2.UpdateActionResponse,extra_headers, timeout_seconds)

    async def update_action(
        self, req: policy.actions.actions_pb2.UpdateActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.UpdateActionResponse:
        response = await self.call_update_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg

    async def call_delete_action(
        self, req: policy.actions.actions_pb2.DeleteActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> UnaryOutput[policy.actions.actions_pb2.DeleteActionResponse]:
        """Low-level method to call DeleteAction, granting access to errors and metadata"""
        url = self.base_url + "/policy.actions.ActionService/DeleteAction"
        return await self._connect_client.call_unary(url, req, policy.actions.actions_pb2.DeleteActionResponse,extra_headers, timeout_seconds)

    async def delete_action(
        self, req: policy.actions.actions_pb2.DeleteActionRequest,extra_headers: HeaderInput | None=None, timeout_seconds: float | None=None
    ) -> policy.actions.actions_pb2.DeleteActionResponse:
        response = await self.call_delete_action(req, extra_headers, timeout_seconds)
        err = response.error()
        if err is not None:
            raise err
        msg = response.message()
        if msg is None:
            raise ConnectProtocolError('missing response message')
        return msg


@typing.runtime_checkable
class ActionServiceProtocol(typing.Protocol):
    def get_action(self, req: ClientRequest[policy.actions.actions_pb2.GetActionRequest]) -> ServerResponse[policy.actions.actions_pb2.GetActionResponse]:
        ...
    def list_actions(self, req: ClientRequest[policy.actions.actions_pb2.ListActionsRequest]) -> ServerResponse[policy.actions.actions_pb2.ListActionsResponse]:
        ...
    def create_action(self, req: ClientRequest[policy.actions.actions_pb2.CreateActionRequest]) -> ServerResponse[policy.actions.actions_pb2.CreateActionResponse]:
        ...
    def update_action(self, req: ClientRequest[policy.actions.actions_pb2.UpdateActionRequest]) -> ServerResponse[policy.actions.actions_pb2.UpdateActionResponse]:
        ...
    def delete_action(self, req: ClientRequest[policy.actions.actions_pb2.DeleteActionRequest]) -> ServerResponse[policy.actions.actions_pb2.DeleteActionResponse]:
        ...

ACTION_SERVICE_PATH_PREFIX = "/policy.actions.ActionService"

def wsgi_action_service(implementation: ActionServiceProtocol) -> WSGIApplication:
    app = ConnectWSGI()
    app.register_unary_rpc("/policy.actions.ActionService/GetAction", implementation.get_action, policy.actions.actions_pb2.GetActionRequest)
    app.register_unary_rpc("/policy.actions.ActionService/ListActions", implementation.list_actions, policy.actions.actions_pb2.ListActionsRequest)
    app.register_unary_rpc("/policy.actions.ActionService/CreateAction", implementation.create_action, policy.actions.actions_pb2.CreateActionRequest)
    app.register_unary_rpc("/policy.actions.ActionService/UpdateAction", implementation.update_action, policy.actions.actions_pb2.UpdateActionRequest)
    app.register_unary_rpc("/policy.actions.ActionService/DeleteAction", implementation.delete_action, policy.actions.actions_pb2.DeleteActionRequest)
    return app
