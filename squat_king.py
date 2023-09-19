import cv2 as cv
import mediapipe as mp
import tkinter as tk
import keyboard as kb
import json as js
from tktooltip import ToolTip

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
is_jump = 0
is_arms = 0
is_paused = False
seconds = 0

#get settings
with open("settings.json", "r") as settings_r:
    data = js.load(settings_r)
    armsY_thr = data['armsY_threshold']
    squatY_thr = data['squatY_threshold']
    difficulty = data['difficulty']
    camera = data['camera']
    #detection_conf = data['min_detection_confidence']
    #tracking_conf = data['min_tracking_confidence']
    settings_r.close()

def find_camera_arrays():
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

def change_settings():
    global armsY_thr, squatY_thr, difficulty, camera #detection_conf, tracking_conf
    global SYT_scale, DIF_scale, AYT_scale, CAM_scale, cam_state
    cam_state = tk.IntVar()
    settings_win = tk.Toplevel()
    settings_win.geometry ("400x400")
    settings_win.title("Settings")
    settings_win.columnconfigure(index = 1, minsize=100, weight=1)
    settings_win.columnconfigure(index = 0, minsize=100, weight=1)
    tk.Label(settings_win, text="Edit your settings").grid(row=0, column=1, padx=2, pady=10)

    defaults_btn = tk.Button(settings_win, text="Reset to defaults", height=2, width=15, command=default_settings)
    defaults_btn.grid(row=5, column=0, pady=25, padx=20)
    apply_btn = tk.Button(settings_win, text="Apply", height=2, width=15, command=apply_settings)
    apply_btn.grid(row=5, column=1, pady=25, padx=1)

    AYT_scale = tk.Scale(settings_win, from_=1, to=9, length=200, orient="horizontal")
    tk.Label(settings_win, text="Arms vert. distance").grid(row=1, column=0, pady=4, padx=4)
    AYT_scale.grid(row=1, column=1, pady=4, padx=4)
    AYT_scale.set(armsY_thr*10)
    ToolTip(AYT_scale, delay=1.0, msg="Adjust the threshold for how close the arms need to be (vertically) "
            "for the input to be detected\n(depends on how far away you are from the camera)")

    SYT_scale = tk.Scale(settings_win, from_=1, to=9, length=200, orient="horizontal")
    tk.Label(settings_win, text="Squat vert. distance").grid(row=2, column=0, pady=4, padx=4)
    SYT_scale.grid(row=2, column=1, pady=4, padx=4)
    SYT_scale.set(squatY_thr*10)
    ToolTip(SYT_scale, delay=1.0, msg="Adjust the detection threshold for what counts as a squat\n"
            "(depends on how far away you are from the camera)")

    DIF_scale = tk.Scale(settings_win, from_=1, to=3, orient="horizontal")
    tk.Label(settings_win, text="Difficulty").grid(row=3, column=0, pady=4, padx=4)
    DIF_scale.grid(row=3, column=1, pady=4, padx=4)
    DIF_scale.set(difficulty)
    ToolTip(DIF_scale, delay=1.0, msg="Pretty self explanatory (1 easy, 3 difficult)\n"
            "Idk, in case you're crazy??\n\n\n\nCrazy? I was crazy once") #they locked me in a room, a rubber room
    
    cam_state.set(camera)
    CAM_scale = tk.Checkbutton(settings_win, variable=cam_state)
    tk.Label(settings_win, text="Camera").grid(row=4, column=0, pady=4, padx=4)
    CAM_scale.grid(row=4, column=1, pady=4, padx=4)
    ToolTip(CAM_scale, delay=1.0, msg="Toggles wether the camera feedback is shown\n\n"
            "NOTE: this does not toggle the USE of the camera, just what you see, "
            "in case you don't wanna see your struggling face")

def default_settings():
    global armsY_thr, squatY_thr, difficulty, camera #detection_conf, tracking_conf
    armsY_thr = 0.2
    squatY_thr = 0.2
    difficulty = 1
    camera = 1

    data['armsY_threshold'] = 0.2
    data['squatY_threshold'] = 0.2
    data['difficulty'] = 1
    data['camera'] = 1
    with open("settings.json", "w") as settings_w:
        js.dump(data, settings_w)
        settings_w.close

def apply_settings():
    global armsY_thr, squatY_thr, difficulty, camera #detection_conf, tracking_conf
    global SYT_scale, DIF_scale, AYT_scale, CAM_scale, cam_state
    armsY_thr = float(AYT_scale.get()/10)
    squatY_thr = float(SYT_scale.get()/10)
    difficulty = int(DIF_scale.get())
    camera = cam_state.get()

    data['armsY_threshold'] = armsY_thr
    data['squatY_threshold'] = squatY_thr
    data['difficulty'] = difficulty
    data['camera'] = camera
    with open("settings.json", "w") as settings_w:
        js.dump(data, settings_w)
        settings_w.close

