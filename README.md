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
pip install otdf-python==0.0.9

# Install a pinned version, from test.pypi.org
pip install -i https://test.pypi.org/simple/ otdf-python==0.0.9
```

## Usage

Simple usage examples are given below.  In addition, we recommend you also:

1. See the contents of [`main.go` on Github](https://github.com/b-long/opentdf-python-sdk/blob/main/main.go).  ✨ Note that all Upper-case functions are available in Python.
1. See the contents of [`validate_otdf_python.py` on Github](https://github.com/b-long/opentdf-python-sdk/blob/main/validate_otdf_python.py).

### Example: Configuration

Creating a helper function may simplify the usage of `otdf-python`.

For example:

```python
def get_encrypt_config(data_attributes: list | None = None):
    """
    The config object returned here can only be used for encryption.

    While 'otdf_python.gotdf_python' internally can use golang interfaces,
     to normalize config objects, that pattern causes a panic
     when used from Python.

    """
    print("Preparing 'EncryptionConfig' object")
    from otdf_python.gotdf_python import EncryptionConfig
    from otdf_python.go import Slice_string

    if isinstance(data_attributes, list):
        # Create config using the attributes from the caller
        da = Slice_string(data_attributes)
        config: EncryptionConfig = EncryptionConfig(
            ClientId="opentdf-sdk",
            ClientSecret="secret",
            PlatformEndpoint=platformEndpoint,
            TokenEndpoint="http://localhost:8888/auth/realms/opentdf/protocol/openid-connect/token",
            KasUrl=f"http://{platformEndpoint}/kas",
            # FIXME: Be careful with binding the 'DataAttributes' field on this struct.
            #
            # In golang, this is initialized as []string , but passing
            # DataAttributes=None, or DataAttributes=[] from Python will fail.
            DataAttributes=da,
        )
    else:
        # Create config without attributes
        config: EncryptionConfig = EncryptionConfig(
            ClientId=testing_credentials.TDF_NPE_CLIENT,
            ClientSecret=testing_credentials.TDF_NPE_CLIENT_SECRET,
            PlatformEndpoint=testing_credentials.PLATFORM_ENDPOINT,
            TokenEndpoint=testing_credentials.OIDC_AUTH_URL,
            KasUrl=testing_credentials.KAS_URL,
        )

    # NOTE: Structs from golang can be printed, like below
    # print(config)
    print("Returning 'EncryptionConfig'")

    return config
```


### Example: Encrypt a string

```python
from otdf_python.gotdf_python import EncryptString

# Depends on the 'get_encrypt_config()' given
# in the README above
config: EncryptionConfig = get_encrypt_config()

tdf_manifest_json = EncryptString(inputText="Hello from Python", config=config)
```

### Example: Encrypt a file

```python
from otdf_python.gotdf_python import EncryptFile
from otdf_python.go import Slice_string

# Depends on the 'get_encrypt_config()' given
# in the README above
config: EncryptionConfig = get_encrypt_config()

with tempfile.TemporaryDirectory() as tmpDir:
    print("Created temporary directory", tmpDir)

    da = Slice_string(["https://example.com/attr/attr1/value/value1", "https://example.com/attr/attr1/value/value2"])

    encrypted_file = Path(tmpDir) / "some-file.tdf"

    if encrypted_file.exists():
        encrypted_file.unlink()

    if encrypted_file.exists():
        raise ValueError(
            "The output path should not exist before calling 'EncryptFile()'."
        )

    outputFilePath = EncryptFile(
        inputFilePath=str(SOME_PLAINTEXT_FILE),
        outputFilePath=str(encrypted_file),
        config=config,
    )

    print(f"The output file was written to destination path: {outputFilePath}")

```
