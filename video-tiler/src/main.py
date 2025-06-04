import os
import cv2
import moviepy as mp
import numpy as np

from moviepy import ImageClip


def get_video_files(directory):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]

def extract_clips(video_file, clip_duration=5, frame_step=2):
    """
    Extracts clips from a video file, sampling every `frame_step` frames.
    """
    clips = []
    video = cv2.VideoCapture(video_file)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    clip_frames = int(clip_duration * fps // frame_step)

    for start_frame in range(0, total_frames, clip_frames * frame_step):
        frames = []
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        for i in range(clip_frames):
            ret, frame = video.read()
            if not ret:
                break
            if i % frame_step == 0:
                frames.append(frame)
            # Skip frames to reduce memory usage
            for _ in range(frame_step - 1):
                video.read()
        if frames:
            clips.append(frames)

    video.release()
    return clips


def create_tiled_video(clips, output_file, grid_size=(2, 3), fps=30):
    tiled_clips = []
    for i in range(0, len(clips), grid_size[0] * grid_size[1]):
        grid_clips = clips[i:i + grid_size[0] * grid_size[1]]
        tiled_frame = create_grid_frame(grid_clips, grid_size)
        # Convert NumPy array to ImageClip with explicit duration
        frame_duration = 1 / fps 
        tiled_clips.append(ImageClip(tiled_frame).with_duration(frame_duration))

    final_video = mp.concatenate_videoclips(tiled_clips)
    final_video.write_videofile(output_file,fps)


def create_grid_frame(
    clips, 
    grid_size, 
    output_resolution=(1920, 1080), 
    background_color=(0, 0, 0)
):
    """
    Creates a fixed-resolution grid frame with clips resized to fit their cells.
    
    Args:
        clips: List of video clips (each clip is a list of frames).
        grid_size: (rows, cols) for the grid.
        output_resolution: (width, height) of the output frame (default: 1080p).
        background_color: RGB color for padding (default: black).
    
    Returns:
        A fixed-size grid frame with clips resized to fit their cells.
    """
    width, height = output_resolution
    rows, cols = grid_size
    
    # Initialize output frame
    grid_frame = np.full((height, width, 3), background_color, dtype=np.uint8)
    
    # Pre-calculate cell dimensions
    cell_w, cell_h = width // cols, height // rows
    
    for idx, clip in enumerate(clips[:rows * cols]):  # Avoid overflows
        row, col = divmod(idx, cols)
        
        for frame in clip:
            # Resize frame to fit cell (maintaining aspect ratio)
            h, w = frame.shape[:2]
            scale = min(cell_w / w, cell_h / h)
            new_size = (int(w * scale), int(h * scale))  # (width, height)
            resized = cv2.resize(frame, new_size)
            
            # Center the resized frame in the grid cell
            x = col * cell_w + (cell_w - new_size[0]) // 2
            y = row * cell_h + (cell_h - new_size[1]) // 2
            grid_frame[y:y+new_size[1], x:x+new_size[0]] = resized
    
    return grid_frame


def main(directory, output_file):
    video_files = get_video_files(directory)
    all_clips = []

    for video_file in video_files:
        clips = extract_clips(video_file)
        all_clips.extend(clips)

    create_tiled_video(all_clips, output_file)

if __name__ == "__main__":
    input_directory = "video-tiler/example_videos"
    output_video_file = "output/tiled_video.mp4"
    main(input_directory, output_video_file)