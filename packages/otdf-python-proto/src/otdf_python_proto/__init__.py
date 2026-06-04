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

# Marker attribute placed on stub modules created by _register_subpackage_aliases.
# Used to distinguish our stubs from pre-existing third-party packages so we never
# clobber the latter.
_STUB_ATTR = "_otdf_python_proto_stub"


def _register_subpackage_aliases() -> None:
    # connect-generated files use absolute top-level imports (e.g. `import kas.kas_pb2`).
    # Register each subpackage as a top-level sys.modules alias so those imports resolve
    # without mutating sys.path for the whole process.
    #
    # Called twice: before the explicit imports below (creates lightweight stubs so that
    # load-time absolute imports inside connect files succeed) and after (upgrades stubs
    # to the fully-initialised module objects).
    pkg_dir = Path(__file__).parent
    for child in pkg_dir.iterdir():
        if not child.is_dir() or not (child / "__init__.py").exists() or child.name.startswith("_"):
            continue
        name = child.name
        current = sys.modules.get(name)
        # Never overwrite a pre-existing entry that we did not create.
        if current is not None and not getattr(current, _STUB_ATTR, False):
            continue
        full_name = f"otdf_python_proto.{name}"
        if full_name in sys.modules:
            # Real module is loaded; point the alias at it.
            sys.modules[name] = sys.modules[full_name]
        else:
            # Subpackage not yet imported; create a lightweight stub with __path__ set
            # so sub-imports like `import authorization.authorization_pb2` can locate
            # modules on disk without needing sys.path mutation.
            stub = types.ModuleType(name)
            stub.__path__ = [str(child)]  # type: ignore[attr-defined]
            stub.__package__ = name
            stub.__file__ = str(child / "__init__.py")
            setattr(stub, _STUB_ATTR, True)
            sys.modules[name] = stub


# First pass: create stubs so that connect-generated files can resolve absolute
# top-level imports (e.g. `import kas.kas_pb2`) at subpackage load time.
_register_subpackage_aliases()

# Import submodules to make them available.
# Note: authorization, entityresolution, wellknownconfiguration and policy subdirectories
# are imported lazily to avoid import errors from generated protobuf files.
from . import common
from . import entity
from . import kas
from . import legacy_grpc
from . import logger
from . import policy

# Second pass: upgrade stubs for the explicitly imported subpackages to the
# fully-initialised module objects.
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
