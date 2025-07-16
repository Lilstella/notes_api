#!/bin/bash
set -e

echo "🧹 Formatting code..."
black app/

echo "🔎 Type checking..."
mypy app/

echo "🔎 Running linters..."
flake8

echo "🧪 Running tests..."
pytest