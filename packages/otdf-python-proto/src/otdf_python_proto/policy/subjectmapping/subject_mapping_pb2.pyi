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

class MatchSubjectMappingsRequest(_message.Message):
    __slots__ = ("subject_properties",)
    SUBJECT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    subject_properties: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectProperty]
    def __init__(self, subject_properties: _Optional[_Iterable[_Union[_objects_pb2.SubjectProperty, _Mapping]]] = ...) -> None: ...

class MatchSubjectMappingsResponse(_message.Message):
    __slots__ = ("subject_mappings",)
    SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    subject_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectMapping]
    def __init__(self, subject_mappings: _Optional[_Iterable[_Union[_objects_pb2.SubjectMapping, _Mapping]]] = ...) -> None: ...

class GetSubjectMappingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSubjectMappingResponse(_message.Message):
    __slots__ = ("subject_mapping",)
    SUBJECT_MAPPING_FIELD_NUMBER: _ClassVar[int]
    subject_mapping: _objects_pb2.SubjectMapping
    def __init__(self, subject_mapping: _Optional[_Union[_objects_pb2.SubjectMapping, _Mapping]] = ...) -> None: ...

class ListSubjectMappingsRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _selectors_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListSubjectMappingsResponse(_message.Message):
    __slots__ = ("subject_mappings", "pagination")
    SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    subject_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectMapping]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, subject_mappings: _Optional[_Iterable[_Union[_objects_pb2.SubjectMapping, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class CreateSubjectMappingRequest(_message.Message):
    __slots__ = ("attribute_value_id", "actions", "existing_subject_condition_set_id", "new_subject_condition_set", "metadata")
    ATTRIBUTE_VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    EXISTING_SUBJECT_CONDITION_SET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    attribute_value_id: str
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    existing_subject_condition_set_id: str
    new_subject_condition_set: SubjectConditionSetCreate
    metadata: _common_pb2.MetadataMutable
    def __init__(self, attribute_value_id: _Optional[str] = ..., actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., existing_subject_condition_set_id: _Optional[str] = ..., new_subject_condition_set: _Optional[_Union[SubjectConditionSetCreate, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateSubjectMappingResponse(_message.Message):
    __slots__ = ("subject_mapping",)
    SUBJECT_MAPPING_FIELD_NUMBER: _ClassVar[int]
    subject_mapping: _objects_pb2.SubjectMapping
    def __init__(self, subject_mapping: _Optional[_Union[_objects_pb2.SubjectMapping, _Mapping]] = ...) -> None: ...

class UpdateSubjectMappingRequest(_message.Message):
    __slots__ = ("id", "subject_condition_set_id", "actions", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_CONDITION_SET_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    subject_condition_set_id: str
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., subject_condition_set_id: _Optional[str] = ..., actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateSubjectMappingResponse(_message.Message):
    __slots__ = ("subject_mapping",)
    SUBJECT_MAPPING_FIELD_NUMBER: _ClassVar[int]
    subject_mapping: _objects_pb2.SubjectMapping
    def __init__(self, subject_mapping: _Optional[_Union[_objects_pb2.SubjectMapping, _Mapping]] = ...) -> None: ...

class DeleteSubjectMappingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSubjectMappingResponse(_message.Message):
    __slots__ = ("subject_mapping",)
    SUBJECT_MAPPING_FIELD_NUMBER: _ClassVar[int]
    subject_mapping: _objects_pb2.SubjectMapping
    def __init__(self, subject_mapping: _Optional[_Union[_objects_pb2.SubjectMapping, _Mapping]] = ...) -> None: ...

class GetSubjectConditionSetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSubjectConditionSetResponse(_message.Message):
    __slots__ = ("subject_condition_set", "associated_subject_mappings")
    SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    ASSOCIATED_SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    subject_condition_set: _objects_pb2.SubjectConditionSet
    associated_subject_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectMapping]
    def __init__(self, subject_condition_set: _Optional[_Union[_objects_pb2.SubjectConditionSet, _Mapping]] = ..., associated_subject_mappings: _Optional[_Iterable[_Union[_objects_pb2.SubjectMapping, _Mapping]]] = ...) -> None: ...

class ListSubjectConditionSetsRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _selectors_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListSubjectConditionSetsResponse(_message.Message):
    __slots__ = ("subject_condition_sets", "pagination")
    SUBJECT_CONDITION_SETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    subject_condition_sets: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectConditionSet]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, subject_condition_sets: _Optional[_Iterable[_Union[_objects_pb2.SubjectConditionSet, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class SubjectConditionSetCreate(_message.Message):
    __slots__ = ("subject_sets", "metadata")
    SUBJECT_SETS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    subject_sets: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectSet]
    metadata: _common_pb2.MetadataMutable
    def __init__(self, subject_sets: _Optional[_Iterable[_Union[_objects_pb2.SubjectSet, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateSubjectConditionSetRequest(_message.Message):
    __slots__ = ("subject_condition_set",)
    SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    subject_condition_set: SubjectConditionSetCreate
    def __init__(self, subject_condition_set: _Optional[_Union[SubjectConditionSetCreate, _Mapping]] = ...) -> None: ...

class CreateSubjectConditionSetResponse(_message.Message):
    __slots__ = ("subject_condition_set",)
    SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    subject_condition_set: _objects_pb2.SubjectConditionSet
    def __init__(self, subject_condition_set: _Optional[_Union[_objects_pb2.SubjectConditionSet, _Mapping]] = ...) -> None: ...

class UpdateSubjectConditionSetRequest(_message.Message):
    __slots__ = ("id", "subject_sets", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_SETS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    subject_sets: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectSet]
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., subject_sets: _Optional[_Iterable[_Union[_objects_pb2.SubjectSet, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateSubjectConditionSetResponse(_message.Message):
    __slots__ = ("subject_condition_set",)
    SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    subject_condition_set: _objects_pb2.SubjectConditionSet
    def __init__(self, subject_condition_set: _Optional[_Union[_objects_pb2.SubjectConditionSet, _Mapping]] = ...) -> None: ...

class DeleteSubjectConditionSetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSubjectConditionSetResponse(_message.Message):
    __slots__ = ("subject_condition_set",)
    SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    subject_condition_set: _objects_pb2.SubjectConditionSet
    def __init__(self, subject_condition_set: _Optional[_Union[_objects_pb2.SubjectConditionSet, _Mapping]] = ...) -> None: ...

class DeleteAllUnmappedSubjectConditionSetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteAllUnmappedSubjectConditionSetsResponse(_message.Message):
    __slots__ = ("subject_condition_sets",)
    SUBJECT_CONDITION_SETS_FIELD_NUMBER: _ClassVar[int]
    subject_condition_sets: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectConditionSet]
    def __init__(self, subject_condition_sets: _Optional[_Iterable[_Union[_objects_pb2.SubjectConditionSet, _Mapping]]] = ...) -> None: ...
