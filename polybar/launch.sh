#!/bin/sh

# Terminate already running bar instances
killall -q polybar

# Wait until the provesses have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# Launch Polybar, using default config location ~/.config/polybar/config
polybar --reload right &
polybar --reload left

