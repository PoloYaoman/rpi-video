# rpi-video

This repository contains code that renders a video selector, designed for use with a Raspberry Pi setup.


## Project Structure

- `deploy_to_rpi.sh` — Ready-to-use script to deploy the project to a Raspberry Pi.
- `launch_vid.bash`— Launch script for rpi, works for Bookworm
- `display-selector/` — Contains the display selector tool.
  - `main.py` — Main script for display selection.
  - `requirements.txt` — Python dependencies for display-selector.
- `input_videos/` — Folder for input video files.
- `output/` — Folder for output tiled video.
- `video-tiler/` — Contains the video tiling tool.
  - `src/main.py` — Main script for video tiling.
  - `requirements.txt` — Python dependencies for video-tiler.
  - `pyvenv.cfg` — Python virtual environment configuration.


## Usage

`deploy_to_rpi.sh` script prepares and renders a program with packed videos that can be copied onto a Raspberry Pi. 

  ```bash
  sh deploy_to_rpi.sh
  ```

Note that this script will overwrite but not delete previously uploaded videos, which will have to be purged manually for the display selector to work properly.

The launch script will be copied to the Raspberry. It was initially intended for a plug-and-play display and can be run on startup. You can use a method of your choice. I achieved that by adding a service to `init.d` : 

  ```bash
  sudo nano /ets/init.d/vidservice
  ```

Copy the following and restart:

  ```bash
  #!/bin/bash
  ### BEGIN INIT INFO
  # Provides: VidService
  # Required-Start: $all
  # Required-Stop:
  # Default-Start:        5
  # Default-Stop:         6
  # Short-Description:    Plays selected video on loop
  ### END INIT INFO

  touch ~/launch_vid1.bash
  ```


The installation can also be performed manually:

### 1. Video Tiler (included in the deploy script)
Processes input videos and creates a tiled output video.

- Place your input videos in the `input_videos/` directory.
- Run the tiler script:
  ```bash
  cd video-tiler/src
  python main.py
  ```
- The output will be saved in the `output/` directory.

### 2. Display Selector (included in the deploy script)
Lets the user select a video to play. Should be run from a Raspberry Pi, where folders `display-selector`, `input_videos`and `output` must be copied.

- Run the display selector script:
  ```bash
  cd display-selector
  python main.py
  ```


## Requirements

- Python 3.x
- See `requirements.txt` in each subfolder for dependencies.
