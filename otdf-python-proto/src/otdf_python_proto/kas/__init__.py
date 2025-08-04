"""KAS (Key Access Service) protobuf definitions."""

from .kas_pb2 import *
from .kas_pb2_connect import AccessServiceClient, AsyncAccessServiceClient

__all__ = [
    "AccessServiceClient",
    "AsyncAccessServiceClient",
]
