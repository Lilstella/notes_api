#!/bin/bash
shopt -s globstar

if [[ -z $1 ]]; then
    "❌ Error: You may introduce the mode of the cleaning."
    exit
fi

mode=$1

echo "🎈 Cleaning tempory files..."

if [[ $mode == "tempory_and_storage" ]]; then
    rm -rf .pytest_cache
    rm -rf **/__pycache__
    rm -rf tmp/
    rm -rf storage/

    echo "✅ Complete cleaning."
    exit

elif [[ $mode == "tempory" ]]; then
    rm -rf .pytest_cache
    rm -rf **/__pycache__
    rm -rf tmp/

    echo "✅ Complete cleaning."
    exit

else 
    echo "❌ Error: with the cleaning mode provided"
    exit
fi