"""Assertion configuration for TDF."""

from enum import Enum, auto
from typing import Any


class Type(Enum):
    """Assertion type enumeration."""

    HANDLING_ASSERTION = "handling"
    BASE_ASSERTION = "base"

    def __str__(self):
        return self.value


class Scope(Enum):
    """Assertion scope enumeration."""

    TRUSTED_DATA_OBJ = "tdo"
    PAYLOAD = "payload"

    def __str__(self):
        return self.value


class AssertionKeyAlg(Enum):
    """Assertion key algorithm enumeration."""

    RS256 = auto()
    HS256 = auto()
    NOT_DEFINED = auto()


class AppliesToState(Enum):
    """Assertion applies-to state enumeration."""

    ENCRYPTED = "encrypted"
    UNENCRYPTED = "unencrypted"

    def __str__(self):
        return self.value


class BindingMethod(Enum):
    """Assertion binding method enumeration."""

    JWS = "jws"

    def __str__(self):
        return self.value


class AssertionKey:
    """Assertion signing key configuration."""

    def __init__(self, alg: AssertionKeyAlg, key: Any):
        """Initialize assertion key."""
        self.alg = alg
        self.key = key

    def is_defined(self):
        return self.alg != AssertionKeyAlg.NOT_DEFINED


class Statement:
    """Assertion statement with format, schema, and value."""

    def __init__(self, format: str, schema: str, value: str):
        """Initialize assertion statement."""
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
    """TDF assertion configuration."""

    def __init__(
        self,
        id: str,
        type: Type,
        scope: Scope,
        applies_to_state: AppliesToState,
        statement: Statement,
        signing_key: AssertionKey | None = None,
    ):
        """Initialize assertion configuration."""
        self.id = id
        self.type = type
        self.scope = scope
        self.applies_to_state = applies_to_state
        self.statement = statement
        self.signing_key = signing_key
