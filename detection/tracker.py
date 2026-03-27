# Simple tracker basé sur centroids pour prototype
import numpy as np

class ObjectTracker:
    def __init__(self):
        self.objects = {}  # id : position

    def update(self, detected_boxes):
        # detected_boxes = list of (x1, y1, x2, y2)
        updated = {}
        for i, box in enumerate(detected_boxes):
            updated[i] = box
        self.objects = updated
        return self.objects