#!/usr/bin/env python3

import asyncio
import evdev


class RemoteControl:
    async def _events(self):
        """ Coroutine printing out incoming events """
        async for event in self.device.async_read_loop():
            self.handle_event(event)

    def __init__(self, input_device='/dev/input/event0', loop=None):
        """ Connect to controller and define buttons """

        print('Trying to connect to controller...')
        self.device = evdev.InputDevice(input_device)
        print(self.device)

        self.LEFT_AXIS_X = 127
        self.LEFT_AXIS_Y = 127
        self.RIGHT_AXIS_X = 127
        self.RIGHT_AXIS_Y = 127
        self.SELECT = False
        self.START = False
        self.LEFT_STICK = False
        self.RIGHT_STICK = False
        self.LEFT = False
        self.UP = False
        self.RIGHT = False
        self.DOWN = False
        self.PS = False
        self.SQUARE = False
        self.TRIANGLE = False
        self.CIRCLE = False
        self.CROSS = False
        self.R1 = False
        self.R2 = False
        self.L1 = False
        self.L2 = False

    async def handle_events(self):
        """
        Handle a single evdev event, this updates the internal state of the Axis objects as well as calling any
        registered button handlers.
        """
        events = await self.device.async_read()
        for event in events:
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
                        self.SELECT = True
                    elif event.code == 291:
                        self.START = True
                    elif event.code == 289:
                        self.LEFT_STICK = True
                    elif event.code == 290:
                        self.RIGHT_STICK = True
                    elif event.code == 295:
                        self.LEFT = True
                    elif event.code == 292:
                        self.UP = True
                    elif event.code == 293:
                        self.RIGHT = True
                    elif event.code == 294:
                        self.DOWN = True
                    elif event.code == 704:
                        self.PS = True
                    elif event.code == 303:
                        self.SQUARE = True
                    elif event.code == 300:
                        self.TRIANGLE = True
                    elif event.code == 301:
                        self.CIRCLE = True
                    elif event.code == 302:
                        self.CROSS = True
                    elif event.code == 299:
                        self.R1 = True
                    elif event.code == 297:
                        self.R2 = True
                    elif event.code == 298:
                        self.L1 = True
                    elif event.code == 296:
                        self.L2 = True
                elif event.value == 2:  # Key hold
                    pass
                elif event.value == 0:  # Key UP
                    if event.code == 288:
                        self.SELECT = False
                    elif event.code == 291:
                        self.START = False
                    elif event.code == 289:
                        self.LEFT_STICK = False
                    elif event.code == 290:
                        self.RIGHT_STICK = False
                    elif event.code == 295:
                        self.LEFT = False
                    elif event.code == 292:
                        self.UP = False
                    elif event.code == 293:
                        self.RIGHT = False
                    elif event.code == 294:
                        self.DOWN = False
                    elif event.code == 704:
                        self.PS = False
                    elif event.code == 303:
                        self.SQUARE = False
                    elif event.code == 300:
                        self.TRIANGLE = False
                    elif event.code == 301:
                        self.CIRCLE = False
                    elif event.code == 302:
                        self.CROSS = False
                    elif event.code == 299:
                        self.R1 = False
                    elif event.code == 297:
                        self.R2 = False
                    elif event.code == 298:
                        self.L1 = False
                    elif event.code == 296:
                        self.L2 = False

if __name__ == '__main__':
    controller = RemoteControl()
    loop = asyncio.get_event_loop()
    while not controller.START:
        future = asyncio.ensure_future(controller.handle_events())
        loop.run_until_complete(future)
        print('x={} y={} x={} y={}'.format(controller.LEFT_AXIS_X,
                                           controller.LEFT_AXIS_Y,
                                           controller.RIGHT_AXIS_X,
                                           controller.RIGHT_AXIS_Y))
