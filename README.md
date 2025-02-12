# opentdf-python-sdk

Unofficial OpenTDF SDK for Python

[![Tests](https://github.com/b-long/opentdf-python-sdk/workflows/PyPIBuild/badge.svg)](https://github.com/b-long/opentdf-python-sdk/actions?query=workflow%3APyPIBuild)

This project is powered by gopy, which generates (and compiles) a CPython extension module from a go package.  The `gopy`
tool unlocks performance, flexibility, and excellent Developer Experience to Python end-users.  Read more about
[`gopy` on Github](https://github.com/go-python/gopy).

## Adding features

If you wish to expand the functionality of `otdf-python`:

1. Create a fork/branch
1. Add new capabilities (e.g. in `main.go`)
1. Add a test (e.g. in `otdf_python_test.go`)
1. Commit your changes, push, and open a Pull Request via
the Github project: https://github.com/b-long/opentdf-python-sdk

## Installation

Install from the [Python Package Index (PyPI)](https://pypi.org):

```bash
# Install the latest from pypi.org
pip install otdf_python

# Install a pinned version
pip install otdf-python==0.2.9

# Install a pinned version, from test.pypi.org
pip install -i https://test.pypi.org/simple/ otdf-python==0.2.9
```

## Usage

Simple usage examples are given below.  In addition, we recommend you also:

1. See the contents of [`main.go` on Github](https://github.com/b-long/opentdf-python-sdk/blob/main/main.go).  ✨ Note that all Upper-case functions are available in Python.
1. See the contents of [`validate_otdf_python.py` on Github](https://github.com/b-long/opentdf-python-sdk/blob/main/validate_otdf_python.py).

### Example: Configuration

Creating a helper function may simplify the usage of `otdf-python`.

For example:

```python
def _get_configuration() -> OpentdfConfig:
    """
    The config returned is used for both encryption and decryption.
    """
    print("Preparing 'OpentdfConfig' object")
    from otdf_python.gotdf_python import OpentdfConfig

    platformEndpoint = "platform.opentdf.local"
    keycloakEndpoint = "keycloak.opentdf.local/auth

    # Create config
    config: OpentdfConfig = OpentdfConfig(
        ClientId="opentdf-sdk",
        ClientSecret="secret",
        PlatformEndpoint=platformEndpoint,
        TokenEndpoint=f"http://{keycloakEndpoint}/realms/opentdf/protocol/openid-connect/token",
        KasUrl=f"http://{platformEndpoint}/kas",
    )

    # NOTE: Structs from golang can be printed, like below
    # print(config)
    print("Returning 'OpentdfConfig'")

    return config
```


### Example: Encrypt a string

```python
from otdf_python.gotdf_python import EncryptString
from otdf_python.go import Slice_string

# Depends on the '_get_opentdf_config()' given
# in the README above
config: OpentdfConfig = _get_opentdf_config()

# da = Slice_string(
#     [
#         "https://example.com/attr/attr1/value/value1",
#         "https://example.com/attr/attr1/value/value2",
#     ]
# )
da = Slice_string([])

tdf_manifest_json = EncryptString(
    inputText="Hello from Python",
    config=config,
    dataAttributes=da,
)
```

### Example: Encrypt a file

```python
from otdf_python.gotdf_python import EncryptFile
from otdf_python.go import Slice_string

# Depends on the '_get_opentdf_config()' given
# in the README above
config: OpentdfConfig = _get_opentdf_config()

with tempfile.TemporaryDirectory() as tmpDir:
    print("Created temporary directory", tmpDir)

    config: OpentdfConfig = _get_configuration()

    SOME_ENCRYPTED_FILE = Path(tmpDir) / "some-file.tdf"

    if SOME_ENCRYPTED_FILE.exists():
        SOME_ENCRYPTED_FILE.unlink()

    if SOME_ENCRYPTED_FILE.exists():
        raise ValueError(
            "The output path should not exist before calling 'EncryptFile()'."
        )

    SOME_PLAINTEXT_FILE = Path(tmpDir) / "new-file.txt"
    SOME_PLAINTEXT_FILE.write_text("Hello world")

    from otdf_python.go import Slice_string

    # da = Slice_string(
    #     [
    #         "https://example.com/attr/attr1/value/value1",
    #         "https://example.com/attr/attr1/value/value2",
    #     ]
    # )
    da = Slice_string([])
    outputFilePath = EncryptFile(
        inputFilePath=str(SOME_PLAINTEXT_FILE),
        outputFilePath=str(SOME_ENCRYPTED_FILE),
        config=config,
        dataAttributes=da,
    )

    print(f"The output file was written to destination path: {outputFilePath}")

```

### Example: Decrypt a file

```python
from otdf_python.gotdf_python import EncryptFile
from otdf_python.go import Slice_string

# Depends on the '_get_opentdf_config()' given
# in the README above
config: OpentdfConfig = _get_opentdf_config()

def decrypt_file(input_file_path: Path, output_file_path: Path) -> Path:
    if output_file_path.exists():
        output_file_path.unlink()

    if output_file_path.exists():
        raise ValueError(
            "The output path should not exist before calling 'DecryptFile()'."
        )

    outputFilePath = DecryptFile(
        inputFilePath=str(input_file_path),
        outputFilePath=str(output_file_path),
        config=config,
    )

    output = Path(outputFilePath)
    if not output.exists():
        raise ValueError("DecryptFile() did not create the output file")

    return output
```
