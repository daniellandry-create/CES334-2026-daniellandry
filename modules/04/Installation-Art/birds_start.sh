#!/bin/bash

# This script is for starting the birds program

# Run from the folder this script lives in, so relative paths work. $0 is env variable containing path to script
cd "$(dirname "$0")" || exit 1  #Exit if directory doesn't exist

echo "Sleeping 20 for Bluetooth"

sleep 20

# Start virtual environment so sounddevice can be installed
echo "Starting Birds program..."

# Launch birds programs
python bird_receiver.py &
.venv/bin/python -u main.py &

wait

# Make note when program ends
echo "Birds program terminated"
