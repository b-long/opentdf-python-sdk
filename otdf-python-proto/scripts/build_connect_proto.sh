#!/bin/bash

# Build Connect RPC protobuf files for OpenTDF Python SDK
# This script sets up the environment and generates Connect RPC clients

set -e

echo "OpenTDF Connect RPC Proto Builder"
echo "================================="

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTO_GEN_DIR="$(dirname "$SCRIPT_DIR")"

echo "Working in: $PROTO_GEN_DIR"

# Check if we're in the right directory
if [[ ! -f "$PROTO_GEN_DIR/buf.yaml" ]]; then
    echo "Error: buf.yaml not found. Are you in the proto-gen directory?"
    exit 1
fi

# Check for required tools
echo "Checking dependencies..."

if ! command -v buf &> /dev/null; then
    echo "Error: buf is not installed."
    echo "Install it with:"
    echo "  brew install bufbuild/buf/buf"
    echo "  # or"
    echo "  go install github.com/bufbuild/buf/cmd/buf@latest"
    exit 1
fi

echo "✓ buf is available"

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Install it with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv is available"

# Install dependencies if needed
echo "Installing/updating dependencies..."
cd "$PROTO_GEN_DIR"
uv sync --dev

# Check if connect-python is available
if ! uv run python -c "import connectrpc" 2>/dev/null; then
    echo "Installing connect-python[compiler]..."
    uv add "connect-python[compiler]>=0.4.2"
fi

echo "✓ connect-python is available"

# Clean up previous generated files
echo "Cleaning up previous generated files..."
if [[ -d "generated" ]]; then
    rm -rf generated/*
fi

# Create generated directory
mkdir -p generated

# Run the generation
echo "Generating Connect RPC protobuf files..."
uv run python scripts/generate_connect_proto.py "$@"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "✓ Connect RPC generation complete!"
    echo ""
    echo "Generated files:"
    echo "  - generated/*_pb2.py      (Protobuf message classes)"
    echo "  - generated/*_pb2.pyi     (Type stubs)"
    echo "  - generated/*_connect.py  (Connect RPC clients)"
    echo ""
    echo "Legacy gRPC files (if generated):"
    echo "  - generated/legacy_grpc/*_pb2_grpc.py (gRPC stubs)"
    echo ""
    echo "Usage examples:"
    echo "  cd .."
    echo "  python examples/connect_rpc_client_example.py"
    echo ""
    echo "For more information, see:"
    echo "  - docs/CONNECT_RPC.md"
    echo "  - https://connectrpc.com/docs/"
else
    echo "✗ Connect RPC generation failed!"
    exit 1
fi
