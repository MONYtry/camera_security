from ultralytics import YOLO


class YOLODetector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")


    def detect(self, frame):

        results = self.model.track(
            frame,
            classes=[0],
            conf=0.3,
            persist=True,
            verbose=False
        )

        return results