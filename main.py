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



while True:
    start = time.time()
    ret, frame = camera.read()
    
    
    if not ret:
        break


    annotated_frame = frame.copy()

    
    # YOLO erkennt Personen
    

    # Tracking
    
    end = time.time()
            
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
        

    cv2.imshow(
        "Camera Overview",
        annotated_frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



camera.release()
cv2.destroyAllWindows()