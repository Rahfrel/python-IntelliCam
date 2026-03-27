import streamlit as st
import cv2
import torch
from utils import save_image, save_video_clip
from playsound import playsound
import numpy as np

st.set_page_config(page_title="Système intelligent AI", layout="wide")
st.title("Surveillance intelligente – Détection d'objets & alertes")

# Charger modèle YOLOv5/YOLOv8 pré-entraîné
@st.cache_resource
def load_model():
    return torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model = load_model()

# Initialiser webcam
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
if not cap.isOpened():
    st.error("Impossible d'accéder à la webcam")
    st.stop()

# Paramètres utilisateur
alert_objects = st.multiselect(
    "Objets pour déclencher alerte",
    options=list(model.names.values()),
    default=["cell phone","bottle"]
)
manual_capture = st.button("Capturer image manuellement")
save_videos = st.checkbox("Enregistrer clips vidéo automatiquement")

# Variables pour enregistrement
recording = False
video_frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Impossible de lire la webcam")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(rgb_frame)
    annotated_frame = results.render()[0]

    # Compteur objets détectés
    detected_labels = [model.names[int(box[5])] for box in results.xyxy[0]]
    counts = {label: detected_labels.count(label) for label in set(detected_labels)}
    st.sidebar.write("Objets détectés:", counts)

    # Alertes visuelles + sonores
    if any(obj in detected_labels for obj in alert_objects):
        cv2.putText(annotated_frame, "ALERTE!", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        playsound("alert.mp3", block=False)
        if save_videos:
            recording = True

    # Capture manuelle d'image
    if manual_capture:
        path = save_image(annotated_frame)
        st.success(f"Image sauvegardée: {path}")
        manual_capture = False

    # Enregistrement vidéo automatique
    if recording:
        video_frames.append(frame)
        if len(video_frames) > 100:  # ~5 sec à 20 fps
            filename = save_video_clip(video_frames, (frame.shape[1], frame.shape[0]))
            st.success(f"Clip vidéo sauvegardé: {filename}")
            video_frames = []
            recording = False

    # Affichage en direct
    FRAME_WINDOW.image(annotated_frame)

    # Sortie
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()