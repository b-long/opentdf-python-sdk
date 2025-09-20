# OpenTDF Python Proto Generator

This sub-module is responsible for generating Python protobuf files and Connect RPC clients from the OpenTDF platform proto definitions.

## What's New: Connect RPC Support

This project now supports **Connect RPC**, a modern HTTP-friendly alternative to gRPC that provides:

- 🌐 **HTTP/1.1 compatibility** - Works with all HTTP infrastructure
- 🔍 **Human-readable debugging** - JSON payloads can be inspected with standard tools
- 🌍 **Browser compatibility** - Can be called directly from web browsers
- 🚀 **Simplified deployment** - No special gRPC infrastructure required
- 📊 **Better observability** - Standard HTTP status codes and headers

See [CONNECT_RPC.md](../docs/CONNECT_RPC.md) for additional information.

## Structure

- `proto-files/`: Contains the raw .proto files downloaded from the OpenTDF platform
- `src/otdf_python_proto/`: Contains the generated Python protobuf and Connect RPC client files
- `scripts/`: Contains build scripts for generating protobuf and Connect RPC files
- `buf.yaml`: Buf configuration for proto validation and management
- `buf.gen.yaml`: Buf generation configuration for Connect RPC and protobuf

## Usage

### Connect RPC Generation (Recommended)

To generate Connect RPC clients and protobuf files:

```bash
cd otdf-python-proto
uv run python scripts/generate_connect_proto.py
```

Or use the convenience script:

```bash
./scripts/build_connect_proto.sh
```

This generates:
- `src/otdf_python_proto/**/*_connect.py` - Connect RPC clients (preferred)
- `src/otdf_python_proto/**/*_pb2.py` - Standard protobuf classes
- `src/otdf_python_proto/**/*_pb2.pyi` - Type stubs for better IDE support
- `src/otdf_python_proto/legacy_grpc/**/*_pb2_grpc.py` - Legacy gRPC clients (backward compatibility)

### Legacy gRPC Generation

To generate traditional gRPC clients (backward compatibility):

```bash
cd otdf-python-proto
uv run python scripts/generate_proto.py
```

Or use the legacy script:

```bash
./scripts/build_proto.sh
```

### Download Fresh Proto Files

To download the latest proto files from OpenTDF platform:

```bash
cd otdf-python-proto
uv run python scripts/generate_connect_proto.py --download
```

## Dependencies

The generated files depend on:

### Connect RPC (Recommended)
- `connect-python[compiler]>=0.4.2` - Connect RPC client and code generator
- `protobuf>=6.31.1` - Protocol Buffers
- `googleapis-common-protos>=1.66.0` - Google API annotations
- `urllib3` or `aiohttp` - HTTP client (for Connect RPC)

### Legacy gRPC (Backward Compatibility)
- `grpcio>=1.74.0` - gRPC runtime
- `grpcio-tools>=1.74.0` - gRPC code generation tools
- `protobuf>=6.31.1` - Protocol Buffers
- `googleapis-common-protos>=1.66.0` - Google API annotations

## Examples

### Connect RPC Client Usage

```python
import urllib3
from otdf_python_proto.policy_pb2 import GetPolicyRequest
from otdf_python_proto.policy_connect import PolicyServiceClient

# Create HTTP client
http_client = urllib3.PoolManager()

# Create Connect RPC client
client = PolicyServiceClient(
    base_url="https://platform.opentdf.io",
    http_client=http_client
)

# Make RPC call
request = GetPolicyRequest(id="policy-123")
response = client.get_policy(
    request,
    extra_headers={"Authorization": "Bearer your-token"},
    timeout_seconds=30.0
)
```

### Async Connect RPC Client

```python
import aiohttp
from otdf_python_proto.policy_connect import AsyncPolicyServiceClient

async with aiohttp.ClientSession() as session:
    client = AsyncPolicyServiceClient(
        base_url="https://platform.opentdf.io",
        http_client=session
    )

    response = await client.get_policy(request)
```

### Legacy gRPC Client

```python
import grpc
from otdf_python_proto.legacy_grpc.policy_pb2_grpc import PolicyServiceStub

channel = grpc.insecure_channel("platform.opentdf.io:443")
client = PolicyServiceStub(channel)
response = client.GetPolicy(request)
```

## Tool Requirements

- **buf** - Protocol buffer management and generation
  ```bash
  # macOS
  brew install bufbuild/buf/buf

  # Or with Go
  go install github.com/bufbuild/buf/cmd/buf@latest
  ```

- **uv** - Python package management
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## Migration from gRPC

If you're migrating from traditional gRPC clients to Connect RPC:

1. Read the [Connect RPC Migration Guide](../docs/CONNECT_RPC.md)
2. Run the Connect RPC generation: `./scripts/build_connect_proto.sh` (or from the submodule: `cd otdf-python-proto && uv run python scripts/generate_connect_proto.py`)
3. Update your client code to use `*_connect.py` modules
4. Test with your authentication and deployment setup
5. Optionally remove legacy gRPC dependencies

## Troubleshooting

### "buf command not found"
Install buf: `brew install bufbuild/buf/buf`

### "protoc-gen-connect_python not found"
Install with compiler support: `uv add connect-python[compiler]`

### Import errors after generation
Ensure `__init__.py` files exist in otdf_python_proto directories

### Protocol version mismatches
Regenerate with latest proto files: `uv run python scripts/generate_connect_proto.py --download`

## Learn More

- [Connect RPC Documentation](https://connectrpc.com/docs/)
- [Connect Python Repository](https://github.com/connectrpc/connect-python)
- [OpenTDF Platform](https://github.com/opentdf/platform)
- [Buf Documentation](https://buf.build/docs/)
