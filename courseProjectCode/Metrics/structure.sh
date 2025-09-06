#!/bin/bash

# Calculating SLOC and comment density using radon's raw output. (C % S) is the total comment density for all source lines.
if ! command -v radon &>/dev/null; then
    echo "radon is not installed. Install with: pip install radon"
    exit 1
fi

echo "Calculating comment density for Python files..."
radon raw -s ../../ | awk '/SLOC:/ {sloc=$2} /Comments:/ {comments=$2} /\(C % S\)/ {density=$4} END {print "SLOC:", sloc,", Comments:", comments,", Density:", density}'

echo
echo "Calculating cyclomatic complexity for Python files..."
PYTHONWARNINGS="ignore" radon cc -s -a ../../ | grep -i average
