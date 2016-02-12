#!/usr/bin/env python3

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import asyncio
import numpy
import time
import random
from collections import deque
from remote_control import RemoteControl

# Global Definitions
MAX_DISTANCE = 200 # The maximum distance the sonar sensor will read
MIN_DISTANCE = 40  # 10 cm before turning random direction
MAX_TURN_ATTEMPTS = 3  # The amount of tries to turn until going in reverse

# Pin Definitions

# DC Motor Front Left
MOTOR1_PIN1 = 30
MOTOR1_PIN2 = 31
MOTOR1_ENABLE_PIN = 7

# DC Motor Rear Left
MOTOR2_PIN1 = 34
MOTOR2_PIN2 = 35
MOTOR2_ENABLE_PIN = 3

# DC Motor Rear Right
MOTOR3_PIN1 = 39
MOTOR3_PIN2 = 38
MOTOR3_ENABLE_PIN = 44

# DC Motor Front Right
MOTOR4_PIN1 = 41
MOTOR4_PIN2 = 40
MOTOR4_ENABLE_PIN = 45

# Sonar distance sensors
TRIGGER_PIN = 22
ECHO_PIN = 23


def moving_average(interval, window_size):
    """ This returns the moving average of a list

    :param interval: List of values
    :param window_size: the number of samples """
    window = numpy.ones(int(window_size))/float(window_size)
    return int(numpy.convolve(interval, window, 'valid')[0])


class Sonar:
    """ Control Sonar Distance Sensors

    HR-SR04 model supported """

    def __init__(self, board, trigger_pin, echo_pin, ping_interval=50, max_distance=MAX_DISTANCE):
        """ Initialize Sonor Sensor(s)

        distance measures in cm.

        :param board: The interface into arduino
        :param trigger_pin: The trigger pin
        :param echo_pin: The echo_pin, set this to the same as trigger ping if using only one pin
        :param ping_interval: The interval of the measurement
        :param max_distance: The maximum distance in cm that the sonar will read
        """
        self.trigger_pin = trigger_pin

        # The sensor data will capture the last three measurements
        # We will use a moving_average to compensate for deviations
        # in the measurements. Initially will fill it up with the
        # maximum distance the sensor is able to detect
        # TODO: Document this somewhere more appropriately
        self._sensor_data = deque([MAX_DISTANCE, MAX_DISTANCE, MAX_DISTANCE], maxlen=3)

        board.sonar_config(trigger_pin=trigger_pin,
                           echo_pin=echo_pin,
                           cb=self.cb_got_data, cb_type=1,
                           ping_interval=ping_interval,
                           max_distance=max_distance)

    @property
    def distance(self):
        """ Returns the moving average of the _sensor_data """
        return moving_average(list(self._sensor_data), 3)

    async def cb_got_data(self, data):
        """ Callback when there is data available

        :param data: list containing [trigger_pin, distance in cm]
        adds the received data to the _sensor_data list
        """
        self._sensor_data.append(data[1])


class DcMotors:
    """ Contol DC Motors """

    def __init__(self, board):
        """ Initialise DC Motor Shield pins """
        self.board = board
        self._action_time_duration = None

        self.state = "stopped"

        self.board.set_pin_mode(MOTOR1_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR1_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR1_ENABLE_PIN, Constants.PWM)

        self.board.set_pin_mode(MOTOR2_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR2_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR2_ENABLE_PIN, Constants.PWM)

        self.board.set_pin_mode(MOTOR3_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR3_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR3_ENABLE_PIN, Constants.PWM)

        self.board.set_pin_mode(MOTOR4_PIN1, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR4_PIN2, Constants.OUTPUT)
        self.board.set_pin_mode(MOTOR4_ENABLE_PIN, Constants.PWM)

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
        self.board.digital_write(MOTOR1_PIN1, 0)
        self.board.digital_write(MOTOR1_PIN2, 1)
        self.board.digital_write(MOTOR2_PIN1, 0)
        self.board.digital_write(MOTOR2_PIN2, 1)
        self.board.digital_write(MOTOR3_PIN1, 0)
        self.board.digital_write(MOTOR3_PIN2, 1)
        self.board.digital_write(MOTOR4_PIN1, 0)
        self.board.digital_write(MOTOR4_PIN2, 1)

        self.board.analog_write(MOTOR1_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR2_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR3_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR4_ENABLE_PIN, speed)

    def reverse(self, speed, duration=None):
        """ Reverse motors

        :param speed: Speed of motors 0-255
        :param duration: Duration of the action in seconds
        """
        self.action_time_duration = duration
        self.action_time_start = time.time()

        self.state = 'reverse'
        self.board.digital_write(MOTOR1_PIN1, 1)
        self.board.digital_write(MOTOR1_PIN2, 0)
        self.board.digital_write(MOTOR2_PIN1, 1)
        self.board.digital_write(MOTOR2_PIN2, 0)
        self.board.digital_write(MOTOR3_PIN1, 1)
        self.board.digital_write(MOTOR3_PIN2, 0)
        self.board.digital_write(MOTOR4_PIN1, 1)
        self.board.digital_write(MOTOR4_PIN2, 0)

        self.board.analog_write(MOTOR1_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR2_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR3_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR4_ENABLE_PIN, speed)

    def right(self, speed, duration=None):
        """ Turns right

        :param speed: speed of motors between 0-255
        :param duration: Duration of the action in seconds
        """

        self.action_time_duration = duration
        self.action_time_start = time.time()
        self.state = 'turning_left'

        self.board.digital_write(MOTOR1_PIN1, 0)
        self.board.digital_write(MOTOR1_PIN2, 1)
        self.board.digital_write(MOTOR2_PIN1, 0)
        self.board.digital_write(MOTOR2_PIN2, 1)
        self.board.digital_write(MOTOR3_PIN1, 1)
        self.board.digital_write(MOTOR3_PIN2, 0)
        self.board.digital_write(MOTOR4_PIN1, 1)
        self.board.digital_write(MOTOR4_PIN2, 0)

        self.board.analog_write(MOTOR1_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR2_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR3_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR4_ENABLE_PIN, speed)

    def left(self, speed, duration=None):
        """ Turn left

        :param speed: speed of motors between 0-255
        :param duration: Duration of the action in seconds
        """

        self.action_time_duration = duration
        self.action_time_start = time.time()
        self.state = 'turning_right'

        self.board.digital_write(MOTOR1_PIN1, 1)
        self.board.digital_write(MOTOR1_PIN2, 0)
        self.board.digital_write(MOTOR2_PIN1, 1)
        self.board.digital_write(MOTOR2_PIN2, 0)
        self.board.digital_write(MOTOR3_PIN1, 0)
        self.board.digital_write(MOTOR3_PIN2, 1)
        self.board.digital_write(MOTOR4_PIN1, 0)
        self.board.digital_write(MOTOR4_PIN2, 1)

        self.board.analog_write(MOTOR1_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR2_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR3_ENABLE_PIN, speed)
        self.board.analog_write(MOTOR4_ENABLE_PIN, speed)

    def stop(self):
        """ Stop all motors """

        self.state = 'stopped'

        board.analog_write(MOTOR1_ENABLE_PIN, 0)
        board.analog_write(MOTOR2_ENABLE_PIN, 0)
        board.analog_write(MOTOR3_ENABLE_PIN, 0)
        board.analog_write(MOTOR4_ENABLE_PIN, 0)


