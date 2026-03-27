import streamlit as st
import cv2
import yaml
from detection.yolo_model import YOLODetector
from detection.tracker import ObjectTracker
from storage.save_image import save_image
from storage.save_video import save_video_clip
from alerts.sound_alert import trigger_alert
from analytics.counter import count_objects

# Charger config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

ALERT_OBJECTS = config['alert_objects']
VIDEO_PATH = config['video_path']
IMAGE_PATH = config['image_path']
CAM_WIDTH = config['cam_width']
CAM_HEIGHT = config['cam_height']
FPS = config['fps']
VIDEO_CLIP_LENGTH = config['video_clip_length']

st.set_page_config(page_title="SmartVisionAI", layout="wide")
st.title("SmartVisionAI – Système de surveillance intelligent")

# Initialisation
detector = YOLODetector()
tracker = ObjectTracker()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
FRAME_WINDOW = st.image([])

video_frames = []
recording = False
manual_capture = st.button("Capturer image manuellement")
save_videos = st.checkbox("Enregistrer clips vidéo automatiquement")

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Impossible de lire la webcam")
        break

    annotated_frame, detected_labels = detector.predict(frame)
    counts = count_objects(detected_labels)
    st.sidebar.write("Objets détectés:", counts)

    # Alerte
    if any(obj in detected_labels for obj in ALERT_OBJECTS):
        annotated_frame = trigger_alert(annotated_frame)
        if save_videos:
            recording = True

    # Capture manuelle
    if manual_capture:
        path = save_image(annotated_frame, IMAGE_PATH)
        st.success(f"Image sauvegardée: {path}")
        manual_capture = False

    # Enregistrement vidéo automatique
    if recording:
        video_frames.append(frame)
        if len(video_frames) >= VIDEO_CLIP_LENGTH:
            save_video_clip(video_frames, (frame.shape[1], frame.shape[0]), VIDEO_PATH, FPS)
            video_frames = []
            recording = False

    FRAME_WINDOW.image(annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()