from otdf_python.sdk_builder import SDKBuilder
from otdf_python.sdk import SDK
from tests.config_pydantic import CONFIG_TDF
import httpx


def get_sdk() -> SDK:
    if CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://"):
        sdk = (
            SDKBuilder()
            .set_platform_endpoint(CONFIG_TDF.OPENTDF_PLATFORM_URL)
            .set_issuer_endpoint(CONFIG_TDF.OPENTDF_KEYCLOAK_HOST)
            .client_secret(
                CONFIG_TDF.OPENTDF_CLIENT_ID,
                CONFIG_TDF.OPENTDF_CLIENT_SECRET,
            )
            .use_insecure_plaintext_connection(True)
            .use_insecure_skip_verify(CONFIG_TDF.INSECURE_SKIP_VERIFY)
            .build()
        )
    elif CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("https://"):
        sdk = (
            SDKBuilder()
            .set_platform_endpoint(CONFIG_TDF.OPENTDF_PLATFORM_URL)
            .set_issuer_endpoint(CONFIG_TDF.OPENTDF_KEYCLOAK_HOST)
            .client_secret(
                CONFIG_TDF.OPENTDF_CLIENT_ID,
                CONFIG_TDF.OPENTDF_CLIENT_SECRET,
            )
            .use_insecure_skip_verify(CONFIG_TDF.INSECURE_SKIP_VERIFY)
            .build()
        )
    else:
        raise ValueError(
            f"Invalid platform URL: {CONFIG_TDF.OPENTDF_PLATFORM_URL}. "
            "It must start with 'http://' or 'https://'."
        )

    return sdk


def get_sdk_for_pe() -> SDK:
    user_token: str = get_user_access_token(
        CONFIG_TDF.OIDC_OP_TOKEN_ENDPOINT,
        CONFIG_TDF.TEST_USER_ID,
        CONFIG_TDF.TEST_USER_PASSWORD,
    )

    if CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("http://"):
        sdk = (
            SDKBuilder(auth_token=user_token)
            .set_platform_endpoint(CONFIG_TDF.OPENTDF_PLATFORM_URL)
            .set_issuer_endpoint(CONFIG_TDF.OPENTDF_KEYCLOAK_HOST)
            .use_insecure_plaintext_connection(True)
            .use_insecure_skip_verify(CONFIG_TDF.INSECURE_SKIP_VERIFY)
            .build()
        )
    elif CONFIG_TDF.OPENTDF_PLATFORM_URL.startswith("https://"):
        sdk = (
            SDKBuilder()
            .set_platform_endpoint(CONFIG_TDF.OPENTDF_PLATFORM_URL)
            .set_issuer_endpoint(CONFIG_TDF.OPENTDF_KEYCLOAK_HOST)
            .use_insecure_skip_verify(CONFIG_TDF.INSECURE_SKIP_VERIFY)
            .build()
        )
    else:
        raise ValueError(
            f"Invalid platform URL: {CONFIG_TDF.OPENTDF_PLATFORM_URL}. "
            "It must start with 'http://' or 'https://'."
        )

    return sdk


def get_user_access_token(
    token_endpoint,
    pe_username,
    pe_password,
):
    """
    When using this function, ensure that:

    1. The client has "fine-grained access control" enabled (in the Advanced tab for the client in Keycloak).
    2. The client is allowed to use "Direct access grants" (in the Settings tab for the client in Keycloak).

    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "password",
        "client_id": CONFIG_TDF.OPENTDF_CLIENT_ID,
        "client_secret": CONFIG_TDF.OPENTDF_CLIENT_SECRET,
        "username": pe_username,
        "password": pe_password,
    }

    with httpx.Client(verify=False) as client:
        response = client.post(token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
