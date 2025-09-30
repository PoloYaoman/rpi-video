import cv2
import os

import subprocess


def highlight_grid(frame, selected_idx, grid_shape=(3,2)):
    """Draws a yellow rectangle around the selected grid cell."""
    h, w, _ = frame.shape
    cell_w = w // grid_shape[0]
    cell_h = h // grid_shape[1]
    row = selected_idx // grid_shape[0]
    col = selected_idx % grid_shape[0]
    x1 = col * cell_w + 30
    y1 = row * cell_h + 20
    x2 = x1 + cell_w - 60
    y2 = y1 + cell_h - 70
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,255), 8)
    return frame


def play_selected_video(video_path):
    """Opens the selected video in VLC player."""

    vlc_command = [
        "cvlc",
        "--fullscreen",
        "--play-and-exit",
        video_path
    ]
    
    try:
        # Run VLC and wait for it to finish
        proc = subprocess.Popen(vlc_command)
        proc.wait()  # Pause until video playback is done
    except FileNotFoundError:
        print("VLC is not installed or not found in PATH.")


def main():
    # Paths
    video_dir = "input_videos"
    image_path = "output/display_frame.jpg"
    video_files = [os.path.join(video_dir, f) for f in sorted(os.listdir(video_dir))
                    if os.path.splitext(f)[1].lower() in ['.mp4', '.avi', '.mov', '.mkv']]
    
    selected_idx = 0
    grid_shape = (3,2)
    mouse_state = {'selected_idx': selected_idx, 'play': False}

    # Load the static grid image
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Could not load image: {image_path}")
        return

    def mouse_callback(event, x, y, flags, param):
        frame_h, frame_w = param['frame_shape'][:2]
        cell_w = frame_w // grid_shape[0]
        cell_h = frame_h // grid_shape[1]
        col = (x - 30) // cell_w
        row = (y - 30) // cell_h
        # Clamp col/row to grid
        col = max(0, min(grid_shape[0]-1, col))
        row = max(0, min(grid_shape[1]-1, row))
        idx = row * grid_shape[0] + col
        if idx < len(video_files):
            mouse_state['selected_idx'] = idx
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse_state['play'] = True

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("window", mouse_callback, param={'frame_shape': frame.shape})

    while True:
        display_frame = frame.copy()
        highlight_grid(display_frame, mouse_state['selected_idx'], grid_shape)
        cv2.imshow("window", display_frame)
        key = cv2.waitKeyEx(1)
        if key == ord('q'):
            break
        if mouse_state['play']:
            video_to_play = video_files[mouse_state['selected_idx']]
            if video_to_play and os.path.exists(video_to_play):
                play_selected_video(video_to_play)
            mouse_state['play'] = False

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()