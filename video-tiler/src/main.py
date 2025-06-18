import os
import cv2
import moviepy as mp
import numpy as np

import argparse

from moviepy import ImageClip


def get_video_files(directory):
    """Retrieves all video files from the specified directory."""

    if not os.path.isdir(directory):
        raise ValueError(f"The specified directory does not exist: {directory}")
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions] # get everything that ends with the video extensions


def extract_clips(video_file, clip_duration=5, fps=30, frame_step=1):
    """Extracts clips from a video file, sampling every `frame_step` frames."""

    clips = []
    video = cv2.VideoCapture(video_file)
    # fps = video.get(cv2.CAP_PROP_FPS)
    # total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    clip_frames = int(clip_duration * fps // frame_step) # get number of frames for the clip 

    frames = []
    for i in range(0, clip_frames, frame_step):
        video.set(cv2.CAP_PROP_POS_FRAMES, i) # set the next starting frame for the clip
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)

    if frames:
        clips.append(frames)

    video.release()
    return clips


def create_tiled_video(clips, output_file, grid_size=(3,2), titles=None, fps=30):
    """Creates a tiled video from a list of clips."""

    tiled_clips = []
    total_frames = fps*5

    # for i in range(0, len(clips)):
    grid_clips = clips[0:min(grid_size[0] * grid_size[1], len(clips))]
    valid_clips = [clip for clip in grid_clips if clip]  # Filter out invalid or empty clips

    for frame in range(total_frames):
        tiled_frame = create_grid_frame(valid_clips, frame, grid_size, titles=titles)
        # Convert NumPy array to ImageClip with explicit duration
        if isinstance(tiled_frame, np.ndarray) and tiled_frame.ndim == 3:
            tiled_clips.append(ImageClip(tiled_frame).with_duration(1/fps))
        else:
            raise ValueError("Invalid tiled_frame: Expected a 3-dimensional NumPy array representing an image.")
        # tiled_clips.append(ImageClip(tiled_frame).with_duration(1/fps))

    final_video = mp.concatenate_videoclips(tiled_clips)
    final_video.write_videofile(output_file, fps=fps, codec='libx264', bitrate='2000k')


def resize_with_aspect_ratio(frame, target_width, target_height):
    """Resize the frame to fit within the target dimensions while maintaining aspect ratio."""
    h, w = frame.shape[:2]
    scale = min(target_width / w, target_height / h)  # Scale to fit within the cell
    new_width = int(w * scale)
    new_height = int(h * scale)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame, new_width, new_height


def create_grid_frame(
    clips, 
    frame_index,
    grid_size, 
    output_resolution=(1920, 1080), 
    background_color=(0, 0, 0),
    titles=None
):
    """Creates a fixed-resolution grid frame with clips resized to fit their cells."""

    grid_frame = np.zeros((output_resolution[1], output_resolution[0], 3), dtype=np.uint8)
    cell_width = output_resolution[0] // grid_size[0]
    cell_height = output_resolution[1] // grid_size[1]

    for i, clip in enumerate(clips):
        if i >= grid_size[0] * grid_size[1]:
            break  # Stop if we exceed the grid size
        row = i // grid_size[0]
        col = i % grid_size[0]
        x_start = col * cell_width
        y_start = row * cell_height

        if frame_index < len(clip):
            frame = clip[frame_index]
            resized_frame, new_width, new_height = resize_with_aspect_ratio(frame, cell_width-50, cell_height-50)
            
            # Center the resized frame in the cell
            x_offset = x_start + (cell_width - new_width) // 2
            y_offset = y_start + (cell_height - new_height) // 2
            grid_frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_frame
        
        else:
            # Fill with background color if the clip does not have enough frames
            grid_frame[y_start:y_start + cell_height, x_start:x_start + cell_width] = background_color
    
    return grid_frame


def main(directory, output_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    video_files = get_video_files(directory)
    all_clips = []

    for video_file in video_files:
        clips = extract_clips(video_file)
        all_clips.extend(clips)

    # Read titles from a file if it exists
    # titles_file = os.path.join(directory, 'titles.txt')
    # titles = read_titles(titles_file) if os.path.exists(titles_file) else None
    create_tiled_video(all_clips, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a visualiser for multiple clips and packs videos for RPI display.")
    parser.add_argument("directory", help="Directory containing video files.")
    args = parser.parse_args()

    # input_directory = "video-tiler/example_videos"
    output_video_file = "output/tiled_video.mp4"
    main(args.directory, output_video_file)