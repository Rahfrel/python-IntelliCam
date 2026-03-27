import cv2
from playsound import playsound
from config import alert_sound

def trigger_alert(frame, text="ALERTE!"):
    cv2.putText(frame, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
    playsound(alert_sound, block=False)
    return frame