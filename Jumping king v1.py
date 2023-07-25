import cv2 as cv
import mediapipe as mp
import tkinter as tk
import keyboard as kb

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#get settings
settings = open("settings.txt", "r")
settings.seek(0)
armsY_threshold = float(settings.readline(4))
squatY_threshold = float(settings.readline(4))
difficulty = int(settings.readline(1))
camera = int(settings.readline(1))
detection_conf = float(settings.readline(3))
tracking_conf = float(settings.readline(3))
win_height = int(settings.readline(3))
win_width = int(settings.readline(3))
settings.close

def settings():
    global armsY_threshold, squatY_threshold, difficulty, camera, detection_conf, tracking_conf, win_height, win_width
    settings_win = tk.Toplevel()
    settings_win.geometry ("400x400")
    settings_win.title("Settings")
    tk.Label(settings_win, text="Edit your settings").pack()
    defaults_btn = tk.Button(settings_win, text="Reset to defaults", height=2, width=15, command=default_settings).pack(side="bottom")
    settings = open("settings.txt", 'r')
    newsettings = settings.readline()
    s1 = tk.Scale(settings_win, from_=1, to=99, orient="horizontal").pack(pady=10)
    settings.close

def default_settings():
    random=1

def squatinput(results):
    global is_jump
    #getting hips and knees
    Lhip = results.pose_landmarks.landmark[23]
    Rhip = results.pose_landmarks.landmark[24]
    Lknee = results.pose_landmarks.landmark[25]
    Rknee = results.pose_landmarks.landmark[26]

    #calculating input
    if (abs(Lhip.y-Lknee.y) < squatY_threshold*difficulty and abs(Rhip.y-Rknee.y) < squatY_threshold*difficulty and is_jump == 0):
        kb.press('space')
        is_jump = 1
    elif (abs(Lhip.y-Lknee.y) > squatY_threshold*difficulty and abs(Rhip.y-Rknee.y) > squatY_threshold*difficulty and is_jump == 1):
        kb.release('space')
        is_jump = 0


def armsinput(frame, results, win_width, win_height):
    global is_arms
    #getting midpoint
    nose = results.pose_landmarks.landmark[0]
    cv.line(frame, (int(nose.x*win_width), int(nose.y*win_height)), (int(nose.x*win_width), win_height), (0, 0, 255))

    #getting wrists
    Lwrist = results.pose_landmarks.landmark[15]
    Rwrist = results.pose_landmarks.landmark[16]
    
    #calculate keystroke
    if ((Lwrist.x > nose.x) and (Rwrist.x > nose.x) and abs(Rwrist.y - Lwrist.y) < armsY_threshold and is_arms != 2):
        kb.press('left')
        is_arms = 2
    elif ((Lwrist.x < nose.x) and (Rwrist.x < nose.x) and abs(Rwrist.y - Lwrist.y) < armsY_threshold and is_arms != 1):
        kb.press('right')
        is_arms = 1
    elif ((Lwrist.x > nose.x) and (Rwrist.x < nose.x) and is_arms != 0):
        kb.release('right')
        kb.release('left')
        is_arms = 0

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
                squatinput(results)
                armsinput(frame, results, win_width, win_height)
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break
    kb.release('space')
    kb.release('left')
    kb.release('right')
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
- settings should be stored in a read&write text file (search fd/read/write equivalents in python)
- Settings (desplegables, sliders, buttons)
- even tho the landmark is not being detected/shown, it still has a value based on where it thinks it is, i don't want that
- FAILSAFES
    - all 4 hand points (for each hand) need to be detected in order to send lateralmov input - ?
    - if not the whole body is detected, pause automatically (whole body is from head to knees)
    - some input to cancel jump ???? -> i dont think it's possible tho
"""