# Py3morTimmy_v2
Yet again another version of my robot

This time around I'm using the library pymata3-aio to control the Arduino. This will allow me to handle things (mostly) in python and do not have to worry with the arduino code.

I'm still keeping my other repositories:
- morTimmy: Uses python2 and my own Arduino firmware. I've written my own protocol between the raspberry pi and arduino using the serial interface.
- Py3morTimmy: Here I wanted to shift to python3 so i could use the asyncio library. It actually doesn't do much related to the robot yet as i was trying to create a pubsub library first
