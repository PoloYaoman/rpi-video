import cv2
import os
import numpy as np
import time


def highlight_grid(frame, selected_idx, grid_shape=(3,2)):
    """Draws a yellow rectangle around the selected grid cell."""
    h, w, _ = frame.shape
    cell_w = w // grid_shape[0]
    cell_h = h // grid_shape[1]
    row = selected_idx // grid_shape[0]
    col = selected_idx % grid_shape[0]
    x1 = col * cell_w + 30
    y1 = row * cell_h + 30
    x2 = x1 + cell_w - 60
    y2 = y1 + cell_h - 60
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,255), 8)
    return frame


def play_selected_video(video_path, window_name="window"):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(30)
        if key == ord('q') or key == ord('s'):
            break
    cap.release()


def main():
    # Paths
    video_dir = "video-tiler/example_videos"
    output_video = "output/tiled_video.mp4"
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir)
                   if os.path.splitext(f)[1].lower() in ['.mp4', '.avi', '.mov', '.mkv']]
    
    selected_idx = 0
    grid_shape = (3,2)
    total_cells = grid_shape[0] * grid_shape[1]

    # Start video playback in a dedicated window
    cap = cv2.VideoCapture(output_video)
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    while(cap.isOpened()):
        ret, frame = cap.read() 
        if ret:
            # Highlight the selected cell
            display_frame = frame.copy()
            highlight_grid(display_frame, selected_idx, grid_shape)
            cv2.imshow("window", display_frame)
            time.sleep(1/30)
        else:
            print('no video')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        key = cv2.waitKeyEx(1) #& 0xFF
        if key == ord('q'):
            break
        elif key == 2424832 :  # Left arrow
            # print('left arrow pressed')
            if selected_idx % grid_shape[0] > 0:
                selected_idx -= 1
        elif key == 2555904 :  # Right arrow
            # print('right arrow pressed')
            if selected_idx % grid_shape[0] < grid_shape[0] - 1:
                selected_idx += 1
        elif key == 2490368 :  # Up arrow
            # print('up arrow pressed')
            if selected_idx >= grid_shape[0]:
                selected_idx -= grid_shape[0]
        elif key == 2621440:  # Down arrow
            # print('down arrow pressed')
            if selected_idx < total_cells - grid_shape[0]:
                selected_idx += grid_shape[0]
        elif key == ord('s'):
            video_to_play = video_files[selected_idx]
            if video_to_play and os.path.exists(video_to_play):
                play_selected_video(video_to_play, window_name="window")
                # After playback, re-open the tiled video
                cap.release()
                cap = cv2.VideoCapture(output_video)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()