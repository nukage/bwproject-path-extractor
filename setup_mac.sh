#!/bin/bash
echo "Setting up Bitwig Path Extractor environment..."

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed."
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Create venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo -e "\nSetup complete! Use ./run_gui.sh to start the application."
chmod +x run_gui.sh
