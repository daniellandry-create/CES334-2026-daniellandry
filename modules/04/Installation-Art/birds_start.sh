#!/bin/bash

# This script is for starting the birds program

# Run from the folder this script lives in, so relative paths work. $0 is env variable containing path to script
cd "$(dirname "$0")" || exit 1  #Exit if directory doesn't exist

# Wait for a Bluetooth audio sink
#while true; do
#    SINK=$(pactl list short sinks 2>/dev/null |
#        awk '$2 ~ /^bluez_output/ {print $2; exit}')
#
#    if [ -n "$SINK" ]; then
#        break
#    fi
#
#    echo "Waiting for bluetooth..."
#    sleep 2
#done

#pactl set-default-sink "$SINK"

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
