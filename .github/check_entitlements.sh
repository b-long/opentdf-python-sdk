#!/usr/bin/env bash

set -euo pipefail

# Derive additional environment variables
TOKEN_URL="${OIDC_OP_TOKEN_ENDPOINT}"
OTDF_HOST_AND_PORT="${OPENTDF_PLATFORM_HOST}"
OTDF_CLIENT="${OPENTDF_CLIENT_ID}"
OTDF_CLIENT_SECRET="${OPENTDF_CLIENT_SECRET}"

echo "🔧 Environment Configuration:"
echo "   TOKEN_URL: ${TOKEN_URL}"
echo "   OTDF_HOST_AND_PORT: ${OTDF_HOST_AND_PORT}"
echo "   OTDF_CLIENT: ${OTDF_CLIENT}"
echo "   OTDF_CLIENT_SECRET: ${OTDF_CLIENT_SECRET}"
echo ""

get_token() {
    curl -k --location "$TOKEN_URL" \
    --header "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "grant_type=client_credentials" \
    --data-urlencode "client_id=$OTDF_CLIENT" \
    --data-urlencode "client_secret=$OTDF_CLIENT_SECRET"
}

echo "🔐 Getting access token..."
BEARER=$( get_token | jq -r '.access_token' )
if [ -z "$BEARER" ]; then
    echo "❌ Failed to get access token."
    exit 1
fi

# NOTE: It's always okay to print this token, because it will
# only be valid / available in dummy / dev scenarios
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
done

echo "🎉 All entitlement checks completed!"
