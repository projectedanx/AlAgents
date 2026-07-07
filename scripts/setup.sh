#!/bin/bash
# /// file: setup.sh ///
# <think>
# Components: Environment Setup
# Dependencies: pip, python
# Data Flows: N/A
# Function Signatures: N/A
# </think>

set -e

echo "Bootstrapping AI Research Agent environment..."

# Ensure pip is up to date
python -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found."
fi

# Download NLTK data
echo "Downloading NLTK datasets..."
python -c "import nltk; nltk.download('all', quiet=True)"

# Set PYTHONPATH to include src directory for local execution
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
echo "PYTHONPATH set to include $(pwd)/src"

echo "Environment bootstrap complete."
