from buf.validate import validate_pb2 as _validate_pb2
from common import common_pb2 as _common_pb2
from policy import objects_pb2 as _objects_pb2
from policy import selectors_pb2 as _selectors_pb2
from policy.subjectmapping import subject_mapping_pb2 as _subject_mapping_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SortDynamicValueMappingsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_DYNAMIC_VALUE_MAPPINGS_TYPE_UNSPECIFIED: _ClassVar[SortDynamicValueMappingsType]
    SORT_DYNAMIC_VALUE_MAPPINGS_TYPE_CREATED_AT: _ClassVar[SortDynamicValueMappingsType]
    SORT_DYNAMIC_VALUE_MAPPINGS_TYPE_UPDATED_AT: _ClassVar[SortDynamicValueMappingsType]
SORT_DYNAMIC_VALUE_MAPPINGS_TYPE_UNSPECIFIED: SortDynamicValueMappingsType
SORT_DYNAMIC_VALUE_MAPPINGS_TYPE_CREATED_AT: SortDynamicValueMappingsType
SORT_DYNAMIC_VALUE_MAPPINGS_TYPE_UPDATED_AT: SortDynamicValueMappingsType

class GetDynamicValueMappingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDynamicValueMappingResponse(_message.Message):
    __slots__ = ("dynamic_value_mapping",)
    DYNAMIC_VALUE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    dynamic_value_mapping: _objects_pb2.DynamicValueMapping
    def __init__(self, dynamic_value_mapping: _Optional[_Union[_objects_pb2.DynamicValueMapping, _Mapping]] = ...) -> None: ...

class DynamicValueMappingsSort(_message.Message):
    __slots__ = ("field", "direction")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    field: SortDynamicValueMappingsType
    direction: _selectors_pb2.SortDirection
    def __init__(self, field: _Optional[_Union[SortDynamicValueMappingsType, str]] = ..., direction: _Optional[_Union[_selectors_pb2.SortDirection, str]] = ...) -> None: ...

class ListDynamicValueMappingsRequest(_message.Message):
    __slots__ = ("namespace_id", "namespace_fqn", "attribute_definition_id", "pagination", "sort")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FQN_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    namespace_fqn: str
    attribute_definition_id: str
    pagination: _selectors_pb2.PageRequest
    sort: _containers.RepeatedCompositeFieldContainer[DynamicValueMappingsSort]
    def __init__(self, namespace_id: _Optional[str] = ..., namespace_fqn: _Optional[str] = ..., attribute_definition_id: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ..., sort: _Optional[_Iterable[_Union[DynamicValueMappingsSort, _Mapping]]] = ...) -> None: ...

class ListDynamicValueMappingsResponse(_message.Message):
    __slots__ = ("dynamic_value_mappings", "pagination")
    DYNAMIC_VALUE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    dynamic_value_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.DynamicValueMapping]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, dynamic_value_mappings: _Optional[_Iterable[_Union[_objects_pb2.DynamicValueMapping, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class CreateDynamicValueMappingRequest(_message.Message):
    __slots__ = ("attribute_definition_id", "attribute_definition_fqn", "value_resolver", "actions", "existing_subject_condition_set_id", "new_subject_condition_set", "namespace_id", "namespace_fqn", "metadata")
    ATTRIBUTE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_DEFINITION_FQN_FIELD_NUMBER: _ClassVar[int]
    VALUE_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    EXISTING_SUBJECT_CONDITION_SET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FQN_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    attribute_definition_id: str
    attribute_definition_fqn: str
    value_resolver: _objects_pb2.DynamicValueResolver
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    existing_subject_condition_set_id: str
    new_subject_condition_set: _subject_mapping_pb2.SubjectConditionSetCreate
    namespace_id: str
    namespace_fqn: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, attribute_definition_id: _Optional[str] = ..., attribute_definition_fqn: _Optional[str] = ..., value_resolver: _Optional[_Union[_objects_pb2.DynamicValueResolver, _Mapping]] = ..., actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., existing_subject_condition_set_id: _Optional[str] = ..., new_subject_condition_set: _Optional[_Union[_subject_mapping_pb2.SubjectConditionSetCreate, _Mapping]] = ..., namespace_id: _Optional[str] = ..., namespace_fqn: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateDynamicValueMappingResponse(_message.Message):
    __slots__ = ("dynamic_value_mapping",)
    DYNAMIC_VALUE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    dynamic_value_mapping: _objects_pb2.DynamicValueMapping
    def __init__(self, dynamic_value_mapping: _Optional[_Union[_objects_pb2.DynamicValueMapping, _Mapping]] = ...) -> None: ...

class UpdateDynamicValueMappingRequest(_message.Message):
    __slots__ = ("id", "value_resolver", "subject_condition_set_id", "actions", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_CONDITION_SET_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    value_resolver: _objects_pb2.DynamicValueResolver
    subject_condition_set_id: str
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., value_resolver: _Optional[_Union[_objects_pb2.DynamicValueResolver, _Mapping]] = ..., subject_condition_set_id: _Optional[str] = ..., actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateDynamicValueMappingResponse(_message.Message):
    __slots__ = ("dynamic_value_mapping",)
    DYNAMIC_VALUE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    dynamic_value_mapping: _objects_pb2.DynamicValueMapping
    def __init__(self, dynamic_value_mapping: _Optional[_Union[_objects_pb2.DynamicValueMapping, _Mapping]] = ...) -> None: ...

class DeleteDynamicValueMappingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDynamicValueMappingResponse(_message.Message):
    __slots__ = ("dynamic_value_mapping",)
    DYNAMIC_VALUE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    dynamic_value_mapping: _objects_pb2.DynamicValueMapping
    def __init__(self, dynamic_value_mapping: _Optional[_Union[_objects_pb2.DynamicValueMapping, _Mapping]] = ...) -> None: ...
