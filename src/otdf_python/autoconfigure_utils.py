"""Utilities for automatic SDK configuration."""

import re
import urllib.parse
from dataclasses import dataclass
from typing import Any


# RuleType constants
class RuleType:
    """Rule type constants for attribute hierarchy."""

    HIERARCHY = "hierarchy"
    ALL_OF = "allOf"
    ANY_OF = "anyOf"
    UNSPECIFIED = "unspecified"
    EMPTY_TERM = "DEFAULT"


@dataclass(frozen=True)
class KeySplitStep:
    """Key split step information."""

    kas: str
    splitID: str

    def __str__(self):
        return f"KeySplitStep{{kas={self.kas}, splitID={self.splitID}}}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, KeySplitStep):
            return False
        return self.kas == other.kas and self.splitID == other.splitID

    def __hash__(self):
        return hash((self.kas, self.splitID))


class AutoConfigureException(Exception):
    """Exception for auto-configuration errors."""

    pass


class AttributeNameFQN:
    """Fully qualified attribute name."""

    def __init__(self, url: str):
        """Initialize attribute name from URL."""
        pattern = re.compile(r"^(https?://[\w./-]+)/attr/([^/\s]*)$")
        matcher = pattern.match(url)
        if not matcher or not matcher.group(1) or not matcher.group(2):
            raise AutoConfigureException("invalid type: attribute regex fail")
        try:
            urllib.parse.unquote(matcher.group(2))
        except Exception as err:
            raise AutoConfigureException(
                f"invalid type: error in attribute name [{matcher.group(2)}]"
            ) from err
        self.url = url
        self.key = url.lower()

    def __str__(self):
        return self.url

    def select(self, value: str):
        new_url = f"{self.url}/value/{urllib.parse.quote(value)}"
        return AttributeValueFQN(new_url)

    def prefix(self):
        return self.url

    def get_key(self):
        return self.key

    def authority(self):
        pattern = re.compile(r"^(https?://[\w./-]+)/attr/[^/\s]*$")
        matcher = pattern.match(self.url)
        if not matcher:
            raise AutoConfigureException("invalid type")
        return matcher.group(1)

    def name(self):
        pattern = re.compile(r"^https?://[\w./-]+/attr/([^/\s]*)$")
        matcher = pattern.match(self.url)
        if not matcher:
            raise AutoConfigureException("invalid attribute")
        try:
            return urllib.parse.unquote(matcher.group(1))
        except Exception as err:
            raise AutoConfigureException("invalid type") from err


class AttributeValueFQN:
    """Fully qualified attribute value."""

    def __init__(self, url: str):
        """Initialize attribute value from URL."""
        pattern = re.compile(r"^(https?://[\w./-]+)/attr/(\S*)/value/(\S*)$")
        matcher = pattern.match(url)
        if (
            not matcher
            or not matcher.group(1)
            or not matcher.group(2)
            or not matcher.group(3)
        ):
            raise AutoConfigureException(
                f"invalid type: attribute regex fail for [{url}]"
            )
        try:
            urllib.parse.unquote(matcher.group(2))
            urllib.parse.unquote(matcher.group(3))
        except Exception as err:
            raise AutoConfigureException(
                "invalid type: error in attribute or value"
            ) from err
        self.url = url
        self.key = url.lower()

    def __str__(self):
        return self.url

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AttributeValueFQN):
            return False
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)
