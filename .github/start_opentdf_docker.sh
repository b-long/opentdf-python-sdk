#!/usr/bin/env bash

set -euo pipefail

if ! [ -d platform ]; then
  # Sparse clone opentdf/platform
  git clone https://github.com/opentdf/platform.git
fi
cd platform
git checkout DSPX-1539-keytoolnomore

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