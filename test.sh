#!/bin/bash

VENV=./venv

PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"
PYTEST="$VENV/bin/pytest"

if [ ! -d "$VENV" ]; then
    mkdir -p "$VENV"
    virtualenv "$VENV"
    "$PIP" install pytest -v
fi

PYTHONPATH=. $PYTEST
