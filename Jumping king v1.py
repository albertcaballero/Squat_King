import cv2 as cv
import numpy as np

body_cascade = cv.CascadeClassifier(r'C:\Users\Albert\Documents\opencv\sources\data\haarcascades\haarcascade_fullbody.xml')
face_cascade = cv.CascadeClassifier(r'C:\Users\Albert\Documents\opencv\sources\data\haarcascades\haarcascade_frontalface_alt.xml')

class joint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

"""
def findjoint_Tracking(frame):
    artic = body_cascade.detectMultiScale(frame)
    for (x, y, width, height) in artic:
        trackframe = cv.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
    return trackframe
"""

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
    grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#   grayframe = cv.rectangle(grayframe, (0,0), (200,200), (23, 255, 200), thickness=-1) #idk why but grayframe is transforming the square to black
#   grayframe = findjoint_Tracking(grayframe)
    artic = body_cascade.detectMultiScale(grayframe)
    for (x, y, width, height) in artic:
        cv.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

capture.release() # When everything done, release the capture
cv.destroyAllWindows()


"""
- explore other kinds of cascades (fullbody is dog water)
    - maybe train my own model/cascade???
- see if we can increase the threshold for detection and limit the number of detections (so it only detects 1 body and not random shit)
"""