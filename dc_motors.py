#!/usr/bin/env python3

from pymata_aio.constants import Constants
import time

# Global Definitions
# Pin Definitions

# DC Motor Front Left
MOTOR_FRONT_LEFT_PIN1 = 30
MOTOR_FRONT_LEFT_PIN2 = 31
MOTOR_FRONT_LEFT_ENABLE_PIN = 7

# DC Motor Rear Left
MOTOR_REAR_LEFT_PIN1 = 34
MOTOR_REAR_LEFT_PIN2 = 35
MOTOR_REAR_LEFT_ENABLE_PIN = 3

# DC Motor Rear Right
MOTOR_REAR_RIGHT_PIN1 = 39
MOTOR_REAR_RIGHT_PIN2 = 38
MOTOR_REAR_RIGHT_ENABLE_PIN = 44

# DC Motor Front Right
MOTOR_FRONT_RIGHT_PIN1 = 41
MOTOR_FRONT_RIGHT_PIN2 = 40
MOTOR_FRONT_RIGHT_ENABLE_PIN = 45


class DcMotors:
    """ Contol DC Motors """

    def __init__(self, board):
        """ Initialise DC Motor Shield pins """
        self.board = board
        self._action_time_duration = None

        self.state = "stopped"

        self.board.set_pin_mode(MOTOR_FRONT_LEFT_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_FRONT_LEFT_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_FRONT_LEFT_ENABLE_PIN, Constants.PWM)

        self.board.set_pin_mode(MOTOR_REAR_LEFT_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_REAR_LEFT_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_REAR_LEFT_ENABLE_PIN, Constants.PWM)

        self.board.set_pin_mode(MOTOR_REAR_RIGHT_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_REAR_RIGHT_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_REAR_RIGHT_ENABLE_PIN, Constants.PWM)

        self.board.set_pin_mode(MOTOR_FRONT_RIGHT_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_FRONT_RIGHT_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR_FRONT_RIGHT_ENABLE_PIN, Constants.PWM)

    @property
    def action_time_duration(self):
        return self._action_time_duration

    @action_time_duration.setter
    def action_time_duration(self, duration):
        """ Setter for action_time_duration

        This variable depicts for how long the motion should
        run. If a time is not None it will return the current
        timestamp
        """
        if duration:
            self._action_time_duration = duration
        else:
            self._action_time_duration = None


    def forward(self, speed, duration=None):
        """ Move forward

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'forward'
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 1)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, speed)

    def up_left(self, speed, duration=None):
        """ Move soft left forward

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'forward'
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 1)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, int(speed/4))
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, int(speed/4))
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, speed)

    def up_right(self, speed, duration=None):
        """ Move soft right forward

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'forward'
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 1)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, int(speed/4))
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, int(speed/4))

    def down_left(self, speed, duration=None):
        """ Move soft left reverse

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'reverse'
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 0)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, int(speed/4))
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, int(speed/4))
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, speed)

    def down_right(self, speed, duration=None):
        """ Move soft right reverse

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'reverse'
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 0)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, int(speed/4))
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, int(speed/4))

    def reverse(self, speed, duration=None):
        """ Reverse motors

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'reverse'
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 0)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, speed)

    def right(self, speed, duration=None):
        """ Turns right

        :param speed: speed of motors between 0-255
        :param duration: Duration of the action in seconds
        """

        self.action_time_duration = duration
        self.action_time_start = time.time()
        self.state = 'turning_left'

        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 0)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, speed)

    def left(self, speed, duration=None):
        """ Turn left

        :param speed: speed of motors between 0-255
        :param duration: Duration of the action in seconds
        """

        self.action_time_duration = duration
        self.action_time_start = time.time()
        self.state = 'turning_right'

        self.board.digital_write(MOTOR_FRONT_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_FRONT_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN1, 1)
        self.board.digital_write(MOTOR_REAR_LEFT_PIN2, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_REAR_RIGHT_PIN2, 1)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN1, 0)
        self.board.digital_write(MOTOR_FRONT_RIGHT_PIN2, 1)

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, speed)

    def stop(self):
        """ Stop all motors """

        self.state = 'stopped'

        self.board.analog_write(MOTOR_FRONT_LEFT_ENABLE_PIN, 0)
        self.board.analog_write(MOTOR_REAR_LEFT_ENABLE_PIN, 0)
        self.board.analog_write(MOTOR_REAR_RIGHT_ENABLE_PIN, 0)
        self.board.analog_write(MOTOR_FRONT_RIGHT_ENABLE_PIN, 0)
