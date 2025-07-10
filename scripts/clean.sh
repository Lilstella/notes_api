#!/bin/bash
shopt -s globstar

echo "🎈 Cleaning tempory files..."

rm -rf .pytest_cache
rm -rf **/__pycache__
rm -rf tmp/

echo "✅ Complete cleaning."
