#!/usr/bin/env python3
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
#  by Ronald S. Burkey <info@sandroid.org> (thanks Ronald!)

from basagc.telemachus import get_telemetry
from basagc import utils
from basagc import config

class Orbit(object):

    """ Represents a Keplerian orbit
    """
    def __init__(self, object_name):

        self.orbiting_body_name = ""
        self.object_name = object_name
        self.type_of_object = ""
        self.body_id = None

        # the next 2 elements describe the orbit's shape
        self.eccentricity = 0.0  # shape of the orbit, describing how much it is elongated compared to a circle
        self.semi_major_axis = 0.0  # the sum of the periapsis and apoapsis distances divided by two

        # the next 2 elements define the orientation of the orbital plane in which the orbit is embedded
        self.inclination = 0.0  # vertical tilt of the ellipse with respect to the reference plane, measured at the
                                # ascending node (where the orbit passes upward through the reference plane)
        self.longitude_of_ascending_node = 0.0  # horizontally orients the ascending node of the ellipse (where the
                                                # orbit passes upward through the reference plane) with respect to the
                                                # reference frame's vernal point

        self.argument_of_periapsis = 0.0  # defines the orientation of the orbit in the orbital plane, as an angle
                                          # measured from the ascending node to the periapsis
        self.mean_anomaly_at_epoch = 0.0  # defines the position of the orbiting body along the ellipse at a specific
                                          # time (the "epoch")

        self.true_anomaly = 0.0  # an angular parameter that defines the position of a body moving along a Keplerian
                                 # orbit. It is the angle between the direction of periapsis and the current position
                                 # of the body, as seen from the main focus of the ellipse (the point around which the
                                 # object orbits)

        self.apoapsis = 0.0  # the point of greatest distance of a body in an elliptic orbit about a larger body
        self.periapsis = 0.0  # the point of least distance of a body in an elliptic orbit about a larger body
        self.time_to_apoapsis = 0.0  # in seconds
        self.time_to_apoapsis_dhms = (0, 0, 0, 0)  # same as above, except in days, hours, minutes, and seconds
        self.time_to_periapsis = 0.0  # in seconds
        self.time_to_periapsis_dhms = (0, 0, 0, 0)  # same as above, except in days, hours, minutes, and seconds
        self.orbital_period = 0.0  # the time it takes to complete one orbit
        self.orbital_period_hms = (0, 0, 0, 0)  # same as above, except in days, hours, minutes, and seconds
        self.time_of_periapsis_passage = 0.0  # in seconds
        self.time_of_periapsis_passage_hms = (0, 0, 0, 0)  # same as above, except in days, hours, minutes, and seconds

    def __str__(self):
        return "Orbit parameters:\nEccentricity: {}\nSemi-major axis: {} km\nInclination: {}°\nLongitude of ascending " \
               "node: {}°\nArgument of periapsis: {}°\nMean anomaly at epoch: {} \n" \
               "True anomaly: {}°".format(round(self.eccentricity, 5),
                                         round(self.semi_major_axis / 1000, 2),
                                         round(self.inclination, 2),
                                         round(self.longitude_of_ascending_node, 2),
                                         round(self.argument_of_periapsis, 2),
                                         round(self.mean_anomaly_at_epoch, 2),
                                         round(self.true_anomaly, 2)
                                         )

    def update_parameters(self):

        try:
            self.body_id = config.BODIES[self.object_name]
        except KeyError:
            self.body_id = None
            self.type_of_object = "Spacecraft"
        else:
            self.type_of_object = "celestial_body"
        self.orbiting_body_name = get_telemetry("body")
        self.eccentricity = get_telemetry("eccentricity")
        self.semi_major_axis = get_telemetry("sma")
        self.inclination = get_telemetry("inclination")
        self.longitude_of_ascending_node = get_telemetry("lan")
        self.argument_of_periapsis = get_telemetry("argumentOfPeriapsis")
        self.mean_anomaly_at_epoch = get_telemetry("maae")
        self.true_anomaly = get_telemetry("trueAnomaly")
        self.apoapsis = get_telemetry("ApA")
        self.periapsis = get_telemetry("PeA")
        self.time_to_apoapsis = get_telemetry("timeToAp")
        self.time_to_periapsis = get_telemetry("timeToPe")
        self.orbital_period = get_telemetry("period")
        self.time_of_periapsis_passage = get_telemetry("timeOfPeriapsisPassage")
        self.time_to_apoapsis_dhms = utils.seconds_to_time(self.time_to_apoapsis)
        self.time_to_periapsis_dhms = utils.seconds_to_time(self.time_to_periapsis)
        self.orbital_period_hms = utils.seconds_to_time(self.orbital_period)
        self.time_of_periapsis_passage_hms = utils.seconds_to_time(self.time_of_periapsis_passage)
