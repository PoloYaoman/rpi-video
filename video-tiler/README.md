# Video Tiler

This project is designed to take short clips from all video files in a specified directory and create a new video file where these clips are displayed in a tiled format.

## Project Structure

```
video-tiler
├── src
│   ├── main.py          # Entry point of the application
│   ├── video_utils.py   # Utility functions for video handling
│   └── tiles.py         # Functions for creating tiled video layouts
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/video-tiler.git
   cd video-tiler
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place your video files in a directory.
2. Modify the `src/main.py` file to specify the path to your video directory.
3. Run the application:
   ```
   python src/main.py
   ```

## Features

- Extracts short clips from video files.
- Creates a tiled video layout from the extracted clips.
- Supports various video formats.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.