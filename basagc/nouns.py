#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
""" This module contains all nouns used by the guidance computer.
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

from collections import OrderedDict
import inspect
import sys

from telemachus import get_telemetry, TelemetryNotAvailable
import utils

gc = None

def octal(value):

    """ Converts a value to octal, but not written as Ooxxx
    :param value: the value to convert
    :return: the octal value
    :rtype: int
    """

    return int(oct(value))


class NounNotImplementedError(Exception):

    """ This exception should be raised when a selected noun is not implemented
        yet
    """

    pass

# -----------------------BEGIN NORMAL NOUNS--------------------------------------

# no noun 00

# def noun01(calling_verb):
#     description = "Specify address and display in fractional format"
#     raise NounNotImplementedError

# def noun02(calling_verb=None, data=None, base=8):
#
#     if data == None:
#         dsky.request_data(calling_verb, 3)
#         return "need data"
#     else:
#         data = int(data)
#         data = octal(data)
#         print("BASE: {}".format(base))
#         if base == 8:
#             return_data = {
#                 1: memory.memory[data].get_oct(),
#                 2: memory.memory[data + 1].get_oct(),
#                 3: memory.memory[data + 2].get_oct(),
#                 "description": "Data in location",
#                 "is_octal": True,
#             }
#         elif base == 10:
#             return_data = {
#                 1: memory.memory[data].get_int,
#                 2: memory.memory[data + 1].get_int,
#                 3: memory.memory[data + 2].get_int,
#                 "description": "Data in location",
#                 "is_octal": False,
#             }
#         else:
#             raise ValueError("Base must be either 8 or 10")
#         return return_data

# def noun03(calling_verb):
#     description = "Specify address and display as degrees"
#     raise NounNotImplementedError

# no noun 04

# def noun05(calling_verb):
#     raise NounNotImplementedError
#
# def noun06(calling_verb):
#     raise NounNotImplementedError
#
# def noun07(calling_verb):
#     raise NounNotImplementedError
#
# def noun08(calling_verb):
#     raise NounNotImplementedError


class Noun(object):

    def __init__(self, description, number):
        self.description = description
        self.number = number

    def return_data(self):
        raise NounNotImplementedError


class Noun09(Noun):

    def __init__(self):
        super(Noun09, self).__init__(description="Alarm Codes", number="09")

    def return_data(self):

        utils.log("Noun 09 requested")
        alarm_codes = gc.alarm_codes
        data = {
            1: str(alarm_codes[0]),
            2: str(alarm_codes[1]),
            3: str(alarm_codes[2]),
            "is_octal": True,
            "tooltips": [
                "First alarm code",
                "Second alarm code",
                "Last alarm code",
            ],
        }
        return data


# def noun09(calling_verb):
#
#     """ Alarm codes.
#     :param calling_verb: the verb calling the noun.
#     :return: noun data
#     """
#     description = "Alarm codes (first, second, last)"
#     utils.log("Noun 09 requested")
#     alarm_codes = computer.alarm_codes
#     data = {
#         1: alarm_codes[0],
#         2: alarm_codes[1],
#         3: alarm_codes[2],
#         "is_octal": True,
#     }
#     return data

# def noun10(calling_verb):
#     raise NounNotImplementedError
#
# def noun11(calling_verb):
#     raise NounNotImplementedError
#
# def noun12(calling_verb):
#     raise NounNotImplementedError
#
# def noun13(calling_verb):
#     raise NounNotImplementedError
#
class Noun14(Noun):

    def __init__(self):
        super(Noun14, self).__init__(description="Burn error display (Expected Δv at cutoff (xxxxx m/s), Actual Δv at"
                                                 "cutoff (xxxxx m/s), Difference (xxxx.x m/s)",
                                     number="14")

    def return_data(self):
        if not gc.next_burn:
            gc.program_alarm(115)
            return False
        burn = gc.next_burn
        expected_delta_v_at_cutoff = burn.velocity_at_cutoff
        actual_delta_v_at_cutoff = get_telemetry("orbitalVelocity")
        delta_v_error = actual_delta_v_at_cutoff - expected_delta_v_at_cutoff

        expected_delta_v_at_cutoff = str(int(expected_delta_v_at_cutoff)).replace(".", "")
        actual_delta_v_at_cutoff = str(int(actual_delta_v_at_cutoff)).replace(".", "")
        delta_v_error = str(round(delta_v_error, 1)).replace(".", "")

        data = {
            1: expected_delta_v_at_cutoff,
            2: actual_delta_v_at_cutoff,
            3: delta_v_error,
            "is_octal": False,
        }
        return data

