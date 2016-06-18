#!/usr/bin/env python3
""" This module contains all nouns used by the guidance computer."""

# noinspection PyUnresolvedReferences
import math
import inspect
import sys
from collections import OrderedDict

from basagc import config
if config.DEBUG:
    # noinspection PyUnresolvedReferences
    from pudb import set_trace  # lint:ok
from basagc import utils

vessel = None


class NounNotImplementedError(Exception):

    """ This exception should be raised when a selected noun is not implemented
        yet
    """

    pass


class Noun(object):

    def __init__(self, description, number):
        self.description = description
        self.number = number
        self.telemetry = {}  # this will be a dict of functions that when called returns the telemetry
        self.ksp = vessel.krpc_connection

# -----------------------BEGIN NORMAL NOUNS--------------------------------------

class Noun06(Noun):
    
    def __init__(self):
        super().__init__(description="Time to event", number="06")

    def return_data(self):

        self.telemetry["ut"] = self.ksp.get_telemetry("space_center", "ut")
        now = self.telemetry["ut"]()
        time_until_event = vessel.computer.noun_data["06"]
        if time_until_event == "":
            return False
        hms_until_event = utils.seconds_to_time(time_until_event)

        hours = "-" + str(hms_until_event["hours"]).replace(".", "").zfill(5)
        minutes = "-" + str(hms_until_event["minutes"]).replace(".", "").zfill(5)
        seconds = hms_until_event["seconds"]

        whole_seconds, frac_seconds = utils.float_to_parts(seconds)
        seconds = "-" + whole_seconds + frac_seconds

        data = {
            1: hours,
            2: minutes,
            3: seconds,
            "is_octal": False,
            "tooltips" : [
                "Hours until event",
                "Minutes until event",
                "Seconds until event"
                ],
            }
        return data

class Noun09(Noun):

    def __init__(self):
        super().__init__(description="Alarm Codes", number="09")

    def return_data(self):

        alarm_codes = vessel.computer.alarm_codes
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


