"""OpenTDF Python Protocol Buffers Package.

This package contains generated Python code from OpenTDF protocol buffer definitions.
It includes modules for authorization, common types, entities, policy management,
and other OpenTDF services.
"""
import sys
from pathlib import Path
from importlib import metadata

# connect-python v0.6+ generates absolute sub-package imports (e.g. `import kas.kas_pb2`)
# rather than relative ones. Add this package's directory to sys.path so those imports resolve.
_pkg_dir = str(Path(__file__).parent)
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

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
