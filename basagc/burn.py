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
from utils import log

gc = None

class Burn(object):

    def __init__(self, delta_v, direction, time_of_ignition, calling_maneuver):

        self.delta_v = delta_v
        self.direction = direction
        self.time_of_ignition = time_of_ignition
        self.calling_maneuver = calling_maneuver
        self.is_display_blanked = False
        self.is_verb_99_executed = False
        self.time_until_ignition = self.time_of_ignition - get_telemetry("missionTime")
        self.velocity_at_cutoff = get_telemetry("orbitalVelocity") + self.delta_v
        self.is_directional_autopilot_engaged = False
        if self.calling_maneuver.time_to_transfer:
            log("Got time to transfer data")
            self.time_to_transfer = self.calling_maneuver.time_to_transfer

    def execute(self):
        gc.burn_data.append(self)
        gc.loop_items.append(self.coarse_start_time_monitor)

    def terminate(self):
        if self.is_directional_autopilot_engaged:
            gc.disable_direction_autopilot()
        gc.loop_items.remove(self)

    def coarse_start_time_monitor(self):
        current_time = get_telemetry("missionTime")
        self.time_until_ignition = self.time_of_ignition - current_time

        # ensure we only blank display first time through the loop
        if int(self.time_until_ignition) == 105 and not self.is_display_blanked:
            gc.dsky.current_verb.terminate()
            for register in gc.dsky.control_registers.itervalues():
                register.blank()
            for register in gc.dsky.registers.itervalues():
                register.blank()
            self.is_display_blanked = True
        # after 5 seconds, reenable display and enable autopilot
        if int(self.time_until_ignition) <= 100 and self.is_display_blanked:
            # restore the displayed program number
            gc.dsky.control_registers["program"].display(gc.active_program.number)

            gc.execute_verb(verb="16", noun="95")
            self.is_display_blanked = False
            self.is_directional_autopilot_engaged = True
            gc.enable_direction_autopilot(self.direction)

        # at TIG - 10, execute verb 99
        if int(self.time_until_ignition) <= 10 and not self.is_verb_99_executed:
            self.is_verb_99_executed = True
            gc.loop_items.remove(self.coarse_start_time_monitor)
            gc.execute_verb(verb="99", object_requesting_proceed=self.execute_burn)

    def execute_burn(self, data):
        if data == "proceed":
            log("Go for burn!", log_level="INFO")
        else:
            return
        gc.loop_items.append(self.fine_start_time_monitor)
        gc.execute_verb(verb="16", noun="95")

    def fine_start_time_monitor(self):

        current_time = get_telemetry("missionTime")
        self.time_until_ignition = self.time_of_ignition - current_time
        if float(self.time_until_ignition) < 0.1:
            # start thrusting and stop the programs running tasks
            # if self.calling_maneuver.recalculate_maneuver in gc.loop_items:
            #     gc.loop_items.remove(self.calling_maneuver.recalculate_maneuver)
            # if self.calling_maneuver.check_time_to_burn in gc.loop_items:
            #     gc.loop_items.remove(self.calling_maneuver.check_time_to_burn)
            gc.loop_items.remove(self.fine_start_time_monitor)
            gc.enable_thrust_autopilot(delta_v_required=self.delta_v, calling_burn=self)
            log("Thrusting", log_level="DEBUG")
