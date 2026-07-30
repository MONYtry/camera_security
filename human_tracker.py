import cv2
import math

from config import BLUE, RED, GREEN
from drawing import draw_box, draw_text, drawWalkPath


MAX_DISTANCE = 80

class Tracker:

    def __init__(self):
        self.track_history = {}
        self.last_position = {}
        self.next_id = 0


    def get_stable_id(self, detected_id, cx, cy):

        # if YOLO already has an knowen ID
        if detected_id in self.last_position:

            self.last_position[detected_id] = (cx, cy)
            return detected_id


        # Checks if an old id is near the position
        for old_id, (old_x, old_y) in self.last_position.items():

            # Calculates the distance
            distance = math.sqrt((cx - old_x)**2 +(cy - old_y)**2)


            if distance < MAX_DISTANCE:

                self.last_position[old_id] = (cx, cy)

                return old_id



        # new id
        new_id = self.next_id
        self.next_id += 1

        self.last_position[new_id] = (cx, cy)

        return new_id



    def humanrecognition(self, frame, results):

        personen = 0

        if results is None:
            return 0

        for box in results[0].boxes:

            personen += 1


            if box.id is not None:
                yolo_id = int(box.id[0])

            else:
                yolo_id = -1



            x1,y1,x2,y2 = box.xyxy[0]


            cx = int((x1+x2)/2)
            cy = int((y1+y2)/2)



            # own stalbe id
            person_id = self.get_stable_id(
                yolo_id,
                cx,
                cy
            )

            #drawWalkPath(
             #   frame,
              #  self.track_history,
               # person_id,
                #cx-5,
                #cy-5
            #)

            draw_text(
                frame,
                f"ID: {person_id}",
                cx,
                cy,
                RED
            )

            cv2.line(
                frame,
                (cx,cy),
                (cx,cy),
                RED,
                10
            )

            # creates ui
            self.make_ui(frame,box,x1,x2,y1,y2)
        return personen

    

    def make_ui(self,frame,box,x1,x2,y1,y2):

        confidence = float(box.conf[0]) * 100
        display_confidence = round(confidence,1)
                    
        draw_text(frame,f"{display_confidence}%",x1,y1-10,RED)
        if confidence > 80:
            draw_box(
                frame,
                x1,y1,x2,y2,
                GREEN
                )
        elif confidence > 50:
        
            draw_box(
                frame,
                x1,y1,x2,y2,
                BLUE
                )
        else:
            draw_box(
            frame,
            x1,y1,x2,y2,
            RED
            )