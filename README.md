# Py3morTimmy_v2
Yet again another version of my robot

This time around I'm using the library pymata3-aio to control the Arduino. This will allow me to handle things (mostly) in python and do not have to worry with the arduino code.

I'm still keeping my other repositories:
- morTimmy: Uses python2 and my own Arduino firmware. I've written my own protocol between the raspberry pi and arduino using the serial interface.
- Py3morTimmy: Here I wanted to shift to python3 so i could use the asyncio library. It actually doesn't do much related to the robot yet as i was trying to create a pubsub library first

## Current state
- Crude autonomous driving using the sonar HR-SR04 sensor to measure distance
- Manual driving using a PS3 controller through USB cable and the pygame library (only for controller support).
- Toggle between the two driving modes using the <SELECT> button on the PS3 controller

## How to run
Required to run as root to get the controller/pygame to run

    sudo ./hardwarecontroller
