"""Hatchling build hook for otdf-python."""

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Dynamically resolves proto sources for wheel builds from source tree or sdist."""

    def initialize(self, version, build_data):
        """Set force_include for otdf_python_proto based on build context."""
        if self.target_name != "wheel":
            return

        root = Path(self.root)

        # When building from source tree, the proto package is a sibling directory.
        # When building from an sdist, we embed the protos at _proto/ inside the sdist root.
        source_tree_path = (
            root / ".." / "otdf-python-proto" / "src" / "otdf_python_proto"
        ).resolve()
        sdist_path = (root / "_proto" / "otdf_python_proto").resolve()

        if source_tree_path.is_dir():
            proto_src = str(source_tree_path)
        elif sdist_path.is_dir():
            proto_src = str(sdist_path)
        else:
            raise FileNotFoundError(
                f"otdf_python_proto sources not found at {source_tree_path!r} or {sdist_path!r}"
            )

        build_data["force_include"][proto_src] = "otdf_python_proto"
