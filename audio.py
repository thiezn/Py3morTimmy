#!/usr/bin/env python3

import asyncio
import subprocess


class Audio:
    """ This class is a asyncio wrapper around the pyaudio library """

    def __init__(self):
        """ Initialise pyaudio. Call before starting asyncio loop

        You might want to set the volume to 100% from the CLI:
        amixer cset numid=1 -- 100%

        Also set this to make sure the audio is routed to the jack in stereo
        amixer cset numid=3 1
        """
        pass

    async def play_audio(self, filename):
        """ Plays an audio file in a subprocess

        :param filename: the audio file to play
        """
        
        player = await asyncio.create_subprocess_exec(*["mpg321", filename],
                                                      stdin=subprocess.DEVNULL,
                                                      stdout=subprocess.DEVNULL,
                                                      stderr=subprocess.DEVNULL)
        # result = await player.wait()  # wait until subprocess finishes, this is blocking?!

    def shutdown(self):
        """ Shuts down pyaudio interface """
        pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    audio = Audio()
    loop.run_until_complete(audio.play_audio('static/audio/hello_son.mp3'))
    loop.close()
