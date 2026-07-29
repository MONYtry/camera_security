import cv2
from config import BLUE
import math

FONT = cv2.FONT_HERSHEY_SIMPLEX
MOVMENT_TOLERANCE = 20

def draw_box(frame,x1,y1,x2,y2,color):

    cv2.rectangle(
        frame,
        (int(x1),int(y1)),
        (int(x2),int(y2)),
        color,
        2
    )


def draw_text(frame,text,x,y,color):

    cv2.putText(
        frame,
        text,
        (int(x),int(y)),
        FONT,
        0.8,
        color,
        2
    )



def drawWalkPath(frame, track_history, person_id, cx, cy):

    if person_id not in track_history:
        track_history[person_id] = []


    history = track_history[person_id]


    # Wenn es schon eine Position gibt
    if len(history) > 0:

        last_x, last_y = history[-1]


        distance = math.sqrt(
            (cx-last_x)**2 +
            (cy-last_y)**2
        )


        # Person bewegt sich nicht genug
        if distance < MOVMENT_TOLERANCE:
            return



    # Neue Position speichern
    history.append((cx,cy))


    if len(history) > 50:
        history.pop(0)



    # Linie zeichnen
    for i in range(len(history)-1):

        cv2.line(
            frame,
            history[i],
            history[i+1],
            BLUE,
            4
        )