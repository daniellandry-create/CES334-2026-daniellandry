#!/bin/bash

# This script is for starting the birds program

# Sleep for a few seconds to ensure RPi establishes netowork connection
sleep 3

# Run from the folder this script lives in, so relative paths work. $0 is env variable containing path to script
cd "$(dirname "$0")" || exit 1  #Exit if directory doesn't exist

# Start virtual environment so sounddevice can be installed
source .venv/bin/activate

echo "Starting Birds program..."

# Launch birds programs
python bird_receiver.py
python main.py

# Make note when program ends
echo "Birds program terminated"