def squatinput(results):
    global is_jump
    #getting hips and knees
    Lhip = results.pose_landmarks.landmark[23]
    Rhip = results.pose_landmarks.landmark[24]
    Lknee = results.pose_landmarks.landmark[25]
    Rknee = results.pose_landmarks.landmark[26]

    #calculating input
    if (abs(Lhip.y-Lknee.y) < squatY_thr*(1/difficulty) and abs(Rhip.y-Rknee.y) < squatY_thr*(1/difficulty) and is_jump == 0):
        kb.press('space')
        is_jump = 1
    elif (abs(Lhip.y-Lknee.y) > squatY_thr*(1/difficulty) and abs(Rhip.y-Rknee.y) > squatY_thr*(1/difficulty) and is_jump == 1):
        kb.release('space')
        is_jump = 0


def armsinput(frame, results, win_width, win_height):
    global is_arms, armsY_thr
    #getting midpoint
    nose = results.pose_landmarks.landmark[0]
    cv.line(frame, (int(nose.x*win_width), int(nose.y*win_height)), (int(nose.x*win_width), win_height), (0, 0, 255))

    #getting wrists
    Lwrist = results.pose_landmarks.landmark[15]
    Rwrist = results.pose_landmarks.landmark[16]
    
    #calculate keystroke
    if ((Lwrist.x > nose.x) and (Rwrist.x > nose.x) and abs(Rwrist.y - Lwrist.y) < armsY_thr and is_arms != 2):
        kb.press('left')
        is_arms = 2
    elif ((Lwrist.x < nose.x) and (Rwrist.x < nose.x) and abs(Rwrist.y - Lwrist.y) < armsY_thr and is_arms != 1):
        kb.press('right')
        is_arms = 1
    elif ((Lwrist.x > nose.x) and (Rwrist.x < nose.x) and is_arms != 0):
        kb.release('right')
        kb.release('left')
        is_arms = 0

def check_pause(results, win_height, win_width):
    global is_paused, seconds
    if (results.pose_landmarks):
        Rwrist = results.pose_landmarks.landmark[16]
    else:
        return
    if (results.pose_landmarks and abs(Rwrist.y*win_height) < 90 and abs(Rwrist.x*win_width) < 90):
        if (is_paused == False and seconds > 10):
            is_paused = True
            seconds = 0
        elif (is_paused == True and seconds > 10):
            is_paused = False
            seconds = 0
        seconds += 1
    else:
        seconds = 0

def capturing():
    global camera, is_paused
    camera_index = camera_current.get()
    capture = cv.VideoCapture(camera_index)
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
            results = pose.process(frame)
            if (camera == 0):
                cv.rectangle(frame, pt1=(0, 0), pt2=(win_width, win_height), color=(0, 0, 0), thickness=-1)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            check_pause(results, win_height, win_width)
            cv.rectangle(frame, pt1=(0,0), pt2=(90, 90), color=(0, 0, 0), thickness=3)
            cv.putText(frame, text="Pause", org=(15,50), fontFace=cv.QT_FONT_NORMAL, fontScale=0.6, color=(0,0,0), thickness=1)
            if (is_paused == True):
                cv.rectangle(frame, pt1=(0,0), pt2=(win_width, win_height), color=(0, 0, 255), thickness=10)
            if (results.pose_landmarks and is_paused == False):
                squatinput(results)
                armsinput(frame, results, win_width, win_height)
            cv.imshow('close with Q', frame)
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
tk.Label(window, text="Welcome!").pack(side="top", pady=10)
tk.Label(window, text="select your camera:").pack(pady=20)
available_cameras = find_camera_arrays()
camera_current = tk.IntVar()
camera_current.set(0)
tk.OptionMenu(window, camera_current, *available_cameras).pack(padx=10)
tk.Button(window, text="Start", height=5, width=10, command=capturing).pack(pady=20)
tk.Button(window, text="Settings", height=5, width=10, command=change_settings).pack(pady = 10)
tk.Label(window, text="Created by Naito ;)").pack(side="bottom")

window.mainloop()

"""
- PAUSE BUTTON/pose --> is_paused Boolean, squat_input and arms_input only if false --> touch corner of the window
- sensitivity setting --> NORMALIZE SENSITIVITY
- even tho the landmark is not being detected/shown, it still has a value based on where it thinks it is, i don't want that
- FAILSAFES
    - all 4 hand points (for each hand) need to be detected in order to send lateralmov input - ?
    - if not the whole body is detected, pause automatically (whole body is from head to knees)
"""