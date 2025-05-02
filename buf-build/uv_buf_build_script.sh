#!/bin/bash

# Based on the excellent work of the sift-stack team:
#   https://github.com/sift-stack/sift/blob/main/docs/python.md
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
BUILD_ROOT="${SCRIPT_DIR}/buf-build-generated"
TEST_ROOT="${SCRIPT_DIR}/buf-build-test"

# Cleanup previous builds
rm -rf .venv-wheel/
rm -rf .venv/
rm -rf dist/
rm -rf "${BUILD_ROOT}"
rm -rf "${TEST_ROOT}"

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


# Shallow clone the 'https://github.com/opentdf/platform.git' repo
git clone --depth 1 https://github.com/opentdf/platform.git

cd platform || { echo "Unable to change to platform directory" ; exit 1; }
buf export --output=$BUILD_ROOT/protos --config buf.yaml

cd $SCRIPT_DIR || { echo "Unable to change to script directory" ; exit 1; }
cp buf.gen.python.yaml $BUILD_ROOT/buf.gen.yaml
cp setup.py $BUILD_ROOT/setup.py

cd "${BUILD_ROOT}" || { echo "Unable to change to build root directory" ; exit 1; }
buf generate protos || { echo "buf generate failed" ; exit 1; }

for dir in $(find gen -type d); do
  touch $dir/__init__.py
done

# PY_TYPE="--python-preference=only-system"
PY_TYPE="--python-preference=only-managed"

loud_print "Creating virtual environment"
# Install python deps
uv venv .venv "$PY_TYPE"

if ! [ -d "${BUILD_ROOT}/.venv" ]; then
    echo "Unable to locate virtual environment directory"
    exit 1
fi

loud_print "Activating virtual environment"
source "${BUILD_ROOT}/.venv/bin/activate"

uv pip install build protobuf grpcio
python -m build --sdist || { echo "Failed to build source distribution" ; exit 1; }
python -m build --wheel || { echo "Failed to build wheel distribution" ; exit 1; }

echo "Build completed successfully."
echo "Directory contents:"
ls -lart
echo "Dist directory contents:"
ls -lart dist/


loud_print "Testing new wheel"

mkdir -p "${TEST_ROOT}" || { echo "Unable to create test root directory" ; exit 1; }
cd "${TEST_ROOT}" || { echo "Unable to change to test root directory" ; exit 1; }
uv venv .venv-wheel
source "${TEST_ROOT}/.venv-wheel/bin/activate"

echo "Ensuring wheel can be installed"
uv pip install ${BUILD_ROOT}/dist/*.whl || { echo "Failed to install wheel" ; exit 1; }

loud_print "Listing all wheel modules"
uvx python ${SCRIPT_DIR}/list_wheel_modules.py ${BUILD_ROOT}/dist/*.whl || { echo "Failed to list wheel modules" ; exit 1; }
