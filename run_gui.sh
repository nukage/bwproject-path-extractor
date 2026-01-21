#!/bin/bash
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    ./setup_mac.sh
fi

echo "Starting Bitwig Path Extractor GUI..."
source venv/bin/activate
python3 gui.py
