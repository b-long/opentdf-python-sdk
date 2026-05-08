"""Tests for the sys.modules alias workaround in otdf_python_proto/__init__.py.

connect-generated files emit absolute top-level imports such as
`import kas.kas_pb2`.  _register_subpackage_aliases() pre-registers each
subpackage in sys.modules so those imports resolve without mutating sys.path.
"""

import sys


def test_explicitly_imported_subpackages_aliased_as_top_level():
    """Subpackages imported in __init__.py are accessible as top-level names."""
    import otdf_python_proto  # noqa: F401

    for name in ("common", "entity", "kas", "legacy_grpc", "logger", "policy"):
        assert name in sys.modules, f"sys.modules missing alias for '{name}'"
        # Aliases for explicitly imported packages must point to the real module,
        # not a stub.
        from otdf_python_proto import _STUB_ATTR

        assert not getattr(sys.modules[name], _STUB_ATTR, False), (
            f"alias for '{name}' still points to a stub after package init"
        )


def test_lazy_subpackages_have_top_level_stub():
    """Lazy subpackages (not imported in __init__) get a stub with __path__ set."""
    import otdf_python_proto  # noqa: F401

    for name in ("authorization", "entityresolution", "wellknownconfiguration"):
        assert name in sys.modules, f"sys.modules missing stub for '{name}'"
        mod = sys.modules[name]
        assert hasattr(mod, "__path__"), f"stub for '{name}' is missing __path__"


def test_alias_does_not_override_existing_sys_modules_entry():
    """_register_subpackage_aliases() must not clobber a pre-existing entry."""
    from otdf_python_proto import _register_subpackage_aliases

    real_kas = sys.modules.get("kas")
    sentinel = object()
    sys.modules["kas"] = sentinel  # type: ignore[assignment]
    try:
        _register_subpackage_aliases()
        assert sys.modules["kas"] is sentinel, (
            "_register_subpackage_aliases() overwrote a pre-existing sys.modules entry"
        )
    finally:
        if real_kas is not None:
            sys.modules["kas"] = real_kas
        else:
            sys.modules.pop("kas", None)


def test_connect_absolute_import_resolves():
    """The absolute import used by kas_connect.py must succeed after package init."""
    import importlib

    import otdf_python_proto  # noqa: F401

    # Mirrors `import kas.kas_pb2 as kas_dot_kas__pb2` in kas_connect.py.
    mod = importlib.import_module("kas.kas_pb2")
    assert mod is not None
    assert hasattr(mod, "PublicKeyRequest"), (
        "kas.kas_pb2 loaded but PublicKeyRequest message is missing"
    )
