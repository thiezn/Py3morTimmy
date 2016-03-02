#!/usr/bin/env python3

from robot import Robot

if __name__ == "__main__":
    robot = Robot()

    print('Robot initialised, remote controlled. press <SELECT> to toggle autonomous driving')
    try:
        robot.run()
    except KeyboardInterrupt:
 #         robot.shutdown()
        pass