#
# def noun15(calling_verb):
#     raise NounNotImplementedError
#
# def noun16(calling_verb):
#     raise NounNotImplementedError

class Noun17(Noun):

    def __init__(self):
        super(Noun17, self).__init__("Attitude (Roll, Pitch, Yaw)", number="17")

    def return_data(self):

        # FIXME: need to make sure that data is correct length (sometimes drops the last 0 when input is xxx.x rather
        # then xxx.xx
        try:
            roll = str(round(get_telemetry("roll"), 1))
            pitch = str(round(get_telemetry("pitch"), 1))
            yaw = str(round(get_telemetry("heading"), 1))
        except TelemetryNotAvailable:
            raise

        roll = roll.replace(".", "")
        pitch = pitch.replace(".", "")
        yaw = yaw.replace(".", "")

        data = {
            1: roll,
            2: pitch,
            3: yaw,
            "is_octal": False,
            "tooltips": [
                "Roll (0xxx.x°)",
                "Pitch (0xxx.x°)",
                "Yaw (0xxx.x°)",
            ],
        }
        return data


# def noun17(calling_verb=None):
#
#     """ Roll, Pitch, Yaw.
#     :param calling_verb: the verb calling the noun.
#     :return: noun data
#     """
#
#     description = "Attitude (Roll, Pitch, Yaw)"
#
#     # FIXME: need to make sure that data is correct length (sometimes drops the last 0 when input is xxx.x rather than
#     # xxx.xx
#     roll = str(round(get_telemetry("roll"), 2))
#     pitch = str(round(get_telemetry("pitch"), 2))
#     yaw = str(round(get_telemetry("heading"), 2))
#
#     roll = roll.replace(".", "")
#     pitch = pitch.replace(".", "")
#     yaw = yaw.replace(".", "")
#
#     data = {
#         1: int(roll),
#         2: int(pitch),
#         3: int(yaw),
#         "is_octal": False,
#     }
#     return data

# def noun18(calling_verb):
#     raise NounNotImplementedError
#
# # no noun 19
#
# def noun20(calling_verb):
#     raise NounNotImplementedError
#
# def noun21(calling_verb):
#     raise NounNotImplementedError
#
#
# def noun22(calling_verb):
#     raise NounNotImplementedError
#
# # no noun 23
#
# def noun24(calling_verb):
#     raise NounNotImplementedError
#
# def noun25(calling_verb):
#     raise NounNotImplementedError
#
# def noun26(calling_verb):
#     raise NounNotImplementedError
#
# def noun27(calling_verb):
#     raise NounNotImplementedError
#
# # no noun 28
#
# def noun29(calling_verb):
#     raise NounNotImplementedError
#
class Noun30(Noun):
    def __init__(self):
        super(Noun30, self).__init__("Octal Target ID (000XX)", number="30")

    def return_data(self):

        target_id = gc.noun_data["30"]
        data = {
            1: target_id,
            2: None,
            3: None,
            "tooltips": ["Target Octal ID", None, None],
            "is_octal": True,
        }
        return data

    def receive_data(self, data):
        gc.noun_data["30"] = data
#
# def noun31(calling_verb):
#     raise NounNotImplementedError
#
# def noun32(calling_verb):
#     raise NounNotImplementedError
#
# def noun33(calling_verb):
#     raise NounNotImplementedError
#
# def noun34(calling_verb):
#     raise NounNotImplementedError
#
# def noun35(calling_verb):
#     raise NounNotImplementedError

