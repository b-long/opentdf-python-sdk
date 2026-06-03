"""Policy object dataclasses for OpenTDF."""

from dataclasses import dataclass


@dataclass
class AttributeObject:
    """An attribute object."""

    attribute: str
    display_name: str | None = None
    is_default: bool = False
    pub_key: str | None = None
    kas_url: str | None = None


@dataclass
class PolicyBody:
    """A policy body."""

    data_attributes: list[AttributeObject]
    dissem: list[str]


@dataclass
class PolicyObject:
    """A policy object."""

    uuid: str
    body: PolicyBody
