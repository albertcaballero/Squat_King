import cv2 as cv
import numpy as np
import mediapipe as mp

body_cascade = cv.CascadeClassifier(r'C:\Users\Albert\Documents\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')
face_cascade = cv.CascadeClassifier(r'C:\Users\Albert\Documents\opencv\sources\data\haarcascades\haarcascade_frontalface_alt.xml')
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def getwinsize(capture):
    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv.CAP_PROP_FPS)
    print(f"W = {width} \nH = {height} \nfps = {fps}")
    return width, height

def squatinput(frame, results):
    random = 1

def armsimput(frame, results):
    random = 1

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera")
    exit()
width, height = getwinsize(capture)
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        results = holistic.process(frame)
        face = face_cascade.detectMultiScale(grayframe)
        for (x, y, width, height) in face:
            cv.rectangle(frame, (x, y), (x + width, y + height), (0,255,0), 2)
            cv.line(frame, (x + width//2,y + height), (x + width//2,480), (0,255,0), thickness=1)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

capture.release()
cv.destroyAllWindows()


"""
- explore other kinds of cascades (fullbody is dog water)
    - maybe train my own model/cascade???
- see if we can increase the threshold for detection and limit the number of detections (so it only detects 1 body and not random shit)
"""