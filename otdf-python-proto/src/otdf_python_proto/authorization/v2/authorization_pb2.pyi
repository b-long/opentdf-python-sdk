from buf.validate import validate_pb2 as _validate_pb2
from entity import entity_pb2 as _entity_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from policy import objects_pb2 as _objects_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Decision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DECISION_UNSPECIFIED: _ClassVar[Decision]
    DECISION_DENY: _ClassVar[Decision]
    DECISION_PERMIT: _ClassVar[Decision]
DECISION_UNSPECIFIED: Decision
DECISION_DENY: Decision
DECISION_PERMIT: Decision

class EntityIdentifier(_message.Message):
    __slots__ = ("entity_chain", "registered_resource_value_fqn", "token")
    ENTITY_CHAIN_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_RESOURCE_VALUE_FQN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    entity_chain: _entity_pb2.EntityChain
    registered_resource_value_fqn: str
    token: _entity_pb2.Token
    def __init__(self, entity_chain: _Optional[_Union[_entity_pb2.EntityChain, _Mapping]] = ..., registered_resource_value_fqn: _Optional[str] = ..., token: _Optional[_Union[_entity_pb2.Token, _Mapping]] = ...) -> None: ...

class EntityEntitlements(_message.Message):
    __slots__ = ("ephemeral_id", "actions_per_attribute_value_fqn")
    class ActionsList(_message.Message):
        __slots__ = ("actions",)
        ACTIONS_FIELD_NUMBER: _ClassVar[int]
        actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
        def __init__(self, actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ...) -> None: ...
    class ActionsPerAttributeValueFqnEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: EntityEntitlements.ActionsList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EntityEntitlements.ActionsList, _Mapping]] = ...) -> None: ...
    EPHEMERAL_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_PER_ATTRIBUTE_VALUE_FQN_FIELD_NUMBER: _ClassVar[int]
    ephemeral_id: str
    actions_per_attribute_value_fqn: _containers.MessageMap[str, EntityEntitlements.ActionsList]
    def __init__(self, ephemeral_id: _Optional[str] = ..., actions_per_attribute_value_fqn: _Optional[_Mapping[str, EntityEntitlements.ActionsList]] = ...) -> None: ...

class Resource(_message.Message):
    __slots__ = ("ephemeral_id", "attribute_values", "registered_resource_value_fqn")
    class AttributeValues(_message.Message):
        __slots__ = ("fqns",)
        FQNS_FIELD_NUMBER: _ClassVar[int]
        fqns: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...
    EPHEMERAL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_RESOURCE_VALUE_FQN_FIELD_NUMBER: _ClassVar[int]
    ephemeral_id: str
    attribute_values: Resource.AttributeValues
    registered_resource_value_fqn: str
    def __init__(self, ephemeral_id: _Optional[str] = ..., attribute_values: _Optional[_Union[Resource.AttributeValues, _Mapping]] = ..., registered_resource_value_fqn: _Optional[str] = ...) -> None: ...

class ResourceDecision(_message.Message):
    __slots__ = ("ephemeral_resource_id", "decision")
    EPHEMERAL_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    ephemeral_resource_id: str
    decision: Decision
    def __init__(self, ephemeral_resource_id: _Optional[str] = ..., decision: _Optional[_Union[Decision, str]] = ...) -> None: ...

class GetDecisionRequest(_message.Message):
    __slots__ = ("entity_identifier", "action", "resource")
    ENTITY_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    entity_identifier: EntityIdentifier
    action: _objects_pb2.Action
    resource: Resource
    def __init__(self, entity_identifier: _Optional[_Union[EntityIdentifier, _Mapping]] = ..., action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ..., resource: _Optional[_Union[Resource, _Mapping]] = ...) -> None: ...

class GetDecisionResponse(_message.Message):
    __slots__ = ("decision",)
    DECISION_FIELD_NUMBER: _ClassVar[int]
    decision: ResourceDecision
    def __init__(self, decision: _Optional[_Union[ResourceDecision, _Mapping]] = ...) -> None: ...

class GetDecisionMultiResourceRequest(_message.Message):
    __slots__ = ("entity_identifier", "action", "resources")
    ENTITY_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    entity_identifier: EntityIdentifier
    action: _objects_pb2.Action
    resources: _containers.RepeatedCompositeFieldContainer[Resource]
    def __init__(self, entity_identifier: _Optional[_Union[EntityIdentifier, _Mapping]] = ..., action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ..., resources: _Optional[_Iterable[_Union[Resource, _Mapping]]] = ...) -> None: ...

class GetDecisionMultiResourceResponse(_message.Message):
    __slots__ = ("all_permitted", "resource_decisions")
    ALL_PERMITTED_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_DECISIONS_FIELD_NUMBER: _ClassVar[int]
    all_permitted: _wrappers_pb2.BoolValue
    resource_decisions: _containers.RepeatedCompositeFieldContainer[ResourceDecision]
    def __init__(self, all_permitted: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., resource_decisions: _Optional[_Iterable[_Union[ResourceDecision, _Mapping]]] = ...) -> None: ...

class GetDecisionBulkRequest(_message.Message):
    __slots__ = ("decision_requests",)
    DECISION_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    decision_requests: _containers.RepeatedCompositeFieldContainer[GetDecisionMultiResourceRequest]
    def __init__(self, decision_requests: _Optional[_Iterable[_Union[GetDecisionMultiResourceRequest, _Mapping]]] = ...) -> None: ...

class GetDecisionBulkResponse(_message.Message):
    __slots__ = ("decision_responses",)
    DECISION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    decision_responses: _containers.RepeatedCompositeFieldContainer[GetDecisionMultiResourceResponse]
    def __init__(self, decision_responses: _Optional[_Iterable[_Union[GetDecisionMultiResourceResponse, _Mapping]]] = ...) -> None: ...

class GetEntitlementsRequest(_message.Message):
    __slots__ = ("entity_identifier", "with_comprehensive_hierarchy")
    ENTITY_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    WITH_COMPREHENSIVE_HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    entity_identifier: EntityIdentifier
    with_comprehensive_hierarchy: bool
    def __init__(self, entity_identifier: _Optional[_Union[EntityIdentifier, _Mapping]] = ..., with_comprehensive_hierarchy: bool = ...) -> None: ...

class GetEntitlementsResponse(_message.Message):
    __slots__ = ("entitlements",)
    ENTITLEMENTS_FIELD_NUMBER: _ClassVar[int]
    entitlements: _containers.RepeatedCompositeFieldContainer[EntityEntitlements]
    def __init__(self, entitlements: _Optional[_Iterable[_Union[EntityEntitlements, _Mapping]]] = ...) -> None: ...
