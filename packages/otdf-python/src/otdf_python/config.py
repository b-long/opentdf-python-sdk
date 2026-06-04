"""Configuration classes for TDF and NanoTDF operations."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from urllib.parse import urlparse, urlunparse


class TDFFormat(Enum):
    """TDF format enumeration."""

    JSONFormat = "JSONFormat"
    XMLFormat = "XMLFormat"


class IntegrityAlgorithm(Enum):
    """Integrity algorithm enumeration."""

    HS256 = "HS256"
    GMAC = "GMAC"


@dataclass
class KASInfo:
    """Key Access Service information."""

    url: str
    public_key: str | None = None
    kid: str | None = None
    default: bool | None = None
    algorithm: str | None = None

    def __str__(self):
        return f"KASInfo{{URL:'{self.url}', PublicKey:'{self.public_key}', KID:'{self.kid}', Default:{self.default}, Algorithm:'{self.algorithm}'}}"


@dataclass
class TDFConfig:
    """TDF encryption configuration."""

    autoconfigure: bool = True
    default_segment_size: int = 2 * 1024 * 1024
    enable_encryption: bool = True
    tdf_format: TDFFormat = TDFFormat.JSONFormat
    tdf_public_key: str | None = None
    tdf_private_key: str | None = None
    meta_data: str | None = None
    integrity_algorithm: IntegrityAlgorithm = IntegrityAlgorithm.HS256
    segment_integrity_algorithm: IntegrityAlgorithm = IntegrityAlgorithm.GMAC
    attributes: list[str] = field(default_factory=list)
    kas_info_list: list[KASInfo] = field(default_factory=list)
    mime_type: str = "application/octet-stream"
    split_plan: list[str] | None = field(default_factory=list)
    wrapping_key_type: str | None = None
    hex_encode_root_and_segment_hashes: bool = False
    render_version_info_in_manifest: bool = True
    policy_object: Any | None = None


@dataclass
class NanoTDFConfig:
    """NanoTDF encryption configuration."""

    ecc_mode: str | None = None
    cipher: str | None = None
    config: str | None = None
    attributes: list[str] = field(default_factory=list)
    kas_info_list: list[KASInfo] = field(default_factory=list)
    collection_config: str | None = None
    policy_type: str | None = None


# Utility function to normalize KAS URLs (Python equivalent)
def get_kas_address(kas_url: str) -> str:
    """Normalize KAS URL by adding https:// if no scheme present."""
    if "://" not in kas_url:
        kas_url = "https://" + kas_url
    parsed = urlparse(kas_url)
    scheme = parsed.scheme or "https"
    netloc = parsed.hostname or ""
    port = parsed.port or 443
    return urlunparse((scheme, f"{netloc}:{port}", "", "", "", ""))
