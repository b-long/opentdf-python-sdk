from buf.validate import validate_pb2 as _validate_pb2
from common import common_pb2 as _common_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from policy import objects_pb2 as _objects_pb2
from policy import selectors_pb2 as _selectors_pb2
from policy.subjectmapping import subject_mapping_pb2 as _subject_mapping_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SortAttributesType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ATTRIBUTES_TYPE_UNSPECIFIED: _ClassVar[SortAttributesType]
    SORT_ATTRIBUTES_TYPE_NAME: _ClassVar[SortAttributesType]
    SORT_ATTRIBUTES_TYPE_CREATED_AT: _ClassVar[SortAttributesType]
    SORT_ATTRIBUTES_TYPE_UPDATED_AT: _ClassVar[SortAttributesType]
SORT_ATTRIBUTES_TYPE_UNSPECIFIED: SortAttributesType
SORT_ATTRIBUTES_TYPE_NAME: SortAttributesType
SORT_ATTRIBUTES_TYPE_CREATED_AT: SortAttributesType
SORT_ATTRIBUTES_TYPE_UPDATED_AT: SortAttributesType

class AttributeKeyAccessServer(_message.Message):
    __slots__ = ("attribute_id", "key_access_server_id")
    ATTRIBUTE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ACCESS_SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    attribute_id: str
    key_access_server_id: str
    def __init__(self, attribute_id: _Optional[str] = ..., key_access_server_id: _Optional[str] = ...) -> None: ...

class ValueKeyAccessServer(_message.Message):
    __slots__ = ("value_id", "key_access_server_id")
    VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ACCESS_SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    value_id: str
    key_access_server_id: str
    def __init__(self, value_id: _Optional[str] = ..., key_access_server_id: _Optional[str] = ...) -> None: ...

class AttributeKey(_message.Message):
    __slots__ = ("attribute_id", "key_id")
    ATTRIBUTE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    attribute_id: str
    key_id: str
    def __init__(self, attribute_id: _Optional[str] = ..., key_id: _Optional[str] = ...) -> None: ...

class ValueKey(_message.Message):
    __slots__ = ("value_id", "key_id")
    VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    value_id: str
    key_id: str
    def __init__(self, value_id: _Optional[str] = ..., key_id: _Optional[str] = ...) -> None: ...

class AttributesSort(_message.Message):
    __slots__ = ("field", "direction")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    field: SortAttributesType
    direction: _selectors_pb2.SortDirection
    def __init__(self, field: _Optional[_Union[SortAttributesType, str]] = ..., direction: _Optional[_Union[_selectors_pb2.SortDirection, str]] = ...) -> None: ...

class ListAttributesRequest(_message.Message):
    __slots__ = ("state", "namespace", "pagination", "sort", "search")
    STATE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    state: _common_pb2.ActiveStateEnum
    namespace: str
    pagination: _selectors_pb2.PageRequest
    sort: _containers.RepeatedCompositeFieldContainer[AttributesSort]
    search: _selectors_pb2.Search
    def __init__(self, state: _Optional[_Union[_common_pb2.ActiveStateEnum, str]] = ..., namespace: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ..., sort: _Optional[_Iterable[_Union[AttributesSort, _Mapping]]] = ..., search: _Optional[_Union[_selectors_pb2.Search, _Mapping]] = ...) -> None: ...