class Noun14(Noun):

    def __init__(self):
        super().__init__(description="Burn error display (Expected Δv at cutoff (xxxxx m/s), Actual Δv at"
                                                 "cutoff (xxxxx m/s), Difference (xxxx.x m/s)",
                                     number="14")

    def return_data(self):
        if not vessel.next_burn:
            vessel.program_alarm(115)
            return False
        burn = vessel.next_burn
        expected_delta_v_at_cutoff = burn.velocity_at_cutoff
        actual_delta_v_at_cutoff = ksp.get_telemetry("flight", "speed", refssmat=config.REFSSMAT["planet_rotating"])  #TODO: check if this works
        delta_v_error = actual_delta_v_at_cutoff - expected_delta_v_at_cutoff

        expected_delta_v_at_cutoff = str(int(expected_delta_v_at_cutoff)).replace(".", "")
        actual_delta_v_at_cutoff = str(int(actual_delta_v_at_cutoff)).replace(".", "")
        delta_v_error = str(round(delta_v_error, 1)).replace(".", "")

        data = {
            1: expected_delta_v_at_cutoff,
            2: actual_delta_v_at_cutoff,
            3: delta_v_error,
            "tooltips": [
                "Expected velocity at cutoff (xxxxx m/s)",
                "Actual velocity at cutoff (xxxxx m/s)",
                "Velocity error (xxxx.x m/s)"
            ],
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
        super().__init__("Attitude (Roll, Pitch, Yaw)", number="17")

    def return_data(self):

        # FIXME: need to make sure that data is correct length (sometimes drops the last 0 when input is xxx.x rather
        # then xxx.xx
        # FIXME: note to self, this is figured out in other nouns that have already been changed to new API

        # get data from IMU
        pitch, roll, yaw = vessel.imu.get_pitch_roll_yaw()

        # format data
        roll = str(round(roll, 1))
        pitch = str(round(pitch, 1))
        yaw = str(round(yaw, 1))
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


class Noun25(Noun):
    
    def __init__(self):
        
        super().__init__("Spacecraft mass", number="25")

    def return_data(self):

        self.telemetry = {
            "mass": self.ksp.get_telemetry("vessel", "mass") / 1000
        }
        mass_whole_part, mass_frac_part = utils.float_to_parts(self.telemetry["mass"])

        data = {
            1: mass_whole_part,
            2: mass_frac_part,
            3: "bbbbb",
            "tooltips": ["Spacecraft mass (whole part, in tons)",
                         "Spacecraft mass (fractional part, in tons)", None],
            "is_octal": True,
        }
        return data


class Noun31(Noun):
    
    def __init__(self):
        
        super().__init__("Stage Max Thrust", number="31")

    def return_data(self):

        available_thrust_kn = self.ksp.get_telemetry("vessel", "available_thrust") / 1000
        thrust_whole_part, thrust_frac_part = utils.float_to_parts(available_thrust_kn)
        data = {
            1: thrust_whole_part,
            2: thrust_frac_part,
            3: "bbbbb",
            "tooltips": ["Stage Max Thrust (whole part) (kN)", "Stage Max Thrust (fractional part) (kN)", None],
            "is_octal": False,
        }
        #set_trace()
        return data

class Noun33(Noun):

    def __init__(self):
        super().__init__("Time to Ignition (00xxx hours, 000xx minutes, 0xx.xx seconds)", number="33")

    def return_data(self):

        if not vessel.next_burn:
            vessel.program_alarm(alarm_code=115, message="No burn data loaded")
            return False
        time_until_ignition = utils.seconds_to_time(vessel.next_burn.calculate_time_to_ignition())
        hours = str(int(time_until_ignition["hours"]))
        minutes = str(int(time_until_ignition["minutes"]))
        seconds = str(int(time_until_ignition["seconds"])).replace(".", "")

        data = {
            1: "-" + hours,
            2: "-000" + minutes,
            3: "-000" + seconds,
            "tooltips": [
                "Time To Ignition (hhhhh)",
                "Time To Ignition (bbbmm)",
                "Time To Ignition (bbbss)",
            ],
            "is_octal": False,
        }
        return data


class Noun36(Noun):

    def __init__(self):
        super().__init__("Mission Elapsed Time (MET) (dddhh, bbbmm, bss.ss)", number="36")

    def return_data(self):

        telemetry = get_telemetry("missionTime")

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

class Noun38(Noun):
    
    def __init__(self):
        
        super().__init__("Specific Impulse", number="38")

    def return_data(self):

        
        data = {
            1: vessel.noun_data["38"][0],
            2: "bbbbb",
            3: "bbbbb",
            "tooltips": ["Stage Specific Impulse (s) ", None, None],
            "is_octal": False,
        }
        return data

#-----------------------BEGIN MIXED NOUNS--------------------------------------

class Noun40(Noun):

    def __init__(self):
        super().__init__("Burn Data (Time from ignition, orbital velocity, accumulated Δv", number="40")

    def return_data(self):
        if not vessel.next_burn:
            vessel.program_alarm(115)
            return False
        burn = vessel.next_burn
        time_to_ignition = utils.seconds_to_time(burn.time_until_ignition)
        minutes_to_ignition = str(int(time_to_ignition["minutes"])).zfill(2)
        seconds_to_ignition = str(int(time_to_ignition["seconds"])).zfill(2)
        velocity = str(int(get_telemetry("orbitalVelocity"))).replace(".", "")
        accumulated_delta_v = str(int(burn.accumulated_delta_v)).replace(".", "")

        data = {
            1: "-" + minutes_to_ignition + "b" + seconds_to_ignition,
            2: velocity,
            3: accumulated_delta_v,
            "is_octal": False,
            "tooltips": [
                "Time From Ignition (mmbss minutes, seconds)",
                "Orbital Velocity (xxxxx m/s)",
                "Accumulated Δv (xxxxx m/s)",
            ],
        }
        return data

class Noun43(Noun):

    def __init__(self):
        super().__init__("Geographic Position (Latitude, Longitude, Altitude)", number="43")

    def return_data(self):
        # latitude = str(round(get_telemetry("lat"), 2)).replace(".", "").zfill(5)
        # longitude = str(round(get_telemetry("long"), 2)).replace(".", "").zfill(5)
        # altitude = str(round(get_telemetry("altitude") / 1000, 1)).replace(".", "").zfill(5)
        latitude = str(round(get_telemetry("lat"), 2))
        longitude = str(round(get_telemetry("long"), 2))
        altitude = str(round(get_telemetry("altitude") / 1000, 1))

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
        super().__init__("Apoapsis (xxxx.x km), Periapsis (xxxx.x km), Time To Apoapsis (hmmss)",
                                     number="44")

    def return_data(self):
        #try:
            #apoapsis = str(round(get_telemetry("ApA") / 100, 1))
            #periapsis = str(round(get_telemetry("PeA") / 100, 1))
            #tff = int(get_telemetry("timeToAp"))
        #except TelemetryNotAvailable:
            #raise
        apoapsis = str(round(ksp.get_telemetry("orbit", "apoapsis_altitude") / 1000, 1))
        periapsis = str(round(ksp.get_telemetry("orbit", "periapsis_altitude") / 1000, 1))
        tff = int(ksp.get_telemetry("orbit", "time_to_apoapsis"))
        print(apoapsis, periapsis, tff)

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
                "Apoapsis Altitude (xxxx.x km)",
                "Periapsis Altitude (xxxx.x km)",
                "Time to Apoapsis (hmmss)"
            ],
            "is_octal": False,
        }
        return data


