from common import common_pb2 as _common_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestPolicyObjectVersionEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEST_POLICY_OBJECT_VERSION_ENUM_UNSPECIFIED: _ClassVar[TestPolicyObjectVersionEnum]
    TEST_POLICY_OBJECT_VERSION_ENUM_OLD: _ClassVar[TestPolicyObjectVersionEnum]
    TEST_POLICY_OBJECT_VERSION_ENUM_NEW: _ClassVar[TestPolicyObjectVersionEnum]
TEST_POLICY_OBJECT_VERSION_ENUM_UNSPECIFIED: TestPolicyObjectVersionEnum
TEST_POLICY_OBJECT_VERSION_ENUM_OLD: TestPolicyObjectVersionEnum
TEST_POLICY_OBJECT_VERSION_ENUM_NEW: TestPolicyObjectVersionEnum

class TestPolicyObject(_message.Message):
    __slots__ = ("id", "active", "version", "tags", "username", "user", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    active: _wrappers_pb2.BoolValue
    version: TestPolicyObjectVersionEnum
    tags: _containers.RepeatedScalarFieldContainer[str]
    username: str
    user: User
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., version: _Optional[_Union[TestPolicyObjectVersionEnum, str]] = ..., tags: _Optional[_Iterable[str]] = ..., username: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
