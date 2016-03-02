#!/usr/bin/env python3

from utils import moving_average
from collections import deque

# Global Definitions
MAX_SONAR_DISTANCE = 200 # The maximum distance the sonar sensor will read

# pins
TRIGGER_PIN = 22
ECHO_PIN = 23


class Sonar:
    """ Control Sonar Distance Sensors

    HR-SR04 model supported """

    def __init__(self, board, trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN, ping_interval=50, max_distance=MAX_SONAR_DISTANCE):
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
        self._sensor_data = deque([MAX_SONAR_DISTANCE, MAX_SONAR_DISTANCE, MAX_SONAR_DISTANCE], maxlen=3)

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
        # print("Async Sensor Data {}".format(data[1]))
        self._sensor_data.append(data[1])
