#!/usr/bin/env python3

import asyncio
import time
import random
from ps3_controller import RemoteControl
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from sonar import Sonar
from dc_motors import DcMotors
from audio import Audio

# Global Definitions
MIN_DISTANCE = 20  # Distance to start avoiding
MAX_TURN_ATTEMPTS = 3  # The amount of tries to turn until going in reverse


class Robot:

    def __init__(self, drive_autonomous=False, loop=None):
        """ Initialise Robot """

        self.board = PyMata3()
        self.dc_motors = DcMotors(self.board)
        self.sonar = Sonar(self.board)
        self.controller = RemoteControl()
        self.audio = Audio()

        if loop:
            self.loop = loop
        else:
            self.loop = self.board.loop
        self.drive_autonomous = drive_autonomous

    def run(self):
        """ This is the main running loop

        This will handle time based action like starting, stopping
        and turning for x amount of time when an obstacle is detected
        """

        music_playing = False
        turn_attempts = 0

        print('Starting main loop')
        while not self.controller.START:
            future = asyncio.ensure_future(self.controller.handle_events())
            self.loop.run_until_complete(future)

            # Switch driving mode
            if self.controller.SELECT:
                if self.drive_autonomous:
                    print('Switching to remote controlled driving')
                    self.drive_autonomous = False
                else:
                    print('Switching to autonomous driving')
                    self.drive_autonomous = True
                    turn_attempts = 0
                    self.dc_motors.forward(100)
            
            if self.controller.CROSS and not music_playing:
                # Start the music baby
                self.loop.run_until_complete(self.audio.play_audio('static/audio/hello_son.mp3'))
                music_playing = True
    
            if self.drive_autonomous:
                self._detect_obstacles(turn_attempts)
            else:
                self._manual_control()

    def _manual_control(self):
        """ Handles one loop cycle of manual driving """
        if self.controller.UP and self.controller.LEFT:
            self.dc_motors.up_left(255)
        elif self.controller.UP and self.controller.RIGHT:
            self.dc_motors.up_right(255)
        elif self.controller.DOWN and self.controller.LEFT:
            self.dc_motors.down_left(255)
        elif self.controller.DOWN and self.controller.RIGHT:
            self.dc_motors.down_right(255)
        elif self.controller.UP:
            self.dc_motors.forward(255)
        elif self.controller.DOWN:
            self.dc_motors.reverse(255)
        elif self.controller.LEFT:
            self.dc_motors.left(255)
        elif self.controller.RIGHT:
            self.dc_motors.right(255)
        else:
            self.dc_motors.stop()

    def _detect_obstacles(self, turn_attempts):
        """ Handles one loop cycle of autonomous driving """
        current_time = time.time()
        distance = self.sonar.distance
        print('Distance: %s' % distance)

        # Getting to close, lets try to turn
        if distance < MIN_DISTANCE and not self.dc_motors.state.startswith('turning'):
            turn_attempts += 1
            random_value = random.randint(1, 2)
            if random_value == 1:
                print('Getting too close, turning left for 2 seconds!')
                self.dc_motors.left(255, 3)
            elif random_value == 2:
                self.dc_motors.right(255, 3)
                print('Getting too close, turning right for 2 seconds!')

        # Turning doesnt seem to work, lets go in reverse
        elif turn_attempts > MAX_TURN_ATTEMPTS:
            self.dc_motors.reverse(100, 3)
            turn_attempts = 0

        # Handle finished motor actions
        elif self.dc_motors.action_time_duration:
            action_end_time = self.dc_motors.action_time_start + self.dc_motors.action_time_duration

            print('start: {}\nduration: {}\nend: {}\ncurrent: {}'
                  .format(self.dc_motors.action_time_start,
                          self.dc_motors.action_time_duration,
                          action_end_time,
                          current_time))

            # TODO: I DONT GET THIS AT ALL!! THIS SHOULD READ
            # if action_end_time >= current_time:
            # BUT THEN IT DOESNT WORK. QUESS IM UP TOO LONG TO SEE IT
            if action_end_time <= current_time:
                # Check if the obstacle is cleared
                if self.dc_motors.state.startswith('turning'):
                    if distance < MIN_DISTANCE:
                        print("%s for 2 seconds wasn't enough. Lets do another 2 sec" % self.dc_motors.state)
                        if self.dc_motors.state.endswith('left'):
                            self.dc_motors.left(255, 2)
                        else:
                            self.dc_motors.right(255, 2)
                        turn_attempts += 1
                    else:
                        print('Ok, obstacle cleared, moving forward...')
                        self.dc_motors.forward(100)
                        turn_attempts = 0

                # Reverse action completed, lets turn around
                elif self.dc_motors.state == 'reverse':
                    # TODO: Deduplicate random turn code
                    turn_attempts += 1
                    random_value = random.randint(1, 2)
                    if random_value == 1:
                        print('Finished reversing, turning left for 2 sec')
                        self.dc_motors.left(255, 2)
                    elif random_value == 2:
                        self.dc_motors.right(255, 2)
                        print('Finished reversing, turning right for 2 sec')

        # run for a bit before re-iterating through the loop again
        self.board.sleep(0.2)

    def shutdown(self):
        """ Shutdown robot """
        self.board.shutdown()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.sleep(.1))
        for t in asyncio.Task.all_tasks(loop):
            t.cancel()
        loop.run_until_complete(asyncio.sleep(.1))
        loop.stop()
        loop.close()
        sys.exit(0)
