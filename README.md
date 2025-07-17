# rpi-video

This repository contains code that renders a video selector, designed for use with a Raspberry Pi setup.


## Project Structure

- `deploy_to_rpi.sh` — Ready-to-use script to deploy the project to a Raspberry Pi.
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

The installation can also be performed manually:

### 1. Video Tiler
Processes input videos and creates a tiled output video.

- Place your input videos in the `input_videos/` directory.
- Run the tiler script:
  ```bash
  cd video-tiler/src
  python main.py
  ```
- The output will be saved in the `output/` directory.

### 2. Display Selector
Lets the user select a video to play. Should be run from a Raspberry Pi, where folders `display-selector`, `input_videos`and `output` must be copied.

- Run the display selector script:
  ```bash
  cd display-selector
  python main.py
  ```

### 3. Deploy to Raspberry Pi

- Use the provided shell script to deploy the project:
  ```bash
  ./deploy_to_rpi.sh
  ```


## Requirements

- Python 3.x
- See `requirements.txt` in each subfolder for dependencies.
