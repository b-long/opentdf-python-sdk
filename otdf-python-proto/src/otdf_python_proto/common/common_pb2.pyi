import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetadataUpdateEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METADATA_UPDATE_ENUM_UNSPECIFIED: _ClassVar[MetadataUpdateEnum]
    METADATA_UPDATE_ENUM_EXTEND: _ClassVar[MetadataUpdateEnum]
    METADATA_UPDATE_ENUM_REPLACE: _ClassVar[MetadataUpdateEnum]

class ActiveStateEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE_STATE_ENUM_UNSPECIFIED: _ClassVar[ActiveStateEnum]
    ACTIVE_STATE_ENUM_ACTIVE: _ClassVar[ActiveStateEnum]
    ACTIVE_STATE_ENUM_INACTIVE: _ClassVar[ActiveStateEnum]
    ACTIVE_STATE_ENUM_ANY: _ClassVar[ActiveStateEnum]
METADATA_UPDATE_ENUM_UNSPECIFIED: MetadataUpdateEnum
METADATA_UPDATE_ENUM_EXTEND: MetadataUpdateEnum
METADATA_UPDATE_ENUM_REPLACE: MetadataUpdateEnum
ACTIVE_STATE_ENUM_UNSPECIFIED: ActiveStateEnum
ACTIVE_STATE_ENUM_ACTIVE: ActiveStateEnum
ACTIVE_STATE_ENUM_INACTIVE: ActiveStateEnum
ACTIVE_STATE_ENUM_ANY: ActiveStateEnum

class Metadata(_message.Message):
    __slots__ = ("created_at", "updated_at", "labels")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    labels: _containers.ScalarMap[str, str]
    def __init__(self, created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MetadataMutable(_message.Message):
    __slots__ = ("labels",)
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    LABELS_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.ScalarMap[str, str]
    def __init__(self, labels: _Optional[_Mapping[str, str]] = ...) -> None: ...
