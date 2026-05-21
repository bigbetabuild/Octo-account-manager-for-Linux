#!/bin/bash

# Roblox Account Manager Installation Script
# This script sets up the application on your Linux system

set -e

echo "Installing Roblox Account Manager for Linux..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create config directory
CONFIG_DIR="$HOME/.config/roblox-account-manager"
mkdir -p "$CONFIG_DIR"
echo "Configuration directory: $CONFIG_DIR"

# Install desktop launcher
DESKTOP_FILE="$HOME/.local/share/applications/roblox-account-manager.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cp roblox-account-manager.desktop "$DESKTOP_FILE"

# Update the Exec path in desktop file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sed -i "s|/path/to/main.py|$SCRIPT_DIR/main.py|g" "$DESKTOP_FILE"

echo "Desktop launcher installed to: $DESKTOP_FILE"

# Make main.py executable
chmod +x main.py

echo ""
echo "Installation complete!"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Or search for 'Roblox Account Manager' in your application menu."
echo ""
echo "First time setup:"
echo "  1. Add your Roblox accounts in the 'Add Account' section"
echo "  2. Verify the Roblox Sober path in Settings"
echo "  3. Launch instances from the Quick Launch tab"
