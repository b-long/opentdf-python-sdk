"""policy.keymanagement protobuf definitions."""

from .key_management_connect import (
    KeyManagementServiceClient,
    KeyManagementServiceClientSync,
)

__all__ = [
    "KeyManagementServiceClient",
    "KeyManagementServiceClientSync",
]
