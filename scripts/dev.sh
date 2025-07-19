#!/bin/bash
set -e

USE_DEV=false

# Parse optional flags
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --dev) USE_DEV=true ;;
        *) echo "❌ Unknown option: $1" ; exit 1 ;;
    esac
    shift
done

echo "🐍 Setting up virtual environment..."
if [[ ! -d "venv" ]]; then
  python -m venv venv
fi

if [[ -d "venv/bin" ]]; then
    source venv/bin/activate
else
    source venv/Scripts/activate
fi

echo "⬆️  Upgrading pip..."
pip install --upgrade pip

if $USE_DEV; then
    echo "📦 Installing development dependencies..."
    pip install -r requirements-dev.txt
else
    echo "📦 Installing runtime dependencies..."
    pip install -r requirements.txt
fi

echo "🔍 Checking dependency compatibility..."
pip check

echo "🧹 Formatting code..."
black app/

echo "🔎 Type checking..."
mypy --config-file=config/mypy.ini app/

echo "🔎 Running linters..."
flake8 --config=config/.flake8 app/

echo "🧪 Running tests..."
pytest -c config/pytest.ini

echo "✅ All checks passed!"
