#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""This module contains internal routines used by the guidance computer."""

# This file is part of basaGC (https://github.com/cashelcomputers/basaGC),
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
#  Includes code and images from the Virtual AGC Project
#  (http://www.ibiblio.org/apollo/index.html) by Ronald S. Burkey
#  <info@sandroid.org>
import math

import config
import telemachus
import utils
from config import TELEMACHUS_BODY_IDS
from telemachus import get_telemetry

gc = None


class Burn(object):

    """ This object models a burn maneuver """

    def __init__(self, delta_v, direction, time_of_ignition, recalc_function=None, calling_program=None):

        """ Class constructor

        :param delta_v: delta_v required for burn
        :type delta_v: float
        :param direction: direction of burn
        :type direction: str (should be in config.DIRECTIONS)
        :param time_of_ignition: Time of Ignition, relative to Mission Elapsed Time
        :type time_of_ignition: float
        :return: None
        """

        self.recalc_function = recalc_function
        self.delta_v_required = delta_v
        self.direction = direction
        self.time_of_ignition = time_of_ignition
        self.is_display_blanked = False
        self.is_verb_99_executed = False
        self.time_until_ignition = self.calculate_time_to_ignition()
        self.velocity_at_cutoff = self._calculate_velocity_at_cutoff()
        self.is_directional_autopilot_engaged = False
        self.is_thrust_autopilot_engaged = False
        self.is_active = False
        self.initial_speed = 0.0
        self.accumulated_delta_v = 0.0
        self._is_thrust_reduced = False
        self.calling_program = calling_program

    def execute(self):

        """ Entry point to execute this burn.
        :return: None
        """

        # check if direction is valid
        if self.direction not in config.DIRECTIONS:
            gc.program_alarm(410)
            return
        # load the course start time monitor into the computers main loop
        gc.execute_verb(verb="16", noun="40")
        gc.main_loop_table.append(self._coarse_start_time_monitor)

    def terminate(self):

        """ Terminates the burn, disabling autopilot if running
        :return: None
        """
        self._disable_directional_autopilot()

        # if the throttle is open, close it
        if telemachus.get_telemetry("throttle") > 0:
            telemachus.cut_throttle()

        gc.remove_burn(self)

    def _coarse_start_time_monitor(self):

        self.time_until_ignition = self.calculate_time_to_ignition()

        # at TIG - 105 seconds:
        # ensure we only blank display first time through the loop
        if int(self.time_until_ignition) == 105 and not self.is_display_blanked:
            gc.dsky.current_verb.terminate()
            for register in list(gc.dsky.control_registers.values()):
                register.blank()
            for register in list(gc.dsky.registers.values()):
                register.blank()
            self.is_display_blanked = True
        # at TIG - 100 seconds, reenable display and enable directional autopilot
        if int(self.time_until_ignition) <= 100 and self.is_display_blanked:
            # restore the displayed program number
            gc.dsky.control_registers["program"].display(gc.running_program.number)
            gc.execute_verb(verb="16", noun="40")
            self.is_display_blanked = False
            self._enable_directional_autopilot()

        # at TIG - 10, execute verb 99
        if int(self.time_until_ignition) <= 10:
            gc.main_loop_table.remove(self._coarse_start_time_monitor)
            gc.execute_verb(verb="99", object_requesting_proceed=self._accept_enable_engine)

    def _accept_enable_engine(self, data):
        if data == "proceed":
            utils.log("Go for burn!", log_level="INFO")
        else:
            return
        gc.main_loop_table.append(self._fine_start_time_monitor)
        gc.execute_verb(verb="16", noun="40")

    def _fine_start_time_monitor(self):

        self.time_until_ignition = self.calculate_time_to_ignition()
        if float(self.time_until_ignition) < 0.1:
            utils.log("Engine Ignition", log_level="INFO")
            self._begin_burn()
            gc.main_loop_table.remove(self._fine_start_time_monitor)

    def _begin_burn(self):

        self.initial_speed = get_telemetry("orbitalVelocity")

        # start thrusting
        telemachus.set_throttle(100)
        gc.main_loop_table.append(self._thrust_monitor)

    def _thrust_monitor(self):

        # recalculate accumulated delta-v so far
        self.accumulated_delta_v = self._calculate_accumulated_delta_v()

        if self.accumulated_delta_v > (self.delta_v_required - 10) and not self._is_thrust_reduced:
            utils.log("Throttling back to 10%", log_level="DEBUG")
            telemachus.set_throttle(10)
            self._is_thrust_reduced = True

        if self.accumulated_delta_v > (self.delta_v_required - 0.5):
            telemachus.cut_throttle()
            utils.log("Closing throttle, burn complete!", log_level="DEBUG")
            gc.dsky.current_verb.terminate()
            gc.execute_verb(verb="06", noun="14")
            gc.main_loop_table.remove(self._thrust_monitor)
            gc.burn_complete()
            self.terminate()
            gc.go_to_poo()

        # utils.log("Accumulated Δv: {}, Δv to go: {}".format(accumulated_speed[0], delta_v_required -
        #                                                     accumulated_speed[0]))

    def _calculate_velocity_at_cutoff(self):
        return get_telemetry("orbitalVelocity") + self.delta_v_required

    def calculate_time_to_ignition(self):

        """ Calculates the time to ignition in seconds
        :return: time to ignition in seconds
        :rtype : float
        """

        current_time = get_telemetry("missionTime")
        return self.time_of_ignition - current_time

    def _calculate_accumulated_delta_v(self):
        current_speed = get_telemetry("orbitalVelocity")
        return current_speed - self.initial_speed

    def _disable_directional_autopilot(self):

        try:
            telemachus.disable_smartass()
        except:
            return False
        else:
            utils.log("Directional autopilot disabled", log_level="INFO")
            return True

    def _enable_directional_autopilot(self):
        try:
            telemachus.set_mechjeb_smartass(self.direction)
        except:
            return False
        else:
            utils.log("Directional autopilot enabled", log_level="INFO")
            return True


