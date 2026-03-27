import os
from PIL import Image
from datetime import datetime

def save_image(frame, folder="captured_images/"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"image_{timestamp}.jpg")
    img = Image.fromarray(frame)
    img.save(path)
    return path