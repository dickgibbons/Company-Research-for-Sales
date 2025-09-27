#!/bin/bash

# EPAM Business Intelligence System Launcher
# Simple shell script to launch the GUI

echo "🏢 EPAM Business Intelligence System"
echo "======================================"
echo ""
echo "Starting GUI launcher..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Try to run the Python GUI launcher
if command -v python3 &> /dev/null; then
    python3 launch_epam_agents.py
elif command -v python &> /dev/null; then
    python launch_epam_agents.py
else
    echo "❌ Error: Python not found!"
    echo "Please install Python 3.8+ to run this system."
    exit 1
fi