class Noun33(Noun):

    def __init__(self):
        super(Noun33, self).__init__("Time to Ignition (00xxx hours, 000xx minutes, 0xx.xx seconds)", number="33")

    def return_data(self):

        if not gc.next_burn:
            gc.program_alarm(alarm_code=115, message="No burn data loaded")
            return False

        time_of_ignition = utils.seconds_to_time(burn.start_time)
        hours = str(int(time_of_ignition["hours"]))
        minutes = str(int(time_of_ignition["minutes"]))
        seconds = str(time_of_ignition["seconds"]).replace(".", "")

        data = {
            1: "-" + hours,
            2: "-bbb" + minutes,
            3: "-b" + seconds,
            "tooltips": [
                "Time To Ignition (hhhhh)",
                "Time To Ignition (bbbmm)",
                "Time To Ignition (bss.ss)",
            ],
            "is_octal": False,
        }
        return data


class Noun36(Noun):

    def __init__(self):
        super(Noun36, self).__init__("Mission Elapsed Time (MET) (dddhh, bbbmm, bss.ss)", number="36")

    def return_data(self):
        try:
            telemetry = get_telemetry("missionTime")
        except TelemetryNotAvailable:
            raise

        minutes, seconds = divmod(telemetry, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        days = str(int(days)).zfill(2)
        hours = str(int(hours)).zfill(2)
        minutes = str(int(minutes)).zfill(2)
        seconds = str(round(seconds, 2)).replace(".", "").zfill(4)

        data = {
            1: days + "b" + hours,
            2: "bbb" + minutes,
            3: "b" + seconds,
            "tooltips": [
                "Mission Elapsed Time (ddbhh)",
                "Mission Elapsed Time (bbbmm)",
                "Mission Elapsed Time (bss.ss)",
            ],
            "is_octal": False,
        }
        return data

# def noun36(calling_verb=None):
#
#     """ Mission Elapsed Time.
#     :param calling_verb: the verb calling the noun.
#     :return: noun data
#     """
#
#     description = "Mission Elapsed Time (MET) (dddhh, bbbmm, bss.ss)"
#
#     telemetry = get_telemetry("missionTime")
#     minutes, seconds = divmod(telemetry, 60)
#     hours, minutes = divmod(minutes, 60)
#     days, hours = divmod(hours, 24)
#     milliseconds, seconds = math.modf(seconds)
#     milliseconds *= 100
#
#     data = {
#         1: (int(days) * 100) + int(hours),
#         2: int(minutes),
#         3: (int(seconds) * 100) + int(milliseconds),
#         "tooltips": [
#             "Mission Elapsed Time (dddhh)",
#             "Mission Elapsed Time (bbbmm)",
#             "Mission Elapsed Time (bss.ss)",
#         ],
#         "is_octal": False,
#     }
#     return data

# def noun37(calling_verb):
#     raise NounNotImplementedError
#
# def noun38(calling_verb):
#     raise NounNotImplementedError
#
# def noun39(calling_verb):
#     raise NounNotImplementedError

#-----------------------BEGIN MIXED NOUNS--------------------------------------

class Noun40(Noun):

    def __init__(self):
        super(Noun40, self).__init__("Burn Data (Time from ignition, Δv to be gained, accumulated Δv", number="40")

    def return_data(self):
        if not gc.next_burn:
            gc.program_alarm(115)
            return False
        burn = gc.next_burn
        time_to_ignition = utils.seconds_to_time(burn.time_until_ignition)
        minutes_to_ignition = str(int(time_to_ignition["minutes"])).zfill(2)
        seconds_to_ignition = str(int(time_to_ignition["seconds"])).zfill(2)
        delta_v_gain = str(int(burn.delta_v_required)).replace(".", "")
        accumulated_delta_v = str(int(burn.accumulated_delta_v)).replace(".", "")

        data = {
            1: minutes_to_ignition + "b" + seconds_to_ignition,
            2: delta_v_gain,
            3: accumulated_delta_v,
            "is_octal": False,
            "tooltips": [
                "Time From Ignition (mmbss minutes, seconds)",
                "Δv (xxxxx m/s)",
                "Accumulated Δv (xxxxx m/s)",
            ],
        }
        return data

class Noun43(Noun):

    def __init__(self):
        super(Noun43, self).__init__("Geographic Position (Latitude, Longitude, Altitude)", number="43")

    def return_data(self):
        try:
            # latitude = str(round(get_telemetry("lat"), 2)).replace(".", "").zfill(5)
            # longitude = str(round(get_telemetry("long"), 2)).replace(".", "").zfill(5)
            # altitude = str(round(get_telemetry("altitude") / 1000, 1)).replace(".", "").zfill(5)
            latitude = str(round(get_telemetry("lat"), 2))
            longitude = str(round(get_telemetry("long"), 2))
            altitude = str(round(get_telemetry("altitude") / 1000, 1))
        except TelemetryNotAvailable:
            raise

        # the following fixes a problem that round() will discard a trailing 0 eg 100.10 becomes 100.1
        if latitude[-2] == ".":
            latitude += "0"
        if longitude[-2] == ".":
            longitude += "0"

        latitude = latitude.replace(".", "")
        longitude = longitude.replace(".", "")
        altitude = altitude.replace(".", "")

        data = {
            1: latitude,
            2: longitude,
            3: altitude,
            "is_octal": False,
            "tooltips": [
                "Latitude (xxx.xx°)",
                "Longitude (xxx.xx°)",
                "Altitude",  # TODO
            ],
        }
        return data

class Noun44(Noun):
    def __init__(self):
        super(Noun44, self).__init__("Apoapsis (xxx.xx km), Periapsis (xxx.xx km), Time To Apoapsis (hmmss)",
                                     number="44")

    def return_data(self):
        try:
            apoapsis = str(round(get_telemetry("ApA") / 100, 1))
            periapsis = str(round(get_telemetry("PeA") / 100, 1))
            tff = int(get_telemetry("timeToAp"))
        except TelemetryNotAvailable:
            raise

        apoapsis = apoapsis.replace(".", "")
        periapsis = periapsis.replace(".", "")

        tff_minutes, tff_seconds = divmod(tff, 60)
        tff_hours, tff_minutes = divmod(tff_minutes, 60)

        tff = str(tff_hours).zfill(1) + str(tff_minutes).zfill(2) + str(tff_seconds).zfill(2)

        data = {
            1: apoapsis,
            2: periapsis,
            3: tff,
            "tooltips": [
                "Apoapsis Altitude (xxx.xx km)",
                "Periapsis Altitude (xxx.xx km)",
                "Time to Apoapsis (hmmss)"
            ],
            "is_octal": False,
        }
        return data

# def noun44(calling_verb=None):
#
#     """ Apoapsis altitude, periapsis altitude, time to apoapsis..
#     :param calling_verb: the verb calling the noun.
#     :return: noun data
#     """
#
#     description = "Apoapsis (xxx.xx km), Periapsis (xxx.xx km), Time To Apoapsis (hmmss)"
#
#     apoapsis = str(round(get_telemetry("ApA") / 100, 1))
#     periapsis = str(round(get_telemetry("PeA") / 100, 1))
#     tff = int(get_telemetry("timeToAp"))
#
#     apoapsis = apoapsis.replace(".", "")
#     periapsis = periapsis.replace(".", "")
#
#     tff_minutes, tff_seconds = divmod(tff, 60)
#     tff_hours, tff_minutes = divmod(tff_minutes, 60)
#
#     tff = str(tff_hours).zfill(2) + str(tff_minutes).zfill(2) + str(tff_seconds).zfill(2)
#
#     data = {
#         1: int(apoapsis),
#         2: int(periapsis),
#         3: int(tff),
#         "tooltips": [
#             "Apoapsis Altitude (xxx.xx km)",
#             "Periapsis Altitude (xxx.xx km)",
#             "Time to Apoapsis (hmmss)"
#         ],
#         "is_octal": False,
#     }
#     return data

# def noun45(calling_verb):
#     raise NounNotImplementedError
#
# def noun46(calling_verb):
#     raise NounNotImplementedError
#
# def noun47(calling_verb):
#     raise NounNotImplementedError
#
# def noun48(calling_verb):
#     raise NounNotImplementedError
#
# def noun49(calling_verb):
#     raise NounNotImplementedError

class Noun50(Noun):
    def __init__(self):
        super(Noun50, self).__init__("Surface Velocity Display (X, Y, Z in xxxx.x m/s)", number="50")

    def return_data(self):
        surface_velocity_x = str(round(get_telemetry("surfaceVelocityx"), 1)).replace(".", "")
        surface_velocity_y = str(round(get_telemetry("surfaceVelocityy"), 1)).replace(".", "")
        surface_velocity_z = str(round(get_telemetry("surfaceVelocityz"), 1)).replace(".", "")

        data = {
            1: surface_velocity_x,
            2: surface_velocity_y,
            3: surface_velocity_z,
            "tooltips": [
                "Surface Velocity X (xxxx.x m/s)",
                "Surface Velocity Y (xxxx.x m/s)",
                "Surface Velocity Z (xxxx.x m/s)"
            ],
            "is_octal": False,
        }
        return data

# def noun50(calling_verb=None):
#
#     """ Surface velocity X, Y, Z.
#     :param calling_verb: the verb calling the noun.
#     :return: noun data
#     """
#
#     description = "Surface Velocity Display (X, Y, Z in xxxx.x m/s)"
#
#     surface_velocity_x = str(round(get_telemetry("surfaceVelocityx"))).replace(".", "")
#     surface_velocity_y = str(round(get_telemetry("surfaceVelocityy"))).replace(".", "")
#     surface_velocity_z = str(round(get_telemetry("surfaceVelocityz"))).replace(".", "")
#
#     data = {
#         1: int(surface_velocity_x),
#         2: int(surface_velocity_y),
#         3: int(surface_velocity_z),
#         "tooltips": [
#             "Surface Velocity X (xxxx.x m/s)",
#             "Surface Velocity Y (xxxx.x m/s)",
#             "Surface Velocity Z (xxxx.x m/s)"
#         ],
#         "is_octal": False,
#     }
#     return data

# def noun51(calling_verb):
#     raise NounNotImplementedError
#
# def noun52(calling_verb):
#     raise NounNotImplementedError
#
# def noun53(calling_verb):
#     raise NounNotImplementedError
#
# def noun54(calling_verb):
#     raise NounNotImplementedError
#
# def noun55(calling_verb):
#     raise NounNotImplementedError
#
# def noun56(calling_verb):
#     raise NounNotImplementedError
#
# # no noun 57
#
# def noun58(calling_verb):
#     raise NounNotImplementedError
#
# def noun59(calling_verb):
#     raise NounNotImplementedError
#
# def noun60(calling_verb):
#     raise NounNotImplementedError
#
# def noun61(calling_verb):
#     raise NounNotImplementedError


class Noun62(Noun):
    def __init__(self):
        super(Noun62, self).__init__("Surface Velocity, Altitude Rate, Altitude", number="62")

    def return_data(self):
        surface_velocity = str(round(get_telemetry("surfaceVelocity"), 1))
        altitude_rate = str(round(get_telemetry("verticalSpeed"), 1))
        altitude = str(round(get_telemetry("altitude") / 1000, 1))

        surface_velocity = surface_velocity.replace(".", "")
        altitude_rate = altitude_rate.replace(".", "")
        altitude = altitude.replace(".", "")

        data = {
            1: surface_velocity,
            2: altitude_rate,
            3: altitude,
            "is_octal": False,
            "tooltips": [
                "Surface Velocity (xxxx.x m/s)",
                "Altitude Rate (xxxx.x m/s)",
                "Altitude (xxxx.x km)",
            ],
        }
        return data

# def noun62(calling_verb=None):
#
#     """ Surface Velocity, vertical speed, altitude
#     :param calling_verb: the verb calling the noun.
#     :return: noun data
#     """
#
#     description = "Surface Velocity, Altitude Rate, Altitude"
#
#     surface_velocity = str(round(get_telemetry("surfaceVelocity"), 1))
#     altitude_rate = str(round(get_telemetry("verticalSpeed"), 1))
#     altitude = str(round(get_telemetry("altitude") / 1000, 1))
#
#     surface_velocity = surface_velocity.replace(".", "")
#     altitude_rate = altitude_rate.replace(".", "")
#     altitude = altitude.replace(".", "")
#
#
#     data = {
#         1: int(surface_velocity),
#         2: int(altitude_rate),
#         3: int(altitude),
#         "is_octal": False,
#     }
#     return data

# def noun63(calling_verb):
#     raise NounNotImplementedError
#
# def noun64(calling_verb):
#     raise NounNotImplementedError
#
# def noun65(calling_verb):
#     raise NounNotImplementedError
#
# def noun66(calling_verb):
#     raise NounNotImplementedError
#
# def noun67(calling_verb):
#     raise NounNotImplementedError
#
# def noun68(calling_verb):
#     raise NounNotImplementedError
#
# def noun69(calling_verb):
#     raise NounNotImplementedError
#
# def noun70(calling_verb):
#     raise NounNotImplementedError
#
# def noun71(calling_verb):
#     raise NounNotImplementedError
#
# # no noun 72
#
# def noun73(calling_verb):
#     raise NounNotImplementedError
#
# def noun74(calling_verb):
#     raise NounNotImplementedError
#
# def noun75(calling_verb):
#     raise NounNotImplementedError
#
# # no noun 76
#
# # no noun 77
#
# def noun78(calling_verb):
#     raise NounNotImplementedError
#
# class Noun79(Noun):
#
#     def __init__(self):
#         super(Noun79, self).__init__("FILL ME IN")
#
# def noun80(calling_verb):
#     raise NounNotImplementedError
#
# def noun81(calling_verb):
#     raise NounNotImplementedError
#
# def noun82(calling_verb):
#     raise NounNotImplementedError
#
# def noun83(calling_verb):
#     raise NounNotImplementedError
#
# def noun84(calling_verb):
#     raise NounNotImplementedError
#
# def noun85(calling_verb):
#     raise NounNotImplementedError
#
# def noun86(calling_verb):
#     raise NounNotImplementedError
#
# def noun87(calling_verb):
#     raise NounNotImplementedError
#
# def noun88(calling_verb):
#     raise NounNotImplementedError
#
# def noun89(calling_verb):
#     raise NounNotImplementedError
#
# def noun90(calling_verb):
#     raise NounNotImplementedError
#
# def noun91(calling_verb):
#     raise NounNotImplementedError
#
# def noun92(calling_verb):
#     raise NounNotImplementedError
#
# def noun93(calling_verb):
#     raise NounNotImplementedError
#
# def noun94(calling_verb):
#     raise NounNotImplementedError
#


class Noun95(Noun):
    
    def __init__(self):
        super(Noun95, self).__init__(description="Hohmann Transfer Data Display", number="95")

    def return_data(self):

        if not gc.next_burn:
            gc.program_alarm(115)
            return False

        time_to_ignition = utils.seconds_to_time(gc.next_burn.time_until_ignition)
        minutes_to_ignition = str(int(time_to_ignition["minutes"])).zfill(2)
        seconds_to_ignition = str(int(time_to_ignition["seconds"])).zfill(2)
        delta_v = str(int(gc.next_burn.delta_v_required))
        velocity_at_cutoff = str(int(gc.next_burn.velocity_at_cutoff))

        data = {
            1: minutes_to_ignition + "b" + seconds_to_ignition,
            2: delta_v,
            3: velocity_at_cutoff,
            "is_octal": False,
            "tooltips": [
                "Time To Ignition (TIG) (xxbxx mins, seconds)",
                "Δv (xxxxx m/s)",
                "Velocity at cutoff (xxxxx m/s)",
            ],
        }
        return data

#
# def noun96(calling_verb):
#     raise NounNotImplementedError
#
# def noun97(calling_verb):
#     raise NounNotImplementedError
#
# def noun98(calling_verb):
#     raise NounNotImplementedError
#
# def noun99(calling_verb):
#     raise NounNotImplementedError

# generate a OrderedDict of all nouns for inclusion in the computer
nouns = OrderedDict()
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for class_tuple in clsmembers:
    if class_tuple[0][-1].isdigit():
        nouns[class_tuple[0][-2:]] = class_tuple[1]

