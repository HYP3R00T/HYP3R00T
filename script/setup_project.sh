#!/bin/bash

# Install pre-commit
if ! command -v pre-commit >/dev/null; then
	uv add --dev pre-commit
fi

# Install hooks if not already installed
if [ ! -f .git/hooks/pre-commit ]; then
	pre-commit install
fi

if [ ! -f .git/hooks/commit-msg ]; then
	pre-commit install --hook-type commit-msg
fi
