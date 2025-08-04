from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WellKnownConfig(_message.Message):
    __slots__ = ("configuration",)
    class ConfigurationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: _containers.MessageMap[str, _struct_pb2.Struct]
    def __init__(self, configuration: _Optional[_Mapping[str, _struct_pb2.Struct]] = ...) -> None: ...

class GetWellKnownConfigurationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetWellKnownConfigurationResponse(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: _struct_pb2.Struct
    def __init__(self, configuration: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
