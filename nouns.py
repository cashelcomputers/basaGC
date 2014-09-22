#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright 2014 Tim Buchanan, cashelcomputers (at) gmail.com
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

import wx
import datetime
import logging
import math
import config

log = logging.getLogger("Nouns")

memory = None
computer = None
dsky = None
frame = None

def octal(value):
    return int(oct(value))

class NounNotImplementedError(Exception):
    
    """ This exception should be raised when a selected noun is not implemented
        yet
    """
    
    pass

#-----------------------BEGIN NORMAL NOUNS--------------------------------------

# no noun 00

def noun01(calling_verb):
    description = "Specify address and display in fractional format"
    raise NounNotImplementedError

def noun02(calling_verb=None, data=None, base=8):
    description = "Specify address and display as whole number"
    if data == None:
        dsky.request_data(calling_verb, 3)
        return "need data"
    else:
        data = int(data)
        data = octal(data)
        print("BASE: {}".format(base))
        if base == 8:
            return_data = {
                1: memory.memory[data].get_oct(),
                2: memory.memory[data + 1].get_oct(),
                3: memory.memory[data + 2].get_oct(),
                "description": "Data in location",
                "is_octal": True,
                "number": 2,
            }
        elif base == 10:
            return_data = {
                1: memory.memory[data].get_int,
                2: memory.memory[data + 1].get_int,
                3: memory.memory[data + 2].get_int,
                "description": "Data in location",
                "is_octal": False,
                "number": 2,
            }
        else:
            raise ValueError("Base must be either 8 or 10")
        print(return_data)
        return return_data

def noun03(calling_verb):
    description = "Specify address and display as degrees"
    raise NounNotImplementedError

# no noun 04

def noun05(calling_verb):
    raise NounNotImplementedError

def noun06(calling_verb):
    raise NounNotImplementedError

def noun07(calling_verb):
    raise NounNotImplementedError

def noun08(calling_verb):
    raise NounNotImplementedError

def noun09(calling_verb):
    log.info("Noun 09 requested")
    alarm_codes = computer.state["alarm_codes"]
    data = {
        1: alarm_codes[0],
        2: alarm_codes[1],
        3: alarm_codes[2],
        "description": "Alarm codes (first, second, last)",
        "is_octal": True,
        "number": 9,
    }
    return data

def noun10(calling_verb):
    raise NounNotImplementedError

def noun11(calling_verb):
    raise NounNotImplementedError

def noun12(calling_verb):
    raise NounNotImplementedError

def noun13(calling_verb):
    raise NounNotImplementedError

def noun14(calling_verb):
    raise NounNotImplementedError

def noun15(calling_verb):
    raise NounNotImplementedError

def noun16(calling_verb):
    raise NounNotImplementedError

def noun17(calling_verb):
    raise NounNotImplementedError

def noun18(calling_verb):
    raise NounNotImplementedError

# no noun 19

def noun20(calling_verb):
    raise NounNotImplementedError

def noun21(calling_verb):
    raise NounNotImplementedError
    """PIPA'S"""
    #inputs = computer.
    #data = {
        #1: 
        #2: 
        #3: 
        #"description": "PIPA pulse rate for X, Y, Z axis",
        #"is_octal": False,
        #"number": 21,
    #}
    #return data

def noun22(calling_verb):
    raise NounNotImplementedError

# no noun 23

def noun24(calling_verb):
    raise NounNotImplementedError

def noun25(calling_verb):
    raise NounNotImplementedError

def noun26(calling_verb):
    raise NounNotImplementedError

def noun27(calling_verb):
    raise NounNotImplementedError

# no noun 28

def noun29(calling_verb):
    raise NounNotImplementedError

def noun30(calling_verb):
    raise NounNotImplementedError

def noun31(calling_verb):
    raise NounNotImplementedError

def noun32(calling_verb):
    raise NounNotImplementedError

def noun33(calling_verb):
    raise NounNotImplementedError

def noun34(calling_verb):
    raise NounNotImplementedError

def noun35(calling_verb):
    raise NounNotImplementedError

