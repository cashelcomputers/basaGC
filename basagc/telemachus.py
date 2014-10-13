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

import json
import urllib2

import config

telemetry = {
    'is_paused': ("Paused", False, "p.paused"),
    'is_rcs': ("RCS", False, "v.rcsValue"),
    'is_sas': ("SAS", False, "v.sasValue"),
    'is_lights': ("Lights", False, "v.lightValue"),
    'ut': ("Universal Time", 0, "t.universalTime"),
    'relative_velocity': (
    'Relative Velocity', 0.0, "o.relativeVelocity"),
    'periapsis': ("Periapsis", 0.0, "o.PeA"),
    'apoapsis': ("Apoapsis", 0.0, "o.ApA"),
    'time_to_periapsis': (
    'Time To Periapsis', 0.0, "o.timeToPe"),
    'time_to_apoapsis': ("Time To Apoapsis", 0.0, "o.timeToAp"),
    'inclination': ("Orbital Inclination", 0.0, "o.inclination"),
    'eccentricity': ("Orbital Eccentricity", 0.0, "o.eccentricity"),
    'orbital_period': ("Orbital Period", 0.0, "o.period"),
    'argument_of_periapsis': ("Argument of Periapsis", 0.0, "o.argumentOfPeriapsis"),
    'time_to_transition_1': ("Time To Transition One", 0.0, "o.timeToTransition1"),
    'time_to_transition_2': ("Time To Transition Two", 0.0, "o.timeToTransition2"),
    'semi_major_axis': ("Semi-Major Axis", 0.0, "o.sma"),
    'longitude_of_ascending_node': ("Longitude Of Ascending Node", 0.0, "o.lan"),
    'mean_anomaly_at_epoch': ("Mean Anomaly At Epoch", 0.0, "o.maae"),
    'time_of_periapsis_passage': ("Time Of Periapsis Passage", 0.0, "o.timeOfPeriapsisPassage"),
    'true_anomaly': ("True Anomaly", 0.0, "o.trueAnomaly"),
    'temperature': ("Temperature Sensor", 0, "s.sensor.temp"),
    'gravity': ("Gravity Sensor", 0, "s.sensor.grav"),
    'pressure': ("Pressure Sensor", 0, "s.sensor.pres"),
    'acceleration': ("Acceleration Sensor", 0, "s.sensor.acc"),
    'asl': ("Altitude Above Sea Level", 0.0, "v.altitude"),
    'agl': ("Altitude Above Ground Level", 0.0, "v.heightFromTerrain"),
    'terrain_height': ("Terrain Height", 0.0, "v.terrainHeight"),
    'met': ("Mission Elapsed Time", 0.0, "v.missionTime"),
    'surface_velocity': ("Surface Velocity", 0.0, "v.surfaceVelocity"),
    'surface_velocity_x': ("Surface Velocity X", 0.0, "v.surfaceVelocityx"),
    'surface_velocity_y': ("Surface Velocity Y", 0.0, "v.surfaceVelocityy"),
    'surface_velocity_z': ("Surface Velocity Z", 0.0, "v.surfaceVelocityz"),
    'angular_velocity': ("Angular Velocity", 0.0, "v.angularVelocity"),
    'orbital_velocity': ("Orbital Velocity", 0.0, "v.orbitalVelocity"),
    'surface_speed': ("Surface Speed", 0.0, "v.surfaceSpeed"),
    'vertical_speed': ("Vertical Speed", 0.0, "v.verticalSpeed"),
    'atmo_density': ("Atmospheric Density", 0.0, "v.atmosphericDensity"),
    'longitude': ("Longitude", 0.0, "v.long"),
    'latitude': ("Latitude", 0.0, "v.lat"),
    'dynamic_pressure': ("Dynamic Pressure", 0.0, "v.dynamicPressure"),
    'name': ("Vessel Name", "", "v.name"),
    'orbiting_body_name': ("Orbiting Body Name", "", "v.body"),
    'angle_to_prograde': ("Angle To Prograde", 0.0, "v.angleToPrograde"),
    'pitch': ("Pitch", 0.0, "n.pitch"),
    'roll': ("Roll", 0.0, "n.roll"),
    'yaw': ("Yaw", 0.0, "n.heading"),
    'raw_pitch': ("Raw Pitch", 0.0, "n.rawpitch"),
    'raw_roll': ("Raw Roll", 0.0, "n.rawroll"),
    'raw_yaw': ("Raw Yaw", 0.0, "n.rawheading"),
    'target_name': ("Target Name", "", "tar.name"),
    'target_semi_major_axis': ("Target Semi-major axis", 0.0, "tar.o.sma"),
    'target_eccentricity': ("Target Eccentricity", 0.0, "tar.o.eccentricity"),
    'target_inclination': ("Target Inclination", 0.0, "tar.o.inclination"),
    'body_semi_major_axis': ("Body semi-major axis", 0.0, "b.o.sma"),
    'body_gravitational_parameter': ("Body gravitational parameter", 0.0, 'b.o.gravParameter'),
    'body_radius': ("Body radius", 0, "b.radius"),
    'body_phase_angle': ("Body Phase Angle", 0.0, "b.o.phaseAngle"),
    'body_soi': ("Body Sphere of Influence", 0.0, "b.soi"),
    'body_apoapsis': ("Body Apoapsis", 0.0, "b.o.ApA"),
    'body_orbital_period': ("Body Orbital Period", 0.0, "b.o.period")
}

def get_telemetry(data, body_number=None):
    """ Contacts telemachus for the requested data.

    """
    try:
        query_string = data + "=" + telemetry[data][2]
    except KeyError as e:
        return e

    if body_number:
        query_string += "[{}]".format(body_number)

    try:
        raw_response = urllib2.urlopen(config.URL + query_string)
    except urllib2.URLError as e:
        print(query_string)
        print(e)
        raise KSPNotConnected
    json_response = json.load(raw_response)
    return json_response[data]


class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass

