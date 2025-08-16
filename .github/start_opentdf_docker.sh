#!/usr/bin/env bash

set -euo pipefail

if ! [ -d platform ]; then
  # Sparse clone opentdf/platform
  git clone https://github.com/opentdf/platform.git
fi
cd platform
git checkout DSPX-1539-keytoolnomore

yq -i '.realms[0].clients[0].client.directAccessGrantsEnabled = true | .realms[0].clients[0].client.serviceAccountsEnabled = true' service/cmd/keycloak_data.yaml

yq -i '.realms[0].clients[1].client.directAccessGrantsEnabled = true | .realms[0].clients[0].client.serviceAccountsEnabled = true' service/cmd/keycloak_data.yaml

yq -i '.realms[0].clients[4].client.directAccessGrantsEnabled = true | .realms[0].clients[0].client.serviceAccountsEnabled = true' service/cmd/keycloak_data.yaml


if [ -d ./keys ]; then
  go mod download

  go mod verify

  .github/scripts/init-temp-keys.sh
  cp opentdf-dev.yaml opentdf.yaml
  chmod -R 777 ./keys
fi

docker compose up -d --wait --wait-timeout 360

go run ./service provision keycloak

go run ./service provision fixtures