# def average_g():
#     """The purpose of the Powered Flight Navigation Sub-
#     routine is to compute the vehicle state vector during periods
#     of powered flight steering. During such periods the effects of
#     gravity and thrusting are taken into account. In order to achieve
#     a short computation time the integration of the effects of gravity
#     is achieved by simple averaging of the gravity acceleration vec-
#     tor. The effect of thrust acceleration is measured by the IMU
#     Pulsed Integrating Pendulous Accelerometers (PIPA) in the form
#     of velocity increments (Av) over the computation time interval
#     (At). The computations are, therefore, in terms of discrete in-
#     crements of velocity rather than instantaneous accelerations.
#     The repetitive computation cycle time At is set at 2 seconds to
#     maintain accuracy and to be compatible with the basic powered
#     flight cycle.
#     """
#     Note that in KSP, position vectors are relative to your current craft (I
#     think), so we are going to simulate a position vector using lat, long and
#     altitude above sea level
#     latitude = computer.memory.get_memory("latitude")
#     longitude = computer.memory.get_memory("longitude")
#     altitude = computer.memory.get_memory("asl")
#
#     velocity_x = computer.memory.get_memory("surface_velocity_x")
#     velocity_y = computer.memory.get_memory("surface_velocity_y")
#     velocity_z = computer.memory.get_memory("surface_velocity_z")
#
#     time_ = computer.memory.get_memory("ut")
#
#     computer.state_vector.position_vector["lat"] = latitude
#     computer.state_vector.position_vector["long"] = longitude
#     computer.state_vector.position_vector["alt"] = altitude
#
#     computer.state_vector.velocity_vector.x = velocity_x
#     computer.state_vector.velocity_vector.y = velocity_y
#     computer.state_vector.velocity_vector.z = velocity_z
#
#     computer.state_vector.time = time_

