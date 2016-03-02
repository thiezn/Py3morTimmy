#!/usr/bin/env python3

import numpy

def moving_average(interval, window_size):
    """ This returns the moving average of a list

    :param interval: List of values
    :param window_size: the number of samples """
    window = numpy.ones(int(window_size))/float(window_size)
    return int(numpy.convolve(interval, window, 'valid')[0])
