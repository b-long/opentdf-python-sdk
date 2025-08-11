from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    def __init__(self, version: _Optional[str] = ...) -> None: ...

class LegacyPublicKeyRequest(_message.Message):
    __slots__ = ("algorithm",)
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    algorithm: str
    def __init__(self, algorithm: _Optional[str] = ...) -> None: ...

class PolicyBinding(_message.Message):
    __slots__ = ("algorithm", "hash")
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    algorithm: str
    hash: str
    def __init__(self, algorithm: _Optional[str] = ..., hash: _Optional[str] = ...) -> None: ...

class KeyAccess(_message.Message):
    __slots__ = ("encrypted_metadata", "policy_binding", "protocol", "key_type", "kas_url", "kid", "split_id", "wrapped_key", "header", "ephemeral_public_key")
    ENCRYPTED_METADATA_FIELD_NUMBER: _ClassVar[int]
    POLICY_BINDING_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    KAS_URL_FIELD_NUMBER: _ClassVar[int]
    KID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    WRAPPED_KEY_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    encrypted_metadata: str
    policy_binding: PolicyBinding
    protocol: str
    key_type: str
    kas_url: str
    kid: str
    split_id: str
    wrapped_key: bytes
    header: bytes
    ephemeral_public_key: str
    def __init__(self, encrypted_metadata: _Optional[str] = ..., policy_binding: _Optional[_Union[PolicyBinding, _Mapping]] = ..., protocol: _Optional[str] = ..., key_type: _Optional[str] = ..., kas_url: _Optional[str] = ..., kid: _Optional[str] = ..., split_id: _Optional[str] = ..., wrapped_key: _Optional[bytes] = ..., header: _Optional[bytes] = ..., ephemeral_public_key: _Optional[str] = ...) -> None: ...

class UnsignedRewrapRequest(_message.Message):
    __slots__ = ("client_public_key", "requests", "key_access", "policy", "algorithm")
    class WithPolicy(_message.Message):
        __slots__ = ("id", "body")
        ID_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        id: str
        body: str
        def __init__(self, id: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...
    class WithKeyAccessObject(_message.Message):
        __slots__ = ("key_access_object_id", "key_access_object")
        KEY_ACCESS_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
        KEY_ACCESS_OBJECT_FIELD_NUMBER: _ClassVar[int]
        key_access_object_id: str
        key_access_object: KeyAccess
        def __init__(self, key_access_object_id: _Optional[str] = ..., key_access_object: _Optional[_Union[KeyAccess, _Mapping]] = ...) -> None: ...
    class WithPolicyRequest(_message.Message):
        __slots__ = ("key_access_objects", "policy", "algorithm")
        KEY_ACCESS_OBJECTS_FIELD_NUMBER: _ClassVar[int]
        POLICY_FIELD_NUMBER: _ClassVar[int]
        ALGORITHM_FIELD_NUMBER: _ClassVar[int]
        key_access_objects: _containers.RepeatedCompositeFieldContainer[UnsignedRewrapRequest.WithKeyAccessObject]
        policy: UnsignedRewrapRequest.WithPolicy
        algorithm: str
        def __init__(self, key_access_objects: _Optional[_Iterable[_Union[UnsignedRewrapRequest.WithKeyAccessObject, _Mapping]]] = ..., policy: _Optional[_Union[UnsignedRewrapRequest.WithPolicy, _Mapping]] = ..., algorithm: _Optional[str] = ...) -> None: ...
    CLIENT_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    KEY_ACCESS_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    client_public_key: str
    requests: _containers.RepeatedCompositeFieldContainer[UnsignedRewrapRequest.WithPolicyRequest]
    key_access: KeyAccess
    policy: str
    algorithm: str
    def __init__(self, client_public_key: _Optional[str] = ..., requests: _Optional[_Iterable[_Union[UnsignedRewrapRequest.WithPolicyRequest, _Mapping]]] = ..., key_access: _Optional[_Union[KeyAccess, _Mapping]] = ..., policy: _Optional[str] = ..., algorithm: _Optional[str] = ...) -> None: ...

class PublicKeyRequest(_message.Message):
    __slots__ = ("algorithm", "fmt", "v")
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    FMT_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    algorithm: str
    fmt: str
    v: str
    def __init__(self, algorithm: _Optional[str] = ..., fmt: _Optional[str] = ..., v: _Optional[str] = ...) -> None: ...

class PublicKeyResponse(_message.Message):
    __slots__ = ("public_key", "kid")
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    KID_FIELD_NUMBER: _ClassVar[int]
    public_key: str
    kid: str
    def __init__(self, public_key: _Optional[str] = ..., kid: _Optional[str] = ...) -> None: ...

class RewrapRequest(_message.Message):
    __slots__ = ("signed_request_token",)
    SIGNED_REQUEST_TOKEN_FIELD_NUMBER: _ClassVar[int]
    signed_request_token: str
    def __init__(self, signed_request_token: _Optional[str] = ...) -> None: ...

class KeyAccessRewrapResult(_message.Message):
    __slots__ = ("metadata", "key_access_object_id", "status", "kas_wrapped_key", "error")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    KEY_ACCESS_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    KAS_WRAPPED_KEY_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    key_access_object_id: str
    status: str
    kas_wrapped_key: bytes
    error: str
    def __init__(self, metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., key_access_object_id: _Optional[str] = ..., status: _Optional[str] = ..., kas_wrapped_key: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...

class PolicyRewrapResult(_message.Message):
    __slots__ = ("policy_id", "results")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    results: _containers.RepeatedCompositeFieldContainer[KeyAccessRewrapResult]
    def __init__(self, policy_id: _Optional[str] = ..., results: _Optional[_Iterable[_Union[KeyAccessRewrapResult, _Mapping]]] = ...) -> None: ...

class RewrapResponse(_message.Message):
    __slots__ = ("metadata", "entity_wrapped_key", "session_public_key", "schema_version", "responses")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_WRAPPED_KEY_FIELD_NUMBER: _ClassVar[int]
    SESSION_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    entity_wrapped_key: bytes
    session_public_key: str
    schema_version: str
    responses: _containers.RepeatedCompositeFieldContainer[PolicyRewrapResult]
    def __init__(self, metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., entity_wrapped_key: _Optional[bytes] = ..., session_public_key: _Optional[str] = ..., schema_version: _Optional[str] = ..., responses: _Optional[_Iterable[_Union[PolicyRewrapResult, _Mapping]]] = ...) -> None: ...
