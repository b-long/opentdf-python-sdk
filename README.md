# OpenTDF Python SDK

Unofficial OpenTDF SDK for Python


## Features

- **TDF Encryption/Decryption**: Create and decrypt TDF files with policy-based access control
- **Flexible Configuration**: Support for various authentication methods and platform endpoints
- **Comprehensive Testing**: Full test suite with unit and integration tests

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

## Quick Start

### Basic Configuration

```python
from otdf_python.config import Config
from otdf_python.sdk import SDK

# Create configuration
config = Config(
    platform_endpoint="https://platform.example.com",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Initialize SDK
sdk = SDK(config)
```

### Encrypt Data

```python
# Encrypt a string
encrypted_data = sdk.encrypt_string(
    data="Hello, World!",
    attributes=["https://example.com/attr/classification/value/public"]
)

# Encrypt a file
sdk.encrypt_file(
    input_path="plaintext.txt",
    output_path="encrypted.tdf"
)
```

### Decrypt Data

```python
# Decrypt to string
decrypted_text = sdk.decrypt_string(encrypted_data)

# Decrypt a file
sdk.decrypt_file(
    input_path="encrypted.tdf",
    output_path="decrypted.txt"
)
```

## Project Structure

```
src/otdf_python/
├── __init__.py              # Package initialization
├── sdk.py                   # Main SDK interface
├── config.py               # Configuration management
├── tdf.py                  # TDF format handling
├── nanotdf.py              # NanoTDF format handling
├── crypto_utils.py         # Cryptographic utilities
├── kas_client.py           # Key Access Service client
└── ...                     # Additional modules

tests/
├── test_sdk.py             # SDK tests
├── test_config.py          # Configuration tests
├── test_tdf.py            # TDF format tests
└── ...                    # Additional test files
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `uv run pytest tests/`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
