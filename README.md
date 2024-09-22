# opentdf-python-sdk

Unofficial OpenTDF SDK for Python

[![Tests](https://github.com/b-long/opentdf-python-sdk/workflows/PyPIBuild/badge.svg)](https://github.com/b-long/opentdf-python-sdk/actions?query=workflow%3APyPIBuild)


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

Simple usage examples are given below.  In addition, see the content of `validate_otdf_python.py` .

### Example: Encrypt a string

```python
from otdf_python.gotdf_python import EncryptString

config: EncryptionConfig = _get_configuration()

tdf_manifest_json = EncryptString(inputText="Hello from Python", config=config)

```

### Example: Encrypt a file

```python
from otdf_python.gotdf_python import EncryptFile
from otdf_python.go import Slice_string

with tempfile.TemporaryDirectory() as tmpDir:
    print("Created temporary directory", tmpDir)

    da = Slice_string(["https://example.com/attr/attr1/value/value1", "https://example.com/attr/attr1/value/value2"])

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
        # DataAttributes=...
        DataAttributes=da,
    )

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
