"""TDFReader is responsible for reading and processing Trusted Data Format (TDF) files."""

from .manifest import Manifest
from .policy_object import PolicyObject
from .sdk_exceptions import SDKException
from .zip_reader import ZipReader

# Constants from TDFWriter
TDF_MANIFEST_FILE_NAME = "0.manifest.json"
TDF_PAYLOAD_FILE_NAME = "0.payload"


class TDFReader:
    """TDFReader is responsible for reading and processing Trusted Data Format (TDF) files.
    The class initializes with a TDF file channel, extracts the manifest and payload entries,
    and provides methods to retrieve the manifest content, read payload bytes, and read policy objects.
    """

    def __init__(self, tdf):
        """Initialize a TDFReader with a TDF file channel.

        Args:
            tdf: A file-like object containing the TDF data

        Raises:
            SDKException: If there's an error reading the TDF
            ValueError: If the TDF doesn't contain a manifest or payload

        """
        try:
            self._zip_reader = ZipReader(tdf)
            namelist = self._zip_reader.namelist()

            if TDF_MANIFEST_FILE_NAME not in namelist:
                raise ValueError("tdf doesn't contain a manifest")
            if TDF_PAYLOAD_FILE_NAME not in namelist:
                raise ValueError("tdf doesn't contain a payload")

            # Store the names for later use
            self._manifest_name = TDF_MANIFEST_FILE_NAME
            self._payload_name = TDF_PAYLOAD_FILE_NAME
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise SDKException("Error initializing TDFReader") from e

    def manifest(self) -> str:
        """Get the manifest content as a string.

        Returns:
            The manifest content as a UTF-8 encoded string

        Raises:
            SDKException: If there's an error retrieving the manifest

        """
        try:
            manifest_data = self._zip_reader.read(self._manifest_name)
            return manifest_data.decode("utf-8")
        except Exception as e:
            raise SDKException("Error retrieving manifest from zip file") from e

    def read_payload_bytes(self, buf: bytearray) -> int:
        """Read bytes from the payload into a buffer.

        Args:
            buf: A bytearray buffer to read into

        Returns:
            The number of bytes read

        Raises:
            SDKException: If there's an error reading from the payload

        """
        try:
            # Read the entire payload
            payload_data = self._zip_reader.read(self._payload_name)

            # Copy to the buffer
            to_copy = min(len(buf), len(payload_data))
            buf[:to_copy] = payload_data[:to_copy]

            return to_copy
        except Exception as e:
            raise SDKException("Error reading from payload in TDF") from e

    def read_policy_object(self) -> PolicyObject:
        """Read the policy object from the manifest.

        Returns:
            The PolicyObject

        Raises:
            SDKException: If there's an error reading the policy object

        """
        try:
            manifest_text = self.manifest()
            manifest = Manifest.from_json(manifest_text)

            # Decode the base64 policy from the manifest
            if (
                not manifest.encryptionInformation
                or not manifest.encryptionInformation.policy
            ):
                raise SDKException("No policy found in manifest")

            import base64
            import json

            policy_base64 = manifest.encryptionInformation.policy
            policy_bytes = base64.b64decode(policy_base64)
            policy_json = policy_bytes.decode("utf-8")
            policy_data = json.loads(policy_json)

            # Convert to PolicyObject
            from otdf_python.policy_object import (
                AttributeObject,
                PolicyBody,
                PolicyObject,
            )

            # Parse data attributes - handle case where body might be None or have None values
            body_data = policy_data.get("body") or {}
            data_attributes = []

            # Handle case where dataAttributes is None
            attrs_data = body_data.get("dataAttributes") or []
            for attr_data in attrs_data:
                attr_obj = AttributeObject(
                    attribute=attr_data["attribute"],
                    display_name=attr_data.get("displayName"),
                    is_default=attr_data.get("isDefault", False),
                    pub_key=attr_data.get("pubKey"),
                    kas_url=attr_data.get("kasUrl"),
                )
                data_attributes.append(attr_obj)

            # Create policy body - handle case where dissem is None
            dissem_data = body_data.get("dissem") or []
            policy_body = PolicyBody(
                data_attributes=data_attributes, dissem=dissem_data
            )

            # Create and return policy object
            return PolicyObject(uuid=policy_data.get("uuid", ""), body=policy_body)

        except Exception as e:
            raise SDKException("Error reading policy object") from e
