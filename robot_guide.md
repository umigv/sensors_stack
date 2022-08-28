# Running the Robot

## Teleop only (no other sensors, SLAM, etc.)

Make sure the sensor stack is building and is using branch ```hersh_devel```.  

This guide also assumes you have the most up-to-date arduino code running on the bot.

Checklist:
- Connect batteries on vehicle
- Flip main power switch (and make sure emergency stop is disabled)
- Plug the Arduino into laptop/NUC via USB
- Connect PS4 controller to laptop/NUC (can do bluetooth or wired)

*Note:* The bot may start the Odrive calibration as soon as the arduino gets power, so be careful! Also, don't continue until that's done.

In separate terminals, run:
```
$ roslaunch sensors_launch embedded.launch
$ roslaunch sensors_launch velocity.launch
```
*Note:*
- DO NOT start embedded.launch while the bot Odrives are calibrating. The bot may automatically start the calibration when powering the arduino; wait for it to complete.
- embedded.launch may throw some sync errors before connecting - this is due to the Odrive calibration process (just wait).
- Controller keymaps
	- Left stick = forward/reverse, right stick = left/right
	- Right bumper = movement enable (must hold this down while driving)
	- X button = teleop/autonomous mode toggle (make sure you're in teleop mode, signified by blue solid light)

## Full sensor teleop

_under construction_
