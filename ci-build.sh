#!/bin/bash

set -eou pipefail

printf """

✨✨✨ Configure gopy / dependencies, and build wheel ✨✨✨

"""

echo "python -VV"
python -VV

echo 'python -c "import sys; print(sys.executable)"'
python -c "import sys; print(sys.executable)"

echo 'pip -V'
pip -V

echo 'pip install poetry'
pip install poetry

# Look for go/bin (skip, we know it exists)
echo '$HOME/'
ls -la "$HOME/"

echo '$HOME/.local/'
ls -la "$HOME/.local/"

echo '$HOME/go/'
ls -la "$HOME/go/"

# Add Go bin directory to PATH
echo "export PATH=$PATH:~/.local/go/bin" >> $GITHUB_ENV

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

pip install dist/otdf_python-0.1.12-py3-none-any.whl
