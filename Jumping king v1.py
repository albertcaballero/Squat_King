import cv2 as cv
import numpy as np
import mediapipe as mp
import win32com.client as kb

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
wsh = kb.Dispatch("WScript.Shell")

def getlandmarks(results):
    LmouthY = results.pose_landmarks.landmark[9].y
    LmouthX = results.pose_landmarks.landmark[9].x
    LhipY = results.pose_landmarks.landmark[23].y
    LhipX = results.pose_landmarks.landmark[23].x
    return LmouthY, LmouthX, LhipY, LhipX


def squatinput(frame, results):
    random = 1


def armsinput(frame, results, win_width, win_height):
    #getting middle
    NoseY = results.pose_landmarks.landmark[0].y
    NoseX = results.pose_landmarks.landmark[0].x
    cv.line(frame, (int(NoseX*win_width), int(NoseY*win_height)), (int(NoseX*win_width), win_height), (0, 0, 255))
    LwristX = results.pose_landmarks.landmark[15].x
    RwristX = results.pose_landmarks.landmark[16].x
    if ((LwristX > NoseX) and (RwristX > NoseX)):
        wsh.SendKeys("L")
    elif ((LwristX < NoseX) and (RwristX < NoseX)):
        wsh.SendKeys("R")


def settings():
    random = 1

def normalize_num(landmarkY, landmarkX):
    landmarkY = landmarkY * 100
    landmarkY = int(landmarkY)
    landmarkX = landmarkX * 100
    landmarkX = int(landmarkX)
    return landmarkY, landmarkX

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera")
    exit()
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        win_height, win_width, c = frame.shape
        grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #    frame.flags.writeable = False #makes frame non editable (readonly), should improve performance
        results = pose.process(frame)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if (results.pose_landmarks):
            LmouthY, LmouthX, LhipY, LhipX = getlandmarks(results)
            cv.circle(frame, (int(LhipX*win_width),int(LhipY*win_height)), 8, (255, 44, 23), -1) #just a test, delete
        #    cv.circle(frame, (int(LmouthX*win_width),int(LmouthY*win_height)), 8, (255, 255, 23), -1) #just a test, delete
            armsinput(frame, results, win_width, win_height)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

capture.release()
cv.destroyAllWindows()


"""
- explore how to work with individual points/joints
- see if we can increase the threshold for detection and limit the number of detections (so it only detects 1 body and not random shit)
- FAILSAFES
    - all 4 hand points (for each hand) need to be detected in order to send lateralmov input - ?
    - t-posing should cancel all lateral movement
    - if not the whole body is detected, pause automatically (whole body is from head to knees)
    - some input to cancel jump ???? -> i dont think it's possible tho
"""