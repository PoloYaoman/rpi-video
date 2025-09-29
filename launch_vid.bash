#!/bin/bash


cd rpi-video/display-selector
#pipx install opencv-python --include-deps
#pipx install numpy --include-deps
python -c "import cv2"
cd ..

if ! xset q &>/dev/null; then
    echo "Starting X server..."
    startx &
    sleep 5  # Wait for X server to initialize
fi

export DISPLAY=:0.0
QT_QPA_PLATFORM=linuxfb python3 display-selector/main.py
