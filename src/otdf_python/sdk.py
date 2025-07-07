"""
Python port of the main SDK class for OpenTDF platform interaction.
"""
from typing import Any, BinaryIO
from io import BytesIO
from contextlib import AbstractContextManager
import httpx

from otdf_python.tdf import TDF, TDFConfig, TDFReaderConfig, TDFReader
from otdf_python.nanotdf import NanoTDF
from otdf_python.sdk_exceptions import SDKException
from otdf_python.config import NanoTDFConfig

# Stubs for service client interfaces (to be implemented)
class AttributesServiceClientInterface: ...
class NamespaceServiceClientInterface: ...
class SubjectMappingServiceClientInterface: ...
class ResourceMappingServiceClientInterface: ...
class AuthorizationServiceClientInterface: ...
class KeyAccessServerRegistryServiceClientInterface: ...

# Placeholder for ProtocolClient and Interceptor
class ProtocolClient: ...
class Interceptor: ...  # Can be dict in Python implementation

# Placeholder for TrustManager
class TrustManager: ...

class SDK(AbstractContextManager):
    def new_tdf_config(self, attributes: list[str] | None = None, **kwargs) -> 'TDFConfig':
        """
        Create a TDFConfig with default kas_info_list from the SDK's platform_url.
        Based on Java implementation.
        """
        from otdf_python.config import TDFConfig, KASInfo
        kas_url = self.platform_url or "https://default.kas.example.com"
        kas_info = KASInfo(url=kas_url, default=True)
        # Accept user override for kas_info_list if provided
        kas_info_list = kwargs.pop("kas_info_list", None)
        if kas_info_list is None:
            kas_info_list = [kas_info]
        return TDFConfig(
            kas_info_list=kas_info_list,
            attributes=attributes or [],
            **kwargs
        )

    def _adapt_tdf_config(self, config):
        """
        Adapts between TDFConfig implementations in config.py and tdf.py.
        This is necessary because the TDF class expects config.kas_info, but the SDK creates a TDFConfig
        with config.kas_info_list from config.py.

        Args:
            config: A TDFConfig object from config.py

        Returns:
            A TDFConfig object compatible with tdf.py
        """
        # If it's already a tdf.py TDFConfig, just return it
        from otdf_python.tdf import TDFConfig as TDFTDFConfig
        if isinstance(config, TDFTDFConfig):
            return config

        # Otherwise, adapt it
        kas_info = getattr(config, "kas_info_list", None)
        if kas_info is None or not kas_info:
            # Try to use platform_url to create a KASInfo
            from otdf_python.kas_info import KASInfo
            kas_info = KASInfo(url=self.platform_url or "https://default.kas.example.com")
        else:
            # Take the first KAS info from the list
            kas_info = kas_info[0] if isinstance(kas_info, list) else kas_info

        return TDFTDFConfig(
            kas_info=kas_info,
            kas_private_key=getattr(config, "tdf_private_key", None),
            policy_object=getattr(config, "policy_object", None),
            attributes=getattr(config, "attributes", None),
            segment_size=getattr(config, "default_segment_size", None)
        )

    """
    Main SDK class for interacting with the OpenTDF platform.
    Provides various services for TDF/NanoTDF operations and platform API calls.
    """

    class KAS(AbstractContextManager):
        """
        KAS (Key Access Service) interface to define methods related to key access and management.
        """
        def get_public_key(self, kas_info: Any) -> Any:
            """
            Retrieves the public key from the KAS for RSA operations.
            If the public key is cached, returns the cached value.
            Otherwise, makes a request to the KAS.

            Args:
                kas_info: KASInfo object containing the URL and algorithm

            Returns:
                Updated KASInfo object with KID and PublicKey populated

            Raises:
                SDKException: If there's an error retrieving the public key
            """
            # Check cache first
            key_cache = self.get_key_cache()
            if key_cache:
                cached_value = key_cache.get(kas_info.url, kas_info.algorithm)
                if cached_value:
                    return cached_value

            # Make request to KAS
            try:

                # Build request based on algorithm
                request_data = {}
                if kas_info.algorithm:
                    request_data["algorithm"] = kas_info.algorithm

                # Make request to KAS
                headers = {"Content-Type": "application/json"}
                url = f"{kas_info.url}/kas/v2/public_key"
                response = httpx.post(url, json=request_data, headers=headers)

                if response.status_code != 200:
                    raise SDKException(f"Error getting public key: HTTP {response.status_code} - {response.text}")

                resp_data = response.json()

                # Create updated KASInfo
                from otdf_python.kas_info import KASInfo
                updated_kas_info = KASInfo(
                    url=kas_info.url,
                    kid=resp_data.get("kid"),
                    public_key=resp_data.get("publicKey"),
                    algorithm=kas_info.algorithm
                )

                # Store in cache
                if key_cache:
                    key_cache.store(updated_kas_info)

                return updated_kas_info

            except Exception as e:
                raise SDKException(f"Error getting public key: {e}")

        def __init__(self, platform_url=None, token_source=None):
            """
            Initialize the KAS client

            Args:
                platform_url: URL of the platform
                token_source: Function that returns an authentication token
            """
            from .kas_client import KASClient
            self._kas_client = KASClient(kas_url=platform_url, token_source=token_source)

        def get_ec_public_key(self, kas_info: Any, curve: Any) -> Any:
            """
            Retrieves the EC public key from the KAS.

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
            return self.get_public_key_from_kas(kas_info_copy)

        def get_public_key_from_kas(self, kas_info: Any) -> Any:
            """
            Retrieves the public key from the KAS for RSA operations.
            Wrapper around the KAS client's get_public_key method.

            Args:
                kas_info: KASInfo object containing the URL and algorithm

            Returns:
                Updated KASInfo object with KID and PublicKey populated
            """
            return self._kas_client.get_public_key(kas_info)

        def unwrap(self, key_access: Any, policy: str, session_key_type: Any) -> bytes:
            """
            Unwraps the key using the KAS.

            Args:
                key_access: KeyAccess object containing the wrapped key
                policy: Policy JSON string
                session_key_type: Type of session key (RSA, EC)

            Returns:
                Unwrapped key as bytes
            """
            return self._kas_client.unwrap(key_access, policy, session_key_type)

        def unwrap_nanotdf(self, curve: Any, header: str, kas_url: str, wrapped_key: bytes | None = None, kas_private_key: str | None = None, mock: bool = False) -> bytes:
            """
            Unwraps the NanoTDF key using the KAS. If mock=True, performs local unwrap using the private key (for tests).

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
                from .asym_decryption import AsymDecryption
                asym = AsymDecryption(private_key_pem=kas_private_key)
                return asym.decrypt(wrapped_key)

            # This would be implemented using nanotdf-specific logic
            raise NotImplementedError("KAS unwrap_nanotdf not implemented.")

        def get_key_cache(self) -> Any:
            """
            Returns the KAS key cache.

            Returns:
                The KAS key cache object
            """
            return self._kas_client.get_key_cache()

        def close(self):
            """Closes resources associated with the KAS interface"""
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    class Services(AbstractContextManager):
        """
        The Services interface provides access to various platform service clients and KAS.
        """
        def attributes(self) -> AttributesServiceClientInterface:
            """Returns the attributes service client"""
            raise NotImplementedError

        def namespaces(self) -> NamespaceServiceClientInterface:
            """Returns the namespaces service client"""
            raise NotImplementedError

        def subject_mappings(self) -> SubjectMappingServiceClientInterface:
            """Returns the subject mappings service client"""
            raise NotImplementedError

        def resource_mappings(self) -> ResourceMappingServiceClientInterface:
            """Returns the resource mappings service client"""
            raise NotImplementedError

        def authorization(self) -> AuthorizationServiceClientInterface:
            """Returns the authorization service client"""
            raise NotImplementedError

        def kas_registry(self) -> KeyAccessServerRegistryServiceClientInterface:
            """Returns the KAS registry service client"""
            raise NotImplementedError

        def kas(self) -> 'SDK.KAS':
            """
            Returns the KAS interface.

            Returns:
                KAS: The KAS interface implementation
            """
            # Return a KAS implementation with the SDK's platform URL
            # This is where we would get the platform URL and token source from the SDK
            from .sdk_builder import SDKBuilder
            platform_url = SDKBuilder.get_platform_url()

            # Create the KAS implementation with the platform URL
            kas_impl = SDK.KAS(platform_url=platform_url)
            return kas_impl

        def close(self):
            """Closes resources associated with the services"""
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    def __init__(self, services: 'SDK.Services', trust_manager: TrustManager | None = None,
                 auth_interceptor: Interceptor | dict[str, str] | None = None,
                 platform_services_client: ProtocolClient | None = None,
                 platform_url: str | None = None):
        """
        Initializes a new SDK instance.

        Args:
            services: The services interface implementation
            trust_manager: Optional trust manager for SSL validation
            auth_interceptor: Optional auth interceptor for API requests
            platform_services_client: Optional client for platform services
            platform_url: Optional platform base URL
        """
        self.services = services
        self.trust_manager = trust_manager
        self.auth_interceptor = auth_interceptor
        self.platform_services_client = platform_services_client
        self.platform_url = platform_url

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context manager"""
        self.services.close()

    def get_services(self) -> 'SDK.Services':
        """Returns the services interface"""
        return self.services

    def get_trust_manager(self) -> TrustManager | None:
        """Returns the trust manager if set"""
        return self.trust_manager

    def get_auth_interceptor(self) -> Interceptor | dict[str, str] | None:
        """Returns the auth interceptor if set"""
        return self.auth_interceptor

    def get_platform_services_client(self) -> ProtocolClient | None:
        """Returns the platform services client if set"""
        return self.platform_services_client

    def get_platform_url(self) -> str | None:
        """Returns the platform URL if set"""
        return self.platform_url

    def load_tdf(self, tdf_data: bytes | BinaryIO | BytesIO, config: TDFReaderConfig) -> TDFReader:
        """
        Loads a TDF from the provided data.

        Args:
            tdf_data: The TDF data as bytes, file object, or BytesIO
            config: TDFReaderConfig dataclass

        Returns:
            TDFReader: Contains payload and manifest

        Raises:
            SDKException: If there's an error loading the TDF
        """
        tdf = TDF(self.services)
        return tdf.load_tdf(tdf_data, config)

    def create_tdf(self, payload: bytes | BinaryIO | BytesIO, config, output_stream: BinaryIO | None = None):
        """
        Creates a TDF with the provided payload.

        Args:
            payload: The payload data as bytes, file object, or BytesIO
            config: TDFConfig dataclass from either config.py or tdf.py
            output_stream: The output stream to write the TDF to

        Returns:
            Manifest, size, output_stream

        Raises:
            SDKException: If there's an error creating the TDF
        """
        # Adapt the config if needed
        adapted_config = self._adapt_tdf_config(config)
        tdf = TDF(self.services)
        return tdf.create_tdf(payload, adapted_config, output_stream)

    def create_nano_tdf(self, payload: bytes | BytesIO, output_stream: BinaryIO, config: 'NanoTDFConfig') -> int:
        """
        Creates a NanoTDF with the provided payload.

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

    def read_nano_tdf(self, nano_tdf_data: bytes | BytesIO, output_stream: BinaryIO, config: NanoTDFConfig) -> None:
        """
        Reads a NanoTDF and writes the payload to the output stream.

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
        """
        Checks if the provided data is a TDF.

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
                return {"0.manifest.json", "0.payload"}.issubset(names) and len(names) == 2
        except Exception:
            return False

    # Exception classes - SDK-specific exceptions that can occur during operations
    class SplitKeyException(SDKException):
        """Thrown when the SDK encounters an error related to split key operations"""
        pass

    class DataSizeNotSupported(SDKException):
        """Thrown when the user attempts to create a TDF with a size larger than the maximum size"""
        pass

    class KasInfoMissing(SDKException):
        """Thrown during TDF creation when no KAS information is present"""
        pass

    class KasPublicKeyMissing(SDKException):
        """Thrown during encryption when the SDK cannot retrieve the public key for a KAS"""
        pass

    class TamperException(SDKException):
        """Base class for exceptions related to signature mismatches"""
        def __init__(self, error_message: str):
            super().__init__(f"[tamper detected] {error_message}")

    class RootSignatureValidationException(TamperException):
        """Thrown when the root signature validation fails"""
        pass

    class SegmentSignatureMismatch(TamperException):
        """Thrown when a segment signature does not match the expected value"""
        pass

    class KasBadRequestException(SDKException):
        """Thrown when the KAS returns a bad request response"""
        pass

    class KasAllowlistException(SDKException):
        """Thrown when the KAS allowlist check fails"""
        pass

    class AssertionException(SDKException):
        """Thrown when an assertion validation fails"""
        def __init__(self, error_message: str, assertion_id: str):
            super().__init__(error_message)
            self.assertion_id = assertion_id
