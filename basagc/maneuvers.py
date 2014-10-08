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


import math

from telemachus import get_telemetry
from config import BODIES

# class ChangeOrbitAltitude(object):
#
#     def __init__(self, computer):
#         self.memory = computer.memory
#
#     def exit_altitude(self):
#         exit_altitude = (self.memory.get_memory("asl") / 1000) + (self.memory.get_memory("body_radius", body_number=BODIES["Kerbin"]) / 1000)
#         #print("Exit altitude: {}".format(exit_altitude))
#         return exit_altitude
#
#     def gravitational_parameter(self):
#         return self.memory.get_memory("body_gravitational_parameter", body_number=BODIES["Kerbin"]) / 100000.0
#     def departure_delta_v(self):
#
#         grav_param = self.gravitational_parameter()
#         departure_altitude = 700000
#         arrival_altitude = self.memory.get_memory("body_semi_major_axis", body_number=BODIES["Mun"]) + 100000
#         v1 = math.sqrt(grav_param / departure_altitude) * math.sqrt((2 * arrival_altitude) / (departure_altitude + arrival_altitude)) - 1
#         # kerbin_radius = self.telemetry.get_memory("body_radius", body_number=BODIES["Kerbin"])
#         # v1 = math.sqrt(grav_param / (departure_altitude + kerbin_radius))
#         # v2 = math.sqrt((2 * arrival_altitude + kerbin_radius) / (departure_altitude + arrival_altitude + (2 * kerbin_radius))) - 1
#         return v1
#     def arrival_delta_v(self):
#         grav_param = self.gravitational_parameter()
#         departure_altitude = self.memory.get_memory("asl")
#         arrival_altitude = self.memory.get_memory("body_semi_major_axis", body_number=BODIES["Mun"])
#         kerbin_radius = self.memory.get_memory("body_radius", body_number=BODIES["Kerbin"])
#         # v1 = math.sqrt(grav_param / (arrival_altitude
#         self.v2 = math.sqrt(grav_param / arrival_altitude) * (
#             math.sqrt((2 * self.destination_orbit_radius) / (self.exit_altitude + self.destination_orbit_radius)) - 1)
#     def delta_v(self):
#         current_altitude = self.computer.memory.get_memory("asl") / 1000
#         departure_orbit_radius = self.orbiting_body_radius + current_altitude
#         delta_v_departure_burn = math.sqrt(self.orbiting_body_gravitational_parameter / departure_orbit_radius)
#         return round((self.ejection_velocity() - delta_v_departure_burn) * 1000, 2)
#         # return self.ejection_velocity() - delta_v_departure_burn
#
#     # def ejection_velocity(self):
#     #
#     #     grav_param = self.gravitational_parameter()
#     #     orbiting_body_soi = self.computer.telemetry.get_memory("body_soi", body_number=BODIES["Kerbin"])
#     #     current_altitude = self.computer.telemetry.get_memory("asl") / 1000
#     #     departure_orbit_radius = self.orbiting_body_radius + current_altitude
#     #     ejection_velocity = math.sqrt((departure_orbit_radius * (orbiting_body_soi * math.pow(v2, 2) - 2 * grav_param) + 2 * self.orbiting_body_soi * self.gravitational_parameter) / (r * self.orbiting_body_soi))
#     #     return ejection_velocity
# class HohmannTransfer(object):
#
#     def __init__(self, computer):
#
#         self.computer = computer
#         self.orbiting_body_name = self.computer.memory.get_memory("orbiting_body_name")
#         self.arriving_body_name = self.computer.memory.get_memory("target_name")
#         self.departure_body_radius = self.computer.memory.get_memory("body_radius", body_number="1") / 1000
#         self.arriving_body_orbit_radius = self.computer.memory.get_memory("body_radius", body_number="2") / 1000
#         self.departure_orbit_radius = self.computer.memory.get_memory("body_semi_major_axis", body_number="1")
#         self.destination_orbit_radius = self.computer.memory.get_memory("target_semi_major_axis")
#         self.orbiting_body_gravitational_parameter = self.computer.memory.get_memory("body_gravitational_parameter", body_number="1") / 1000000000
#         self.orbiting_body_soi = self.computer.memory.get_memory("body_soi", body_number="1")
#         # self.v2 = math.sqrt(self.orbiting_body_gravitational_parameter / self.destination_orbit_radius) * (math.sqrt((2 * self.destination_orbit_radius) / (self.exit_altitude + self.destination_orbit_radius)) - 1)
#         self.orbiting_body_radius = self.computer.memory.get_memory("body_radius", body_number="1")
#
#         self.data = {
#             "is_calculated": False,
#             "time_to_transfer": 0,
#             "phase_angle": 0,
#             "ejection_velocity": 0,
#             "ejection_angle": 0,
#             "delta_v": 0,
#             "phase_angle_difference": 0,
#             "ejection_angle_difference": 0,
#         }
#
#     def departure_delta_v(self):
#
#
#         current_altitude = self.computer.memory.get_memory("asl") / 1000
#         departure_altitude = current_altitude + self.departure_body_radius
#         arrival_altitude = 13500000
#         dV1 = math.sqrt(self.orbiting_body_gravitational_parameter / (current_altitude + self.departure_body_radius))
#         dV2 = math.sqrt(2 * (arrival_altitude + self.departure_body_radius) / (self.departure_body_radius + arrival_altitude + (2 * self.departure_body_radius))) - 1 # FIXME
#         dv = dV1 * dV2
#         return dv
#
#     # def time_to_transfer(self):
#     #
#     #     tH = math.pi * math.sqrt(math.pow(self.departure_orbit_radius + self.destination_orbit_radius, 3) / (8 * self.orbiting_body_gravitational_parameter))
#     #     return round(tH, 2)
#     #
#     # def phase_angle(self):
#     #
#     #     tH = self.time_to_transfer()
#     #     phase_angle = 180 - math.sqrt(self.orbiting_body_gravitational_parameter / self.destination_orbit_radius) * (tH / self.destination_orbit_radius) * (180 / math.pi)
#     #     return phase_angle
#     #
#     # def ejection_velocity(self):
#     #
#     #     #current_altitude = float(json.load(urllib2.urlopen(URL + 'alt=v.altitude'))["alt"]) / 1000
#     #     current_altitude = self.computer.telemetry.get_memory("asl") / 1000
#     #     r = self.orbiting_body_radius + current_altitude
#     #     ejection_velocity = math.sqrt((r * (self.orbiting_body_soi * math.pow(self.v2, 2) - 2 * self.gravitational_parameter) + 2 * self.orbiting_body_soi * self.gravitational_parameter) / (r * self.orbiting_body_soi))
#     #     return ejection_velocity
#     #
#     # def ejection_angle(self):
#     #
#     #     current_altitude = self.computer.telemetry.get_memory("asl") / 1000
#     #     r = self.orbiting_body_radius + current_altitude
#     #     v = self.ejection_velocity()
#     #     eta = (math.pow(v, 2) / 2) - (self.gravitational_parameter  / r)
#     #     h = r * v
#     #     e = math.sqrt(1 + ((2 * eta * math.pow(h, 2)) / math.pow(self.gravitational_parameter, 2)))
#     #     print(e)
#     #     # if e < 1:
#     #     #
#     #     # # eject = (180 - (math.acos(1 / e) * (180 / math.pi))) % 360
#     #     eject = 90
#     #     return eject
#     #
#     # def delta_v(self):
#     #     current_altitude = self.computer.telemetry.get_memory("asl") / 1000
#     #     departure_orbit_radius = self.orbiting_body_radius + current_altitude
#     #     delta_v_departure_burn = math.sqrt(self.orbiting_body_gravitational_parameter / departure_orbit_radius)
#     #     #return round((self.ejection_velocity() - delta_v_departure_burn) * 1000, 2)
#     #     return self.ejection_velocity() - delta_v_departure_burn
#     #
#     # def phase_angle_difference(self):
#     #     current_relative_phase = self.computer.telemetry.get_memory("body_phase_angle")
#     #     desired_phase = self.phase_angle()
#     #     return (current_relative_phase - desired_phase + 360) % 360
#     #
#     # def ejection_angle_difference(self):
#     #     current_angle_to_prograde = self.computer.telemetry.get_memory("angle_to_prograde")
#     #     ejection_angle = self.ejection_angle()
#     #
#     #     # handle cases where data is NaN
#     #     if current_angle_to_prograde == "NaN" or ejection_angle == "nan":
#     #         return 0
#     #
#     #     if self.departure_orbit_radius > self.destination_orbit_radius:
#     #         return 180 - ((ejection_angle - current_angle_to_prograde + 360) % 360)
#     #     else:
#     #         return 360 - ((ejection_angle - current_angle_to_prograde + 360) % 360)
#     #
#     # #def adjust_ejection_angle(self):
#     #     #ejection_angle = self.ejection_angle()
#     #     #time = (0.2 / 0.3) * self.burn_length()
#     #     #print self.burn_length()
#     #     #adjustment = ejection_angle - (360 * (time / self.computer.get_telemetry("orbital_period")))
#     #     #if adjustment < 0:
#     #         #adjustment += 360
#     #     #print "Adjustment:", adjustment, adjustment / 9.81
#     #     #return (adjustment - self.ejection_angle_difference() + 360) % 360
#     #
#     # #def burn_length(self):
#     #     #return self.ejection_velocity() / float(self.computer.telemetry.get_memory(["orbiting_body_name"]))
#     #
#     # def execute(self):
#     #
#     #     self.data["is_calculated"] = True
#     #     self.data["time_to_transfer"] = self.time_to_transfer()
#     #     self.data["phase_angle"] = self.phase_angle()
#     #     self.data["ejection_velocity"] = self.ejection_velocity()
#     #     self.data["ejection_angle"] = self.ejection_angle()
#     #     self.data["delta_v"] = self.delta_v() * 1000
#     #     self.data["phase_angle_difference"] = self.phase_angle_difference()
#     #     self.data["ejection_angle_difference"] = self.ejection_angle_difference()
#     #     print(self.data)
# def time_to_transfer(departure_orbit_radius, destination_orbit_radius, grav_param=None):
#
#     """ Calculates how much time it will take to transfer from one planet’s orbit around the parent body to the other
#         planet’s orbit.
#     :departure_orbit_radius: float
#     :param destination_orbit_radius: float
#     :param grav_param: float
#     :return:
#     """
#     if grav_param is None:
#         grav_param = 3531600000000.0
#     tH = math.pi * math.sqrt(math.pow((departure_orbit_radius / 1000) + (destination_orbit_radius / 1000), 3) / (8 * (grav_param / 1000000000)))
#     print(seconds_to_time(tH))
#     return tH
#
# def phase_angle(departure_orbit_radius, destination_orbit_radius, grav_param=None):
#
#     tH = time_to_transfer(departure_orbit_radius, destination_orbit_radius, grav_param)
#     phase_angle = 180 - math.sqrt((grav_param / 1000000000) / (destination_orbit_radius / 1000)) * (tH / (destination_orbit_radius / 1000)) * 180 / math.pi
#     return phase_angle
#
# def seconds_to_time(seconds):
#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     days, hours = divmod(hours, 24)
#     print("{} days, {} hours, {} minutes, {} seconds".format(days, hours, minutes, round(seconds, 2)))
#     return (days, hours, minutes, seconds)