def noun36(*args, **kwargs):
    
    telemetry = memory.get_memory(["met"])
    minutes, seconds = divmod(telemetry["met"], 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    milliseconds, seconds = math.modf(seconds)
    milliseconds = milliseconds * 100
    print(days, hours, minutes, seconds, milliseconds)
    data = {
        1: (int(days) * 100) + int(hours),
        2: int(minutes),
        3: (int(seconds)  * 100) + int(milliseconds),
        "description": "Time of AGC clock",
        "is_octal": False,
        "number": 36,
    }
    return data

def noun37(calling_verb):
    raise NounNotImplementedError

def noun38(calling_verb):
    raise NounNotImplementedError

def noun39(calling_verb):
    raise NounNotImplementedError

#-----------------------BEGIN MIXED NOUNS--------------------------------------

def noun40(calling_verb):
    raise NounNotImplementedError

def noun41(calling_verb):
    raise NounNotImplementedError

def noun42(calling_verb):
    raise NounNotImplementedError

def noun43(calling_verb):
    raise NounNotImplementedError

def noun44(calling_verb=None):

    apoapsis = str(round(computer.memory.get_memory("apoapsis") / 100, 1))
    periapsis = str(round(computer.memory.get_memory("periapsis") / 100, 1))
    tff = int(computer.memory.get_memory("orbital_period"))

    apoapsis = apoapsis.replace(".", "")
    periapsis = periapsis.replace(".", "")

    tff_minutes, tff_seconds = divmod(tff, 60)
    tff_hours, tff_minutes = divmod(tff_minutes, 60)

    tff = str(tff_hours) + str(tff_minutes) + str(tff_seconds)
    print(tff)

    data = {
        1: int(apoapsis),
        2: int(periapsis),
        3: int(tff),
        # "description": "Orbital Parameter Display",
        "is_octal": False,
        "number": 44,
    }
    return data

def noun45(calling_verb):
    raise NounNotImplementedError

def noun46(calling_verb):
    raise NounNotImplementedError

def noun47(calling_verb):
    raise NounNotImplementedError

def noun48(calling_verb):
    raise NounNotImplementedError

def noun49(calling_verb):
    raise NounNotImplementedError

def noun50(calling_verb):
    raise NounNotImplementedError

def noun51(calling_verb):
    raise NounNotImplementedError

def noun52(calling_verb):
    raise NounNotImplementedError

def noun53(calling_verb):
    raise NounNotImplementedError

def noun54(calling_verb):
    raise NounNotImplementedError

def noun55(calling_verb):
    raise NounNotImplementedError

def noun56(calling_verb):
    raise NounNotImplementedError

# no noun 57

def noun58(calling_verb):
    raise NounNotImplementedError

def noun59(calling_verb):
    raise NounNotImplementedError

def noun60(calling_verb):
    raise NounNotImplementedError

def noun61(calling_verb):
    raise NounNotImplementedError

def noun62():

    """Surface Velocity (m/s), Altitude rate (m/s), Altitude (km)"""
    log.info("Noun 62 requested")
    
    surface_velocity = str(round(computer.memory.get_memory("surface_velocity"), 1))
    altitude_rate = str(round(computer.memory.get_memory("vertical_speed"), 1))
    altitude = str(round(computer.memory.get_memory("asl") / 1000, 1))

    surface_velocity = surface_velocity.replace(".", "")
    altitude_rate = altitude_rate.replace(".", "")
    altitude = altitude.replace(".", "")
    
    print(surface_velocity, altitude_rate, altitude)
    
    data = {
        1: int(surface_velocity),
        2: int(altitude_rate),
        3: int(altitude),
        #"description": "Alarm codes (first, second, last)",
        "is_octal": False,
        "number": 62,
    }
    return data

def noun63(calling_verb):
    raise NounNotImplementedError

def noun64(calling_verb):
    raise NounNotImplementedError

def noun65(calling_verb):
    raise NounNotImplementedError

def noun66(calling_verb):
    raise NounNotImplementedError

def noun67(calling_verb):
    raise NounNotImplementedError

def noun68(calling_verb):
    raise NounNotImplementedError

def noun69(calling_verb):
    raise NounNotImplementedError

def noun70(calling_verb):
    raise NounNotImplementedError

def noun71(calling_verb):
    raise NounNotImplementedError

# no noun 72

def noun73(calling_verb):
    raise NounNotImplementedError

def noun74(calling_verb):
    raise NounNotImplementedError

def noun75(calling_verb):
    raise NounNotImplementedError

# no noun 76

# no noun 77

def noun78(calling_verb):
    raise NounNotImplementedError

def noun79(calling_verb):
    raise NounNotImplementedError

def noun80(calling_verb):
    raise NounNotImplementedError

def noun81(calling_verb):
    raise NounNotImplementedError

def noun82(calling_verb):
    raise NounNotImplementedError

def noun83(calling_verb):
    raise NounNotImplementedError

def noun84(calling_verb):
    raise NounNotImplementedError

def noun85(calling_verb):
    raise NounNotImplementedError

def noun86(calling_verb):
    raise NounNotImplementedError

def noun87(calling_verb):
    raise NounNotImplementedError

def noun88(calling_verb):
    raise NounNotImplementedError

def noun89(calling_verb):
    raise NounNotImplementedError

def noun90(calling_verb):
    raise NounNotImplementedError

def noun91(calling_verb):
    raise NounNotImplementedError

def noun92(calling_verb):
    raise NounNotImplementedError

def noun93(calling_verb):
    raise NounNotImplementedError

def noun94(calling_verb):
    raise NounNotImplementedError

def noun95(calling_verb):
    raise NounNotImplementedError

def noun96(calling_verb):
    raise NounNotImplementedError

def noun97(calling_verb):
    raise NounNotImplementedError

def noun98(calling_verb):
    raise NounNotImplementedError

def noun99(calling_verb):
    raise NounNotImplementedError


