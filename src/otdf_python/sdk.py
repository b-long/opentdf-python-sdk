"""The main SDK class for OpenTDF platform interaction."""

from contextlib import AbstractContextManager
from io import BytesIO
from typing import Any, BinaryIO

from otdf_python.config import KASInfo, NanoTDFConfig, TDFConfig
from otdf_python.nanotdf import NanoTDF
from otdf_python.sdk_exceptions import SDKException
from otdf_python.tdf import TDF, TDFReader, TDFReaderConfig


class KAS(AbstractContextManager):
    """KAS (Key Access Service) interface to define methods related to key access and management."""

    def get_public_key(self, kas_info: Any) -> Any:
        """Retrieve the public key from KAS for RSA operations.
        If the public key is cached, returns the cached value.
        Otherwise, makes a request to the KAS.

        Args:
            kas_info: KASInfo object containing the URL and algorithm

        Returns:
            Updated KASInfo object with KID and PublicKey populated

        Raises:
            SDKException: If there's an error retrieving the public key

        """
        # Delegate to the underlying KAS client which handles authentication properly
        return self._kas_client.get_public_key(kas_info)

    def __init__(
        self,
        platform_url=None,
        token_source=None,
        sdk_ssl_verify=True,
        use_plaintext=False,
    ):
        """Initialize the KAS client.

        Args:
            platform_url: URL of the platform
            token_source: Function that returns an authentication token
            sdk_ssl_verify: Whether to verify SSL certificates
            use_plaintext: Whether to use plaintext HTTP connections instead of HTTPS

        """
        from .kas_client import KASClient

        self._kas_client = KASClient(
            kas_url=platform_url,
            token_source=token_source,
            verify_ssl=sdk_ssl_verify,
            use_plaintext=use_plaintext,
        )
        # Store the parameters for potential use
        self._sdk_ssl_verify = sdk_ssl_verify
        self._use_plaintext = use_plaintext

    def get_ec_public_key(self, kas_info: Any, curve: Any) -> Any:
        """Retrieve the EC public key from KAS.

        Args:
            kas_info: KASInfo object containing the URL
            curve: The EC curve to use

        Returns:
            Updated KASInfo object with KID and PublicKey populated

        """
        # Set algorithm to "ec:<curve>"
        from copy import copy

        kas_info_copy = copy(kas_info)
        kas_info_copy.algorithm = f"ec:{curve}"
        return self.get_public_key(kas_info_copy)

    def unwrap(self, key_access: Any, policy: str, session_key_type: Any) -> bytes:
        """Unwraps the key using the KAS.

        Args:
            key_access: KeyAccess object containing the wrapped key
            policy: Policy JSON string
            session_key_type: Type of session key (RSA, EC)

        Returns:
            Unwrapped key as bytes

        """
        return self._kas_client.unwrap(key_access, policy, session_key_type)

    def unwrap_nanotdf(
        self,
        curve: Any,
        header: str,
        kas_url: str,
        wrapped_key: bytes | None = None,
        kas_private_key: str | None = None,
        mock: bool = False,
    ) -> bytes:
        """Unwraps the NanoTDF key using the KAS. If mock=True, performs local unwrap using the private key (for tests).

        Args:
            curve: EC curve used
            header: NanoTDF header
            kas_url: URL of the KAS
            wrapped_key: Optional wrapped key bytes (for mock mode)
            kas_private_key: Optional KAS private key (for mock mode)
            mock: If True, unwrap locally using provided private key

        Returns:
            Unwrapped key as bytes

        """
        if mock and wrapped_key and kas_private_key:
            from .asym_crypto import AsymDecryption

            asym = AsymDecryption(private_key_pem=kas_private_key)
            return asym.decrypt(wrapped_key)

        # This would be implemented using nanotdf-specific logic
        raise NotImplementedError("KAS unwrap_nanotdf not implemented.")

    def get_key_cache(self) -> Any:
        """Return the KAS key cache.

        Returns:
            The KAS key cache object

        """
        return self._kas_client.get_key_cache()

    def close(self):
        """Close resources associated with KAS interface."""
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SDK(AbstractContextManager):
    """SDK for OpenTDF platform interaction."""

    def new_tdf_config(
        self,
        attributes: list[str] | None = None,
        kas_info_list: list[KASInfo] | None = None,
        **kwargs,
    ) -> TDFConfig:
        """Create a TDFConfig with default kas_info_list from the SDK's platform_url."""
        if self.platform_url is None:
            raise SDKException("Cannot create TDFConfig: SDK platform_url is not set.")

        # Get use_plaintext setting - allow override via kwargs, fall back to SDK setting
        use_plaintext = kwargs.pop(
            "use_plaintext", getattr(self, "_use_plaintext", False)
        )

        # Construct proper KAS URL by appending /kas to platform URL, like Java SDK
        # Include explicit port for HTTPS to match otdfctl behavior
        from urllib.parse import urlparse

        parsed_url = urlparse(self.platform_url)

        # Determine scheme and default port based on use_plaintext setting
        if use_plaintext:
            target_scheme = "http"
            default_port = 80
        else:
            target_scheme = "https"
            default_port = 443

        # Use the original scheme if it exists, otherwise apply target_scheme
        # This preserves the platform URL's scheme when it's already appropriate
        original_scheme = parsed_url.scheme
        if original_scheme in ("http", "https"):
            # If platform URL already has a scheme, check if it's compatible with use_plaintext
            if use_plaintext and original_scheme == "http":
                scheme = "http"
            elif not use_plaintext and original_scheme == "https":
                scheme = "https"
            else:
                # Scheme conflicts with use_plaintext setting, apply target_scheme
                scheme = target_scheme
        else:
            # No scheme or unknown scheme, apply target_scheme
            scheme = target_scheme

        # Handle URL construction with proper scheme and port
        if parsed_url.port is None:
            # Add explicit port if not present
            kas_url = f"{scheme}://{parsed_url.hostname}:{default_port}{parsed_url.path.rstrip('/')}/kas"
        else:
            # Use existing port with the determined scheme
            kas_url = f"{scheme}://{parsed_url.hostname}:{parsed_url.port}{parsed_url.path.rstrip('/')}/kas"

        if kas_info_list is None:
            kas_info = KASInfo(url=kas_url, default=True)
            kas_info_list = [kas_info]
        return TDFConfig(
            kas_info_list=kas_info_list, attributes=attributes or [], **kwargs
        )

    """
    Main SDK class for interacting with the OpenTDF platform.
    Provides various services for TDF/NanoTDF operations and platform API calls.
    """

    class Services(AbstractContextManager):
        """The Services interface provides access to various platform service clients and KAS."""

        def kas(self) -> KAS:
            """Return the KAS client for key access operations.
            This should be implemented to return an instance of KAS.
            """
            raise NotImplementedError

        def close(self):
            """Close resources associated with the services."""
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    def __init__(
        self,
        services: "SDK.Services",
        platform_url: str | None = None,
        ssl_verify: bool = True,
        use_plaintext: bool = False,
    ):
        """Initialize a new SDK instance.

        Args:
            services: The services interface implementation
            platform_url: Optional platform base URL
            ssl_verify: Whether to verify SSL certificates (default: True)
            use_plaintext: Whether to use HTTP instead of HTTPS (default: False)

        """
        self.services = services
        self.platform_url = platform_url
        self.ssl_verify = ssl_verify
        self._use_plaintext = use_plaintext

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context manager."""
        self.close()

    def close(self):
        """Close the SDK and release resources."""
        if hasattr(self.services, "close"):
            self.services.close()

    def get_services(self) -> "SDK.Services":
        """Return the services interface."""
        return self.services

    def get_platform_url(self) -> str | None:
        """Return the platform URL if set."""
        return self.platform_url

    def load_tdf(
        self,
        tdf_data: bytes | BinaryIO | BytesIO,
        config: TDFReaderConfig | None = None,
    ) -> TDFReader:
        """Load a TDF from the provided data, optionally according to config.

        Args:
            tdf_data: The TDF data as bytes, file object, or BytesIO
            config: TDFReaderConfig dataclass

        Returns:
            TDFReader: Contains payload and manifest

        Raises:
            SDKException: If there's an error loading the TDF

        """
        tdf = TDF(self.services)
        if config is None:
            config = TDFReaderConfig()

        return tdf.load_tdf(tdf_data, config)

    def create_tdf(
        self,
        payload: bytes | BinaryIO | BytesIO,
        config,
        output_stream: BinaryIO | None = None,
    ):
        """Create a TDF with the provided payload.

        Args:
            payload: The payload data as bytes, file object, or BytesIO
            config: TDFConfig dataclass from config.py
            output_stream: The output stream to write the TDF to

        Returns:
            Manifest, size, output_stream

        Raises:
            SDKException: If there's an error creating the TDF

        """
        tdf = TDF(self.services)
        return tdf.create_tdf(payload, config, output_stream)

    def create_nano_tdf(
        self, payload: bytes | BytesIO, output_stream: BinaryIO, config: "NanoTDFConfig"
    ) -> int:
        """Create a NanoTDF with the provided payload.

        Args:
            payload: The payload data as bytes or BytesIO
            output_stream: The output stream to write the NanoTDF to
            config: NanoTDFConfig for the NanoTDF creation

        Returns:
            int: The size of the created NanoTDF

        Raises:
            SDKException: If there's an error creating the NanoTDF

        """
        nano_tdf = NanoTDF(self.services)
        return nano_tdf.create_nano_tdf(payload, output_stream, config)

    def read_nano_tdf(
        self,
        nano_tdf_data: bytes | BytesIO,
        output_stream: BinaryIO,
        config: NanoTDFConfig,
    ) -> None:
        """Read a NanoTDF and write the payload to the output stream.

        Args:
            nano_tdf_data: The NanoTDF data as bytes or BytesIO
            output_stream: The output stream to write the payload to
            config: NanoTDFConfig configuration for the NanoTDF reader

        Raises:
            SDKException: If there's an error reading the NanoTDF

        """
        nano_tdf = NanoTDF(self.services)
        nano_tdf.read_nano_tdf(nano_tdf_data, output_stream, config)

    @staticmethod
    def is_tdf(data: bytes | BinaryIO) -> bool:
        """Check if the provided data is a TDF.

        Args:
            data: The data to check

        Returns:
            bool: True if the data is a TDF, False otherwise

        """
        import zipfile
        from io import BytesIO

        try:
            file_like = BytesIO(data) if isinstance(data, bytes | bytearray) else data
            with zipfile.ZipFile(file_like) as zf:
                names = set(zf.namelist())
                return {"0.manifest.json", "0.payload"}.issubset(names) and len(
                    names
                ) == 2
        except Exception:
            return False

    # Exception classes - SDK-specific exceptions that can occur during operations
    class SplitKeyException(SDKException):
        """Throw when SDK encounters error related to split key operations."""

        pass

    class DataSizeNotSupported(SDKException):
        """Throw when user attempts to create TDF larger than maximum size."""

        pass

    class KasInfoMissing(SDKException):
        """Throw during TDF creation when no KAS information is present."""

        pass

    class KasPublicKeyMissing(SDKException):
        """Throw during encryption when SDK cannot retrieve public key for KAS."""

        pass

    class TamperException(SDKException):
        """Base class for exceptions related to signature mismatches."""

        def __init__(self, error_message: str):
            """Initialize tamper exception."""
            super().__init__(f"[tamper detected] {error_message}")

    class RootSignatureValidationException(TamperException):
        """Throw when root signature validation fails."""

    class SegmentSignatureMismatch(TamperException):
        """Throw when segment signature does not match expected value."""

        pass

    class KasBadRequestException(SDKException):
        """Throw when KAS returns bad request response."""

        pass

    class KasAllowlistException(SDKException):
        """Throw when KAS allowlist check fails."""

        pass

    class AssertionException(SDKException):
        """Throw when an assertion validation fails."""

        def __init__(self, error_message: str, assertion_id: str):
            """Initialize exception."""
            super().__init__(error_message)
            self.assertion_id = assertion_id
