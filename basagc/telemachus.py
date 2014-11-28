#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""This module contains code that interacts with the Telemachus mod to access KSP telemetry"""

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
#  Includes code and images from the Virtual AGC Project (http://www.ibiblio.org/apollo/index.html)
#  by Ronald S. Burkey <info@sandroid.org>

import json
import urllib2

import utils
import config

telemetry = None
commands = None


class TelemetryNotAvailable(Exception):
    """This exception should be raised when we do not have a list of available telemetry"""
    pass


class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass


def check_connection():

    """ Checks if there is a connection available to Telemachus
    Returns True if so, False otherwise
    """

    try:
        urllib2.urlopen(config.URL + "paused=p.paused")
    except urllib2.URLError:
        return False
    else:
        return True


def get_api_listing():

    """ Gets the list of API calls provided by Telemachus
    :rtype: dict
    """

    try:
        response = urllib2.urlopen(config.URL + "api=a.api")
    except urllib2.URLError:
        raise KSPNotConnected
    data = json.load(response)
    telemetry_available = {}
    commands_available = {}
    for a in data.itervalues():
        for b in a:
            if b["apistring"].startswith("b."):
                name = "body_" + b["apistring"].rsplit(".", 1)[1]
            elif b["apistring"].startswith("tar."):
                name = "target_" + b["apistring"].rsplit(".", 1)[1]
            elif b["apistring"].startswith("f.") or b["apistring"].startswith("mj.") or \
                    b["apistring"].startswith("v.set"):
                command = b["apistring"].rsplit(".", 1)[1]
                commands_available[command] = b["apistring"]
                continue
            else:
                name = b["apistring"].rsplit(".", 1)[1]
            telemetry_available[name] = b["apistring"]
    global telemetry
    global commands
    telemetry = telemetry_available
    commands = commands_available


def get_telemetry(data, body_number=None):
    """ Contacts telemachus for the requested data.

    :param data: The API call required
    :type data: string
    :param body_number: Specify which body to obtain data for
    :type body_number: string
    :rtype: string
    """
    if telemetry is None:
        raise TelemetryNotAvailable
    try:
        query_string = data + "=" + telemetry[data]
    except KeyError as e:
        return e

    if body_number:
        query_string += "[{}]".format(body_number)

    try:
        raw_response = urllib2.urlopen(config.URL + query_string)
    except urllib2.URLError:
        utils.log("Query string: {}".format(query_string), log_level="ERROR")
        utils.log("Caught exception urllib2.URLERROR", log_level="ERROR")
        raise KSPNotConnected
    json_response = json.load(raw_response)
    return json_response[data]

# def enable_smartass():
#     query_string = "command="

def set_mechjeb_smartass(direction):

    command_string = "command=" + commands[direction]
    send_command_to_ksp(command_string)

def disable_smartass():
    command_string = "command=" + commands["smartassoff"]
    send_command_to_ksp(command_string)

def set_throttle(throttle_percent):
    if throttle_percent == 0:
        throttle_magnitude = 0
    else:
        throttle_magnitude = throttle_percent / 100.0
    command_string = "command=" + commands["setThrottle"] + "[" + str(throttle_magnitude) + "]"
    send_command_to_ksp(command_string)

def cut_throttle():
    command_string = "command=" + commands["throttleZero"]
    send_command_to_ksp(command_string)

def send_command_to_ksp(command_string):
    try:
        urllib2.urlopen(config.URL + command_string)
    except urllib2.URLError:
        utils.log("Query string: {}".format(command_string), log_level="ERROR")
        utils.log("Caught exception urllib2.URLERROR", log_level="ERROR")
        raise KSPNotConnected
