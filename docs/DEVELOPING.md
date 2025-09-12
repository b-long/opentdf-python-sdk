# Developing the OpenTDF Python SDK

## Enabling Direct Access Grants

In order to use token exchange with direct access grants, you will need to enable the `Direct Access Grants` option in your IdP (e.g. Keycloak)
client settings.

## Setting Up Your Development Environment

A convenience script is provided to help set up your development environment with an OpenTDF platform running in docker.

You can run the following command in your terminal:

```bash
.github/start_opentdf_docker.sh
```

Using this script will automatically enable direct access grants in Keycloak for you.

## Dependency Management

### Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and task running.

#### Installing uv

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
git clone https://github.com/b-long/opentdf-python-sdk.git
cd opentdf-python-sdk
```

2. Install dependencies:
```bash
uv sync
```

### Running Tests

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


### Protobuf & Connect RPC Generation

This project uses a dedicated submodule, `otdf-python-proto/`, for generating Python protobuf files and Connect RPC clients from OpenTDF platform proto definitions.

#### Regenerating Protobuf & Connect RPC Files

From the submodule:
```bash
cd otdf-python-proto
uv run python scripts/generate_connect_proto.py
```

See [`otdf-python-proto/README.md`](../otdf-python-proto/README.md) and [`PROTOBUF_SETUP.md`](./PROTOBUF_SETUP.md) for details.
