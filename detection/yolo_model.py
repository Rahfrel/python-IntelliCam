import torch

class YOLODetector:
    def __init__(self, model_name='yolov5s', pretrained=True):
        self.model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=pretrained)

    def predict(self, frame):
        results = self.model(frame)
        annotated_frame = results.render()[0]
        detected_labels = [self.model.names[int(box[5])] for box in results.xyxy[0]]
        return annotated_frame, detected_labels