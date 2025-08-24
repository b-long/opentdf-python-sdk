# OpenTDF Python SDK - Protobuf Generation Sub-Module

This document explains the protobuf generation sub-module that was created for the OpenTDF Python SDK project.

## Overview

A dedicated sub-module (`proto-gen/`) has been created to handle downloading and generating protobuf files from the OpenTDF platform. This provides a clean separation of concerns and makes it easy to update protobuf definitions.

## Structure

```
opentdf-python-sdk.rewrite/
├── proto-gen/                     # Protobuf generation sub-module
│   ├── pyproject.toml             # Sub-module dependencies
│   ├── README.md                  # Sub-module documentation
│   ├── proto-files/               # Raw .proto files
│   │   ├── kas.proto             # Downloaded from OpenTDF platform
│   │   └── kas_simplified.proto   # Simplified version (auto-generated)
│   ├── generated/                 # Generated Python files
│   │   ├── __init__.py
│   │   ├── kas_pb2.py            # Generated protobuf classes
│   │   └── kas_pb2_grpc.py       # Generated gRPC service stubs
│   └── scripts/
│       ├── generate_proto.py     # Python script to generate protobuf files
│       └── build_proto.sh        # Shell script wrapper
├── scripts/
│   └── update-proto.sh           # Convenience script to regenerate and sync
├── uv.toml                       # UV workspace configuration
└── pyproject.toml                # Main project (includes proto dependency)
```

## What Was Accomplished

### 1. Downloaded Proto File ✅
- Downloaded the latest `kas.proto` file from: `https://raw.githubusercontent.com/opentdf/platform/refs/tags/service/v0.8.0/service/kas/kas.proto`
- Stored in `proto-gen/proto-files/kas.proto`

### 2. Built Usable Library ✅
- Created a robust protobuf generation system using `uv run python -m grpc_tools.protoc`
- Handles dependency issues gracefully with fallback generation
- Generates both protobuf classes (`kas_pb2.py`) and gRPC service stubs (`kas_pb2_grpc.py`)

## Key Features

### Smart Dependency Handling
- Automatically detects and uses `googleapis-common-protos` when available
- Falls back to a simplified proto definition when external dependencies are missing
- Handles import issues gracefully

### Multiple Ways to Generate
1. **Python script**: `uv run python scripts/generate_proto.py`
2. **Shell script**: `./scripts/build_proto.sh`
3. **Convenience script**: `./scripts/update-proto.sh` (from main project)

### Workspace Integration
- Uses UV workspace configuration to link the sub-module
- Main project depends on `otdf-python-proto` for the generated files
- Automatic syncing of generated files to the main project's proto directory

## Usage

### Regenerate Protobuf Files

From the main project root:
```bash
./scripts/update-proto.sh
```

From the proto-gen sub-module:
```bash
cd proto-gen
uv run python scripts/generate_proto.py
```

### Update Proto Definition

1. Download the latest proto file:
```bash
curl -o proto-gen/proto-files/kas.proto https://raw.githubusercontent.com/opentdf/platform/refs/tags/service/v0.8.0/service/kas/kas.proto
```

2. Regenerate the Python files:
```bash
./scripts/update-proto.sh
```

## Dependencies

The otdf-python-proto sub-module includes these dependencies:
- `grpcio>=1.74.0` - gRPC runtime
- `grpcio-tools>=1.74.0` - Protocol buffer compiler
- `protobuf>=6.31.1` - Protocol buffer runtime
- `googleapis-common-protos>=1.66.0` - Google API common proto definitions

## Final Status ✅

The protobuf sub-module has been successfully implemented and tested:

### ✅ Completed Tasks
1. **Downloaded proto file** from OpenTDF platform (service/v0.8.0)
2. **Built usable library** with `uv run python -m grpc_tools.protoc`
3. **Generated working Python files** (`kas_pb2.py`, `kas_pb2_grpc.py`)
4. **Verified imports and functionality** - all message types are accessible
5. **Created automated build scripts** for easy regeneration
6. **Integrated with main project** via file syncing

### ✅ Verified Working Features
- ✅ Import: `from otdf_python.proto import kas_pb2, kas_pb2_grpc`
- ✅ Message creation: `req = kas_pb2.RewrapRequest()`
- ✅ gRPC service stubs: `kas_pb2_grpc.AccessServiceStub`
- ✅ All core message types: `RewrapRequest`, `RewrapResponse`, `InfoRequest`, etc.

### Test Results
```bash
Successfully imported protobuf files
Found 35 symbols in kas_pb2
Found 19 symbols in kas_pb2_grpc
Available message types:
- RewrapRequest: True
- RewrapResponse: True
- AccessService: True
Created request with token: test
```

## Generated Files

The generated Python files include:
- **`kas_pb2.py`** - Protocol buffer message classes
- **`kas_pb2_grpc.py`** - gRPC service client and server classes

These files are automatically synced to `otdf-python-proto/generated/` and used by the main project in `src/otdf_python/`.

## Fallback Strategy

When the original proto file has missing dependencies (like Google API annotations), the system automatically creates a simplified version that includes all the core message types and services but removes problematic imports. This ensures the build always succeeds and provides usable protobuf classes.
