from common import common_pb2 as _common_pb2
from policy import objects_pb2 as _objects_pb2
from policy import selectors_pb2 as _selectors_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetObligationRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class GetObligationResponse(_message.Message):
    __slots__ = ("obligation",)
    OBLIGATION_FIELD_NUMBER: _ClassVar[int]
    obligation: _objects_pb2.Obligation
    def __init__(self, obligation: _Optional[_Union[_objects_pb2.Obligation, _Mapping]] = ...) -> None: ...

class GetObligationsByFQNsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetObligationsByFQNsResponse(_message.Message):
    __slots__ = ("fqn_obligation_map",)
    class FqnObligationMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _objects_pb2.Obligation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_objects_pb2.Obligation, _Mapping]] = ...) -> None: ...
    FQN_OBLIGATION_MAP_FIELD_NUMBER: _ClassVar[int]
    fqn_obligation_map: _containers.MessageMap[str, _objects_pb2.Obligation]
    def __init__(self, fqn_obligation_map: _Optional[_Mapping[str, _objects_pb2.Obligation]] = ...) -> None: ...

class CreateObligationRequest(_message.Message):
    __slots__ = ("id", "fqn", "name", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    name: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateObligationResponse(_message.Message):
    __slots__ = ("obligation",)
    OBLIGATION_FIELD_NUMBER: _ClassVar[int]
    obligation: _objects_pb2.Obligation
    def __init__(self, obligation: _Optional[_Union[_objects_pb2.Obligation, _Mapping]] = ...) -> None: ...

class UpdateObligationRequest(_message.Message):
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

class UpdateObligationResponse(_message.Message):
    __slots__ = ("obligation",)
    OBLIGATION_FIELD_NUMBER: _ClassVar[int]
    obligation: _objects_pb2.Obligation
    def __init__(self, obligation: _Optional[_Union[_objects_pb2.Obligation, _Mapping]] = ...) -> None: ...

class DeleteObligationRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class DeleteObligationResponse(_message.Message):
    __slots__ = ("obligation",)
    OBLIGATION_FIELD_NUMBER: _ClassVar[int]
    obligation: _objects_pb2.Obligation
    def __init__(self, obligation: _Optional[_Union[_objects_pb2.Obligation, _Mapping]] = ...) -> None: ...

class ListObligationsRequest(_message.Message):
    __slots__ = ("id", "fqn", "pagination")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListObligationsResponse(_message.Message):
    __slots__ = ("obligations", "pagination")
    OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    obligations: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Obligation]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, obligations: _Optional[_Iterable[_Union[_objects_pb2.Obligation, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class GetObligationValueRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class GetObligationValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.ObligationValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.ObligationValue, _Mapping]] = ...) -> None: ...

class GetObligationValuesByFQNsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetObligationValuesByFQNsResponse(_message.Message):
    __slots__ = ("fqn_value_map",)
    class FqnValueMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _objects_pb2.ObligationValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_objects_pb2.ObligationValue, _Mapping]] = ...) -> None: ...
    FQN_VALUE_MAP_FIELD_NUMBER: _ClassVar[int]
    fqn_value_map: _containers.MessageMap[str, _objects_pb2.ObligationValue]
    def __init__(self, fqn_value_map: _Optional[_Mapping[str, _objects_pb2.ObligationValue]] = ...) -> None: ...

class CreateObligationValueRequest(_message.Message):
    __slots__ = ("id", "fqn", "value", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    value: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ..., value: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateObligationValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.ObligationValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.ObligationValue, _Mapping]] = ...) -> None: ...

class UpdateObligationValueRequest(_message.Message):
    __slots__ = ("id", "value", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    value: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., value: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateObligationValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.ObligationValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.ObligationValue, _Mapping]] = ...) -> None: ...

class DeleteObligationValueRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class DeleteObligationValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.ObligationValue
    def __init__(self, value: _Optional[_Union[_objects_pb2.ObligationValue, _Mapping]] = ...) -> None: ...

class AddObligationTriggerRequest(_message.Message):
    __slots__ = ("obligation_value_id", "action_id", "attribute_value_id", "metadata")
    OBLIGATION_VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    obligation_value_id: str
    action_id: str
    attribute_value_id: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, obligation_value_id: _Optional[str] = ..., action_id: _Optional[str] = ..., attribute_value_id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class AddObligationTriggerResponse(_message.Message):
    __slots__ = ("trigger",)
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    trigger: _objects_pb2.ObligationTrigger
    def __init__(self, trigger: _Optional[_Union[_objects_pb2.ObligationTrigger, _Mapping]] = ...) -> None: ...

class RemoveObligationTriggerRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RemoveObligationTriggerResponse(_message.Message):
    __slots__ = ("trigger",)
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    trigger: _objects_pb2.ObligationTrigger
    def __init__(self, trigger: _Optional[_Union[_objects_pb2.ObligationTrigger, _Mapping]] = ...) -> None: ...
