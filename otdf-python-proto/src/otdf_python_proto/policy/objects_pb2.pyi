from buf.validate import validate_pb2 as _validate_pb2
from common import common_pb2 as _common_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttributeRuleTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ATTRIBUTE_RULE_TYPE_ENUM_UNSPECIFIED: _ClassVar[AttributeRuleTypeEnum]
    ATTRIBUTE_RULE_TYPE_ENUM_ALL_OF: _ClassVar[AttributeRuleTypeEnum]
    ATTRIBUTE_RULE_TYPE_ENUM_ANY_OF: _ClassVar[AttributeRuleTypeEnum]
    ATTRIBUTE_RULE_TYPE_ENUM_HIERARCHY: _ClassVar[AttributeRuleTypeEnum]

class SubjectMappingOperatorEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBJECT_MAPPING_OPERATOR_ENUM_UNSPECIFIED: _ClassVar[SubjectMappingOperatorEnum]
    SUBJECT_MAPPING_OPERATOR_ENUM_IN: _ClassVar[SubjectMappingOperatorEnum]
    SUBJECT_MAPPING_OPERATOR_ENUM_NOT_IN: _ClassVar[SubjectMappingOperatorEnum]
    SUBJECT_MAPPING_OPERATOR_ENUM_IN_CONTAINS: _ClassVar[SubjectMappingOperatorEnum]

class ConditionBooleanTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONDITION_BOOLEAN_TYPE_ENUM_UNSPECIFIED: _ClassVar[ConditionBooleanTypeEnum]
    CONDITION_BOOLEAN_TYPE_ENUM_AND: _ClassVar[ConditionBooleanTypeEnum]
    CONDITION_BOOLEAN_TYPE_ENUM_OR: _ClassVar[ConditionBooleanTypeEnum]

class SourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOURCE_TYPE_UNSPECIFIED: _ClassVar[SourceType]
    SOURCE_TYPE_INTERNAL: _ClassVar[SourceType]
    SOURCE_TYPE_EXTERNAL: _ClassVar[SourceType]

class KasPublicKeyAlgEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KAS_PUBLIC_KEY_ALG_ENUM_UNSPECIFIED: _ClassVar[KasPublicKeyAlgEnum]
    KAS_PUBLIC_KEY_ALG_ENUM_RSA_2048: _ClassVar[KasPublicKeyAlgEnum]
    KAS_PUBLIC_KEY_ALG_ENUM_RSA_4096: _ClassVar[KasPublicKeyAlgEnum]
    KAS_PUBLIC_KEY_ALG_ENUM_EC_SECP256R1: _ClassVar[KasPublicKeyAlgEnum]
    KAS_PUBLIC_KEY_ALG_ENUM_EC_SECP384R1: _ClassVar[KasPublicKeyAlgEnum]
    KAS_PUBLIC_KEY_ALG_ENUM_EC_SECP521R1: _ClassVar[KasPublicKeyAlgEnum]

class Algorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALGORITHM_UNSPECIFIED: _ClassVar[Algorithm]
    ALGORITHM_RSA_2048: _ClassVar[Algorithm]
    ALGORITHM_RSA_4096: _ClassVar[Algorithm]
    ALGORITHM_EC_P256: _ClassVar[Algorithm]
    ALGORITHM_EC_P384: _ClassVar[Algorithm]
    ALGORITHM_EC_P521: _ClassVar[Algorithm]

class KeyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KEY_STATUS_UNSPECIFIED: _ClassVar[KeyStatus]
    KEY_STATUS_ACTIVE: _ClassVar[KeyStatus]
    KEY_STATUS_ROTATED: _ClassVar[KeyStatus]

class KeyMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KEY_MODE_UNSPECIFIED: _ClassVar[KeyMode]
    KEY_MODE_CONFIG_ROOT_KEY: _ClassVar[KeyMode]
    KEY_MODE_PROVIDER_ROOT_KEY: _ClassVar[KeyMode]
    KEY_MODE_REMOTE: _ClassVar[KeyMode]
    KEY_MODE_PUBLIC_KEY_ONLY: _ClassVar[KeyMode]
