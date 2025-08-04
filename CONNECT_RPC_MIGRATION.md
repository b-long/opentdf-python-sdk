# Connect RPC Migration Guide

This document explains how to migrate from traditional gRPC clients to Connect RPC clients in the OpenTDF Python SDK.

## What is Connect RPC?

Connect RPC is a modern, HTTP-friendly alternative to gRPC that provides:

- **HTTP/1.1 compatibility** - Works with all HTTP infrastructure
- **Human-readable debugging** - JSON payloads can be inspected with standard tools
- **Browser compatibility** - Can be called directly from web browsers
- **Simplified deployment** - No special gRPC infrastructure required
- **Better observability** - Standard HTTP status codes and headers

For more information, see the [Connect RPC Protocol Documentation](https://connectrpc.com/docs/protocol/).

## Dependencies

The project now includes both Connect RPC and legacy gRPC dependencies:

```toml
dependencies = [
    "connect-python>=0.4.2",  # Connect RPC client
    "grpcio>=1.74.0",         # Legacy gRPC (backward compatibility)
    "grpcio-tools>=1.74.0",   # Legacy gRPC tools
    # ... other dependencies
]
```

## Code Generation

### Connect RPC Generation (Recommended)

Use the new Connect RPC generation script:

```bash
cd proto-gen
uv run python scripts/generate_connect_proto.py
```

This generates:
- `*_connect.py` - Connect RPC clients (preferred)
- `*_pb2.py` - Standard protobuf classes
- `*_pb2.pyi` - Type stubs
- `legacy_grpc/*_pb2_grpc.py` - Legacy gRPC clients (backward compatibility)

### Legacy gRPC Generation

The old script still works for backward compatibility:

```bash
cd proto-gen
uv run python scripts/generate_proto.py
```

## Client Usage Examples

### Connect RPC Client (Recommended)

```python
import urllib3
from otdf_python_proto.policy_pb2 import GetPolicyRequest
from otdf_python_proto.policy_connect import PolicyServiceClient

# Create HTTP client
http_client = urllib3.PoolManager()

# Create Connect RPC client
policy_client = PolicyServiceClient(
    base_url="https://platform.opentdf.io",
    http_client=http_client
)

# Make unary RPC call
request = GetPolicyRequest(id="policy-123")
response = policy_client.get_policy(request)
print(f"Policy: {response}")

# With extra headers and timeout
response = policy_client.get_policy(
    request,
    extra_headers={"Authorization": "Bearer your-token"},
    timeout_seconds=30.0
)
```

### Async Connect RPC Client

```python
import aiohttp
from otdf_python_proto.policy_pb2 import ListPoliciesRequest
from otdf_python_proto.policy_connect import AsyncPolicyServiceClient

async def main():
    async with aiohttp.ClientSession() as http_client:
        policy_client = AsyncPolicyServiceClient(
            base_url="https://platform.opentdf.io",
            http_client=http_client
        )

        # Make async RPC call
        request = ListPoliciesRequest()
        response = await policy_client.list_policies(request)
        print(f"Policies: {response}")

        # Server streaming example
        async for policy in policy_client.stream_policies(request):
            print(f"Streaming policy: {policy}")
```

### Legacy gRPC Client (Backward Compatibility)

```python
import grpc
from otdf_python_proto.policy_pb2 import GetPolicyRequest
from otdf_python_proto.legacy_grpc.policy_pb2_grpc import PolicyServiceStub

# Create gRPC channel
channel = grpc.insecure_channel("platform.opentdf.io:443")
policy_client = PolicyServiceStub(channel)

# Make RPC call
request = GetPolicyRequest(id="policy-123")
response = policy_client.GetPolicy(request)
print(f"Policy: {response}")
```

## Error Handling

### Connect RPC Error Handling

```python
from connectrpc.errors import ConnectError

try:
    response = policy_client.get_policy(request)
except ConnectError as e:
    print(f"Connect error: {e.code} - {e.message}")
    # e.code can be: "not_found", "permission_denied", etc.
    # Full list: https://connectrpc.com/docs/protocol/#error-codes
```

### gRPC Error Handling

```python
import grpc

try:
    response = policy_client.GetPolicy(request)
except grpc.RpcError as e:
    print(f"gRPC error: {e.code()} - {e.details()}")
```

## Protocol Differences

| Feature | Connect RPC | gRPC |
|---------|-------------|------|
| Transport | HTTP/1.1, HTTP/2 | HTTP/2 only |
| Payload | JSON or Binary | Binary only |
| Status Codes | HTTP status codes | gRPC status codes |
| Headers | Standard HTTP headers | Custom gRPC headers |
| Browser Support | ✅ Yes | ❌ No (requires gRPC-Web) |
| Debugging | ✅ Human-readable | ❌ Binary format |
| Infrastructure | ✅ Standard HTTP | ❌ Requires gRPC support |

## Migration Checklist

- [ ] Update dependencies to include `connect-python`
- [ ] Regenerate proto files with Connect RPC support
- [ ] Update client code to use Connect RPC clients
- [ ] Update error handling for Connect error types
- [ ] Test with your authentication/authorization setup
- [ ] Update deployment configuration (if needed)
- [ ] Remove legacy gRPC dependencies (optional)

## Advanced Usage

### Custom HTTP Configuration

```python
import urllib3

# Configure HTTP client with custom settings
http_client = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=10.0, read=30.0),
    retries=urllib3.Retry(total=3, backoff_factor=0.3),
    headers={"User-Agent": "MyApp/1.0"}
)

policy_client = PolicyServiceClient(
    base_url="https://platform.opentdf.io",
    http_client=http_client
)
```

### Low-level API Access

```python
# Access response metadata
output = policy_client.call_get_policy(request)
response = output.message()
headers = output.response_headers()
trailers = output.response_trailers()

if output.error():
    raise output.error()
```

### Server Streaming

```python
# Server streaming RPC
request = StreamPoliciesRequest()
for policy in policy_client.stream_policies(request):
    print(f"Received policy: {policy.id}")

# With error handling
try:
    for policy in policy_client.stream_policies(request):
        process_policy(policy)
except ConnectError as e:
    print(f"Stream error: {e.code} - {e.message}")
```

## Troubleshooting

### Common Issues

1. **"buf command not found"**
   ```bash
   # Install buf
   brew install bufbuild/buf/buf
   # Or
   go install github.com/bufbuild/buf/cmd/buf@latest
   ```

2. **"protoc-gen-connect_python not found"**
   ```bash
   # Install with compiler support
   uv add connect-python[compiler]
   ```

3. **Import errors after generation**
   ```bash
   # Ensure __init__.py files exist
   find proto-gen/generated -type d -exec touch {}/__init__.py \;
   ```

4. **HTTP/2 server issues**
   - Connect RPC works with HTTP/1.1, so this is rarely an issue
   - If using streaming, ensure your server supports Connect protocol

### Debug HTTP Traffic

```python
import logging

# Enable HTTP debug logging
logging.basicConfig(level=logging.DEBUG)
urllib3.disable_warnings()

# You can now see all HTTP requests/responses
```

## Performance Considerations

- **HTTP/1.1**: Good for most use cases, supports connection pooling
- **JSON vs Binary**: Binary protobuf is more efficient, JSON is more debuggable
- **Connection Reuse**: Reuse `urllib3.PoolManager` instances across calls
- **Async**: Use async clients for high-concurrency applications

## Next Steps

1. **Start with unary RPCs**: Easiest to migrate and test
2. **Test authentication**: Ensure your auth tokens work with HTTP headers
3. **Migrate streaming RPCs**: More complex but follow similar patterns
4. **Remove gRPC dependencies**: Once fully migrated, clean up dependencies
5. **Update documentation**: Update your team's documentation and examples

For more information, see:
- [Connect RPC Documentation](https://connectrpc.com/docs/)
- [Connect Python Repository](https://github.com/connectrpc/connect-python)
- [OpenTDF Platform](https://github.com/opentdf/platform)