#class Noun49(Noun):
    #def __init__(self):
        #super().__init__("Phase angles for automaneuver", number="49")
    #
    #def return_data(self):
        ## check that the maneuver has phase angles loaded
        #try:
            #if not computer.next_burn.calling_program and not computer.next_burn.calling_program.phase_angle_required:
                #computer.program_alarm(120)
                #return False
        #except AttributeError:
            #computer.program_alarm(120)
            #return False
        #
        #phase_angle_required = computer.next_burn.calling_program.phase_angle_required
        #telemachus_target_id = config.TELEMACHUS_BODY_IDS[computer.next_burn.calling_program.target_name]
        #current_phase_angle = get_telemetry("body_phaseAngle", body_number=telemachus_target_id)
        #phase_angle_difference = str(round(current_phase_angle - phase_angle_required, 1)).replace(".", "")
        #current_phase_angle = str(round(current_phase_angle, 1)).replace(".", "")
        #phase_angle_required = str(round(phase_angle_required, 1)).replace(".", "")
        #
        #data = {
            #1: phase_angle_required,
            #2: current_phase_angle,
            #3: phase_angle_difference,
            #"tooltips": [
                #"Phase Angle Required (0xxx.x °)",
                #"Current Phase Angle (0xxx.x °)",
                #"Phase Angle Difference (0xxx.x °)",
            #],
            #"is_octal": False,
        #}
        #return data
        

class Noun50(Noun):
    def __init__(self):
        super().__init__("Surface Velocity Display (X, Y, Z in xxxx.x m/s)", number="50")

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


class Noun62(Noun):
    def __init__(self):
        super().__init__("Orbital Velocity, Altitude Rate, Altitude", number="62")

    def return_data(self):
        surface_velocity = str(round(get_telemetry("relativeVelocity"), 1))
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
                "Inertial Velocity (xxxx.x m/s)",
                "Altitude Rate (xxxx.x m/s)",
                "Altitude (xxxx.x km)",
            ],
        }
        return data


class Noun95(Noun):
    
    def __init__(self):
        super().__init__(description="TMI Burn Data Display", number="95")

    def return_data(self):

        if not vessel.next_burn:
            vessel.program_alarm(115)
            return False

        time_to_ignition = utils.seconds_to_time(vessel.next_burn.time_until_ignition)
        minutes_to_ignition = str(int(time_to_ignition["minutes"])).zfill(2)
        seconds_to_ignition = str(int(time_to_ignition["seconds"])).zfill(2)
        delta_v = str(int(vessel.next_burn.delta_v_required))
        burn_duration = str(int(vessel.next_burn.burn_duration))

        data = {
            1: "-" + minutes_to_ignition + "b" + seconds_to_ignition,
            2: delta_v,
            3: burn_duration,
            "is_octal": False,
            "tooltips": [
                "Time To Ignition (TIG) (xxbxx mins, seconds)",
                "Δv (xxxxx m/s)",
                "Burn duration (xxxxx seconds)",
            ],
        }
        return data

# generate a OrderedDict of all nouns for inclusion in the computer
nouns = OrderedDict()
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for class_tuple in clsmembers:
    if class_tuple[0][-1].isdigit():
        nouns[class_tuple[0][-2:]] = class_tuple[1]

