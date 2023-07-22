import cv2 as cv
import mediapipe as mp
import win32com.client as kb
import tkinter as tk

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

def settings():
    settings_win = tk.Toplevel()
    settings_win.geometry ("400x400")
    settings_win.title("Settings")
    tk.Label(settings_win, text="Edit your settings").pack()
    settings_file = open(r"settings.txt", 'r')

def armsinput(frame, results, win_width, win_height):
    armsY_threshold = 0.2 #this value should be changed in settings, depends on how far away you are from camera
    #getting midpoint
    NoseY = results.pose_landmarks.landmark[0].y
    NoseX = results.pose_landmarks.landmark[0].x
    cv.line(frame, (int(NoseX*win_width), int(NoseY*win_height)), (int(NoseX*win_width), win_height), (0, 0, 255))

    #getting wrists
    LwristX = results.pose_landmarks.landmark[15].x
    LwristY = results.pose_landmarks.landmark[15].y
    RwristX = results.pose_landmarks.landmark[16].x
    RwristY = results.pose_landmarks.landmark[16].y
    
    #calculate keystroke
    if ((LwristX > NoseX) and (RwristX > NoseX) and abs(RwristY - LwristY) < armsY_threshold):
        wsh.SendKeys("L")
    elif ((LwristX < NoseX) and (RwristX < NoseX) and abs(RwristY - LwristY) < armsY_threshold):
        wsh.SendKeys("R")

def capturing():
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
        #    frame.flags.writeable = False #makes frame non editable (readonly), should improve performance
            results = pose.process(frame)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            if (results.pose_landmarks):
                LmouthY, LmouthX, LhipY, LhipX = getlandmarks(results)
                if cv.waitKey(1) == ord('i'): #JUST TO PREVENT RANDOM INPUTS WHILE TESTING, DELETE
                    armsinput(frame, results, win_width, win_height)
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break
    capture.release()
    cv.destroyAllWindows()

window = tk.Tk()
window.geometry("400x400")
window.title("Squat King")
start_btn = tk.Button(window, text="Start", height=5, width=10, command=capturing).pack(pady=70)
settings_btn = tk.Button(window, text="Settings", height=5, width=10, command=settings).pack(pady = 10)

credits = tk.Label(window, text="Created by Naito ;)").pack(side="bottom")
window.mainloop()

"""
- Creating window
- settings should be stored in a read&write text file (search fd/read/write equivalents in python)
- Settings (desplegables, sliders, buttons)
- even tho the landmark is not being detected/shown, it still has a value based on where it thinks it is, i don't want that
- FAILSAFES
    - all 4 hand points (for each hand) need to be detected in order to send lateralmov input - ?
    - if not the whole body is detected, pause automatically (whole body is from head to knees)
    - some input to cancel jump ???? -> i dont think it's possible tho
"""