import cv2 as cv
import numpy as np

body_cascade = cv.CascadeClassifier(r'c:\Users\Albert\Documents\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')

class joint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def findjoint_Tracking(gray):
    bodpart = body_cascade.detectMultiScale(gray)

def drawjoint(joint, frame):
    cv.circle(frame, (joint.x, joint.y), 10, (0, 0, 255), 2)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()