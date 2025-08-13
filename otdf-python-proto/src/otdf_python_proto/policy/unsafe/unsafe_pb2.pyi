from buf.validate import validate_pb2 as _validate_pb2
from policy import objects_pb2 as _objects_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UnsafeUpdateNamespaceRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UnsafeUpdateNamespaceResponse(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _objects_pb2.Namespace
    def __init__(self, namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ...) -> None: ...

class UnsafeReactivateNamespaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnsafeReactivateNamespaceResponse(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _objects_pb2.Namespace
    def __init__(self, namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ...) -> None: ...

class UnsafeDeleteNamespaceRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class UnsafeDeleteNamespaceResponse(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _objects_pb2.Namespace
    def __init__(self, namespace: _Optional[_Union[_objects_pb2.Namespace, _Mapping]] = ...) -> None: ...

class UnsafeUpdateAttributeRequest(_message.Message):
    __slots__ = ("id", "name", "rule", "values_order")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    VALUES_ORDER_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    rule: _objects_pb2.AttributeRuleTypeEnum
    values_order: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., rule: _Optional[_Union[_objects_pb2.AttributeRuleTypeEnum, str]] = ..., values_order: _Optional[_Iterable[str]] = ...) -> None: ...

class UnsafeUpdateAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class UnsafeReactivateAttributeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnsafeReactivateAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class UnsafeDeleteAttributeRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class UnsafeDeleteAttributeResponse(_message.Message):
    __slots__ = ("attribute",)
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    attribute: _objects_pb2.Attribute
    def __init__(self, attribute: _Optional[_Union[_objects_pb2.Attribute, _Mapping]] = ...) -> None: ...

class UnsafeUpdateAttributeValueRequest(_message.Message):
    __slots__ = ("id", "value")
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    value: str
    def __init__(self, id: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class UnsafeUpdateAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class UnsafeReactivateAttributeValueRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnsafeReactivateAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class UnsafeDeleteAttributeValueRequest(_message.Message):
    __slots__ = ("id", "fqn")
    ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    id: str
    fqn: str
    def __init__(self, id: _Optional[str] = ..., fqn: _Optional[str] = ...) -> None: ...

class UnsafeDeleteAttributeValueResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _objects_pb2.Value
    def __init__(self, value: _Optional[_Union[_objects_pb2.Value, _Mapping]] = ...) -> None: ...

class UnsafeDeleteKasKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnsafeDeleteKasKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: _objects_pb2.Key
    def __init__(self, key: _Optional[_Union[_objects_pb2.Key, _Mapping]] = ...) -> None: ...
