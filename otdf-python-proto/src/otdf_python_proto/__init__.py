"""OpenTDF Python Protocol Buffers Package.

This package contains generated Python code from OpenTDF protocol buffer definitions.
It includes modules for authorization, common types, entities, policy management,
and other OpenTDF services.
"""

__version__ = "0.1.0"

# Import submodules to make them available
from . import authorization
from . import common
from . import entity
from . import entityresolution
from . import kas
from . import legacy_grpc
from . import logger
from . import policy
from . import wellknownconfiguration

# Export main module categories
__all__ = [
    "authorization",
    "common",
    "entity",
    "entityresolution",
    "kas",
    "legacy_grpc",
    "logger",
    "policy",
    "wellknownconfiguration",
]
