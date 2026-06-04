"""Key Access Service information and configuration."""

from dataclasses import dataclass


@dataclass
class KASInfo:
    """Configuration for Key Access Server (KAS) information.
    This class stores details about a Key Access Server including its URL,
    public key, key ID, default status, and cryptographic algorithm.
    """

    url: str
    public_key: str | None = None
    kid: str | None = None
    default: bool | None = None
    algorithm: str | None = None

    def clone(self):
        """Create a copy of this KASInfo object."""
        from copy import copy

        return copy(self)

    def __str__(self):
        return f"KASInfo(url={self.url}, kid={self.kid}, default={self.default}, algorithm={self.algorithm})"
