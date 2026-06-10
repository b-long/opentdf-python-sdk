from buf.validate import validate_pb2 as _validate_pb2
from common import common_pb2 as _common_pb2
from policy import objects_pb2 as _objects_pb2
from policy import selectors_pb2 as _selectors_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SortRegisteredResourcesType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_REGISTERED_RESOURCES_TYPE_UNSPECIFIED: _ClassVar[SortRegisteredResourcesType]
    SORT_REGISTERED_RESOURCES_TYPE_NAME: _ClassVar[SortRegisteredResourcesType]
    SORT_REGISTERED_RESOURCES_TYPE_CREATED_AT: _ClassVar[SortRegisteredResourcesType]
    SORT_REGISTERED_RESOURCES_TYPE_UPDATED_AT: _ClassVar[SortRegisteredResourcesType]
SORT_REGISTERED_RESOURCES_TYPE_UNSPECIFIED: SortRegisteredResourcesType
SORT_REGISTERED_RESOURCES_TYPE_NAME: SortRegisteredResourcesType
SORT_REGISTERED_RESOURCES_TYPE_CREATED_AT: SortRegisteredResourcesType
SORT_REGISTERED_RESOURCES_TYPE_UPDATED_AT: SortRegisteredResourcesType

class CreateRegisteredResourceRequest(_message.Message):
    __slots__ = ("name", "values", "namespace_id", "namespace_fqn", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FQN_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    values: _containers.RepeatedScalarFieldContainer[str]
    namespace_id: str
    namespace_fqn: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, name: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ..., namespace_id: _Optional[str] = ..., namespace_fqn: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateRegisteredResourceResponse(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _objects_pb2.RegisteredResource
    def __init__(self, resource: _Optional[_Union[_objects_pb2.RegisteredResource, _Mapping]] = ...) -> None: ...

class GetRegisteredResourceRequest(_message.Message):
    __slots__ = ("id", "name", "namespace_fqn", "namespace_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FQN_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    namespace_fqn: str
    namespace_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., namespace_fqn: _Optional[str] = ..., namespace_id: _Optional[str] = ...) -> None: ...

class GetRegisteredResourceResponse(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _objects_pb2.RegisteredResource
    def __init__(self, resource: _Optional[_Union[_objects_pb2.RegisteredResource, _Mapping]] = ...) -> None: ...

class RegisteredResourcesSort(_message.Message):
    __slots__ = ("field", "direction")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    field: SortRegisteredResourcesType
    direction: _selectors_pb2.SortDirection
    def __init__(self, field: _Optional[_Union[SortRegisteredResourcesType, str]] = ..., direction: _Optional[_Union[_selectors_pb2.SortDirection, str]] = ...) -> None: ...

class ListRegisteredResourcesRequest(_message.Message):
    __slots__ = ("namespace_id", "namespace_fqn", "pagination", "sort")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FQN_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    namespace_fqn: str
    pagination: _selectors_pb2.PageRequest
    sort: _containers.RepeatedCompositeFieldContainer[RegisteredResourcesSort]
    def __init__(self, namespace_id: _Optional[str] = ..., namespace_fqn: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ..., sort: _Optional[_Iterable[_Union[RegisteredResourcesSort, _Mapping]]] = ...) -> None: ...

class ListRegisteredResourcesResponse(_message.Message):
    __slots__ = ("resources", "pagination")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[_objects_pb2.RegisteredResource]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, resources: _Optional[_Iterable[_Union[_objects_pb2.RegisteredResource, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class UpdateRegisteredResourceRequest(_message.Message):
    __slots__ = ("id", "name", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateRegisteredResourceResponse(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _objects_pb2.RegisteredResource
    def __init__(self, resource: _Optional[_Union[_objects_pb2.RegisteredResource, _Mapping]] = ...) -> None: ...

class DeleteRegisteredResourceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteRegisteredResourceResponse(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _objects_pb2.RegisteredResource
    def __init__(self, resource: _Optional[_Union[_objects_pb2.RegisteredResource, _Mapping]] = ...) -> None: ...

class ActionAttributeValue(_message.Message):
    __slots__ = ("action_id", "action_name", "attribute_value_id", "attribute_value_fqn")
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FQN_FIELD_NUMBER: _ClassVar[int]
    action_id: str
    action_name: str
    attribute_value_id: str
    attribute_value_fqn: str
    def __init__(self, action_id: _Optional[str] = ..., action_name: _Optional[str] = ..., attribute_value_id: _Optional[str] = ..., attribute_value_fqn: _Optional[str] = ...) -> None: ...

class CreateRegisteredResourceValueRequest(_message.Message):
    __slots__ = ("resource_id", "value", "action_attribute_values", "metadata")
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTION_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    resource_id: str
    value: str
    action_attribute_values: _containers.RepeatedCompositeFieldContainer[ActionAttributeValue]
    metadata: _common_pb2.MetadataMutable
    def __init__(self, resource_id: _Optional[str] = ..., value: _Optional[str] = ..., action_attribute_values: _Optional[_Iterable[_Union[ActionAttributeValue, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateRegisteredResourceValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.RegisteredResourceValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.RegisteredResourceValue, _Mapping]] = ...) -> None: ...

class GetRegisteredResourceValueRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class GetRegisteredResourceValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.RegisteredResourceValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.RegisteredResourceValue, _Mapping]] = ...) -> None: ...

class GetRegisteredResourceValuesByFQNsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetRegisteredResourceValuesByFQNsResponse(_message.Message):
    __slots__ = ("fqn_value_map",)
    class FqnValueMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _objects_pb2.RegisteredResourceValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_objects_pb2.RegisteredResourceValue, _Mapping]] = ...) -> None: ...
    FQN_VALUE_MAP_FIELD_NUMBER: _ClassVar[int]
    fqn_value_map: _containers.MessageMap[str, _objects_pb2.RegisteredResourceValue]
    def __init__(self, fqn_value_map: _Optional[_Mapping[str, _objects_pb2.RegisteredResourceValue]] = ...) -> None: ...

class ListRegisteredResourceValuesRequest(_message.Message):
    __slots__ = ("resource_id", "pagination")
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    resource_id: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, resource_id: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListRegisteredResourceValuesResponse(_message.Message):
    __slots__ = ("values", "pagination")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[_objects_pb2.RegisteredResourceValue]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, values: _Optional[_Iterable[_Union[_objects_pb2.RegisteredResourceValue, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class UpdateRegisteredResourceValueRequest(_message.Message):
    __slots__ = ("id", "value", "action_attribute_values", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTION_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    value: str
    action_attribute_values: _containers.RepeatedCompositeFieldContainer[ActionAttributeValue]
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., value: _Optional[str] = ..., action_attribute_values: _Optional[_Iterable[_Union[ActionAttributeValue, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateRegisteredResourceValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.RegisteredResourceValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.RegisteredResourceValue, _Mapping]] = ...) -> None: ...

class DeleteRegisteredResourceValueRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteRegisteredResourceValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.RegisteredResourceValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.RegisteredResourceValue, _Mapping]] = ...) -> None: ...
