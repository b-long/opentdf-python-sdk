#!/usr/bin/env bash

set -euo pipefail

if ! [ -d platform ]; then
  git clone https://github.com/opentdf/platform.git
fi
cd platform
git checkout 3360befcb3e6e9791d7bfd2e89128aee0e7d2818 # Branch 'DSPX-1539-keytoolnomore'

yq -i '.realms[0].clients[0].client.directAccessGrantsEnabled = true | .realms[0].clients[0].client.serviceAccountsEnabled = true' service/cmd/keycloak_data.yaml

yq -i '.realms[0].clients[1].client.directAccessGrantsEnabled = true | .realms[0].clients[1].client.serviceAccountsEnabled = true' service/cmd/keycloak_data.yaml

yq -i '.realms[0].clients[4].client.directAccessGrantsEnabled = true | .realms[0].clients[4].client.serviceAccountsEnabled = true' service/cmd/keycloak_data.yaml


if ! [ -d ./keys ]; then
  go mod download

  go mod verify

  .github/scripts/init-temp-keys.sh
  cp opentdf-example.yaml opentdf.yaml

  # Edit 'opentdf.yaml' for our use case
  yq -i 'del(.db) | .services.entityresolution.url = "http://localhost:8888/auth" | .server.auth.issuer = "http://localhost:8888/auth/realms/opentdf"' opentdf.yaml
  # The above expression can also be written as 3 separate commands:
  # yq -i 'del(.db)' opentdf.yaml
  # yq -i '.services.entityresolution.url = "http://localhost:8888/auth"' opentdf.yaml
  # yq -i '.server.auth.issuer = "http://localhost:8888/auth/realms/opentdf"' opentdf.yaml

  yq -i '
.server.cryptoProvider = {
  "type": "standard",
  "standard": {
    "keys": [
      {
        "kid": "r1",
        "alg": "rsa:2048",
        "private": "kas-private.pem",
        "cert": "kas-cert.pem"
      },
      {
        "kid": "e1",
        "alg": "ec:secp256r1",
        "private": "kas-ec-private.pem",
        "cert": "kas-ec-cert.pem"
      }
    ]
  }
}
' opentdf.yaml
  chmod -R 700 ./keys
fi

docker compose up -d --wait --wait-timeout 360

go run ./service provision keycloak

go run ./service provision fixtures
