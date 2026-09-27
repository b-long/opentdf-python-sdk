"""Policy binding serialization for HMAC calculation."""

from typing import Any


class PolicyBinding:
    """Represents a policy binding in the TDF manifest.

    This is a placeholder implementation as the complete details of
    the PolicyBinding class aren't provided in the code snippets.
    """

    def __init__(self, **kwargs):
        """Initialize policy binding from kwargs."""
        for key, value in kwargs.items():
            setattr(self, key, value)


class PolicyBindingSerializer:
    """Handles serialization and deserialization of policy bindings.

    This class provides static methods to convert between JSON representations
    and PolicyBinding objects.
    """

    @staticmethod
    def deserialize(
        json_data: Any, _typeof_t: type | None = None, _context: Any = None
    ) -> Any:
        if isinstance(json_data, dict):
            return PolicyBinding(**json_data)
        if isinstance(json_data, str):
            return json_data
        raise ValueError("Invalid type for PolicyBinding deserialization")

    @staticmethod
    def serialize(
        src: Any, _typeof_src: type | None = None, _context: Any = None
    ) -> dict | str:
        if isinstance(src, PolicyBinding):
            return vars(src)
        return str(src)
