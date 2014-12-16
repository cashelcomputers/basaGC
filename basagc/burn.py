#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""This file contains a class to model a GC-controlled burn"""

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

from telemachus import get_telemetry
import utils
import config
import telemachus

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
            for register in gc.dsky.control_registers.itervalues():
                register.blank()
            for register in gc.dsky.registers.itervalues():
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
