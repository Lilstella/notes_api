#!/bin/bash
set -e

echo "🧹 Formatting code..."
black app/

echo "🔎 Type checking..."
mypy --config-file=config/mypy.ini app/

echo "🔎 Running linters..."
flake8 --config=config/.flake8 app/

echo "🧪 Running tests..."
pytest -c config/pytest.ini
