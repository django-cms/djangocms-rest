#!/bin/bash

# Live documentation server script
# This script starts sphinx-autobuild for live documentation development

echo "Starting live documentation server with auto-reload..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"

# Change to the docs directory if not already there
if [ ! -f "conf.py" ]; then
    if [ -d "docs" ]; then
        cd docs
    else
        echo "Error: conf.py not found. Please run this script from the project root or docs directory."
        exit 1
    fi
fi

# Start sphinx-autobuild
poetry run sphinx-autobuild . _build/html --port 8000 --host 0.0.0.0 --open-browser 