#!/bin/bash

set -eou pipefail

# Based on: https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BUILD_ROOT="${SCRIPT_DIR}/.."
cd "${BUILD_ROOT}" || { echo "Unable to change to build root directory" ; exit 1; }

printf """

✨✨✨ Configure gopy / dependencies, and build wheel ✨✨✨

"""

echo "✨✨✨ Display Python version"
echo "python -VV"
python -VV

echo "✨✨✨ Display Python executable path"
echo 'python -c "import sys; print(sys.executable)"'
python -c "import sys; print(sys.executable)"

echo "✨✨✨ Display pip version"
echo 'pip -V'
pip -V

echo "✨✨✨ Install poetry"
echo 'pip install poetry'
pip install poetry

echo "✨✨✨ List home directory contents"
# Look for go/bin (skip, we know it exists)
echo '$HOME/'
ls -la "$HOME/"

echo "✨✨✨ List Go directory contents"
echo '$HOME/go/'
ls -la "$HOME/go/"

echo "✨✨✨ Display Go version"
go version

echo "✨✨✨ Add Go bin directory to PATH"
# Add Go bin directory to PATH
echo "export PATH=$PATH:~/.local/go/bin" >> $GITHUB_ENV

echo "✨✨✨ Install dependencies with poetry"
# Since we don't have our wheel build / install configured yet we use '--no-root'
poetry install --no-root

echo "✨✨✨ Activate poetry environment"
source $(poetry env info --path)/bin/activate

echo "✨✨✨ Add Go bin directory to PATH again"
# Add Go bin directory to PATH
echo "export PATH=$PATH:~/.local/go/bin" >> $GITHUB_ENV

echo "✨✨✨ Install goimports"
go install golang.org/x/tools/cmd/goimports@latest

echo "✨✨✨ Install gopy"
go install github.com/go-python/gopy@latest

echo "✨✨✨ Upgrade setuptools and wheel"
poetry run pip install --upgrade setuptools wheel

echo "✨✨✨ Build gopy"
gopy build --output=otdf_python -vm=python3 .

echo "✨✨✨ Build wheel"
poetry run python3 setup.py bdist_wheel

echo "✨✨✨ Install wheel"
pip install dist/otdf_python-0.2.19-py3-none-any.whl