ATTRIBUTE_RULE_TYPE_ENUM_UNSPECIFIED: AttributeRuleTypeEnum
ATTRIBUTE_RULE_TYPE_ENUM_ALL_OF: AttributeRuleTypeEnum
ATTRIBUTE_RULE_TYPE_ENUM_ANY_OF: AttributeRuleTypeEnum
ATTRIBUTE_RULE_TYPE_ENUM_HIERARCHY: AttributeRuleTypeEnum
SUBJECT_MAPPING_OPERATOR_ENUM_UNSPECIFIED: SubjectMappingOperatorEnum
SUBJECT_MAPPING_OPERATOR_ENUM_IN: SubjectMappingOperatorEnum
SUBJECT_MAPPING_OPERATOR_ENUM_NOT_IN: SubjectMappingOperatorEnum
SUBJECT_MAPPING_OPERATOR_ENUM_IN_CONTAINS: SubjectMappingOperatorEnum
CONDITION_BOOLEAN_TYPE_ENUM_UNSPECIFIED: ConditionBooleanTypeEnum
CONDITION_BOOLEAN_TYPE_ENUM_AND: ConditionBooleanTypeEnum
CONDITION_BOOLEAN_TYPE_ENUM_OR: ConditionBooleanTypeEnum
SOURCE_TYPE_UNSPECIFIED: SourceType
SOURCE_TYPE_INTERNAL: SourceType
SOURCE_TYPE_EXTERNAL: SourceType
KAS_PUBLIC_KEY_ALG_ENUM_UNSPECIFIED: KasPublicKeyAlgEnum
KAS_PUBLIC_KEY_ALG_ENUM_RSA_2048: KasPublicKeyAlgEnum
KAS_PUBLIC_KEY_ALG_ENUM_RSA_4096: KasPublicKeyAlgEnum
KAS_PUBLIC_KEY_ALG_ENUM_EC_SECP256R1: KasPublicKeyAlgEnum
KAS_PUBLIC_KEY_ALG_ENUM_EC_SECP384R1: KasPublicKeyAlgEnum
KAS_PUBLIC_KEY_ALG_ENUM_EC_SECP521R1: KasPublicKeyAlgEnum
ALGORITHM_UNSPECIFIED: Algorithm
ALGORITHM_RSA_2048: Algorithm
ALGORITHM_RSA_4096: Algorithm
ALGORITHM_EC_P256: Algorithm
ALGORITHM_EC_P384: Algorithm
ALGORITHM_EC_P521: Algorithm
KEY_STATUS_UNSPECIFIED: KeyStatus
KEY_STATUS_ACTIVE: KeyStatus
KEY_STATUS_ROTATED: KeyStatus
KEY_MODE_UNSPECIFIED: KeyMode
KEY_MODE_CONFIG_ROOT_KEY: KeyMode
KEY_MODE_PROVIDER_ROOT_KEY: KeyMode
KEY_MODE_REMOTE: KeyMode
KEY_MODE_PUBLIC_KEY_ONLY: KeyMode

class SimpleKasPublicKey(_message.Message):
    __slots__ = ("algorithm", "kid", "pem")
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    KID_FIELD_NUMBER: _ClassVar[int]
    PEM_FIELD_NUMBER: _ClassVar[int]
    algorithm: Algorithm
    kid: str
    pem: str
    def __init__(self, algorithm: _Optional[_Union[Algorithm, str]] = ..., kid: _Optional[str] = ..., pem: _Optional[str] = ...) -> None: ...

class SimpleKasKey(_message.Message):
    __slots__ = ("kas_uri", "public_key", "kas_id")
    KAS_URI_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    kas_uri: str
    public_key: SimpleKasPublicKey
    kas_id: str
    def __init__(self, kas_uri: _Optional[str] = ..., public_key: _Optional[_Union[SimpleKasPublicKey, _Mapping]] = ..., kas_id: _Optional[str] = ...) -> None: ...

class KeyProviderConfig(_message.Message):
    __slots__ = ("id", "name", "config_json", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    config_json: bytes
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., config_json: _Optional[bytes] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class Namespace(_message.Message):
    __slots__ = ("id", "name", "fqn", "active", "metadata", "grants", "kas_keys")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    KAS_KEYS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    fqn: str
    active: _wrappers_pb2.BoolValue
    metadata: _common_pb2.Metadata
    grants: _containers.RepeatedCompositeFieldContainer[KeyAccessServer]
    kas_keys: _containers.RepeatedCompositeFieldContainer[SimpleKasKey]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., fqn: _Optional[str] = ..., active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ..., grants: _Optional[_Iterable[_Union[KeyAccessServer, _Mapping]]] = ..., kas_keys: _Optional[_Iterable[_Union[SimpleKasKey, _Mapping]]] = ...) -> None: ...

