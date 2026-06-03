from authorization import authorization_pb2 as _authorization_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResolveEntitiesRequest(_message.Message):
    __slots__ = ("entities",)
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[_authorization_pb2.Entity]
    def __init__(self, entities: _Optional[_Iterable[_Union[_authorization_pb2.Entity, _Mapping]]] = ...) -> None: ...

class EntityRepresentation(_message.Message):
    __slots__ = ("additional_props", "original_id")
    ADDITIONAL_PROPS_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ID_FIELD_NUMBER: _ClassVar[int]
    additional_props: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    original_id: str
    def __init__(self, additional_props: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., original_id: _Optional[str] = ...) -> None: ...

class ResolveEntitiesResponse(_message.Message):
    __slots__ = ("entity_representations",)
    ENTITY_REPRESENTATIONS_FIELD_NUMBER: _ClassVar[int]
    entity_representations: _containers.RepeatedCompositeFieldContainer[EntityRepresentation]
    def __init__(self, entity_representations: _Optional[_Iterable[_Union[EntityRepresentation, _Mapping]]] = ...) -> None: ...

class EntityNotFoundError(_message.Message):
    __slots__ = ("code", "message", "details", "entity")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    details: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    entity: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ..., details: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., entity: _Optional[str] = ...) -> None: ...

class CreateEntityChainFromJwtRequest(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[_authorization_pb2.Token]
    def __init__(self, tokens: _Optional[_Iterable[_Union[_authorization_pb2.Token, _Mapping]]] = ...) -> None: ...

class CreateEntityChainFromJwtResponse(_message.Message):
    __slots__ = ("entity_chains",)
    ENTITY_CHAINS_FIELD_NUMBER: _ClassVar[int]
    entity_chains: _containers.RepeatedCompositeFieldContainer[_authorization_pb2.EntityChain]
    def __init__(self, entity_chains: _Optional[_Iterable[_Union[_authorization_pb2.EntityChain, _Mapping]]] = ...) -> None: ...