# def routine_30():
#
#     def receive_data(data):
#
#         """ control will pass to here upon data being loaded by user """
#
#         if data not in ("00001", "00002", "proceed"):
#             computer.dsky.operator_error("Invalid data entered, expecting either '00001' or '00002', got {}".format(
#                                          data))
#         if data != "proceed":
#             computer.option_codes["00002"] = data
#             routine_30()
#
#     # --> is another extended verb active?
#     if computer.dsky.state["current_verb"] >= 40:
#         computer.dsky.operator_error("Cannot run two extended verbs at the same time")
#         return
#
#     # --> is average g routine on?
#     if computer.state["run_average_g_routine"]:
#
#         # --> compute apoapsis, periapsis and TFF
#         # I think TFF (Time to FreeFall) means orbital period?
#
#         # --> is TFF computable (i.e is periapsis < 300,000ft in Earth orbit or
#         # --> 35,000ft in Lunar orbit?
#
#         # --> yes:
#         # --> set TF periapsis = 0 and compute TFF
#
#         # --> no:
#         # --> set TFF = -59859 and compute TF periapsis
#
#         # we ignore this test and "compute" the required data anyways
#         pass
#     else:
#         # --> set CMC assumed (vehicle) option to 00001
#         if computer.option_codes["00002"] == "":
#             computer.option_codes["00002"] = "00001"
#         # set V04N12 and request data entry
#         computer.dsky.set_noun(12)
#         computer.dsky.control_registers["verb"].display("04")
#         computer.dsky.registers[1].display(value="00002")
#         computer.dsky.registers[2].display(value=computer.option_codes["00002"])
#         computer.dsky.request_data(receive_data, computer.dsky.registers[3])


def delta_v(departure_altitude, destination_altitude, departure_body="Kerbin"):
    """
    Given a circular orbit at altitude departure_altitude and a target orbit at altitude
    destination_altitude, return the delta-V budget of the two burns required for a Hohmann
    transfer.

    departure_altitude and destination_altitude are in meters above the surface.
    returns a float of the burn delta-v required, positive means prograde, negative means retrograde

    :param departure_body:
    :param departure_altitude: departure orbit altitude
    :param destination_altitude: destination orbit altitude
    """

    departure_planet_radius = get_telemetry("body_radius", body_number=TELEMACHUS_BODY_IDS[departure_body])
    r1 = departure_altitude + departure_planet_radius
    r2 = destination_altitude + departure_planet_radius
    mu = float(get_telemetry("body_gravParameter", body_number=TELEMACHUS_BODY_IDS[departure_body]))
    sqrt_r1 = math.sqrt(r1)
    sqrt_r2 = math.sqrt(r2)
    sqrt_2_sum = math.sqrt(2 / (r1 + r2))
    sqrt_mu = math.sqrt(mu)
    delta_v_1 = sqrt_mu / sqrt_r1 * (sqrt_r2 * sqrt_2_sum - 1)
    delta_v_2 = sqrt_mu / sqrt_r2 * (1 - sqrt_r1 * sqrt_2_sum)
    return delta_v_1, delta_v_2


def time_to_transfer(departure_orbit, destination_orbit, grav_param):
    """
    Calculates the time to transfer from one orbit to another,
    :param departure_orbit: departure orbit altitude
    :param destination_orbit: destination orbit altitude
    :param grav_param: orbiting body gravitational parameter
    :return: a float in seconds of the time to transfer
    """
    tH = math.pi * math.sqrt(math.pow(departure_orbit + destination_orbit, 3) / (8 * grav_param))
    return tH


def phase_angle(departure_orbit, destination_orbit, grav_param):
    """ Calculates the required phase angle for transfer.
    :param departure_orbit: departure orbit altitude
    :param destination_orbit: destination orbit altitude
    :param grav_param: orbiting body gravitational parameter
    :return: the required phase angle
    """

    tH = time_to_transfer(departure_orbit, destination_orbit, grav_param)
    required_phase_angle = 180 - math.sqrt(grav_param / destination_orbit) * (tH / destination_orbit) * 180 / math.pi
    return required_phase_angle
