import cv2 as cv
import numpy as np

body_cascade = cv.CascadeClassifier(r'C:\Users\Albert\Documents\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')

class joint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def findjoint_Tracking(gray):
    bodpart = body_cascade.detectMultiScale(gray)

def drawjoint(joint, frame):
    cv.circle(frame, (joint.x, joint.y), 10, (0, 0, 255), 2)

def getwinsize(capture):
    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv.CAP_PROP_FPS)
 #   print("W =" + (str)width + "\nH = " + (str)height + "\nfps = " + (str)fps)
    print(f"W = {width} \nH = {height} \nfps = {fps}")
    return width, height

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera")
    exit()
width, height = getwinsize(capture)
while True:
    ret, frame = capture.read() # Capture frame-by-frame, 'ret' is boolean, 'frame' is the actual frame/image
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # frame transforms into grayframe (b&w)
    cv.rectangle(frame, (0,0), (200,200), (23, 255, 200), thickness=-1)
    cv.imshow('frame', grayframe) # Display the resulting frame
    if cv.waitKey(1) == ord('q'):
        break

capture.release() # When everything done, release the capture
cv.destroyAllWindows()