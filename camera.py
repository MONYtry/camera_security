import cv2

from config import CAM_WIDTH, CAM_HEIGHT


class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAM_WIDTH
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAM_HEIGHT
        )
        
        if not self.cap.isOpened():
            raise Exception("Camera couldnt be opend!")

    
    def read(self):

        ret, frame = self.cap.read()

        return ret, frame


    def release(self):

        self.cap.release()