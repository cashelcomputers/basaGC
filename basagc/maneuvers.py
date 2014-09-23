#!/usr/bin/env python
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


import math
#from celestial_body import CELESTIAL_BODIES
import config

class HohmannTransfer(object):

    def __init__(self, computer):

        self.computer = computer
        self.origin = self.computer.memory.get_memory("orbiting_body_name")
        self.target = self.computer.memory.get_memory("target_name")
        # self.r1 = self.computer.memory.get_memory("body_semi_major_axis")
        self.r1 = 13599840.256
        self.r2 = self.computer.memory.get_memory("target_semi_major_axis")
        # self.u = self.computer.memory.get_memory("body_gravitational_parameter")
        self.u = 3531.6
        self.soi = 84159.2865  # TODO: get SOI value from KSP
        self.exit_altitude = self.r1 + self.soi
        self.ou = self.u
        self.v2 = math.sqrt(self.u / self.exit_altitude) * (math.sqrt((2 * self.r2) / (self.exit_altitude + self.r2)) - 1)
        self.radius = self.computer.memory.get_memory("body_radius")

        self.data = {
            "is_calculated": False,
            "time_to_transfer": 0,
            "phase_angle": 0,
            "ejection_velocity": 0,
            "ejection_angle": 0,
            "delta_v": 0,
            "phase_angle_difference": 0,
            "ejection_angle_difference": 0,
        }


    def time_to_transfer(self):

        tH = math.pi * math.sqrt(math.pow(self.r1 + self.r2, 3) / (8 * self.u))
        return round(tH, 2)

    def phase_angle(self):

        tH = self.time_to_transfer()
        phase_angle = 180 - math.sqrt(self.u / self.r2) * (tH / self.r2) * (180 / math.pi)
        return phase_angle

    def ejection_velocity(self):

        #current_altitude = float(json.load(urllib2.urlopen(URL + 'alt=v.altitude'))["alt"]) / 1000
        current_altitude = self.computer.memory.get_memory("asl") / 1000
        r = self.radius + current_altitude
        ejection_velocity = math.sqrt((r * (self.soi * math.pow(self.v2, 2) - 2 * self.ou) + 2 * self.soi * self.ou) / (r * self.soi))
        return ejection_velocity

    def ejection_angle(self):

        current_altitude = self.computer.memory.get_memory("asl") / 1000
        r = self.radius + current_altitude
        v = self.ejection_velocity()
        eta = (math.pow(v, 2) / 2) - (self.ou  / r)
        h = r * v
        e = math.sqrt(1 + ((2 * eta * math.pow(h, 2)) / math.pow(self.ou, 2)))
        eject = (180 - (math.acos(1 / e) * (180 / math.pi))) % 360
        return eject

    def delta_v(self):
        current_altitude = self.computer.memory.get_memory("asl") / 1000
        r = self.radius + current_altitude
        vd = math.sqrt(self.ou / r)
        #return round((self.ejection_velocity() - vd) * 1000, 2)
        return self.ejection_velocity() - vd

    def phase_angle_difference(self):
        current_relative_phase = self.computer.memory.get_memory("body_phase_angle")
        desired_phase = self.phase_angle()
        return (current_relative_phase - desired_phase + 360) % 360

    def ejection_angle_difference(self):
        current_angle_to_prograde = self.computer.memory.get_memory("angle_to_prograde")
        ejection_angle = self.ejection_angle()

        # handle cases where data is NaN
        if current_angle_to_prograde == "NaN" or ejection_angle == "nan":
            return 0

        if self.r1 > self.r2:
            return 180 - ((ejection_angle - current_angle_to_prograde + 360) % 360)
        else:
            return 360 - ((ejection_angle - current_angle_to_prograde + 360) % 360)

    #def adjust_ejection_angle(self):
        #ejection_angle = self.ejection_angle()
        #time = (0.2 / 0.3) * self.burn_length()
        #print self.burn_length()
        #adjustment = ejection_angle - (360 * (time / self.computer.get_telemetry("orbital_period")))
        #if adjustment < 0:
            #adjustment += 360
        #print "Adjustment:", adjustment, adjustment / 9.81
        #return (adjustment - self.ejection_angle_difference() + 360) % 360

    #def burn_length(self):
        #return self.ejection_velocity() / float(self.computer.memory.get_memory(["orbiting_body_name"]))

    def calculate(self):

        self.data["is_calculated"] = True
        self.data["time_to_transfer"] = self.time_to_transfer()
        self.data["phase_angle"] = self.phase_angle()
        self.data["ejection_velocity"] = self.ejection_velocity()
        self.data["ejection_angle"] = self.ejection_angle()
        self.data["delta_v"] = self.delta_v() * 1000
        self.data["phase_angle_difference"] = self.phase_angle_difference()
        self.data["ejection_angle_difference"] = self.ejection_angle_difference()
        print(self.data)