#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

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
import simplevector
import gui
import time

LOG_VIEWER = None

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d/%m/%y %H:%M',
                    filename='../gc.log',
                    filemode='w')

gc_log = logging.getLogger()

class StateVector(object):
    def __init__(self):
        self.position_vector = {
            "lat": 0.0,
            "long": 0.0,
            "alt": 0.0,
        }
        self.velocity_vector = simplevector.Vector(0, 0, 0)
        self.time = 0.0

class Attitude(object):
    def __init__(self, pitch=0.0, roll=0.0, yaw=0.0):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw

def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes, seconds

def log(message, log_type="debug"):
    now = time.strftime("%d/%m/%Y %H:%M:%S")
    LOG_VIEWER.viewer.AppendText(now + ": " + message + "\n")
    if log_type == "debug":
        gc_log.debug(message)
