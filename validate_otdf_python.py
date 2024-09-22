"""
This file serves as a test of otdf_python.
"""

import tempfile
from pathlib import Path
from zipfile import is_zipfile

from otdf_python.gotdf_python import EncryptionConfig

SOME_PLAINTEXT_FILE = Path(__file__).parent / "go.mod"


def verify_hello():
    from otdf_python.gotdf_python import Hello

    # Prints a basic str value: 'Hello, world'
    print(Hello())


def _get_configuration() -> EncryptionConfig:
    platformEndpoint = "localhost:8080"

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
    )

    # NOTE: Structs from golang can be printed, like below
    # This should print a string like
    #   gotdf_python.EncryptionConfig{ClientId=opentdf-sdk, ClientSecret=secret, KasUrl=http://localhost:8080/kas, PlatformEndpoint=localhost:8080, TokenEndpoint=http://localhost:8888/auth/realms/opentdf/protocol/openid-connect/token, handle=1}
    print(config)

    return config


def verify_encrypt_str() -> None:
    print("Validating string encryption")
    try:
        from otdf_python.gotdf_python import EncryptString

        config: EncryptionConfig = _get_configuration()

        tdf_manifest_json = EncryptString(inputText="Hello from Python", config=config)

        print(tdf_manifest_json)
        # breakpoint()
    except Exception as e:
        raise RuntimeError("An unexpected error occurred testing otdf_python") from e


def verify_encrypt_file() -> None:
    print("Validating file encryption")
    try:
        from otdf_python.gotdf_python import EncryptFile

        with tempfile.TemporaryDirectory() as tmpDir:
            print("Created temporary directory", tmpDir)

            config: EncryptionConfig = _get_configuration()

            SOME_ENCRYPTED_FILE = Path(tmpDir) / "some-file.tdf"

            if SOME_ENCRYPTED_FILE.exists():
                SOME_ENCRYPTED_FILE.unlink()

            if SOME_ENCRYPTED_FILE.exists():
                raise ValueError(
                    "The output path should not exist before calling 'EncryptFile()'."
                )

            outputFilePath = EncryptFile(
                inputFilePath=str(SOME_PLAINTEXT_FILE),
                outputFilePath=str(SOME_ENCRYPTED_FILE),
                config=config,
            )

            print(f"The output file was written to destination path: {outputFilePath}")
            if not SOME_ENCRYPTED_FILE.exists():
                raise ValueError("The output file does not exist!")

            if not (
                SOME_ENCRYPTED_FILE.stat().st_size > 2500
                and is_zipfile(SOME_ENCRYPTED_FILE)
            ):
                raise ValueError("The output file has unexpected content!")

            # breakpoint()
    except Exception as e:
        raise RuntimeError("An unexpected error occurred testing otdf_python") from e


if __name__ == "__main__":
    print("Attempting 'Hello, world'")
    verify_hello()

    print("Attempting string encryption")
    verify_encrypt_str()

    print("Attempting file encryption")
    verify_encrypt_file()

    print("All tests have passed 👍")
