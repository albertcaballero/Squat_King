# Jumpking
## What it is
Squat King is a "mod" (not exactly) for the game Jump King, it uses camera input to detect people and based on the movements emulate a keyboard press to play the game.
Since the game only has 3 inputs, it is very simple: squat to jump and hold both arms in one direction or the other to move there.

It is not an *actual* Jump King mod since it is just emulating 3 keyboard presses (Space, Left, Right), so it works with any program/game since it is not modifying the actual game. That being said, it was made with Jump King in mind, hence the name.

## How to use it
OpenCV takes a while to start the cameras, so each time the program is run it will take a while, since it has to check all available cameras. After that, select the camera you want to use (default 0).
Selecting 'Start' will open a new window with the capturing. Close this window with 'Q' or 'Esc'. You cannot close the main window without closing this one first.

### Settings
- Arms threshold: Change the minimum (vertical) distance the wrists have to be for the program to detect an input.
- Squat threshold: Change the minimum (vertical) distance the knees and hips have to be for the program to detect an input. 
	(Both of these will depend on how far away from the camera you are, default is 2 (standing 3 meters away from the camera)).
- Difficulty: self explanatory, 1 normal, 3 easiest (default is 1).
- Camera: toggles the visibility of the camera feed. Made with people who don't want to show themselves on camera (vtubers) in mind. The camera will still be used.

### TIPS
- Since the program actually emulates a keyboard, once you start the program, have the focus window be the game, or you might start seeing weird behaviours
- It is impossible for 2 programs to be using the same camera at once, so if you're planning on recording (OBS, etc), dont use camera capture, just capture the Squat King window.
