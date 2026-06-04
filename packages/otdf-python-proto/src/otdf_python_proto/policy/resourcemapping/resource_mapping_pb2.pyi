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

class ListResourceMappingGroupsRequest(_message.Message):
    __slots__ = ("namespace_id", "pagination")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, namespace_id: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListResourceMappingGroupsResponse(_message.Message):
    __slots__ = ("resource_mapping_groups", "pagination")
    RESOURCE_MAPPING_GROUPS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    resource_mapping_groups: _containers.RepeatedCompositeFieldContainer[_objects_pb2.ResourceMappingGroup]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, resource_mapping_groups: _Optional[_Iterable[_Union[_objects_pb2.ResourceMappingGroup, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class GetResourceMappingGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetResourceMappingGroupResponse(_message.Message):
    __slots__ = ("resource_mapping_group",)
    RESOURCE_MAPPING_GROUP_FIELD_NUMBER: _ClassVar[int]
    resource_mapping_group: _objects_pb2.ResourceMappingGroup
    def __init__(self, resource_mapping_group: _Optional[_Union[_objects_pb2.ResourceMappingGroup, _Mapping]] = ...) -> None: ...

class CreateResourceMappingGroupRequest(_message.Message):
    __slots__ = ("namespace_id", "name", "metadata")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    name: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, namespace_id: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateResourceMappingGroupResponse(_message.Message):
    __slots__ = ("resource_mapping_group",)
    RESOURCE_MAPPING_GROUP_FIELD_NUMBER: _ClassVar[int]
    resource_mapping_group: _objects_pb2.ResourceMappingGroup
    def __init__(self, resource_mapping_group: _Optional[_Union[_objects_pb2.ResourceMappingGroup, _Mapping]] = ...) -> None: ...

class UpdateResourceMappingGroupRequest(_message.Message):
    __slots__ = ("id", "namespace_id", "name", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    namespace_id: str
    name: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., namespace_id: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateResourceMappingGroupResponse(_message.Message):
    __slots__ = ("resource_mapping_group",)
    RESOURCE_MAPPING_GROUP_FIELD_NUMBER: _ClassVar[int]
    resource_mapping_group: _objects_pb2.ResourceMappingGroup
    def __init__(self, resource_mapping_group: _Optional[_Union[_objects_pb2.ResourceMappingGroup, _Mapping]] = ...) -> None: ...

class DeleteResourceMappingGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteResourceMappingGroupResponse(_message.Message):
    __slots__ = ("resource_mapping_group",)
    RESOURCE_MAPPING_GROUP_FIELD_NUMBER: _ClassVar[int]
    resource_mapping_group: _objects_pb2.ResourceMappingGroup
    def __init__(self, resource_mapping_group: _Optional[_Union[_objects_pb2.ResourceMappingGroup, _Mapping]] = ...) -> None: ...

class ListResourceMappingsRequest(_message.Message):
    __slots__ = ("group_id", "pagination")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, group_id: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListResourceMappingsResponse(_message.Message):
    __slots__ = ("resource_mappings", "pagination")
    RESOURCE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    resource_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.ResourceMapping]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, resource_mappings: _Optional[_Iterable[_Union[_objects_pb2.ResourceMapping, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class ListResourceMappingsByGroupFqnsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class ResourceMappingsByGroup(_message.Message):
    __slots__ = ("group", "mappings")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    group: _objects_pb2.ResourceMappingGroup
    mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.ResourceMapping]
    def __init__(self, group: _Optional[_Union[_objects_pb2.ResourceMappingGroup, _Mapping]] = ..., mappings: _Optional[_Iterable[_Union[_objects_pb2.ResourceMapping, _Mapping]]] = ...) -> None: ...

class ListResourceMappingsByGroupFqnsResponse(_message.Message):
    __slots__ = ("fqn_resource_mapping_groups",)
    class FqnResourceMappingGroupsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ResourceMappingsByGroup
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ResourceMappingsByGroup, _Mapping]] = ...) -> None: ...
    FQN_RESOURCE_MAPPING_GROUPS_FIELD_NUMBER: _ClassVar[int]
    fqn_resource_mapping_groups: _containers.MessageMap[str, ResourceMappingsByGroup]
    def __init__(self, fqn_resource_mapping_groups: _Optional[_Mapping[str, ResourceMappingsByGroup]] = ...) -> None: ...

class GetResourceMappingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetResourceMappingResponse(_message.Message):
    __slots__ = ("resource_mapping",)
    RESOURCE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    resource_mapping: _objects_pb2.ResourceMapping
    def __init__(self, resource_mapping: _Optional[_Union[_objects_pb2.ResourceMapping, _Mapping]] = ...) -> None: ...

class CreateResourceMappingRequest(_message.Message):
    __slots__ = ("attribute_value_id", "terms", "group_id", "metadata")
    ATTRIBUTE_VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    attribute_value_id: str
    terms: _containers.RepeatedScalarFieldContainer[str]
    group_id: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, attribute_value_id: _Optional[str] = ..., terms: _Optional[_Iterable[str]] = ..., group_id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateResourceMappingResponse(_message.Message):
    __slots__ = ("resource_mapping",)
    RESOURCE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    resource_mapping: _objects_pb2.ResourceMapping
    def __init__(self, resource_mapping: _Optional[_Union[_objects_pb2.ResourceMapping, _Mapping]] = ...) -> None: ...

class UpdateResourceMappingRequest(_message.Message):
    __slots__ = ("id", "attribute_value_id", "terms", "group_id", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    attribute_value_id: str
    terms: _containers.RepeatedScalarFieldContainer[str]
    group_id: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., attribute_value_id: _Optional[str] = ..., terms: _Optional[_Iterable[str]] = ..., group_id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateResourceMappingResponse(_message.Message):
    __slots__ = ("resource_mapping",)
    RESOURCE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    resource_mapping: _objects_pb2.ResourceMapping
    def __init__(self, resource_mapping: _Optional[_Union[_objects_pb2.ResourceMapping, _Mapping]] = ...) -> None: ...

class DeleteResourceMappingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteResourceMappingResponse(_message.Message):
    __slots__ = ("resource_mapping",)
    RESOURCE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    resource_mapping: _objects_pb2.ResourceMapping
    def __init__(self, resource_mapping: _Optional[_Union[_objects_pb2.ResourceMapping, _Mapping]] = ...) -> None: ...
