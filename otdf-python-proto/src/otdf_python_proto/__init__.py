"""OpenTDF Python Protocol Buffers Package.

This package contains generated Python code from OpenTDF protocol buffer definitions.
It includes modules for authorization, common types, entities, policy management,
and other OpenTDF services.
"""
from importlib import metadata

try:
    __version__ = metadata.version("otdf-python-proto")
except metadata.PackageNotFoundError:
    # package is not installed, e.g., in development
    __version__ = "0.0.0"

# Import submodules to make them available
# Note: authorization, entityresolution, wellknownconfiguration and policy subdirectories
# are imported lazily to avoid import errors from generated protobuf files
from . import common
from . import entity
from . import kas
from . import legacy_grpc
from . import logger
from . import policy

# Export main module categories
__all__ = [
    "common",
    "entity",
    "kas",
    "legacy_grpc",
    "logger",
    "policy",
]
