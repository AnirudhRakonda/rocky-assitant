#!/bin/bash
# Quick start script for Rocky Assistant
# Run from project root: ./start.sh

cd "$(dirname "$0")" || exit 1

echo "🎵 Rocky Assistant - Starting..."
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running!"
    echo "Start it in another terminal with: ollama serve"
    echo ""
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found"
    echo "Create it with: python3 -m venv venv"
    exit 1
fi

# Run from project root (not app directory)
if [ "$1" == "--list-devices" ]; then
    python app/main.py --list-devices
elif [ "$1" == "--test" ]; then
    python app/main.py --test "$2"
elif [ "$1" == "--debug" ]; then
    python app/main.py --debug
else
    python app/main.py
fi
