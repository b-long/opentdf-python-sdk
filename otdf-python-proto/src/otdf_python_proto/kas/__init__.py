"""KAS (Key Access Service) protobuf definitions."""

from .kas_pb2 import *
from .kas_connect import AccessServiceClient, AccessServiceClientSync

__all__ = [
    "AccessServiceClient",
    "AccessServiceClientSync",
]
