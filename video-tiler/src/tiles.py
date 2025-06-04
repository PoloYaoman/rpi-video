from moviepy import VideoFileClip, clips_array
import os

def create_tiled_video(video_clips, output_file, grid_shape):
    """
    Create a tiled video from a list of video clips and save it to the specified output file.
    
    :param video_clips: List of VideoFileClip objects to be tiled.
    :param output_file: Path to the output video file.
    :param grid_shape: Tuple indicating the number of rows and columns in the tile layout.
    """
    # Arrange clips in a grid format
    tiled_clips = clips_array([video_clips[i:i + grid_shape[1]] for i in range(0, len(video_clips), grid_shape[1])])
    
    # Write the result to a file
    tiled_clips.write_videofile(output_file, codec='libx264')

def extract_clips_from_directory(directory, clip_duration=5):
    """
    Extract short clips from all video files in the specified directory.
    
    :param directory: Path to the directory containing video files.
    :param clip_duration: Duration of each clip in seconds.
    :return: List of VideoFileClip objects.
    """
    video_clips = []
    
    for filename in os.listdir(directory):
        if filename.endswith(('.mp4', '.avi', '.mov')):
            video_path = os.path.join(directory, filename)
            video = VideoFileClip(video_path)
            # Extract a short clip from the beginning of the video
            clip = video.subclip(0, min(clip_duration, video.duration))
            video_clips.append(clip)
    
    return video_clips