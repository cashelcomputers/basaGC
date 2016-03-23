#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" This module contains various utility functions and classes used by basaGC
"""
#  This file is part of basaGC (https://github.com/cashelcomputers/basaGC),
#  copyright 2014 Tim Buchanan, cashelcomputers (at) gmail.com
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
#  Includes code and images from the Virtual AGC Project (http://www.ibiblio.org/apollo/index.html)
#  by Ronald S. Burkey <info@sandroid.org>

import logging
import time

import config

LOG_VIEWER = None

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d/%m/%y %H:%M',
                    filename='../gc.log',
                    filemode='w')

gc_log = logging.getLogger()


# class StateVector(object):
#
#     """ This class represents a state vector. Not currently used by any code!
#     """
#
#     def __init__(self):
#
#         """ Class constructor
#         """
#
#         self.position_vector = {
#             "lat": 0.0,
#             "long": 0.0,
#             "alt": 0.0,
#         }
#         self.velocity_vector = simplevector.Vector(0, 0, 0)
#         self.time = 0.0
#
#
# class Attitude(object):
#
#     """ This class represents a spacecraft attitude. Not currently used by any code!
#     """
#
#     def __init__(self, pitch=0.0, roll=0.0, yaw=0.0):
#         self.pitch = pitch
#         self.roll = roll
#         self.yaw = yaw
#

def seconds_to_time(seconds):

    """ Converts a time in seconds to days, hours, minutes and seconds
    :param seconds: time in seconds to convert
    :type seconds: int or float
    :return: tuple containing days, hours, minutes, seconds
    :rtype: tuple of ints
    """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": round(seconds, 2),
    }


def log(message, log_level="DEBUG"):

    """ Logs messages to log file and log viewer
    :param message: the message to log
    :type message: string
    :param log_level: the log level for this message
    :type log_level: string
    :return: nothing
    """

    if log_level not in config.LOG_LEVELS:
        gc_log.error("Log level does not exist!")
        return
    now = time.strftime("%d/%m/%Y %H:%M:%S")
    log_level_number = config.LOG_LEVELS.index(log_level)
    if log_level_number >= config.LOG_LEVELS.index(config.current_log_level):
        LOG_VIEWER.viewer.AppendText(now + ": " + log_level + ": " + message + "\n")
    if log_level == "DEBUG":
        gc_log.debug(message)
    elif log_level == "INFO":
        gc_log.info(message)
    elif log_level == "WARNING":
        gc_log.warning(message)
    elif log_level == "ERROR":
        gc_log.error(message)
    elif log_level == "CRITICAL":
        gc_log.critical(message)



# class Timer(object):
#
#     """ A timer for the guidance gc """
#
#     def __init__(self, interval, function, enable=False, *args, **kwargs):
#         self._timer = None
#         self.function = function
#         self.interval = interval
#         self.args = args
#         self.kwargs = kwargs
#         self.is_running = False
#         if enable:
#             self._run()
#
#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)
#
#     def start(self):
#         if not self.is_running:
#             self._timer = threading.Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True
#
#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False