class Attribute(_message.Message):
    __slots__ = ("id", "namespace", "name", "rule", "values", "grants", "fqn", "active", "kas_keys", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    KAS_KEYS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    namespace: Namespace
    name: str
    rule: AttributeRuleTypeEnum
    values: _containers.RepeatedCompositeFieldContainer[Value]
    grants: _containers.RepeatedCompositeFieldContainer[KeyAccessServer]
    fqn: str
    active: _wrappers_pb2.BoolValue
    kas_keys: _containers.RepeatedCompositeFieldContainer[SimpleKasKey]
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., namespace: _Optional[_Union[Namespace, _Mapping]] = ..., name: _Optional[str] = ..., rule: _Optional[_Union[AttributeRuleTypeEnum, str]] = ..., values: _Optional[_Iterable[_Union[Value, _Mapping]]] = ..., grants: _Optional[_Iterable[_Union[KeyAccessServer, _Mapping]]] = ..., fqn: _Optional[str] = ..., active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., kas_keys: _Optional[_Iterable[_Union[SimpleKasKey, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ("id", "attribute", "value", "grants", "fqn", "active", "subject_mappings", "kas_keys", "resource_mappings", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    KAS_KEYS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    attribute: Attribute
    value: str
    grants: _containers.RepeatedCompositeFieldContainer[KeyAccessServer]
    fqn: str
    active: _wrappers_pb2.BoolValue
    subject_mappings: _containers.RepeatedCompositeFieldContainer[SubjectMapping]
    kas_keys: _containers.RepeatedCompositeFieldContainer[SimpleKasKey]
    resource_mappings: _containers.RepeatedCompositeFieldContainer[ResourceMapping]
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., attribute: _Optional[_Union[Attribute, _Mapping]] = ..., value: _Optional[str] = ..., grants: _Optional[_Iterable[_Union[KeyAccessServer, _Mapping]]] = ..., fqn: _Optional[str] = ..., active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., subject_mappings: _Optional[_Iterable[_Union[SubjectMapping, _Mapping]]] = ..., kas_keys: _Optional[_Iterable[_Union[SimpleKasKey, _Mapping]]] = ..., resource_mappings: _Optional[_Iterable[_Union[ResourceMapping, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class Action(_message.Message):
    __slots__ = ("id", "standard", "custom", "name", "metadata")
    class StandardAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STANDARD_ACTION_UNSPECIFIED: _ClassVar[Action.StandardAction]
        STANDARD_ACTION_DECRYPT: _ClassVar[Action.StandardAction]
        STANDARD_ACTION_TRANSMIT: _ClassVar[Action.StandardAction]
    STANDARD_ACTION_UNSPECIFIED: Action.StandardAction
    STANDARD_ACTION_DECRYPT: Action.StandardAction
    STANDARD_ACTION_TRANSMIT: Action.StandardAction
    ID_FIELD_NUMBER: _ClassVar[int]
    STANDARD_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    standard: Action.StandardAction
    custom: str
    name: str
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., standard: _Optional[_Union[Action.StandardAction, str]] = ..., custom: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class SubjectMapping(_message.Message):
    __slots__ = ("id", "attribute_value", "subject_condition_set", "actions", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_CONDITION_SET_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    attribute_value: Value
    subject_condition_set: SubjectConditionSet
    actions: _containers.RepeatedCompositeFieldContainer[Action]
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., attribute_value: _Optional[_Union[Value, _Mapping]] = ..., subject_condition_set: _Optional[_Union[SubjectConditionSet, _Mapping]] = ..., actions: _Optional[_Iterable[_Union[Action, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class Condition(_message.Message):
    __slots__ = ("subject_external_selector_value", "operator", "subject_external_values")
    SUBJECT_EXTERNAL_SELECTOR_VALUE_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_EXTERNAL_VALUES_FIELD_NUMBER: _ClassVar[int]
    subject_external_selector_value: str
    operator: SubjectMappingOperatorEnum
    subject_external_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, subject_external_selector_value: _Optional[str] = ..., operator: _Optional[_Union[SubjectMappingOperatorEnum, str]] = ..., subject_external_values: _Optional[_Iterable[str]] = ...) -> None: ...

class ConditionGroup(_message.Message):
    __slots__ = ("conditions", "boolean_operator")
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[Condition]
    boolean_operator: ConditionBooleanTypeEnum
    def __init__(self, conditions: _Optional[_Iterable[_Union[Condition, _Mapping]]] = ..., boolean_operator: _Optional[_Union[ConditionBooleanTypeEnum, str]] = ...) -> None: ...

class SubjectSet(_message.Message):
    __slots__ = ("condition_groups",)
    CONDITION_GROUPS_FIELD_NUMBER: _ClassVar[int]
    condition_groups: _containers.RepeatedCompositeFieldContainer[ConditionGroup]
    def __init__(self, condition_groups: _Optional[_Iterable[_Union[ConditionGroup, _Mapping]]] = ...) -> None: ...

class SubjectConditionSet(_message.Message):
    __slots__ = ("id", "subject_sets", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_SETS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    subject_sets: _containers.RepeatedCompositeFieldContainer[SubjectSet]
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., subject_sets: _Optional[_Iterable[_Union[SubjectSet, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class SubjectProperty(_message.Message):
    __slots__ = ("external_selector_value", "external_value")
    EXTERNAL_SELECTOR_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    external_selector_value: str
    external_value: str
    def __init__(self, external_selector_value: _Optional[str] = ..., external_value: _Optional[str] = ...) -> None: ...

class ResourceMappingGroup(_message.Message):
    __slots__ = ("id", "namespace_id", "name", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    namespace_id: str
    name: str
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., namespace_id: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class ResourceMapping(_message.Message):
    __slots__ = ("id", "metadata", "attribute_value", "terms", "group")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _common_pb2.Metadata
    attribute_value: Value
    terms: _containers.RepeatedScalarFieldContainer[str]
    group: ResourceMappingGroup
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ..., attribute_value: _Optional[_Union[Value, _Mapping]] = ..., terms: _Optional[_Iterable[str]] = ..., group: _Optional[_Union[ResourceMappingGroup, _Mapping]] = ...) -> None: ...

class KeyAccessServer(_message.Message):
    __slots__ = ("id", "uri", "public_key", "source_type", "kas_keys", "name", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    KAS_KEYS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    uri: str
    public_key: PublicKey
    source_type: SourceType
    kas_keys: _containers.RepeatedCompositeFieldContainer[SimpleKasKey]
    name: str
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., uri: _Optional[str] = ..., public_key: _Optional[_Union[PublicKey, _Mapping]] = ..., source_type: _Optional[_Union[SourceType, str]] = ..., kas_keys: _Optional[_Iterable[_Union[SimpleKasKey, _Mapping]]] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class Key(_message.Message):
    __slots__ = ("id", "is_active", "was_mapped", "public_key", "kas", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    WAS_MAPPED_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    KAS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    is_active: _wrappers_pb2.BoolValue
    was_mapped: _wrappers_pb2.BoolValue
    public_key: KasPublicKey
    kas: KeyAccessServer
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., is_active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., was_mapped: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., public_key: _Optional[_Union[KasPublicKey, _Mapping]] = ..., kas: _Optional[_Union[KeyAccessServer, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class KasPublicKey(_message.Message):
    __slots__ = ("pem", "kid", "alg")
    PEM_FIELD_NUMBER: _ClassVar[int]
    KID_FIELD_NUMBER: _ClassVar[int]
    ALG_FIELD_NUMBER: _ClassVar[int]
    pem: str
    kid: str
    alg: KasPublicKeyAlgEnum
    def __init__(self, pem: _Optional[str] = ..., kid: _Optional[str] = ..., alg: _Optional[_Union[KasPublicKeyAlgEnum, str]] = ...) -> None: ...

class KasPublicKeySet(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[KasPublicKey]
    def __init__(self, keys: _Optional[_Iterable[_Union[KasPublicKey, _Mapping]]] = ...) -> None: ...

class PublicKey(_message.Message):
    __slots__ = ("remote", "cached")
    REMOTE_FIELD_NUMBER: _ClassVar[int]
    CACHED_FIELD_NUMBER: _ClassVar[int]
    remote: str
    cached: KasPublicKeySet
    def __init__(self, remote: _Optional[str] = ..., cached: _Optional[_Union[KasPublicKeySet, _Mapping]] = ...) -> None: ...

class RegisteredResource(_message.Message):
    __slots__ = ("id", "name", "values", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    values: _containers.RepeatedCompositeFieldContainer[RegisteredResourceValue]
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., values: _Optional[_Iterable[_Union[RegisteredResourceValue, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class RegisteredResourceValue(_message.Message):
    __slots__ = ("id", "value", "resource", "action_attribute_values", "metadata")
    class ActionAttributeValue(_message.Message):
        __slots__ = ("id", "action", "attribute_value", "metadata")
        ID_FIELD_NUMBER: _ClassVar[int]
        ACTION_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        id: str
        action: Action
        attribute_value: Value
        metadata: _common_pb2.Metadata
        def __init__(self, id: _Optional[str] = ..., action: _Optional[_Union[Action, _Mapping]] = ..., attribute_value: _Optional[_Union[Value, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    value: str
    resource: RegisteredResource
    action_attribute_values: _containers.RepeatedCompositeFieldContainer[RegisteredResourceValue.ActionAttributeValue]
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., value: _Optional[str] = ..., resource: _Optional[_Union[RegisteredResource, _Mapping]] = ..., action_attribute_values: _Optional[_Iterable[_Union[RegisteredResourceValue.ActionAttributeValue, _Mapping]]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class KasKey(_message.Message):
    __slots__ = ("kas_id", "key", "kas_uri")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    KAS_URI_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    key: AsymmetricKey
    kas_uri: str
    def __init__(self, kas_id: _Optional[str] = ..., key: _Optional[_Union[AsymmetricKey, _Mapping]] = ..., kas_uri: _Optional[str] = ...) -> None: ...

class PublicKeyCtx(_message.Message):
    __slots__ = ("pem",)
    PEM_FIELD_NUMBER: _ClassVar[int]
    pem: str
    def __init__(self, pem: _Optional[str] = ...) -> None: ...

class PrivateKeyCtx(_message.Message):
    __slots__ = ("key_id", "wrapped_key")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    WRAPPED_KEY_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    wrapped_key: str
    def __init__(self, key_id: _Optional[str] = ..., wrapped_key: _Optional[str] = ...) -> None: ...

class AsymmetricKey(_message.Message):
    __slots__ = ("id", "key_id", "key_algorithm", "key_status", "key_mode", "public_key_ctx", "private_key_ctx", "provider_config", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    KEY_STATUS_FIELD_NUMBER: _ClassVar[int]
    KEY_MODE_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_CTX_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_CTX_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    key_id: str
    key_algorithm: Algorithm
    key_status: KeyStatus
    key_mode: KeyMode
    public_key_ctx: PublicKeyCtx
    private_key_ctx: PrivateKeyCtx
    provider_config: KeyProviderConfig
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., key_id: _Optional[str] = ..., key_algorithm: _Optional[_Union[Algorithm, str]] = ..., key_status: _Optional[_Union[KeyStatus, str]] = ..., key_mode: _Optional[_Union[KeyMode, str]] = ..., public_key_ctx: _Optional[_Union[PublicKeyCtx, _Mapping]] = ..., private_key_ctx: _Optional[_Union[PrivateKeyCtx, _Mapping]] = ..., provider_config: _Optional[_Union[KeyProviderConfig, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...

class SymmetricKey(_message.Message):
    __slots__ = ("id", "key_id", "key_status", "key_mode", "key_ctx", "provider_config", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_STATUS_FIELD_NUMBER: _ClassVar[int]
    KEY_MODE_FIELD_NUMBER: _ClassVar[int]
    KEY_CTX_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    key_id: str
    key_status: KeyStatus
    key_mode: KeyMode
    key_ctx: bytes
    provider_config: KeyProviderConfig
    metadata: _common_pb2.Metadata
    def __init__(self, id: _Optional[str] = ..., key_id: _Optional[str] = ..., key_status: _Optional[_Union[KeyStatus, str]] = ..., key_mode: _Optional[_Union[KeyMode, str]] = ..., key_ctx: _Optional[bytes] = ..., provider_config: _Optional[_Union[KeyProviderConfig, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.Metadata, _Mapping]] = ...) -> None: ...
