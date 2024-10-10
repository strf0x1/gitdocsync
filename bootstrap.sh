#!/usr/bin/env bash

set -e

check_poetry() {
    if ! command -v poetry &> /dev/null; then
        echo "Poetry not found. Please install Poetry first: https://python-poetry.org/docs/#installation"
        exit 1
    fi
}

main() {
    check_poetry

    if [ ! -d ".venv" ]; then
        echo "Creating new virtual environment..."
        poetry config virtualenvs.in-project true
        poetry install
    else
        echo "Virtual environment already exists. Updating dependencies..."
        poetry update
    fi

    echo -e "\nSetup complete! You can now run the docs updater using:"
    echo "poetry run python docs_updater.py"
}

main