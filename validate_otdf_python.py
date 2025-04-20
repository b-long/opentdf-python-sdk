"""
This file serves as a test of otdf_python.
"""

import tempfile
from pathlib import Path
from zipfile import is_zipfile
from os import environ

from otdf_python.gotdf_python import OpentdfConfig


def _get_configuration() -> OpentdfConfig:
    platformEndpoint = "localhost:8080"

    config: OpentdfConfig = OpentdfConfig(
        ClientId=environ.get("OPENTDF_CLIENT_ID", "opentdf-sdk"),
        ClientSecret=environ.get("OPENTDF_CLIENT_SECRET", "secret"),
        PlatformEndpoint=environ.get("OPENTDF_HOSTNAME", platformEndpoint),
        TokenEndpoint=environ.get(
            "OIDC_TOKEN_ENDPOINT",
            "http://localhost:8888/auth/realms/opentdf/protocol/openid-connect/token",
        ),
        KasUrl=environ.get("OPENTDF_KAS_URL", f"http://{platformEndpoint}/kas"),
    )

    # NOTE: Structs from golang can be printed, like below
    # This should print a string like
    #   gotdf_python.OpentdfConfig{ClientId=opentdf-sdk, ClientSecret=secret, KasUrl=http://localhost:8080/kas, PlatformEndpoint=localhost:8080, TokenEndpoint=http://localhost:8888/auth/realms/opentdf/protocol/openid-connect/token, handle=1}
    print(config)

    return config


def verify_encrypt_str() -> None:
    print("Validating string encryption")
    try:
        from otdf_python.gotdf_python import EncryptString

        config: OpentdfConfig = _get_configuration()

        from otdf_python.go import Slice_string

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
            authScopes=Slice_string(["email"]),
        )

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
                authScopes=Slice_string(["email"]),
            )

            print(f"The output file was written to destination path: {outputFilePath}")
            if not SOME_ENCRYPTED_FILE.exists():
                raise ValueError("The output file does not exist!")

            encrypted_file_size = SOME_ENCRYPTED_FILE.stat().st_size
            print(f"The encrypted file size is {encrypted_file_size}")

            if not (encrypted_file_size > 1500 and is_zipfile(SOME_ENCRYPTED_FILE)):
                raise ValueError("The output file has unexpected content!")

            # breakpoint()
    except Exception as e:
        raise RuntimeError("An unexpected error occurred testing otdf_python") from e


if __name__ == "__main__":
    print("Attempting string encryption")
    verify_encrypt_str()

    print("Attempting file encryption")
    verify_encrypt_file()

    print("All tests have passed 👍")
