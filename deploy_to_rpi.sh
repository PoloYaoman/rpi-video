#!/bin/bash

# 1. Ask for a directory and copy all videos to input_videos
read -p "Enter the directory containing your videos: " VIDEOSRC
mkdir -p input_videos
find "$VIDEOSRC" -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mov" -o -iname "*.mkv" \) -exec cp {} input_videos/ \;

# 2. Install required dependencies via pipx
echo "Installing dependencies with pipx..."
pip install -r video-tiler/requirements.txt || pipx inject $(basename $(pwd)) -r video-tiler/requirements.txt

# 3. Run the video tiler program with input_videos as argument
echo "Running video tiler..."
python3 video-tiler/src/main.py input_videos

# 4. Ask for Raspberry Pi host and user
read -p "Enter Raspberry Pi hostname or IP: " RPI_HOST
read -p "Enter Raspberry Pi username: " RPI_USER

# 5. Copy output, input_videos, and display-selector to ~/rpi-video on the Pi
echo "Copying files to Raspberry Pi..."

scp -r output input_videos display-selector launch_vid.bash "$RPI_USER@$RPI_HOST:~/rpi-video/"

echo "Deployment complete! Restart your RPI!"