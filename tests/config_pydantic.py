"""In this module, we are migrating to using `pydantic-settings`.

Docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

In addition to environment variables, `pydantic-settings` can be loaded from
".env" files:

https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support

This implementation is preferred over plain Python dictionaries, for a more
robust configuration.  It also gives the user an interface with guaranteed
types, saving us from doing type conversion.

"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigureTdf(BaseSettings):
    # Down the road, we can use a prefix here to isolate module-specific settings.
    model_config = SettingsConfigDict(
        # env_prefix="common_",
        env_file=".env",
        # `.env.prod` takes priority over `.env`
        # env_file=(".env", ".env.prod"),
        env_file_encoding="utf-8",
        extra="forbid",  # Forbid extra fields in the environment
    )

    OPENTDF_PLATFORM_HOST: str = "localhost:8080"
    OPENTDF_PLATFORM_PORT: int = 8080

    # NOTE: If an end-user wants to provide a different protocol or custom
    # port, they can do so by providing the full endpoint here
    OPENTDF_PLATFORM_URL: str = Field(
        default_factory=lambda data: f"https://{data['OPENTDF_PLATFORM_HOST']}"
    )

    KAS_ENDPOINT: str = Field(
        default_factory=lambda data: f"{data['OPENTDF_PLATFORM_URL']}/kas"
    )

    # OIDC settings
    OPENTDF_KEYCLOAK_HOST: str = "localhost:8443"

    # NOTE: Be careful about the Keycloak URL.  You may see an HTTP 404 error
    # if it is misconfigured, as the Python Keycloak library is finnicky, and
    # may not handle a missing trailing slash well.  For more info, see:
    #   https://github.com/marcospereirampj/python-keycloak/issues/127
    KEYCLOAK_URL: str = Field(
        # default_factory=lambda data: f"https://{data['OPENTDF_KEYCLOAK_HOST']}:8443/auth/"
        default_factory=lambda data: f"https://{data['OPENTDF_KEYCLOAK_HOST']}/"
    )

    OIDC_OP_TOKEN_ENDPOINT: str = Field(
        default_factory=lambda data: f"{data['KEYCLOAK_URL']}realms/opentdf/protocol/openid-connect/token"
    )

    # NOTE: The following variableis used for OIDC, NPE encryption/decryption, as
    # well as 'tructl' integration.
    OPENTDF_CLIENT_ID: str = "opentdf"
    # NOTE: The following variableis used for OIDC, NPE encryption/decryption, as
    # well as 'tructl' integration.
    OPENTDF_CLIENT_SECRET: str = "secret"

    # TODO: Default to False
    INSECURE_SKIP_VERIFY: bool = True

    OPENTDF_USE_SPECIFIED_CA_CERT: bool = False

    TEST_OPENTDF_ATTRIBUTE_1: str = "https://example.com/attr/attr1/value/value1"
    TEST_OPENTDF_ATTRIBUTE_2: str = "https://example.com/attr/attr1/value/value2"

    TEST_USER_ID: str = "sample-user"
    TEST_USER_PASSWORD: str = "testuser123"


class ConfigureTesting(BaseSettings):
    """Used by integration tests (in particular for SSH and Kubernetes access)."""

    model_config = SettingsConfigDict(
        # env_prefix="common_",
        env_file=".env-testing",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    ENABLE_LOG_COLLECTION: bool = False
    POD_NAME: str = "some-pod-name-123456789-abcde"
    NAMESPACE: str = "default"
    SSH_TARGET: str = "default"
    LOG_LINES: int = 10


# Load and validate environment variables
CONFIG_TDF = ConfigureTdf()
CONFIG_TESTING = ConfigureTesting()

# For debugging only
# print(ConfigureTdf().model_dump())
