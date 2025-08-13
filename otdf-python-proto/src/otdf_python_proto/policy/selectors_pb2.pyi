from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttributeNamespaceSelector(_message.Message):
    __slots__ = ("with_attributes",)
    class AttributeSelector(_message.Message):
        __slots__ = ("with_key_access_grants", "with_values")
        class ValueSelector(_message.Message):
            __slots__ = ("with_key_access_grants", "with_subject_maps", "with_resource_maps")
            WITH_KEY_ACCESS_GRANTS_FIELD_NUMBER: _ClassVar[int]
            WITH_SUBJECT_MAPS_FIELD_NUMBER: _ClassVar[int]
            WITH_RESOURCE_MAPS_FIELD_NUMBER: _ClassVar[int]
            with_key_access_grants: bool
            with_subject_maps: bool
            with_resource_maps: bool
            def __init__(self, with_key_access_grants: bool = ..., with_subject_maps: bool = ..., with_resource_maps: bool = ...) -> None: ...
        WITH_KEY_ACCESS_GRANTS_FIELD_NUMBER: _ClassVar[int]
        WITH_VALUES_FIELD_NUMBER: _ClassVar[int]
        with_key_access_grants: bool
        with_values: AttributeNamespaceSelector.AttributeSelector.ValueSelector
        def __init__(self, with_key_access_grants: bool = ..., with_values: _Optional[_Union[AttributeNamespaceSelector.AttributeSelector.ValueSelector, _Mapping]] = ...) -> None: ...
    WITH_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    with_attributes: AttributeNamespaceSelector.AttributeSelector
    def __init__(self, with_attributes: _Optional[_Union[AttributeNamespaceSelector.AttributeSelector, _Mapping]] = ...) -> None: ...

class AttributeDefinitionSelector(_message.Message):
    __slots__ = ("with_key_access_grants", "with_namespace", "with_values")
    class NamespaceSelector(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ValueSelector(_message.Message):
        __slots__ = ("with_key_access_grants", "with_subject_maps", "with_resource_maps")
        WITH_KEY_ACCESS_GRANTS_FIELD_NUMBER: _ClassVar[int]
        WITH_SUBJECT_MAPS_FIELD_NUMBER: _ClassVar[int]
        WITH_RESOURCE_MAPS_FIELD_NUMBER: _ClassVar[int]
        with_key_access_grants: bool
        with_subject_maps: bool
        with_resource_maps: bool
        def __init__(self, with_key_access_grants: bool = ..., with_subject_maps: bool = ..., with_resource_maps: bool = ...) -> None: ...
    WITH_KEY_ACCESS_GRANTS_FIELD_NUMBER: _ClassVar[int]
    WITH_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    WITH_VALUES_FIELD_NUMBER: _ClassVar[int]
    with_key_access_grants: bool
    with_namespace: AttributeDefinitionSelector.NamespaceSelector
    with_values: AttributeDefinitionSelector.ValueSelector
    def __init__(self, with_key_access_grants: bool = ..., with_namespace: _Optional[_Union[AttributeDefinitionSelector.NamespaceSelector, _Mapping]] = ..., with_values: _Optional[_Union[AttributeDefinitionSelector.ValueSelector, _Mapping]] = ...) -> None: ...

class AttributeValueSelector(_message.Message):
    __slots__ = ("with_key_access_grants", "with_subject_maps", "with_resource_maps", "with_attribute")
    class AttributeSelector(_message.Message):
        __slots__ = ("with_key_access_grants", "with_namespace")
        class NamespaceSelector(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        WITH_KEY_ACCESS_GRANTS_FIELD_NUMBER: _ClassVar[int]
        WITH_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
        with_key_access_grants: bool
        with_namespace: AttributeValueSelector.AttributeSelector.NamespaceSelector
        def __init__(self, with_key_access_grants: bool = ..., with_namespace: _Optional[_Union[AttributeValueSelector.AttributeSelector.NamespaceSelector, _Mapping]] = ...) -> None: ...
    WITH_KEY_ACCESS_GRANTS_FIELD_NUMBER: _ClassVar[int]
    WITH_SUBJECT_MAPS_FIELD_NUMBER: _ClassVar[int]
    WITH_RESOURCE_MAPS_FIELD_NUMBER: _ClassVar[int]
    WITH_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    with_key_access_grants: bool
    with_subject_maps: bool
    with_resource_maps: bool
    with_attribute: AttributeValueSelector.AttributeSelector
    def __init__(self, with_key_access_grants: bool = ..., with_subject_maps: bool = ..., with_resource_maps: bool = ..., with_attribute: _Optional[_Union[AttributeValueSelector.AttributeSelector, _Mapping]] = ...) -> None: ...

class PageRequest(_message.Message):
    __slots__ = ("limit", "offset")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class PageResponse(_message.Message):
    __slots__ = ("current_offset", "next_offset", "total")
    CURRENT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    NEXT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    current_offset: int
    next_offset: int
    total: int
    def __init__(self, current_offset: _Optional[int] = ..., next_offset: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...
