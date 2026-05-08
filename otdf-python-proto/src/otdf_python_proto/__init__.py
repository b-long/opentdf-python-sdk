"""OpenTDF Python Protocol Buffers Package.

This package contains generated Python code from OpenTDF protocol buffer definitions.
It includes modules for authorization, common types, entities, policy management,
and other OpenTDF services.
"""
import sys
import types
from pathlib import Path
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


def _register_subpackage_aliases() -> None:
    # connect-generated files use absolute top-level imports (e.g. `import kas.kas_pb2`).
    # Register each subpackage as a top-level sys.modules alias so those imports resolve
    # without mutating sys.path for the whole process.
    pkg_dir = Path(__file__).parent
    for child in pkg_dir.iterdir():
        if not child.is_dir() or not (child / "__init__.py").exists() or child.name.startswith("_"):
            continue
        name = child.name
        if name in sys.modules:
            continue
        full_name = f"otdf_python_proto.{name}"
        if full_name in sys.modules:
            sys.modules[name] = sys.modules[full_name]
        else:
            # Subpackage not yet imported (lazy); create a lightweight stub so that
            # sub-imports like `import authorization.authorization_pb2` can still
            # locate the module on disk via __path__.
            stub = types.ModuleType(name)
            stub.__path__ = [str(child)]  # type: ignore[attr-defined]
            stub.__package__ = name
            stub.__file__ = str(child / "__init__.py")
            sys.modules[name] = stub


_register_subpackage_aliases()

# Export main module categories
__all__ = [
    "common",
    "entity",
    "kas",
    "legacy_grpc",
    "logger",
    "policy",
]
