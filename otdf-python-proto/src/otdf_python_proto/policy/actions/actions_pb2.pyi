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

class GetActionRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetActionResponse(_message.Message):
    __slots__ = ("action", "subject_mappings")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    action: _objects_pb2.Action
    subject_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectMapping]
    def __init__(self, action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ..., subject_mappings: _Optional[_Iterable[_Union[_objects_pb2.SubjectMapping, _Mapping]]] = ...) -> None: ...

class ListActionsRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _selectors_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListActionsResponse(_message.Message):
    __slots__ = ("actions_standard", "actions_custom", "pagination")
    ACTIONS_STANDARD_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    actions_standard: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    actions_custom: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, actions_standard: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., actions_custom: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class CreateActionRequest(_message.Message):
    __slots__ = ("name", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateActionResponse(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: _objects_pb2.Action
    def __init__(self, action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ...) -> None: ...

class UpdateActionRequest(_message.Message):
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

class UpdateActionResponse(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: _objects_pb2.Action
    def __init__(self, action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ...) -> None: ...

class DeleteActionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteActionResponse(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: _objects_pb2.Action
    def __init__(self, action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ...) -> None: ...
