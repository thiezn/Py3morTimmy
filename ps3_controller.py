#!/usr/bin/env python3

import asyncio
import evdev


class Ps3Controller:
    async def _events(self):
        """ Coroutine printing out incoming events """
        async for event in self.device.async_read_loop():
            self.handle_event(event)

    def __init__(self, input_device='/dev/input/event0'):
        """ Connect to controller and define buttons """

        print('Trying to connect to controller')
        self.device = evdev.InputDevice(input_device)
        print(self.device)

        self.LEFT_AXIS_X = 127
        self.LEFT_AXIS_Y = 127
        self.RIGHT_AXIS_X = 127
        self.RIGHT_AXIS_Y = 127
        self.BUTTON_SELECT = False
        self.BUTTON_START = False
        self.BUTTON_LEFT_STICK = False
        self.BUTTON_RIGHT_STICK = False
        self.BUTTON_D_LEFT = False
        self.BUTTON_D_UP = False
        self.BUTTON_D_RIGHT = False
        self.BUTTON_D_DOWN = False
        self.BUTTON_PS = False
        self.BUTTON_SQUARE = False
        self.BUTTON_TRIANGLE = False
        self.BUTTON_CIRCLE = False
        self.BUTTON_CROSS = False
        self.BUTTON_R1 = False
        self.BUTTON_R2 = False
        self.BUTTON_L1 = False
        self.BUTTON_L2 = False

    async def handle_events(self):
        """
        Handle a single evdev event, this updates the internal state of the Axis objects as well as calling any
        registered button handlers.
        """
        async for event in self.device.async_read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == 0:
                    # Left stick, X axis
                    self.LEFT_AXIS_X = event.value
                elif event.code == 1:
                    # Left stick, Y axis
                    self.LEFT_AXIS_Y = event.value
                elif event.code == 2:
                    # Right stick, X axis
                    self.RIGHT_AXIS_X = event.value
                elif event.code == 5:
                    # Right stick, Y axis (yes, 5...)
                    self.RIGHT_AXIS_Y = event.value
            elif event.type == evdev.ecodes.EV_KEY:
                if event.value == 1:  # Key Down
                    if event.code == 288:
                        self.BUTTON_SELECT = True
                    elif event.code == 291:
                        self.BUTTON_START = True
                    elif event.code == 289:
                        self.BUTTON_LEFT_STICK = True
                    elif event.code == 290:
                        self.BUTTON_RIGHT_STICK = True
                    elif event.code == 295:
                        self.BUTTON_D_LEFT = True
                    elif event.code == 292:
                        self.BUTTON_D_UP = True
                    elif event.code == 293:
                        self.BUTTON_D_RIGHT = True
                    elif event.code == 294:
                        self.BUTTON_D_DOWN = True
                    elif event.code == 704:
                        self.BUTTON_PS = True
                    elif event.code == 303:
                        self.BUTTON_SQUARE = True
                    elif event.code == 300:
                        self.BUTTON_TRIANGLE = True
                    elif event.code == 301:
                        self.BUTTON_CIRCLE = True
                    elif event.code == 302:
                        self.BUTTON_CROSS = True
                    elif event.code == 299:
                        self.BUTTON_R1 = True
                    elif event.code == 297:
                        self.BUTTON_R2 = True
                    elif event.code == 298:
                        self.BUTTON_L1 = True
                    elif event.code == 296:
                        self.BUTTON_L2 = True
                elif event.value == 2:  # Key hold
                    pass
                elif event.value == 0:  # Key UP
                    if event.code == 288:
                        self.BUTTON_SELECT = False
                    elif event.code == 291:
                        self.BUTTON_START = False
                    elif event.code == 289:
                        self.BUTTON_LEFT_STICK = False
                    elif event.code == 290:
                        self.BUTTON_RIGHT_STICK = False
                    elif event.code == 295:
                        self.BUTTON_D_LEFT = False
                    elif event.code == 292:
                        self.BUTTON_D_UP = False
                    elif event.code == 293:
                        self.BUTTON_D_RIGHT = False
                    elif event.code == 294:
                        self.BUTTON_D_DOWN = False
                    elif event.code == 704:
                        self.BUTTON_PS = False
                    elif event.code == 303:
                        self.BUTTON_SQUARE = False
                    elif event.code == 300:
                        self.BUTTON_TRIANGLE = False
                    elif event.code == 301:
                        self.BUTTON_CIRCLE = False
                    elif event.code == 302:
                        self.BUTTON_CROSS = False
                    elif event.code == 299:
                        self.BUTTON_R1 = False
                    elif event.code == 297:
                        self.BUTTON_R2 = False
                    elif event.code == 298:
                        self.BUTTON_L1 = False
                    elif event.code == 296:
                        self.BUTTON_L2 = False
            print('left x={} y={}    right x={} y={}'.format(self.LEFT_AXIS_X,
                                                             self.LEFT_AXIS_Y,
                                                             self.RIGHT_AXIS_X,
                                                             self.RIGHT_AXIS_Y))




if __name__ == '__main__':
    controller = Ps3Controller()
    future = asyncio.ensure_future(controller.handle_events())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)