def loop(board, dc_motors, sonar):
    """ This is the main running loop

    This will handle time based action like starting, stopping
    and turning for x amount of time when an obstacle is detected
    """

    joystick = RemoteControl()
    turn_attempts = 0  # Keeps track of the amount of turn iterations
    drive_autonomous = False

    while not joystick.START:
        current_time = time.time()

        # Switch driving mode
        if joystick.SELECT:
            if drive_autonomous:
                print('Switching to remote controlled driving')
                drive_autonomous = False
            else:
                print('Switching to autonomous driving')
                drive_autonomous = True
                turn_attempts = 0
                dc_motors.forward(100)
            # Have to wait for a few seconds as a single button press
            # on SELECT generates multiple hits
            board.sleep(0.2)

        # Remote controlled driving
        if not drive_autonomous:
            if joystick.UP:
                dc_motors.forward(255)
            elif joystick.DOWN:
                dc_motors.reverse(255)
            elif joystick.LEFT:
                dc_motors.left(255)
            elif joystick.RIGHT:
                dc_motors.right(255)
            else:
                dc_motors.stop()

        # Autonomous Driving
        else: 
            distance = sonar.distance
            print('distance: %s' % distance)

            # Getting to close, lets try to turn
            if distance < MIN_DISTANCE and not dc_motors.state.startswith('turning'):
                turn_attempts += 1
                random_value = random.randint(1, 2)
                if random_value == 1:
                    print('Getting too close, turning left for 1 seconds!')
                    dc_motors.left(255, 1)
                elif random_value == 2:
                    dc_motors.right(255, 1)
                    print('Getting too close, turning right for 1 seconds!')

            # Turning doesnt seem to work, lets go in reverse
            elif turn_attempts > MAX_TURN_ATTEMPTS:
                dc_motors.reverse(100, 3)
                turn_attempts = 0

            # Handle finished motor actions
            elif(dc_motors.action_time_duration and
                 (dc_motors.action_time_start + dc_motors.action_time_duration) >= current_time):

                    # Check if the obstacle is cleared
                    if dc_motors.state.startswith('turning'):
                        if distance < MIN_DISTANCE:
                            print("%s for 2 seconds wasn't enough. Lets do another sec" % dc_motors.state)
                            if dc_motors.state.endswith('left'):
                                dc_motors.left(255, 1)
                            else:
                                dc_motors.right(255, 1)
                            turn_attempts += 1
                        else:
                            print('Ok, obstacle cleared, moving forward...')
                            dc_motors.forward(100)
                            turn_attempts = 0

                    # Reverse action completed, lets turn around
                    elif dc_motors.state == 'reverse':
                        # TODO: Deduplicate random turn code
                        turn_attempts += 1
                        random_value = random.randint(1, 2)
                        if random_value == 1:
                            print('Finished reversing, turning left for a sec')
                            dc_motors.left(255, 1)
                        elif random_value == 2:
                            dc_motors.right(255, 1)
                            print('Finished reversing, turning right for a sec')

            # run for a bit before re-iterating through the loop again
            board.sleep(0.2)

    # End while loop
    joystick.shutdown()
    board.shutdown()

if __name__ == "__main__":
    board = PyMata3()

    dc_motors = DcMotors(board)
    sonar = Sonar(board, TRIGGER_PIN, ECHO_PIN)

    print('Robot initialised, remote controlled. press <SELECT> to toggle autonomous driving')
    try:
        loop(board, dc_motors, sonar)
    except KeyboardInterrupt:
        board.shutdown()
