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
BUILD_ROOT="${SCRIPT_DIR}/.."
cd "${BUILD_ROOT}" || { echo "Unable to change to build root directory" ; exit 1; }

SKIP_TESTS="${1:-NO}"

# Cleanup
rm -rf .venv-wheel/
rm -rf .venv/
rm -rf dist/

# PY_TYPE="--python-preference=only-system"
PY_TYPE="--python-preference=only-managed"

loud_print "Creating virtual environment"
# Install python deps
uv venv .venv --python 3.12 "$PY_TYPE"
source "${BUILD_ROOT}/.venv/bin/activate"

loud_print "Installing dependencies"
uv pip install wheel pybindgen

if ! [ -d ".venv" ]; then
    echo "Unable to locate virtual environment directory"
    exit 1
fi

loud_print "Activating virtual environment"
source "${BUILD_ROOT}/.venv/bin/activate"

loud_print "Installing goimports"
go install golang.org/x/tools/cmd/goimports@latest
loud_print "Installing gopy"
go install github.com/go-python/gopy@v0.4.10

# For every step below, 'which python' should return '.venv/bin/python'
loud_print "Executing gopy"
PATH="$PATH:$HOME/go/bin" gopy build --output=otdf_python -vm=python3 .

loud_print "Installing setuptools"
uv pip install --upgrade setuptools

# Build the 'dist/' folder (wheel)
loud_print "Running 'setup.py bdist_wheel'"
python setup.py bdist_wheel

deactivate

# Prove that the wheel can be installed
loud_print "Installing wheel"

uv venv .venv-wheel --python 3.12 "$PY_TYPE"
source "${BUILD_ROOT}/.venv-wheel/bin/activate"
pip install pybindgen
pip install dist/otdf_python-0.2.9-py3-none-any.whl

if [[ "$SKIP_TESTS" == "-s" || "$SKIP_TESTS" == "--skip-tests" ]]; then
    echo "Build is complete, skipping tests."
else
    # Validate functionality
    echo "Build is complete, running tests."
    python validate_otdf_python.py
fi
