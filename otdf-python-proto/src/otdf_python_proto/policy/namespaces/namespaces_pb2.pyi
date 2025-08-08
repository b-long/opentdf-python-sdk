from buf.validate import validate_pb2 as _validate_pb2
from common import common_pb2 as _common_pb2
from policy import objects_pb2 as _objects_pb2
from policy import selectors_pb2 as _selectors_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NamespaceKeyAccessServer(_message.Message):
    __slots__ = ("namespace_id", "key_access_server_id")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ACCESS_SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    key_access_server_id: str
    def __init__(self, namespace_id: _Optional[str] = ..., key_access_server_id: _Optional[str] = ...) -> None: ...

class NamespaceKey(_message.Message):
    __slots__ = ("namespace_id", "key_id")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    key_id: str
    def __init__(self, namespace_id: _Optional[str] = ..., key_id: _Optional[str] = ...) -> None: ...

class GetNamespaceRequest(_message.Message):
    __slots__ = ("id", "namespace_id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    namespace_id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., namespace_id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class GetNamespaceResponse(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _objects_pb2.Namespace
    def __init__(self, namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ...) -> None: ...

class ListNamespacesRequest(_message.Message):
    __slots__ = ("state", "pagination")
    STATE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    state: _common_pb2.ActiveStateEnum
    pagination: _selectors_pb2.PageRequest
    def __init__(self, state: _Optional[_Union[_common_pb2.ActiveStateEnum, str]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListNamespacesResponse(_message.Message):
    __slots__ = ("namespaces", "pagination")
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Namespace]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, namespaces: _Optional[_Iterable[_Union[_objects_pb2.Namespace, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class CreateNamespaceRequest(_message.Message):
    __slots__ = ("name", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateNamespaceResponse(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _objects_pb2.Namespace
    def __init__(self, namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ...) -> None: ...

class UpdateNamespaceRequest(_message.Message):
    __slots__ = ("id", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateNamespaceResponse(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _objects_pb2.Namespace
    def __init__(self, namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ...) -> None: ...

class DeactivateNamespaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeactivateNamespaceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AssignKeyAccessServerToNamespaceRequest(_message.Message):
    __slots__ = ("namespace_key_access_server",)
    NAMESPACE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    namespace_key_access_server: NamespaceKeyAccessServer
    def __init__(self, namespace_key_access_server: _Optional[_Union[NamespaceKeyAccessServer, _Mapping]] = ...) -> None: ...

class AssignKeyAccessServerToNamespaceResponse(_message.Message):
    __slots__ = ("namespace_key_access_server",)
    NAMESPACE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    namespace_key_access_server: NamespaceKeyAccessServer
    def __init__(self, namespace_key_access_server: _Optional[_Union[NamespaceKeyAccessServer, _Mapping]] = ...) -> None: ...

class RemoveKeyAccessServerFromNamespaceRequest(_message.Message):
    __slots__ = ("namespace_key_access_server",)
    NAMESPACE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    namespace_key_access_server: NamespaceKeyAccessServer
    def __init__(self, namespace_key_access_server: _Optional[_Union[NamespaceKeyAccessServer, _Mapping]] = ...) -> None: ...

class RemoveKeyAccessServerFromNamespaceResponse(_message.Message):
    __slots__ = ("namespace_key_access_server",)
    NAMESPACE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    namespace_key_access_server: NamespaceKeyAccessServer
    def __init__(self, namespace_key_access_server: _Optional[_Union[NamespaceKeyAccessServer, _Mapping]] = ...) -> None: ...

class AssignPublicKeyToNamespaceRequest(_message.Message):
    __slots__ = ("namespace_key",)
    NAMESPACE_KEY_FIELD_NUMBER: _ClassVar[int]
    namespace_key: NamespaceKey
    def __init__(self, namespace_key: _Optional[_Union[NamespaceKey, _Mapping]] = ...) -> None: ...

class AssignPublicKeyToNamespaceResponse(_message.Message):
    __slots__ = ("namespace_key",)
    NAMESPACE_KEY_FIELD_NUMBER: _ClassVar[int]
    namespace_key: NamespaceKey
    def __init__(self, namespace_key: _Optional[_Union[NamespaceKey, _Mapping]] = ...) -> None: ...

class RemovePublicKeyFromNamespaceRequest(_message.Message):
    __slots__ = ("namespace_key",)
    NAMESPACE_KEY_FIELD_NUMBER: _ClassVar[int]
    namespace_key: NamespaceKey
    def __init__(self, namespace_key: _Optional[_Union[NamespaceKey, _Mapping]] = ...) -> None: ...

class RemovePublicKeyFromNamespaceResponse(_message.Message):
    __slots__ = ("namespace_key",)
    NAMESPACE_KEY_FIELD_NUMBER: _ClassVar[int]
    namespace_key: NamespaceKey
    def __init__(self, namespace_key: _Optional[_Union[NamespaceKey, _Mapping]] = ...) -> None: ...
