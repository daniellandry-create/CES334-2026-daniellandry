#!/bin/bash
PAGE="file:///home/stu3340/Documents/repos/CES334-2026-daniellandry/modules/01/generativeArt/index.html"

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"

exec chromium --kiosk --ozone-platform=wayland --noerrdialogs \
  --disable-infobars --no-first-run --password-store=basic "$PAGE"


