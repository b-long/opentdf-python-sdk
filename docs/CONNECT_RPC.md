# Connect RPC in OpenTDF Python SDK

This document describes the Connect RPC implementation in the OpenTDF Python SDK, which provides a modern HTTP-friendly alternative to traditional gRPC.

## Overview

Connect RPC is a protocol that brings the benefits of RPC to HTTP APIs. It's designed to be:
- **HTTP-compatible**: Works with standard HTTP infrastructure
- **Type-safe**: Generated from Protocol Buffer definitions
- **Efficient**: Binary protocol with JSON fallback
- **Simple**: Easy to debug and integrate

## Architecture

The SDK uses a two-module structure for protocol buffer generation:

- **Main SDK**: `src/otdf_python/` - Core SDK functionality
- **Protocol Generation**: `otdf-python-proto/` - Generated Connect RPC and protobuf files

### Generated Files

Connect RPC generates the following files in `otdf-python-proto/src/otdf_python_proto/`:

- `*_connect.py` - Connect RPC client implementations (recommended)
- `*_pb2.py` - Protocol buffer message definitions
- `legacy_grpc/*_pb2_grpc.py` - Traditional gRPC clients (backward compatibility)

## Usage

### Client Creation

Connect RPC clients are created using the generated `*_connect.py` modules:

```python
from otdf_python_proto.kas import kas_connect
from otdf_python_proto.policy import policy_connect

# Create Connect RPC clients
kas_client = kas_connect.KeyAccessServiceClient(base_url="https://example.com")
policy_client = policy_connect.PolicyServiceClient(base_url="https://your-policy-endpoint")
```

### Authentication

Connect RPC clients support standard HTTP authentication:

```python
import httpx

# Create authenticated HTTP client
http_client = httpx.Client(
    headers={"Authorization": f"Bearer {token}"}
)

# Use with Connect RPC client
kas_client = kas_connect.KeyAccessServiceClient(
    base_url="https://example.com",
    http_client=http_client
)
```

## Regenerating Connect RPC Files

To regenerate the Connect RPC and protobuf files:

```bash
cd otdf-python-proto
uv run python scripts/generate_connect_proto.py
```

### Download Fresh Proto Files

To download the latest protocol definitions:

```bash
cd otdf-python-proto
uv run python scripts/generate_connect_proto.py --download
```

### Requirements

- `buf` tool: `brew install bufbuild/buf/buf`
- Python dependencies managed by `uv`

## Benefits Over gRPC

1. **HTTP Compatibility**: Works with load balancers, proxies, and other HTTP infrastructure
2. **Debugging**: Easy to inspect with standard HTTP tools
3. **Flexibility**: Supports both binary and JSON encoding
4. **Simplicity**: No special HTTP/2 requirements

## Migration from gRPC

If migrating from legacy gRPC clients:

1. Replace `*_pb2_grpc.py` imports with `*_connect.py`
2. Update client instantiation to use base URLs instead of channels
3. Leverage HTTP client features for authentication and configuration

## Testing

Connect RPC clients can be easily mocked and tested using standard HTTP testing tools:

```python
import httpx
import respx

@respx.mock
def test_connect_rpc_client():
    respx.post("https://example.com/rewrap").mock(
        return_value=httpx.Response(200, json={"key": "decrypted"})
    )
    
    client = kas_connect.KeyAccessServiceClient(base_url="https://example.com")
    # Test client calls...
```

## Error Handling

Connect RPC provides structured error handling through standard HTTP status codes and error details:

```python
from connectrpc import ConnectError

try:
    response = client.some_method(request)
except ConnectError as e:
    print(f"Connect RPC error: {e.code} - {e.message}")
    # Handle specific error types
```

## Performance Considerations

- Use connection pooling with `httpx.Client` for better performance
- Configure appropriate timeouts for your use case
- Consider using binary encoding for high-throughput scenarios