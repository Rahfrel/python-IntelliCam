import os
from PIL import Image
import cv2
from datetime import datetime

def save_image(frame, folder="captured_images/"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"image_{timestamp}.jpg")
    img = Image.fromarray(frame)
    img.save(path)
    return path

def save_video_clip(frames, frame_size, folder="recorded_videos/", fps=20.0):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"clip_{timestamp}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, frame_size)
    for f in frames:
        out.write(f)
    out.release()
    return filename