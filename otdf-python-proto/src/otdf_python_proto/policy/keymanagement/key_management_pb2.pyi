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

class CreateProviderConfigRequest(_message.Message):
    __slots__ = ("name", "config_json", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    config_json: bytes
    metadata: _common_pb2.MetadataMutable
    def __init__(self, name: _Optional[str] = ..., config_json: _Optional[bytes] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateProviderConfigResponse(_message.Message):
    __slots__ = ("provider_config",)
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    provider_config: _objects_pb2.KeyProviderConfig
    def __init__(self, provider_config: _Optional[_Union[_objects_pb2.KeyProviderConfig, _Mapping]] = ...) -> None: ...

class GetProviderConfigRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetProviderConfigResponse(_message.Message):
    __slots__ = ("provider_config",)
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    provider_config: _objects_pb2.KeyProviderConfig
    def __init__(self, provider_config: _Optional[_Union[_objects_pb2.KeyProviderConfig, _Mapping]] = ...) -> None: ...

class ListProviderConfigsRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _selectors_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListProviderConfigsResponse(_message.Message):
    __slots__ = ("provider_configs", "pagination")
    PROVIDER_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    provider_configs: _containers.RepeatedCompositeFieldContainer[_objects_pb2.KeyProviderConfig]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, provider_configs: _Optional[_Iterable[_Union[_objects_pb2.KeyProviderConfig, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class UpdateProviderConfigRequest(_message.Message):
    __slots__ = ("id", "name", "config_json", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    config_json: bytes
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., config_json: _Optional[bytes] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateProviderConfigResponse(_message.Message):
    __slots__ = ("provider_config",)
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    provider_config: _objects_pb2.KeyProviderConfig
    def __init__(self, provider_config: _Optional[_Union[_objects_pb2.KeyProviderConfig, _Mapping]] = ...) -> None: ...

class DeleteProviderConfigRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteProviderConfigResponse(_message.Message):
    __slots__ = ("provider_config",)
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    provider_config: _objects_pb2.KeyProviderConfig
    def __init__(self, provider_config: _Optional[_Union[_objects_pb2.KeyProviderConfig, _Mapping]] = ...) -> None: ...
