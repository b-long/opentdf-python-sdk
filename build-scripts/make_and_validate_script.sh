#!/bin/bash

set -x
set -eou pipefail

# Ensure we aren't in a virtual environment
deactivate || { echo "Not currently in a virtual environment" ; }

# Based on: https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BUILD_ROOT="${SCRIPT_DIR}/.."
cd "${BUILD_ROOT}" || { echo "Unable to change to build root directory" ; exit 1; }

SKIP_TESTS="${1:-NO}"

# Cleanup
rm -rf .venv/
rm -rf dist/

# Install python deps
poetry config virtualenvs.create true --local
poetry config virtualenvs.in-project true --local
poetry install --no-root

# Activate virtual environment with 'pybindgen' etc.
#
# NOTE: Using 'poetry shell' does not work, and we
# can't assume that the virtual environment is ./.venv/
if ! [ -d "$( poetry env info --path )" ]; then
    echo "Unable to locate virtual environment directory"
    exit 1
fi

# shellcheck disable=SC1091
source "$( poetry env info --path )/bin/activate"

python3 -m pip install pybindgen
go install golang.org/x/tools/cmd/goimports@latest
go install github.com/go-python/gopy@v0.4.10

# For every step below, 'which python' should return '.venv/bin/python'
PATH="$PATH:$HOME/go/bin" gopy build --output=otdf_python -vm=python3 .

python3 -m pip install --upgrade setuptools wheel

# Build the 'dist/' folder (wheel)
python3 setup.py bdist_wheel

# Prove that the wheel can be installed
pip install dist/otdf_python-0.2.6-py3-none-any.whl

if [[ "$SKIP_TESTS" == "-s" || "$SKIP_TESTS" == "--skip-tests" ]]; then
    echo "Build is complete, skipping tests."
else
    # Validate functionality
    echo "Build is complete, running tests."
    python3 validate_otdf_python.py
fi
