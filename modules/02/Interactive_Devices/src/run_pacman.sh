#!/bin/bash

# Run from the folder this script lives in, so relative paths work
cd "$(dirname "$0")"

# Point PyGame at the Pi's desktop session
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export WAYLAND_DISPLAY=wayland-0

# Launch the game (swap in your venv's python if you use one)
python3 display_test.py