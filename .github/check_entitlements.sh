#!/bin/bash


# Derive additional environment variables
TOKEN_URL="${OIDC_OP_TOKEN_ENDPOINT}"
OTDF_HOST_AND_PORT="${OPENTDF_PLATFORM_HOST}"
OTDF_CLIENT="${OPENTDF_CLIENT_ID}"
OTDF_CLIENT_SECRET="${OPENTDF_CLIENT_SECRET}"

# Used to test PE auth
CLIENT_ID="opentdf-sdk"

# Enable debug mode
DEBUG=1

echo "🔧 Environment Configuration:"
echo "   TOKEN_URL: ${TOKEN_URL}"
echo "   OTDF_HOST_AND_PORT: ${OTDF_HOST_AND_PORT}"
echo "   OTDF_CLIENT: ${OTDF_CLIENT}"
echo "   OTDF_CLIENT_SECRET: ${OTDF_CLIENT_SECRET}"
echo ""

get_token() {
    curl -k --location "$TOKEN_URL" \
    --header "X-VirtruPubKey;" \
    --header "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "grant_type=client_credentials" \
    --data-urlencode "client_id=$OTDF_CLIENT" \
    --data-urlencode "client_secret=$OTDF_CLIENT_SECRET"
}

auth_pe() {
  # Auth, according to sample user accounts
  # https://github.com/opentdf/platform/blob/service/v0.8.1/service/cmd/keycloak_data.yaml#L84-L92
  USERNAME="${1}"
  PASSWORD="testuser123"
  AUTH_CLIENT="${2}"

  curl -k -X POST "$TOKEN_URL" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=password" \
    -d "client_id=$AUTH_CLIENT" \
    -d "username=$USERNAME" \
    -d "password=$PASSWORD"
}

echo "🔐 Getting access token..."
BEARER=$( get_token | jq -r '.access_token' )
[[ "${DEBUG:-}" == "1" ]] && echo "Got Access Token: ${BEARER}"
echo ""

# Array of usernames to check
USERNAMES=("opentdf" "sample-user" "sample-user-1" "cli-client" "opentdf-sdk")

for USERNAME in "${USERNAMES[@]}"; do
    echo "👤 Fetching entitlements for username: ${USERNAME}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    grpcurl -plaintext \
      -H "authorization: Bearer $BEARER" \
      -d "{
      \"entities\": [
        {
          \"userName\": \"$USERNAME\"
        }
      ]
    }" \
      "$OTDF_HOST_AND_PORT" \
      authorization.AuthorizationService/GetEntitlements

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Entitlements retrieval complete for ${USERNAME}!"
    echo ""

    # Test two different values for AUTH_CLIENT
    echo "Testing auth_pe for ${USERNAME} with ${CLIENT_ID}..."
    auth_pe "$USERNAME" "$CLIENT_ID"
    echo "Testing auth_pe for ${USERNAME} with ${OTDF_CLIENT}..."
    auth_pe "$USERNAME" "$OTDF_CLIENT"
    echo ""
done

echo "🎉 All entitlement checks completed!"
