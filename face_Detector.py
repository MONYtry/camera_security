import cv2
import time
import mediapipe as mp

from deepface import DeepFace
from config import EMOTION_DELAY,RED
from drawing import draw_box, draw_text




class FaceDetector:

    def __init__(self):

        # create Mediapipe Facedetction 
        mp_face = mp.solutions.face_detection

        # Settings for Detection
        self.face_detector = mp_face.FaceDetection(
            # Human Model
            model_selection=1,
            # Confidence for Human Face
            min_detection_confidence=0.6
        )


        # Placeholder for Emotions
        self.display_emotion = "Unknown"

        # Timer
        self.last_emotion = 0



    def detect_Face(self, frame, annotated_frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        results = self.face_detector.process(rgb)


        gesichter = 0


        if results.detections:

            gesichter = len(results.detections)


            for face in results.detections:

                # returns needed values for calculating the Box and Text
                x1,x2,y1,y2 = self.get_box_size(face,annotated_frame)
                
                # Isnt recomended for low tier Computers
                # More Infomations in Readme.md
                self.track_emotions(annotated_frame,y1,y2,x1,x2)

                # Creates an Box
                draw_box(
                    annotated_frame,
                    x1,
                    y1,
                    x2,
                    y2,
                    RED
                )

                # Creates an Text above the Box and displays the current emotion
                draw_text(
                    annotated_frame,
                    f"FACE | {self.display_emotion}",
                    x1,
                    y1-10,
                    RED
                )


        return gesichter

    # An function for Tracking the face 
    def track_emotions(self,frame,y1,y2,x1,x2):

        # Uses an delay (better perfomance, but you could remove it) 
        if time.time() - self.last_emotion > EMOTION_DELAY:

            # Sets the Size
            face_image = frame[y1:y2,x1:x2]

            # If size isnt nothing
            if face_image.size > 0:

                try:
                    # tries to get an emotion from the face
                    # it might lag for a blink
                    result = DeepFace.analyze(
                    face_image,
                    actions=["emotion"],
                    enforce_detection=False
                    )

                    # safes the tracked Emotion
                    emotion = result[0]["dominant_emotion"]

                    # sets it in an String
                    self.display_emotion = emotion

                    # Timer
                    self.last_emotion = time.time()



                except Exception as e:

                    print("Emotion Error!:", e)

    # Helps you to get the size of any box
    def get_box_size(self,face,frame):
        # creates variable
        box = face.location_data.relative_bounding_box
    
        # Calculates the Box Size
        h,w,_ = frame.shape
    
        # Coordinates
        x1 = int(box.xmin*w)
        y1 = int(box.ymin*h)
    
        x2 = int((box.xmin+box.width)*w)
        y2 = int((box.ymin+box.height)*h)
    
    
        # Borders check
        x1 = max(0,x1)
        y1 = max(0,y1)
        x2 = min(w,x2)
        y2 = min(h,y2)
        
        # And finally gives back the value of the calculations
        return x1,x2,y1,y2