from dataclasses import dataclass


@dataclass
class AttributeObject:
    attribute: str
    display_name: str | None = None
    is_default: bool = False
    pub_key: str | None = None
    kas_url: str | None = None


@dataclass
class PolicyBody:
    data_attributes: list[AttributeObject]
    dissem: list[str]


@dataclass
class PolicyObject:
    uuid: str
    body: PolicyBody
