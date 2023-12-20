# Jumpking
## What is it?
Squat King is a "mod" (not exactly) for the game [Jump King](https://www.jump-king.com/), it uses camera input to detect people and based on the movements emulate a keyboard press to play the game.
Since the game only has 3 inputs, it is very simple: squat to jump and hold both arms in one direction or the other to move there.

It is not an *actual* Jump King mod since it is just emulating 3 keyboard presses (Space, Left, Right), so it works with any program/game since it is not modifying the actual game. That being said, it was made with Jump King in mind, hence the name.

## How to use it
Once you clone and install all necessary modules (mediapipe, openCV, tkinter, ...), just run the program with the interpreter.
Each run takes a while to start, since OpenCV has to check all available cameras. After that, select the camera you want to use (default 0).
Selecting ```Start``` will open a new window with the capturing. Close this window with ```Q``` or ```Esc```. (You cannot close the main window without closing this one first)

### Settings
- Arms threshold: Change the minimum (vertical) distance the wrists have to be for the program to detect an input.
- Squat sensitivity: Change the minimum (vertical) distance the knees and hips have to be for the program to detect an input. 
	(Both of these will depend on how far away from the camera you are, default is 2 (standing 3 meters away from the camera)).
- Camera: toggles the visibility of the camera feed. Made with people who don't want to show themselves on camera (vtubers) in mind. Obviously, the camera will still be used.

### TIPS/Troubleshooting
- Since the program actually emulates a keyboard, once you start the program, have the focus window be the game, or you might start seeing weird behaviours
- It is impossible for 2 programs to be using the same camera at once, so if you're planning on recording (OBS, etc), dont use camera capture, instead just capture the Squat King window.
