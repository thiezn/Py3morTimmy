# py3morTimmy
Python 3 version of morTimmy the Robot

This time around I'm using the library pymata3-aio to control the Arduino. This will allow me to handle things (mostly) in python and do not have to worry with the arduino code.

I'm still keeping my other repository:
- morTimmy: Uses python2 and my own Arduino firmware. I've written my own protocol between the raspberry pi and arduino using the serial interface.

## Current state
- Crude autonomous driving using the sonar HR-SR04 sensor to measure distance
- Manual driving using a PS3 controller through USB cable and the pygame library (only for controller support).
- Toggle between the two driving modes using the <SELECT> button on the PS3 controller. Using evdev to control the remote

## How to run
    ./hardwarecontroller
