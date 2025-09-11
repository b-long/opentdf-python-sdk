from enum import Enum, auto
from typing import Any


class Type(Enum):
    HANDLING_ASSERTION = "handling"
    BASE_ASSERTION = "base"

    def __str__(self):
        return self.value


class Scope(Enum):
    TRUSTED_DATA_OBJ = "tdo"
    PAYLOAD = "payload"

    def __str__(self):
        return self.value


class AssertionKeyAlg(Enum):
    RS256 = auto()
    HS256 = auto()
    NOT_DEFINED = auto()


class AppliesToState(Enum):
    ENCRYPTED = "encrypted"
    UNENCRYPTED = "unencrypted"

    def __str__(self):
        return self.value


class BindingMethod(Enum):
    JWS = "jws"

    def __str__(self):
        return self.value


class AssertionKey:
    def __init__(self, alg: AssertionKeyAlg, key: Any):
        self.alg = alg
        self.key = key

    def is_defined(self):
        return self.alg != AssertionKeyAlg.NOT_DEFINED


class Statement:
    def __init__(self, format: str, schema: str, value: str):
        self.format = format
        self.schema = schema
        self.value = value

    def __eq__(self, other):
        return (
            isinstance(other, Statement)
            and self.format == other.format
            and self.schema == other.schema
            and self.value == other.value
        )

    def __hash__(self):
        return hash((self.format, self.schema, self.value))


class AssertionConfig:
    def __init__(
        self,
        id: str,
        type: Type,
        scope: Scope,
        applies_to_state: AppliesToState,
        statement: Statement,
        signing_key: AssertionKey | None = None,
    ):
        self.id = id
        self.type = type
        self.scope = scope
        self.applies_to_state = applies_to_state
        self.statement = statement
        self.signing_key = signing_key
