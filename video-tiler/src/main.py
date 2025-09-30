
import os
import cv2
# import moviepy as mp
import numpy as np

import argparse
# from tqdm import tqdm

# from moviepy import ImageClip


def get_video_files(directory):
    """Retrieves all video files from the specified directory."""

    if not os.path.isdir(directory):
        raise ValueError(f"The specified directory does not exist: {directory}")
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    return [os.path.join(directory, f) for f in sorted(os.listdir(directory)) 
            if os.path.splitext(f)[1].lower() in video_extensions] # get everything that ends with the video extensions


def resize_with_aspect_ratio(frame, target_width, target_height):
    """Resize the frame to fit within the target dimensions while maintaining aspect ratio."""
    h, w = frame.shape[:2]
    scale = min(target_width / w, target_height / h)  # Scale to fit within the cell
    new_width = int(w * scale)
    new_height = int(h * scale)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame, new_width, new_height


def prompt_for_titles(video_files):
    """Prompt the user to enter a title for each video file."""
    titles = []
    print("Enter a title for each video (leave blank to use filename):")
    for path in video_files:
        base = os.path.basename(path)
        title = input(f"Title for '{base}': ").strip()
        if not title:
            title = os.path.splitext(base)[0]
        titles.append(title)
    return titles


def create_grid_frame(
    frames, 
    grid_size, 
    output_resolution=(1920, 1080), 
    background_color=(0, 0, 0),
    titles=None
):
    """Creates a fixed-resolution grid frame with thumbnails resized to fit their cells."""

    grid_frame = np.zeros((output_resolution[1], output_resolution[0], 3), dtype=np.uint8)
    cell_width = output_resolution[0] // grid_size[0]
    cell_height = output_resolution[1] // grid_size[1]

    for i, img in enumerate(frames):
        if i >= grid_size[0] * grid_size[1]:
            break  # Stop if we exceed the grid size
        row = i // grid_size[0]
        col = i % grid_size[0]
        x_start = col * cell_width
        y_start = row * cell_height

        if img is not None:
            resized_img, new_width, new_height = resize_with_aspect_ratio(img, cell_width-50, cell_height-70)
            # Center the resized image in the cell, leave space for title
            x_offset = x_start + (cell_width - new_width) // 2
            y_offset = y_start + (cell_height - new_height - 20) // 2
            grid_frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_img
        else:
            # Fill with background color if the image is None
            grid_frame[y_start:y_start + cell_height, x_start:x_start + cell_width] = background_color

        # Draw title if provided
        if titles and i < len(titles):
            title_text = titles[i]
            font = cv2.FONT_HERSHEY_COMPLEX
            font_scale = 1.0
            font_thickness = 2
            text_size, _ = cv2.getTextSize(title_text, font, font_scale, font_thickness)
            text_x = x_start + (cell_width - text_size[0]) // 2
            text_y = y_start + cell_height - 10
            cv2.putText(grid_frame, title_text, (text_x, text_y), font, font_scale, (255,255,255), font_thickness, cv2.LINE_AA)
    
    cv2.imwrite('output/display_frame.jpg', grid_frame)
    return grid_frame


def extract_frame(video_file):
    """Extracts a random frame from a video file"""

    video = cv2.VideoCapture(video_file)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        video.release()
        return []

    random_frame_idx = np.random.randint(0, total_frames)
    video.set(cv2.CAP_PROP_POS_FRAMES, random_frame_idx)
    ret, frame = video.read()
    video.release()

    if ret:
        return [frame]
    else:
        return []


def main(directory, output_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    video_files = get_video_files(directory)
    all_frames = []

    for video_file in video_files:
        print(f"Processing video: {video_file}...")
        frame = extract_frame(video_file)
        all_frames.extend(frame)

    titles = None
    if titles is None:
        titles = prompt_for_titles(video_files)

    # create_tiled_video(all_clips, output_file, titles=titles)
    create_grid_frame(all_frames, (3,2), output_resolution=(1920,1080), titles=titles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a visualiser for multiple clips and packs videos for RPI display.")
    parser.add_argument("directory", help="Directory containing video files.")
    args = parser.parse_args()

    # input_directory = "video-tiler/example_videos"
    output_video_file = "output/tiled_video.mp4"
    main(args.directory, output_video_file)