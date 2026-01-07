"""authorization protobuf definitions."""

from .authorization_connect import (
    AuthorizationServiceClient,
    AuthorizationServiceClientSync,
)

__all__ = [
    "AuthorizationServiceClient",
    "AuthorizationServiceClientSync",
]
