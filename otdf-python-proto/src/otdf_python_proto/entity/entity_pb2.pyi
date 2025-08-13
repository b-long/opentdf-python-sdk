from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Token(_message.Message):
    __slots__ = ("ephemeral_id", "jwt")
    EPHEMERAL_ID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ephemeral_id: str
    jwt: str
    def __init__(self, ephemeral_id: _Optional[str] = ..., jwt: _Optional[str] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("ephemeral_id", "email_address", "user_name", "claims", "client_id", "category")
    class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CATEGORY_UNSPECIFIED: _ClassVar[Entity.Category]
        CATEGORY_SUBJECT: _ClassVar[Entity.Category]
        CATEGORY_ENVIRONMENT: _ClassVar[Entity.Category]
    CATEGORY_UNSPECIFIED: Entity.Category
    CATEGORY_SUBJECT: Entity.Category
    CATEGORY_ENVIRONMENT: Entity.Category
    EPHEMERAL_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    CLAIMS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ephemeral_id: str
    email_address: str
    user_name: str
    claims: _any_pb2.Any
    client_id: str
    category: Entity.Category
    def __init__(self, ephemeral_id: _Optional[str] = ..., email_address: _Optional[str] = ..., user_name: _Optional[str] = ..., claims: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., client_id: _Optional[str] = ..., category: _Optional[_Union[Entity.Category, str]] = ...) -> None: ...

class EntityChain(_message.Message):
    __slots__ = ("ephemeral_id", "entities")
    EPHEMERAL_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    ephemeral_id: str
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    def __init__(self, ephemeral_id: _Optional[str] = ..., entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ...) -> None: ...
