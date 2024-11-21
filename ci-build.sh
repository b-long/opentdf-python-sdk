#!/bin/bash

set -eou pipefail

# Since we don't have our wheel build / install configured yet we use '--no-root'
poetry install --no-root

source $(poetry env info --path)/bin/activate

# Add Go bin directory to PATH
echo "export PATH=$PATH:~/.local/go/bin" >> $GITHUB_ENV

go install golang.org/x/tools/cmd/goimports@latest

go install github.com/go-python/gopy@latest

poetry run pip install --upgrade setuptools wheel

gopy build --output=otdf_python -vm=python3 .

poetry run python3 setup.py bdist_wheel
