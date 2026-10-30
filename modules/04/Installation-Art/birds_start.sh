#!/bin/bash

# This script is for starting the birds program

# Sleep for a few seconds to ensure RPi establishes netowork connection
sleep 3

# Run from the folder this script lives in, so relative paths work. Exit if directory doesn't exist
cd "$(dirname "$0")" || exit 1

echo "Starting Birds program..."

# Launch birds program
python main.py

# Make note when program ends
echo "Birds program terminated"
