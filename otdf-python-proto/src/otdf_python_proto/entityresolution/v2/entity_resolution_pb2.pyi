from buf.validate import validate_pb2 as _validate_pb2
from entity import entity_pb2 as _entity_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityRepresentation(_message.Message):
    __slots__ = ("original_id", "additional_props")
    ORIGINAL_ID_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PROPS_FIELD_NUMBER: _ClassVar[int]
    original_id: str
    additional_props: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, original_id: _Optional[str] = ..., additional_props: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...

class ResolveEntitiesRequest(_message.Message):
    __slots__ = ("entities",)
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[_entity_pb2.Entity]
    def __init__(self, entities: _Optional[_Iterable[_Union[_entity_pb2.Entity, _Mapping]]] = ...) -> None: ...

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

class CreateEntityChainsFromTokensRequest(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[_entity_pb2.Token]
    def __init__(self, tokens: _Optional[_Iterable[_Union[_entity_pb2.Token, _Mapping]]] = ...) -> None: ...

class CreateEntityChainsFromTokensResponse(_message.Message):
    __slots__ = ("entity_chains",)
    ENTITY_CHAINS_FIELD_NUMBER: _ClassVar[int]
    entity_chains: _containers.RepeatedCompositeFieldContainer[_entity_pb2.EntityChain]
    def __init__(self, entity_chains: _Optional[_Iterable[_Union[_entity_pb2.EntityChain, _Mapping]]] = ...) -> None: ...
