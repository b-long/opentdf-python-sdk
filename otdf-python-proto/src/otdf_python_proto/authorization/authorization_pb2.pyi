from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from policy import objects_pb2 as _objects_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Token(_message.Message):
    __slots__ = ("id", "jwt")
    ID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    id: str
    jwt: str
    def __init__(self, id: _Optional[str] = ..., jwt: _Optional[str] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("id", "email_address", "user_name", "remote_claims_url", "uuid", "claims", "custom", "client_id", "category")
    class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CATEGORY_UNSPECIFIED: _ClassVar[Entity.Category]
        CATEGORY_SUBJECT: _ClassVar[Entity.Category]
        CATEGORY_ENVIRONMENT: _ClassVar[Entity.Category]
    CATEGORY_UNSPECIFIED: Entity.Category
    CATEGORY_SUBJECT: Entity.Category
    CATEGORY_ENVIRONMENT: Entity.Category
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CLAIMS_URL_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    CLAIMS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    id: str
    email_address: str
    user_name: str
    remote_claims_url: str
    uuid: str
    claims: _any_pb2.Any
    custom: EntityCustom
    client_id: str
    category: Entity.Category
    def __init__(self, id: _Optional[str] = ..., email_address: _Optional[str] = ..., user_name: _Optional[str] = ..., remote_claims_url: _Optional[str] = ..., uuid: _Optional[str] = ..., claims: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., custom: _Optional[_Union[EntityCustom, _Mapping]] = ..., client_id: _Optional[str] = ..., category: _Optional[_Union[Entity.Category, str]] = ...) -> None: ...

class EntityCustom(_message.Message):
    __slots__ = ("extension",)
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    extension: _any_pb2.Any
    def __init__(self, extension: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class EntityChain(_message.Message):
    __slots__ = ("id", "entities")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    def __init__(self, id: _Optional[str] = ..., entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ...) -> None: ...

class DecisionRequest(_message.Message):
    __slots__ = ("actions", "entity_chains", "resource_attributes")
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    ENTITY_CHAINS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    entity_chains: _containers.RepeatedCompositeFieldContainer[EntityChain]
    resource_attributes: _containers.RepeatedCompositeFieldContainer[ResourceAttribute]
    def __init__(self, actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., entity_chains: _Optional[_Iterable[_Union[EntityChain, _Mapping]]] = ..., resource_attributes: _Optional[_Iterable[_Union[ResourceAttribute, _Mapping]]] = ...) -> None: ...

class DecisionResponse(_message.Message):
    __slots__ = ("entity_chain_id", "resource_attributes_id", "action", "decision", "obligations")
    class Decision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DECISION_UNSPECIFIED: _ClassVar[DecisionResponse.Decision]
        DECISION_DENY: _ClassVar[DecisionResponse.Decision]
        DECISION_PERMIT: _ClassVar[DecisionResponse.Decision]
    DECISION_UNSPECIFIED: DecisionResponse.Decision
    DECISION_DENY: DecisionResponse.Decision
    DECISION_PERMIT: DecisionResponse.Decision
    ENTITY_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    entity_chain_id: str
    resource_attributes_id: str
    action: _objects_pb2.Action
    decision: DecisionResponse.Decision
    obligations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entity_chain_id: _Optional[str] = ..., resource_attributes_id: _Optional[str] = ..., action: _Optional[_Union[_objects_pb2.Action, _Mapping]] = ..., decision: _Optional[_Union[DecisionResponse.Decision, str]] = ..., obligations: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDecisionsRequest(_message.Message):
    __slots__ = ("decision_requests",)
    DECISION_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    decision_requests: _containers.RepeatedCompositeFieldContainer[DecisionRequest]
    def __init__(self, decision_requests: _Optional[_Iterable[_Union[DecisionRequest, _Mapping]]] = ...) -> None: ...

class GetDecisionsResponse(_message.Message):
    __slots__ = ("decision_responses",)
    DECISION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    decision_responses: _containers.RepeatedCompositeFieldContainer[DecisionResponse]
    def __init__(self, decision_responses: _Optional[_Iterable[_Union[DecisionResponse, _Mapping]]] = ...) -> None: ...

class GetEntitlementsRequest(_message.Message):
    __slots__ = ("entities", "scope", "with_comprehensive_hierarchy")
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    WITH_COMPREHENSIVE_HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    scope: ResourceAttribute
    with_comprehensive_hierarchy: bool
    def __init__(self, entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ..., scope: _Optional[_Union[ResourceAttribute, _Mapping]] = ..., with_comprehensive_hierarchy: bool = ...) -> None: ...

class EntityEntitlements(_message.Message):
    __slots__ = ("entity_id", "attribute_value_fqns")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FQNS_FIELD_NUMBER: _ClassVar[int]
    entity_id: str
    attribute_value_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entity_id: _Optional[str] = ..., attribute_value_fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class ResourceAttribute(_message.Message):
    __slots__ = ("resource_attributes_id", "attribute_value_fqns")
    RESOURCE_ATTRIBUTES_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FQNS_FIELD_NUMBER: _ClassVar[int]
    resource_attributes_id: str
    attribute_value_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource_attributes_id: _Optional[str] = ..., attribute_value_fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetEntitlementsResponse(_message.Message):
    __slots__ = ("entitlements",)
    ENTITLEMENTS_FIELD_NUMBER: _ClassVar[int]
    entitlements: _containers.RepeatedCompositeFieldContainer[EntityEntitlements]
    def __init__(self, entitlements: _Optional[_Iterable[_Union[EntityEntitlements, _Mapping]]] = ...) -> None: ...

class TokenDecisionRequest(_message.Message):
    __slots__ = ("actions", "tokens", "resource_attributes")
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    resource_attributes: _containers.RepeatedCompositeFieldContainer[ResourceAttribute]
    def __init__(self, actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., resource_attributes: _Optional[_Iterable[_Union[ResourceAttribute, _Mapping]]] = ...) -> None: ...

class GetDecisionsByTokenRequest(_message.Message):
    __slots__ = ("decision_requests",)
    DECISION_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    decision_requests: _containers.RepeatedCompositeFieldContainer[TokenDecisionRequest]
    def __init__(self, decision_requests: _Optional[_Iterable[_Union[TokenDecisionRequest, _Mapping]]] = ...) -> None: ...

class GetDecisionsByTokenResponse(_message.Message):
    __slots__ = ("decision_responses",)
    DECISION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    decision_responses: _containers.RepeatedCompositeFieldContainer[DecisionResponse]
    def __init__(self, decision_responses: _Optional[_Iterable[_Union[DecisionResponse, _Mapping]]] = ...) -> None: ...