def hohmann(departure_altitude, destination_altitude):
    """
    Given a circular orbit at altitude departure_altitude and a target orbit at altitude
    destination_altitude, return the delta-V budget of the two burns required for a Hohmann
    transfer.

    departure_altitude and destination_altitude are in meters above the surface.
    returns a pair (dV1, dV2) corresponding to the two burns required,
        positive means prograde, negative means retrograde
    """
    departure_planet_radius = get_telemetry("body_radius", body_number=BODIES["Kerbin"])
    r1 = departure_altitude + departure_planet_radius
    r2 = destination_altitude + departure_planet_radius
    mu = get_telemetry("body_gravitational_parameter", body_number=BODIES["Kerbin"])

    sqrt_r1 = math.sqrt(r1)
    sqrt_r2 = math.sqrt(r2)
    sqrt_2_sum = math.sqrt(2 / (r1 + r2))
    sqrt_mu = math.sqrt(mu)
    dV1 = sqrt_mu / sqrt_r1 * (sqrt_r2 * sqrt_2_sum - 1)
    return dV1

def time_to_transfer(departure_orbit, destination_orbit, grav_param):

    tH = math.pi * math.sqrt(math.pow(departure_orbit + destination_orbit, 3) / (8 * grav_param))
    return tH

def phase_angle(departure_orbit, destination_orbit, grav_param):

    tH = time_to_transfer(departure_orbit, destination_orbit, grav_param)
    phase_angle = 180 - math.sqrt(grav_param / (destination_orbit) * (tH / destination_orbit ) * 180 / math.pi)
    return phase_angle
