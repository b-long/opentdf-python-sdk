# OpenTDF Python SDK

Unofficial OpenTDF SDK for Python


## Features

- **TDF Encryption/Decryption**: Create and decrypt TDF files with policy-based access control
- **Flexible Configuration**: Support for various authentication methods and platform endpoints
- **Comprehensive Testing**: Full test suite with unit and integration tests

## Legacy Version

A legacy version (0.2.x) of this project is available for users who need the previous implementation. For more information, see [LEGACY_VERSION.md](docs/LEGACY_VERSION.md) or visit the [legacy branch on GitHub](https://github.com/b-long/opentdf-python-sdk/tree/0.2.x).

## Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and task running.

### Installing uv

Install `uv` using one of the following methods:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using Homebrew (macOS):**
```bash
brew install uv
```

For more installation options, see the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd opentdf-python-sdk
```

2. Install dependencies:
```bash
uv sync
```

## Running Tests

Run the full test suite:
```bash
uv run pytest tests/
```

Run specific test files:
```bash
uv run pytest tests/test_sdk.py
```

Run tests with verbose output:
```bash
uv run pytest tests/ -v
```

Run integration tests only:
```bash
uv run pytest tests/ -m integration
```

## Installation

Install from PyPI:
```bash
pip install otdf-python
```


## Protobuf & Connect RPC Generation

This project uses a dedicated submodule, `otdf-python-proto/`, for generating Python protobuf files and Connect RPC clients from OpenTDF platform proto definitions.

### Regenerating Protobuf & Connect RPC Files

From the submodule:
```bash
cd otdf-python-proto
uv run python scripts/generate_connect_proto.py
```

See [`otdf-python-proto/README.md`](otdf-python-proto/README.md) and [`PROTOBUF_SETUP.md`](PROTOBUF_SETUP.md) for details.

## Quick Start

### Basic Configuration

```python
from otdf_python.sdk_builder import SDKBuilder

# Create and configure SDK using builder pattern
builder = SDKBuilder()
builder.set_platform_endpoint("https://platform.example.com")
builder.client_secret("your-client-id", "your-client-secret")

# Build the SDK instance
sdk = builder.build()
```

### Advanced Configuration

```python
from otdf_python.sdk_builder import SDKBuilder

# Create SDK with additional configuration options
builder = SDKBuilder()
builder.set_platform_endpoint("https://platform.example.com")
builder.set_issuer_endpoint("https://auth.example.com")
builder.client_secret("your-client-id", "your-client-secret")

# Examples, for local development

# Use HTTP instead of HTTPS
builder.use_insecure_plaintext_connection(True)

# Or
# Skip TLS verification
builder.use_insecure_skip_verify(True)

# Build the SDK instance
sdk = builder.build()
```

### Encrypt Data

```python
from io import BytesIO

# Create TDF configuration with attributes
config = sdk.new_tdf_config(attributes=["https://example.com/attr/classification/value/public"])

# Encrypt data to TDF format
input_data = b"Hello, World!"
output_stream = BytesIO()
manifest, size, _ = sdk.create_tdf(BytesIO(input_data), config, output_stream)
encrypted_data = output_stream.getvalue()

# Save encrypted data to file
with open("encrypted.tdf", "wb") as f:
    f.write(encrypted_data)
```

### Decrypt Data

```python
from otdf_python.tdf import TDFReaderConfig

# Read encrypted TDF file
with open("encrypted.tdf", "rb") as f:
    encrypted_data = f.read()

# Decrypt TDF
reader_config = TDFReaderConfig()
tdf_reader = sdk.load_tdf(encrypted_data, reader_config)
decrypted_data = tdf_reader.payload

# Save decrypted data
with open("decrypted.txt", "wb") as f:
    f.write(decrypted_data)

# Don't forget to close the SDK when done
sdk.close()
```

## Project Structure

```
src/otdf_python/
├── sdk.py                  # Main SDK interface
├── config.py               # Configuration management
├── tdf.py                  # TDF format handling
├── nanotdf.py              # NanoTDF format handling
├── crypto_utils.py         # Cryptographic utilities
├── kas_client.py           # Key Access Service client
└── ...                     # Additional modules
tests/
└── ...                     # Various tests

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `uv run pytest tests/`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Release Process

For maintainers and contributors working on releases:
- See [RELEASES.md](RELEASES.md) for comprehensive release documentation
- Feature branch alpha releases available for testing changes before merge
- Automated releases via Release Please on the main branch

## License

This project is licensed under the MIT License - see the LICENSE file for details.
