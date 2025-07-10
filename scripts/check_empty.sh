re#!/bin/bash

if [[ -z $1 ]]; then
    echo "❌ Error: A directory path must be provided"
    exit
fi

directory=$1

if [[ ! -d $directory ]]; then
    echo "❌ Error: $directory is not a valid directory"
    exit
fi

if find $directory -type f | grep -q .; then
    exit 1
else
    exit 0
fi