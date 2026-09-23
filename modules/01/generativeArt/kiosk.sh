#!/usr/bin/env bash

# Disable xset blanking, let xscreensaveer handle that
xset s noblank
xset s off

# Start xscreensaver
xscreensaver &

# Hide the mouse cursor
unclutter -idle 1 -root &

# Let chromium think it always exited cleanly
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' '~/.config/chromium/Default/Preferences'
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' '~/.config/chromium/Default/Preferences'

# Start Chromium 
chromium-browser --kiosk -noerrdialogs --disable-infobars 'file: /home/stu3340/Documents/repos/CES334-2026-daniellandry/modules/01/generativeArt/index.html' &