"""SDK version information."""

import re
from functools import total_ordering


@total_ordering
class Version:
    """Semantic version representation."""

    SEMVER_PATTERN = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?P<prereleaseAndMetadata>\D.*)?$"
    )

    def __init__(
        self,
        semver_or_major,
        minor=None,
        patch=None,
        prerelease_and_metadata: str | None = None,
    ):
        """Initialize semantic version."""
        if minor is None and patch is None:
            # Parse from string
            m = self.SEMVER_PATTERN.match(semver_or_major)
            if not m:
                raise ValueError(f"Invalid version format: {semver_or_major}")
            self.major = int(m.group("major"))
            self.minor = int(m.group("minor"))
            self.patch = int(m.group("patch"))
            self.prerelease_and_metadata = m.group("prereleaseAndMetadata")
        else:
            self.major = int(semver_or_major)
            self.minor = int(minor)
            self.patch = int(patch)
            self.prerelease_and_metadata = prerelease_and_metadata

    def __str__(self):
        return f"Version{{major={self.major}, minor={self.minor}, patch={self.patch}, prereleaseAndMetadata='{self.prerelease_and_metadata}'}}"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        return (self.major, self.minor, self.patch) == (
            other.major,
            other.minor,
            other.patch,
        )

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        return False

    def __hash__(self):
        return hash((self.major, self.minor, self.patch))
