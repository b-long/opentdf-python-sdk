from buf.validate import validate_pb2 as _validate_pb2
from common import common_pb2 as _common_pb2
from google.api import annotations_pb2 as _annotations_pb2
from policy import objects_pb2 as _objects_pb2
from policy import selectors_pb2 as _selectors_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetKeyAccessServerRequest(_message.Message):
    __slots__ = ("id", "kas_id", "name", "uri")
    ID_FIELD_NUMBER: _ClassVar[int]
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    id: str
    kas_id: str
    name: str
    uri: str
    def __init__(self, id: _Optional[str] = ..., kas_id: _Optional[str] = ..., name: _Optional[str] = ..., uri: _Optional[str] = ...) -> None: ...

class GetKeyAccessServerResponse(_message.Message):
    __slots__ = ("key_access_server",)
    KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    key_access_server: _objects_pb2.KeyAccessServer
    def __init__(self, key_access_server: _Optional[_Union[_objects_pb2.KeyAccessServer, _Mapping]] = ...) -> None: ...

class ListKeyAccessServersRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _selectors_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListKeyAccessServersResponse(_message.Message):
    __slots__ = ("key_access_servers", "pagination")
    KEY_ACCESS_SERVERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    key_access_servers: _containers.RepeatedCompositeFieldContainer[_objects_pb2.KeyAccessServer]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, key_access_servers: _Optional[_Iterable[_Union[_objects_pb2.KeyAccessServer, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class CreateKeyAccessServerRequest(_message.Message):
    __slots__ = ("uri", "public_key", "source_type", "name", "metadata")
    URI_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    uri: str
    public_key: _objects_pb2.PublicKey
    source_type: _objects_pb2.SourceType
    name: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, uri: _Optional[str] = ..., public_key: _Optional[_Union[_objects_pb2.PublicKey, _Mapping]] = ..., source_type: _Optional[_Union[_objects_pb2.SourceType, str]] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateKeyAccessServerResponse(_message.Message):
    __slots__ = ("key_access_server",)
    KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    key_access_server: _objects_pb2.KeyAccessServer
    def __init__(self, key_access_server: _Optional[_Union[_objects_pb2.KeyAccessServer, _Mapping]] = ...) -> None: ...

class UpdateKeyAccessServerRequest(_message.Message):
    __slots__ = ("id", "uri", "public_key", "source_type", "name", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    uri: str
    public_key: _objects_pb2.PublicKey
    source_type: _objects_pb2.SourceType
    name: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., uri: _Optional[str] = ..., public_key: _Optional[_Union[_objects_pb2.PublicKey, _Mapping]] = ..., source_type: _Optional[_Union[_objects_pb2.SourceType, str]] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateKeyAccessServerResponse(_message.Message):
    __slots__ = ("key_access_server",)
    KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    key_access_server: _objects_pb2.KeyAccessServer
    def __init__(self, key_access_server: _Optional[_Union[_objects_pb2.KeyAccessServer, _Mapping]] = ...) -> None: ...

class DeleteKeyAccessServerRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteKeyAccessServerResponse(_message.Message):
    __slots__ = ("key_access_server",)
    KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    key_access_server: _objects_pb2.KeyAccessServer
    def __init__(self, key_access_server: _Optional[_Union[_objects_pb2.KeyAccessServer, _Mapping]] = ...) -> None: ...

class GrantedPolicyObject(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class KeyAccessServerGrants(_message.Message):
    __slots__ = ("key_access_server", "namespace_grants", "attribute_grants", "value_grants")
    KEY_ACCESS_SERVER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_GRANTS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_GRANTS_FIELD_NUMBER: _ClassVar[int]
    VALUE_GRANTS_FIELD_NUMBER: _ClassVar[int]
    key_access_server: _objects_pb2.KeyAccessServer
    namespace_grants: _containers.RepeatedCompositeFieldContainer[GrantedPolicyObject]
    attribute_grants: _containers.RepeatedCompositeFieldContainer[GrantedPolicyObject]
    value_grants: _containers.RepeatedCompositeFieldContainer[GrantedPolicyObject]
    def __init__(self, key_access_server: _Optional[_Union[_objects_pb2.KeyAccessServer, _Mapping]] = ..., namespace_grants: _Optional[_Iterable[_Union[GrantedPolicyObject, _Mapping]]] = ..., attribute_grants: _Optional[_Iterable[_Union[GrantedPolicyObject, _Mapping]]] = ..., value_grants: _Optional[_Iterable[_Union[GrantedPolicyObject, _Mapping]]] = ...) -> None: ...

class CreatePublicKeyRequest(_message.Message):
    __slots__ = ("kas_id", "key", "metadata")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    key: _objects_pb2.KasPublicKey
    metadata: _common_pb2.MetadataMutable
    def __init__(self, kas_id: _Optional[str] = ..., key: _Optional[_Union[_objects_pb2.KasPublicKey, _Mapping]] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreatePublicKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _objects_pb2.Key
    def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ...) -> None: ...

class GetPublicKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPublicKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _objects_pb2.Key
    def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ...) -> None: ...

class ListPublicKeysRequest(_message.Message):
    __slots__ = ("kas_id", "kas_name", "kas_uri", "pagination")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KAS_NAME_FIELD_NUMBER: _ClassVar[int]
    KAS_URI_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    kas_name: str
    kas_uri: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, kas_id: _Optional[str] = ..., kas_name: _Optional[str] = ..., kas_uri: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListPublicKeysResponse(_message.Message):
    __slots__ = ("keys", "pagination")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[_objects_pb2.Key]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, keys: _Optional[_Iterable[_Union[_objects_pb2.Key, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class ListPublicKeyMappingRequest(_message.Message):
    __slots__ = ("kas_id", "kas_name", "kas_uri", "public_key_id", "pagination")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KAS_NAME_FIELD_NUMBER: _ClassVar[int]
    KAS_URI_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    kas_name: str
    kas_uri: str
    public_key_id: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, kas_id: _Optional[str] = ..., kas_name: _Optional[str] = ..., kas_uri: _Optional[str] = ..., public_key_id: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListPublicKeyMappingResponse(_message.Message):
    __slots__ = ("public_key_mappings", "pagination")
    class PublicKeyMapping(_message.Message):
        __slots__ = ("kas_id", "kas_name", "kas_uri", "public_keys")
        KAS_ID_FIELD_NUMBER: _ClassVar[int]
        KAS_NAME_FIELD_NUMBER: _ClassVar[int]
        KAS_URI_FIELD_NUMBER: _ClassVar[int]
        PUBLIC_KEYS_FIELD_NUMBER: _ClassVar[int]
        kas_id: str
        kas_name: str
        kas_uri: str
        public_keys: _containers.RepeatedCompositeFieldContainer[ListPublicKeyMappingResponse.PublicKey]
        def __init__(self, kas_id: _Optional[str] = ..., kas_name: _Optional[str] = ..., kas_uri: _Optional[str] = ..., public_keys: _Optional[_Iterable[_Union[ListPublicKeyMappingResponse.PublicKey, _Mapping]]] = ...) -> None: ...
    class PublicKey(_message.Message):
        __slots__ = ("key", "values", "definitions", "namespaces")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
        NAMESPACES_FIELD_NUMBER: _ClassVar[int]
        key: _objects_pb2.Key
        values: _containers.RepeatedCompositeFieldContainer[ListPublicKeyMappingResponse.Association]
        definitions: _containers.RepeatedCompositeFieldContainer[ListPublicKeyMappingResponse.Association]
        namespaces: _containers.RepeatedCompositeFieldContainer[ListPublicKeyMappingResponse.Association]
        def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ..., values: _Optional[_Iterable[_Union[ListPublicKeyMappingResponse.Association, _Mapping]]] = ..., definitions: _Optional[_Iterable[_Union[ListPublicKeyMappingResponse.Association, _Mapping]]] = ..., namespaces: _Optional[_Iterable[_Union[ListPublicKeyMappingResponse.Association, _Mapping]]] = ...) -> None: ...
    class Association(_message.Message):
        __slots__ = ("id", "fqn")
        ID_FIELD_NUMBER: _ClassVar[int]
        FQN_FIELD_NUMBER: _ClassVar[int]
        id: str
        fqn: str
        def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...
    PUBLIC_KEY_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    public_key_mappings: _containers.RepeatedCompositeFieldContainer[ListPublicKeyMappingResponse.PublicKeyMapping]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, public_key_mappings: _Optional[_Iterable[_Union[ListPublicKeyMappingResponse.PublicKeyMapping, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class UpdatePublicKeyRequest(_message.Message):
    __slots__ = ("id", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdatePublicKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _objects_pb2.Key
    def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ...) -> None: ...

class DeactivatePublicKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeactivatePublicKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _objects_pb2.Key
    def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ...) -> None: ...

class ActivatePublicKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ActivatePublicKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _objects_pb2.Key
    def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ...) -> None: ...

class ListKeyAccessServerGrantsRequest(_message.Message):
    __slots__ = ("kas_id", "kas_uri", "kas_name", "pagination")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KAS_URI_FIELD_NUMBER: _ClassVar[int]
    KAS_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    kas_uri: str
    kas_name: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, kas_id: _Optional[str] = ..., kas_uri: _Optional[str] = ..., kas_name: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListKeyAccessServerGrantsResponse(_message.Message):
    __slots__ = ("grants", "pagination")
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    grants: _containers.RepeatedCompositeFieldContainer[KeyAccessServerGrants]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, grants: _Optional[_Iterable[_Union[KeyAccessServerGrants, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class CreateKeyRequest(_message.Message):
    __slots__ = ("kas_id", "key_id", "key_algorithm", "key_mode", "public_key_ctx", "private_key_ctx", "provider_config_id", "metadata")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    KEY_MODE_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_CTX_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_CTX_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    key_id: str
    key_algorithm: _objects_pb2.Algorithm
    key_mode: _objects_pb2.KeyMode
    public_key_ctx: _objects_pb2.PublicKeyCtx
    private_key_ctx: _objects_pb2.PrivateKeyCtx
    provider_config_id: str
    metadata: _common_pb2.MetadataMutable
    def __init__(self, kas_id: _Optional[str] = ..., key_id: _Optional[str] = ..., key_algorithm: _Optional[_Union[_objects_pb2.Algorithm, str]] = ..., key_mode: _Optional[_Union[_objects_pb2.KeyMode, str]] = ..., public_key_ctx: _Optional[_Union[_objects_pb2.PublicKeyCtx, _Mapping]] = ..., private_key_ctx: _Optional[_Union[_objects_pb2.PrivateKeyCtx, _Mapping]] = ..., provider_config_id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...

class CreateKeyResponse(_message.Message):
    __slots__ = ("kas_key",)
    KAS_KEY_FIELD_NUMBER: _ClassVar[int]
    kas_key: _objects_pb2.KasKey
    def __init__(self, kas_key: _Optional[_Union[_objects_pb2.KasKey, _Mapping]] = ...) -> None: ...

class GetKeyRequest(_message.Message):
    __slots__ = ("id", "key")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    key: KasKeyIdentifier
    def __init__(self, id: _Optional[str] = ..., key: _Optional[_Union[KasKeyIdentifier, _Mapping]] = ...) -> None: ...

class GetKeyResponse(_message.Message):
    __slots__ = ("kas_key",)
    KAS_KEY_FIELD_NUMBER: _ClassVar[int]
    kas_key: _objects_pb2.KasKey
    def __init__(self, kas_key: _Optional[_Union[_objects_pb2.KasKey, _Mapping]] = ...) -> None: ...

class ListKeysRequest(_message.Message):
    __slots__ = ("key_algorithm", "kas_id", "kas_name", "kas_uri", "pagination")
    KEY_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    KAS_NAME_FIELD_NUMBER: _ClassVar[int]
    KAS_URI_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    key_algorithm: _objects_pb2.Algorithm
    kas_id: str
    kas_name: str
    kas_uri: str
    pagination: _selectors_pb2.PageRequest
    def __init__(self, key_algorithm: _Optional[_Union[_objects_pb2.Algorithm, str]] = ..., kas_id: _Optional[str] = ..., kas_name: _Optional[str] = ..., kas_uri: _Optional[str] = ..., pagination: _Optional[_Union[_selectors_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class ListKeysResponse(_message.Message):
    __slots__ = ("kas_keys", "pagination")
    KAS_KEYS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    kas_keys: _containers.RepeatedCompositeFieldContainer[_objects_pb2.KasKey]
    pagination: _selectors_pb2.PageResponse
    def __init__(self, kas_keys: _Optional[_Iterable[_Union[_objects_pb2.KasKey, _Mapping]]] = ..., pagination: _Optional[_Union[_selectors_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class UpdateKeyRequest(_message.Message):
    __slots__ = ("id", "metadata", "metadata_update_behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_UPDATE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _common_pb2.MetadataMutable
    metadata_update_behavior: _common_pb2.MetadataUpdateEnum
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ..., metadata_update_behavior: _Optional[_Union[_common_pb2.MetadataUpdateEnum, str]] = ...) -> None: ...

class UpdateKeyResponse(_message.Message):
    __slots__ = ("kas_key",)
    KAS_KEY_FIELD_NUMBER: _ClassVar[int]
    kas_key: _objects_pb2.KasKey
    def __init__(self, kas_key: _Optional[_Union[_objects_pb2.KasKey, _Mapping]] = ...) -> None: ...

class KasKeyIdentifier(_message.Message):
    __slots__ = ("kas_id", "name", "uri", "kid")
    KAS_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    KID_FIELD_NUMBER: _ClassVar[int]
    kas_id: str
    name: str
    uri: str
    kid: str
    def __init__(self, kas_id: _Optional[str] = ..., name: _Optional[str] = ..., uri: _Optional[str] = ..., kid: _Optional[str] = ...) -> None: ...

class RotateKeyRequest(_message.Message):
    __slots__ = ("id", "key", "new_key")
    class NewKey(_message.Message):
        __slots__ = ("key_id", "algorithm", "key_mode", "public_key_ctx", "private_key_ctx", "provider_config_id", "metadata")
        KEY_ID_FIELD_NUMBER: _ClassVar[int]
        ALGORITHM_FIELD_NUMBER: _ClassVar[int]
        KEY_MODE_FIELD_NUMBER: _ClassVar[int]
        PUBLIC_KEY_CTX_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_KEY_CTX_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        key_id: str
        algorithm: _objects_pb2.Algorithm
        key_mode: _objects_pb2.KeyMode
        public_key_ctx: _objects_pb2.PublicKeyCtx
        private_key_ctx: _objects_pb2.PrivateKeyCtx
        provider_config_id: str
        metadata: _common_pb2.MetadataMutable
        def __init__(self, key_id: _Optional[str] = ..., algorithm: _Optional[_Union[_objects_pb2.Algorithm, str]] = ..., key_mode: _Optional[_Union[_objects_pb2.KeyMode, str]] = ..., public_key_ctx: _Optional[_Union[_objects_pb2.PublicKeyCtx, _Mapping]] = ..., private_key_ctx: _Optional[_Union[_objects_pb2.PrivateKeyCtx, _Mapping]] = ..., provider_config_id: _Optional[str] = ..., metadata: _Optional[_Union[_common_pb2.MetadataMutable, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NEW_KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    key: KasKeyIdentifier
    new_key: RotateKeyRequest.NewKey
    def __init__(self, id: _Optional[str] = ..., key: _Optional[_Union[KasKeyIdentifier, _Mapping]] = ..., new_key: _Optional[_Union[RotateKeyRequest.NewKey, _Mapping]] = ...) -> None: ...

class ChangeMappings(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class RotatedResources(_message.Message):
    __slots__ = ("rotated_out_key", "attribute_definition_mappings", "attribute_value_mappings", "namespace_mappings")
    ROTATED_OUT_KEY_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_DEFINITION_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    rotated_out_key: _objects_pb2.KasKey
    attribute_definition_mappings: _containers.RepeatedCompositeFieldContainer[ChangeMappings]
    attribute_value_mappings: _containers.RepeatedCompositeFieldContainer[ChangeMappings]
    namespace_mappings: _containers.RepeatedCompositeFieldContainer[ChangeMappings]
    def __init__(self, rotated_out_key: _Optional[_Union[_objects_pb2.KasKey, _Mapping]] = ..., attribute_definition_mappings: _Optional[_Iterable[_Union[ChangeMappings, _Mapping]]] = ..., attribute_value_mappings: _Optional[_Iterable[_Union[ChangeMappings, _Mapping]]] = ..., namespace_mappings: _Optional[_Iterable[_Union[ChangeMappings, _Mapping]]] = ...) -> None: ...

class RotateKeyResponse(_message.Message):
    __slots__ = ("kas_key", "rotated_resources")
    KAS_KEY_FIELD_NUMBER: _ClassVar[int]
    ROTATED_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    kas_key: _objects_pb2.KasKey
    rotated_resources: RotatedResources
    def __init__(self, kas_key: _Optional[_Union[_objects_pb2.KasKey, _Mapping]] = ..., rotated_resources: _Optional[_Union[RotatedResources, _Mapping]] = ...) -> None: ...

class SetBaseKeyRequest(_message.Message):
    __slots__ = ("id", "key")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    key: KasKeyIdentifier
    def __init__(self, id: _Optional[str] = ..., key: _Optional[_Union[KasKeyIdentifier, _Mapping]] = ...) -> None: ...

class GetBaseKeyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBaseKeyResponse(_message.Message):
    __slots__ = ("base_key",)
    BASE_KEY_FIELD_NUMBER: _ClassVar[int]
    base_key: _objects_pb2.SimpleKasKey
    def __init__(self, base_key: _Optional[_Union[_objects_pb2.SimpleKasKey, _Mapping]] = ...) -> None: ...

class SetBaseKeyResponse(_message.Message):
    __slots__ = ("new_base_key", "previous_base_key")
    NEW_BASE_KEY_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_BASE_KEY_FIELD_NUMBER: _ClassVar[int]
    new_base_key: _objects_pb2.SimpleKasKey
    previous_base_key: _objects_pb2.SimpleKasKey
    def __init__(self, new_base_key: _Optional[_Union[_objects_pb2.SimpleKasKey, _Mapping]] = ..., previous_base_key: _Optional[_Union[_objects_pb2.SimpleKasKey, _Mapping]] = ...) -> None: ...