class ListAttributesResponse(_message.Message):
    __slots__ = ("attributes", "pagination")
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Attribute]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, attributes: _Optional[_Iterable[_Union[_objects_pb2.Attribute, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class GetAttributeRequest(_message.Message):
    __slots__ = ("id", "attribute_id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    attribute_id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., attribute_id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class GetAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class CreateAttributeRequest(_message.Message):
    __slots__ = ("namespace_id", "name", "rule", "values", "allow_traversal", "metadata")
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    ALLOW_TRAVERSAL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    name: str
    rule: _objects_pb2.AttributeRuleTypeEnum
    values: _containers.RepeatedScalarFieldContainer[str]
    allow_traversal: _wrappers_pb2.BoolValue
    metadata: _common_pb2.MetadataMutable
    def __init__(self, namespace_id: _Optional[str] = ..., name: _Optional[str] = ..., rule: _Optional[_Union[_objects_pb2.AttributeRuleTypeEnum, str]] = ..., values: _Optional[_Iterable[str]] = ..., allow_traversal: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class UpdateAttributeRequest(_message.Message):
    __slots__ = ("id", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class DeactivateAttributeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeactivateAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class GetAttributeValueRequest(_message.Message):
    __slots__ = ("id", "value_id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    value_id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., value_id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class GetAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class ListAttributeValuesRequest(_message.Message):
    __slots__ = ("attribute_id", "state", "pagination")
    ATTRIBUTE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    attribute_id: str
    state: _common_pb2.ActiveStateEnum
    pagination: _selectors_pb2.PageRequest
    def __init__(self, attribute_id: _Optional[str] = ..., state: _Optional[_Union[_common_pb2.ActiveStateEnum, str]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListAttributeValuesResponse(_message.Message):
    __slots__ = ("values", "pagination")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Value]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, values: _Optional[_Iterable[_Union[_objects_pb2.Value, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class AttributeValueObligationTriggerRequest(_message.Message):
    __slots__ = ("obligation_value", "action", "context", "metadata")
    OBLIGATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    obligation_value: _common_pb2.IdFqnIdentifier
    action: _common_pb2.IdNameIdentifier
    context: _objects_pb2.RequestContext
    metadata: _common_pb2.MetadataMutable
    def __init__(self, obligation_value: _Optional[_Union[_common_pb2.IdFqnIdentifier, _Mapping]] = ..., action: _Optional[_Union[_common_pb2.IdNameIdentifier, _Mapping]] = ..., context: _Optional[_Union[_objects_pb2.RequestContext, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class AttributeValueSubjectMappingRequest(_message.Message):
    __slots__ = ("actions", "existing_subject_condition_set_id", "new_subject_condition_set", "namespace_id", "namespace_fqn", "metadata")
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    EXISTING_SUBJECT_CONDITION_SET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FQN_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Action]
    existing_subject_condition_set_id: str
    new_subject_condition_set: _subject_mapping_pb2.SubjectConditionSetCreate
    namespace_id: str
    namespace_fqn: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, actions: _Optional[_Iterable[_Union[_objects_pb2.Action, _Mapping]]] = ..., existing_subject_condition_set_id: _Optional[str] = ..., new_subject_condition_set: _Optional[_Union[_subject_mapping_pb2.SubjectConditionSetCreate, _Mapping]] = ..., namespace_id: _Optional[str] = ..., namespace_fqn: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateAttributeValueRequest(_message.Message):
    __slots__ = ("attribute_id", "value", "obligation_triggers", "subject_mappings", "metadata")
    ATTRIBUTE_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    attribute_id: str
    value: str
    obligation_triggers: _containers.RepeatedCompositeFieldContainer[AttributeValueObligationTriggerRequest]
    subject_mappings: _containers.RepeatedCompositeFieldContainer[AttributeValueSubjectMappingRequest]
    metadata: _common_pb2.MetadataMutable
    def __init__(self, attribute_id: _Optional[str] = ..., value: _Optional[str] = ..., obligation_triggers: _Optional[_Iterable[_Union[AttributeValueObligationTriggerRequest, _Mapping]]] = ..., subject_mappings: _Optional[_Iterable[_Union[AttributeValueSubjectMappingRequest, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class UpdateAttributeValueRequest(_message.Message):
    __slots__ = ("id", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class DeactivateAttributeValueRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeactivateAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class GetAttributeValuesByFqnsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAttributeValuesByFqnsResponse(_message.Message):
    __slots__ = ("fqn_attribute_values",)
    class AttributeAndValue(_message.Message):
        __slots__ = ("attribute", "value")
        ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        attribute: _objects_pb2.Attribute
        value: _objects_pb2.Value
        def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ..., value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...
    class FqnAttributeValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GetAttributeValuesByFqnsResponse.AttributeAndValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetAttributeValuesByFqnsResponse.AttributeAndValue, _Mapping]] = ...) -> None: ...
    FQN_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    fqn_attribute_values: _containers.MessageMap[str, GetAttributeValuesByFqnsResponse.AttributeAndValue]
    def __init__(self, fqn_attribute_values: _Optional[_Mapping[str, GetAttributeValuesByFqnsResponse.AttributeAndValue]] = ...) -> None: ...

class GetKeyMappingsByFqnsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetKeyMappingsByFqnsResponse(_message.Message):
    __slots__ = ("fqn_key_mappings",)
    class AttributeKeyMapping(_message.Message):
        __slots__ = ("rule", "keys")
        RULE_FIELD_NUMBER: _ClassVar[int]
        KEYS_FIELD_NUMBER: _ClassVar[int]
        rule: _objects_pb2.AttributeRuleTypeEnum
        keys: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SimpleKasKey]
        def __init__(self, rule: _Optional[_Union[_objects_pb2.AttributeRuleTypeEnum, str]] = ..., keys: _Optional[_Iterable[_Union[_objects_pb2.SimpleKasKey, _Mapping]]] = ...) -> None: ...
    class FqnKeyMappingsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GetKeyMappingsByFqnsResponse.AttributeKeyMapping
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetKeyMappingsByFqnsResponse.AttributeKeyMapping, _Mapping]] = ...) -> None: ...
    FQN_KEY_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    fqn_key_mappings: _containers.MessageMap[str, GetKeyMappingsByFqnsResponse.AttributeKeyMapping]
    def __init__(self, fqn_key_mappings: _Optional[_Mapping[str, GetKeyMappingsByFqnsResponse.AttributeKeyMapping]] = ...) -> None: ...

class GetEntitleableAttributesByFqnsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetEntitleableAttributesByFqnsResponse(_message.Message):
    __slots__ = ("definitions", "fqn_entitleable_attributes")
    class EntitleableValue(_message.Message):
        __slots__ = ("fqn", "value_id", "subject_mappings", "active")
        FQN_FIELD_NUMBER: _ClassVar[int]
        VALUE_ID_FIELD_NUMBER: _ClassVar[int]
        SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        fqn: str
        value_id: str
        subject_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.SubjectMapping]
        active: _wrappers_pb2.BoolValue
        def __init__(self, fqn: _Optional[str] = ..., value_id: _Optional[str] = ..., subject_mappings: _Optional[_Iterable[_Union[_objects_pb2.SubjectMapping, _Mapping]]] = ..., active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...
    class EntitleableDefinition(_message.Message):
        __slots__ = ("rule", "values", "namespace", "dynamic_value_mappings")
        RULE_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        NAMESPACE_FIELD_NUMBER: _ClassVar[int]
        DYNAMIC_VALUE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
        rule: _objects_pb2.AttributeRuleTypeEnum
        values: _containers.RepeatedCompositeFieldContainer[GetEntitleableAttributesByFqnsResponse.EntitleableValue]
        namespace: _objects_pb2.Namespace
        dynamic_value_mappings: _containers.RepeatedCompositeFieldContainer[_objects_pb2.DynamicValueMapping]
        def __init__(self, rule: _Optional[_Union[_objects_pb2.AttributeRuleTypeEnum, str]] = ..., values: _Optional[_Iterable[_Union[GetEntitleableAttributesByFqnsResponse.EntitleableValue, _Mapping]]] = ..., namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ..., dynamic_value_mappings: _Optional[_Iterable[_Union[_objects_pb2.DynamicValueMapping, _Mapping]]] = ...) -> None: ...
    class EntitleableAttribute(_message.Message):
        __slots__ = ("definition_fqn", "value")
        DEFINITION_FQN_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        definition_fqn: str
        value: GetEntitleableAttributesByFqnsResponse.EntitleableValue
        def __init__(self, definition_fqn: _Optional[str] = ..., value: _Optional[_Union[GetEntitleableAttributesByFqnsResponse.EntitleableValue, _Mapping]] = ...) -> None: ...
    class DefinitionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GetEntitleableAttributesByFqnsResponse.EntitleableDefinition
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetEntitleableAttributesByFqnsResponse.EntitleableDefinition, _Mapping]] = ...) -> None: ...
    class FqnEntitleableAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GetEntitleableAttributesByFqnsResponse.EntitleableAttribute
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetEntitleableAttributesByFqnsResponse.EntitleableAttribute, _Mapping]] = ...) -> None: ...
    DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    FQN_ENTITLEABLE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    definitions: _containers.MessageMap[str, GetEntitleableAttributesByFqnsResponse.EntitleableDefinition]
    fqn_entitleable_attributes: _containers.MessageMap[str, GetEntitleableAttributesByFqnsResponse.EntitleableAttribute]
    def __init__(self, definitions: _Optional[_Mapping[str, GetEntitleableAttributesByFqnsResponse.EntitleableDefinition]] = ..., fqn_entitleable_attributes: _Optional[_Mapping[str, GetEntitleableAttributesByFqnsResponse.EntitleableAttribute]] = ...) -> None: ...

class AssignKeyAccessServerToAttributeRequest(_message.Message):
    __slots__ = ("attribute_key_access_server",)
    ATTRIBUTE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    attribute_key_access_server: AttributeKeyAccessServer
    def __init__(self, attribute_key_access_server: _Optional[_Union[AttributeKeyAccessServer, _Mapping]] = ...) -> None: ...

class AssignKeyAccessServerToAttributeResponse(_message.Message):
    __slots__ = ("attribute_key_access_server",)
    ATTRIBUTE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    attribute_key_access_server: AttributeKeyAccessServer
    def __init__(self, attribute_key_access_server: _Optional[_Union[AttributeKeyAccessServer, _Mapping]] = ...) -> None: ...

class RemoveKeyAccessServerFromAttributeRequest(_message.Message):
    __slots__ = ("attribute_key_access_server",)
    ATTRIBUTE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    attribute_key_access_server: AttributeKeyAccessServer
    def __init__(self, attribute_key_access_server: _Optional[_Union[AttributeKeyAccessServer, _Mapping]] = ...) -> None: ...

class RemoveKeyAccessServerFromAttributeResponse(_message.Message):
    __slots__ = ("attribute_key_access_server",)
    ATTRIBUTE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    attribute_key_access_server: AttributeKeyAccessServer
    def __init__(self, attribute_key_access_server: _Optional[_Union[AttributeKeyAccessServer, _Mapping]] = ...) -> None: ...

class AssignKeyAccessServerToValueRequest(_message.Message):
    __slots__ = ("value_key_access_server",)
    VALUE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    value_key_access_server: ValueKeyAccessServer
    def __init__(self, value_key_access_server: _Optional[_Union[ValueKeyAccessServer, _Mapping]] = ...) -> None: ...

class AssignKeyAccessServerToValueResponse(_message.Message):
    __slots__ = ("value_key_access_server",)
    VALUE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    value_key_access_server: ValueKeyAccessServer
    def __init__(self, value_key_access_server: _Optional[_Union[ValueKeyAccessServer, _Mapping]] = ...) -> None: ...

class RemoveKeyAccessServerFromValueRequest(_message.Message):
    __slots__ = ("value_key_access_server",)
    VALUE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    value_key_access_server: ValueKeyAccessServer
    def __init__(self, value_key_access_server: _Optional[_Union[ValueKeyAccessServer, _Mapping]] = ...) -> None: ...

class RemoveKeyAccessServerFromValueResponse(_message.Message):
    __slots__ = ("value_key_access_server",)
    VALUE_KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    value_key_access_server: ValueKeyAccessServer
    def __init__(self, value_key_access_server: _Optional[_Union[ValueKeyAccessServer, _Mapping]] = ...) -> None: ...

class AssignPublicKeyToAttributeRequest(_message.Message):
    __slots__ = ("attribute_key",)
    ATTRIBUTE_KEY_FIELD_NUMBER: _ClassVar[int]
    attribute_key: AttributeKey
    def __init__(self, attribute_key: _Optional[_Union[AttributeKey, _Mapping]] = ...) -> None: ...

class AssignPublicKeyToAttributeResponse(_message.Message):
    __slots__ = ("attribute_key",)
    ATTRIBUTE_KEY_FIELD_NUMBER: _ClassVar[int]
    attribute_key: AttributeKey
    def __init__(self, attribute_key: _Optional[_Union[AttributeKey, _Mapping]] = ...) -> None: ...

class RemovePublicKeyFromAttributeRequest(_message.Message):
    __slots__ = ("attribute_key",)
    ATTRIBUTE_KEY_FIELD_NUMBER: _ClassVar[int]
    attribute_key: AttributeKey
    def __init__(self, attribute_key: _Optional[_Union[AttributeKey, _Mapping]] = ...) -> None: ...

class RemovePublicKeyFromAttributeResponse(_message.Message):
    __slots__ = ("attribute_key",)
    ATTRIBUTE_KEY_FIELD_NUMBER: _ClassVar[int]
    attribute_key: AttributeKey
    def __init__(self, attribute_key: _Optional[_Union[AttributeKey, _Mapping]] = ...) -> None: ...

class AssignPublicKeyToValueRequest(_message.Message):
    __slots__ = ("value_key",)
    VALUE_KEY_FIELD_NUMBER: _ClassVar[int]
    value_key: ValueKey
    def __init__(self, value_key: _Optional[_Union[ValueKey, _Mapping]] = ...) -> None: ...

class AssignPublicKeyToValueResponse(_message.Message):
    __slots__ = ("value_key",)
    VALUE_KEY_FIELD_NUMBER: _ClassVar[int]
    value_key: ValueKey
    def __init__(self, value_key: _Optional[_Union[ValueKey, _Mapping]] = ...) -> None: ...

class RemovePublicKeyFromValueRequest(_message.Message):
    __slots__ = ("value_key",)
    VALUE_KEY_FIELD_NUMBER: _ClassVar[int]
    value_key: ValueKey
    def __init__(self, value_key: _Optional[_Union[ValueKey, _Mapping]] = ...) -> None: ...

class RemovePublicKeyFromValueResponse(_message.Message):
    __slots__ = ("value_key",)
    VALUE_KEY_FIELD_NUMBER: _ClassVar[int]
    value_key: ValueKey
    def __init__(self, value_key: _Optional[_Union[ValueKey, _Mapping]] = ...) -> None: ...
