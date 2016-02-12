#!/usr/bin/env python3

# TODO: Only import the modules we want from pygame
import pygame
import time
import os
import threading


class RemoteControl:

    def __init__(self):
        """ Initialise the PS3 controller """

        # Initialize a dummy display for pygame to run
        # if you suddenly need to give a KeyboardInterrupt to get this to run check this post:
        #  http://stackoverflow.com/questions/17035699/pygame-requires-keyboard-interrupt-to-init-display
        # os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init() 
        pygame.display.set_mode((1,1))

        # Wait for a joystick
        while pygame.joystick.get_count() == 0:
           print("Waiting for joystick count = %i" % pygame.joystick.get_count())
           time.sleep(10)
           pygame.joystick.quit()
           pygame.joystick.init()

        j = pygame.joystick.Joystick(0)
        j.init()

        # Button Mappings
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.TRIANGLE = False
        self.SQUARE = False
        self.CIRCLE = False
        self.X = False
        self.SELECT = False
        self.START = False
        self.PS = False
        self.R1 = False
        self.R2 = False
        self.L1 = False
        self.L2 = False

        # Run controller in seperate thread
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def shutdown(self):
        """ Terminates the running thread and kills pygame """
        pygame.quit()

    def run(self):
        """ Run the main event loop grabbing input from the controller """
        while True:
            # Check for any queued events and then process each one
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: sys.exit()
                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYAXISMOTION:
                    pass
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 4:
                        self.UP = True
                    elif event.button == 6:
                        self.DOWN = True
                    elif event.button == 7:
                        self.LEFT = True
                    elif event.button == 5:
                        self.RIGHT = True
                    elif event.button == 12:
                        self.TRIANGLE = True
                    elif event.button == 13:
                        self.CIRCLE = True
                    elif event.button == 14:
                        self.X = True
                    elif event.button == 15:
                        self.SQUARE = True
                    elif event.button == 11:
                        self.R1 = True
                    elif event.button == 9:
                        self.R2 = True
                    elif event.button == 10:
                        self.L1 = True
                    elif event.button == 8:
                        self.L2 = True
                    elif event.button == 0:
                        self.SELECT = True
                    elif event.button == 3:
                        self.START = True
                    elif event.button == 16:
                        self.PS = True
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 4:
                        self.UP = False
                    elif event.button == 6:
                        self.DOWN = False
                    elif event.button == 7:
                        self.LEFT = False
                    elif event.button == 5:
                        self.RIGHT = False
                    elif event.button == 12:
                        self.TRIANGLE = False
                    elif event.button == 13:
                        self.CIRCLE = False
                    elif event.button == 14:
                        self.X = False
                    elif event.button == 15:
                        self.SQUARE = False
                    elif event.button == 11:
                        self.R1 = False
                    elif event.button == 9:
                        self.R2 = False
                    elif event.button == 10:
                        self.L1 = False
                    elif event.button == 8:
                        self.L2 = False
                    elif event.button == 0:
                        self.SELECT = False
                    elif event.button == 3:
                        self.START = False
                    elif event.button == 16:
                        self.PS = False

if __name__ == '__main__':
    # Test code:
    # This mimicks an event loop and makes sure we're able to 
    # get the joystick state from a seperate thread
    joystick = RemoteControl()
    while True:
        if joystick.UP:
            print('UP')
        if joystick.DOWN:
            print('DOWN')
        if joystick.LEFT:
            print('LEFT')
        if joystick.RIGHT:
            print('RIGHT')
        if joystick.TRIANGLE:
            print('TRIANGlE')
        if joystick.CIRCLE:
            print('CIRCLE')
        if joystick.SQUARE:
            print('SQUARE')
        if joystick.X:
            print('X')
        if joystick.SELECT:
            print('SELECT')
        if joystick.START:
            print('START')
        if joystick.PS:
            print('PS')
        if joystick.R1:
            print('R1')
        if joystick.R2:
            print('R2')
        if joystick.L1:
            print('L1')
        if joystick.L2:
            print('L2')
