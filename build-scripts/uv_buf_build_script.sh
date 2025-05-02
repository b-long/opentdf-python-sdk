#!/bin/bash

set -x
set -eou pipefail

loud_print(){
    printf """

    ========================================
    $1


    ========================================

    """
}

# Based on: https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BUILD_ROOT="${SCRIPT_DIR}/buf-build"

# Cleanup previous builds
rm -rf .venv-wheel/
rm -rf .venv/
rm -rf dist/
rm -rf "${BUILD_ROOT}"

mkdir -p "${BUILD_ROOT}" || { echo "Unable to create build root directory" ; exit 1; }
cd "${BUILD_ROOT}" || { echo "Unable to change to build root directory" ; exit 1; }

SKIP_TESTS="${1:-NO}"

# Ensure 'buf' is installed
if ! command -v buf &> /dev/null; then
    echo "[opentdf-python-sdk] buf could not be found, please install buf and retry."
    exit 1
fi

# Ensure 'go' is installed
if ! command -v go &> /dev/null; then
    echo "[opentdf-python-sdk] go could not be found, please install go and retry."
    exit 1
fi


# PY_TYPE="--python-preference=only-system"
PY_TYPE="--python-preference=only-managed"

loud_print "Creating virtual environment"
# Install python deps
uv venv .venv --python 3.12 "$PY_TYPE"

if ! [ -d "${BUILD_ROOT}/.venv" ]; then
    echo "Unable to locate virtual environment directory"
    exit 1
fi

loud_print "Activating virtual environment"
source "${BUILD_ROOT}/.venv/bin/activate"


# Shallow clone the 'https://github.com/opentdf/platform.git' repo
git clone --depth 1 https://github.com/opentdf/platform.git

cd platform || { echo "Unable to change to platform directory" ; exit 1; }
buf export --output=$BUILD_ROOT/protos --config buf.yaml
