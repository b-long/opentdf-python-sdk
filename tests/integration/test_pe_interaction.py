"""Integration test: Single attribute encryption/decryption using SDK and otdfctl"""

import logging
import tempfile
from pathlib import Path

import pytest

from otdf_python.sdk import SDK
from otdf_python.sdk_exceptions import SDKException
from tests.config_pydantic import CONFIG_TDF
from tests.integration.support_sdk import get_sdk_for_pe

# Test files (adjust paths as needed)
DECRYPTED_FILE_OTDFCTL = "decrypted_otdfctl.txt"

_test_attributes = [CONFIG_TDF.TEST_OPENTDF_ATTRIBUTE_1]
logger = logging.getLogger(__name__)


def decrypt(input_path: Path, output_path: Path, sdk: SDK):
    # Determine output
    with input_path.open("rb") as infile, output_path.open("wb") as outfile:
        try:
            logger.debug("Decrypting TDF")
            tdf_reader = sdk.load_tdf(infile.read())
            # Access payload directly from TDFReader
            payload_bytes = tdf_reader.payload
            outfile.write(payload_bytes)
            logger.info("Successfully decrypted TDF")

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            # Clean up the output file if there was an error
            output_path.unlink(missing_ok=True)
            raise SDKException("Decryption failed") from e


@pytest.mark.integration
def test_single_attribute_encryption_decryption():
    # Encrypt with SDK using a single attribute
    sdk = get_sdk_for_pe()

    with tempfile.TemporaryDirectory() as tmpDir:
        print("Created temporary directory", tmpDir)
        some_plaintext_file = Path(tmpDir) / "new-file.txt"
        some_plaintext_file.write_text("Hello world")

        INPUT_FILE = some_plaintext_file

        config = sdk.new_tdf_config(
            attributes=_test_attributes,
        )

        input_path = Path(INPUT_FILE)

        output_path = input_path.with_suffix(input_path.suffix + ".tdf")
        with input_path.open("rb") as infile, output_path.open("wb") as outfile:
            sdk.create_tdf(infile.read(), config, output_stream=outfile)

        TDF_FILE = output_path

        assert TDF_FILE.exists()

        # Decrypt with SDK
        DECRYPTED_FILE_SDK = Path(tmpDir) / "decrypted.txt"
        DECRYPTED_FILE_SDK.touch()  # Ensure the file exists

        decrypt(TDF_FILE, DECRYPTED_FILE_SDK, sdk)
        with INPUT_FILE.open("rb") as f1, DECRYPTED_FILE_SDK.open("rb") as f2:
            assert f1.read() == f2.read(), "SDK decrypted output does not match input"

        # # Decrypt with otdfctl
        # otdfctl_cmd = [
        #     "otdfctl",
        #     "decrypt",
        #     "--kas-url",
        #     kas_info["url"],
        #     "--kas-public-key",
        #     kas_info["public_key"],
        #     "--kas-token",
        #     kas_info["token"],
        #     "--attribute",
        #     _test_attributes,
        #     "-i",
        #     TDF_FILE,
        #     "-o",
        #     DECRYPTED_FILE_OTDFCTL,
        # ]
        # subprocess.run(otdfctl_cmd, check=True)
        # with open(INPUT_FILE, "rb") as f1, open(DECRYPTED_FILE_OTDFCTL, "rb") as f2:
        #     assert f1.read() == f2.read(), (
        #         "otdfctl decrypted output does not match input"
        #     )
