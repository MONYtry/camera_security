from camera import Camera
from human_tracker import Tracker
from yolo_detector import YOLODetector
from face_Detector import FaceDetector
import math 
import time
import cv2


camera = Camera()

tracker = Tracker()
yolo = YOLODetector()
face = FaceDetector()


def calc_fps(end,start):

    fps = math.ceil(1 / (end - start))
    
    if fps < 10:
        cv2.putText(
            annotated_frame,
            f"FPS: {fps}, critical",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
            )
        print(f"Hey you've only got {fps} fps, lower your settings")
    else:
        cv2.putText(
            annotated_frame,
            f"FPS: {fps}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
            )   


while True:
    # FPS Start
    start = time.time()

    ret, frame = camera.read()
    
    if not ret:
        break


    annotated_frame = frame.copy()

    
    # YOLO detects human 
    result = yolo.detect(annotated_frame)

    # Tracker uses the result and creates an UI
    human = tracker.humanrecognition(annotated_frame,result)

    # FACE Tracking
    faces = face.detect_Face(frame,annotated_frame)

   
    # FPS End 
    end = time.time()
    calc_fps(end,start)
        

    cv2.imshow(
        "Camera Overview",
        annotated_frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

