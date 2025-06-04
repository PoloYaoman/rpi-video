import os
import cv2
import moviepy as mp

def get_video_files(directory):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]

def extract_clips(video_path, start_time, duration):
    video = mp.VideoFileClip(video_path)
    clip = video.subclip(start_time, start_time + duration)
    return clip

def save_clip(clip, output_path):
    clip.write_videofile(output_path, codec='libx264')

def combine_clips(clips, grid_size):
    return mp.concatenate_videoclips(clips, method="compose")

def create_tiled_video(clips, grid_size, output_path):
    tiled_video = combine_clips(clips, grid_size)
    tiled_video.write_videofile(output_path, codec='libx264')