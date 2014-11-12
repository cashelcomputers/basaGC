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

class TelemetryNotAvailable(Exception):
    """This exception should be raised when we do not have a list of available telemetry"""
    pass

class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass


def _get_api_listing():

    """ Gets the list of API calls provided by Telemachus
    :rtype: dict
    """

    try:
        response = urllib2.urlopen(config.URL + "api=a.api")
    except urllib2.URLError as e:
        print(e)
        raise KSPNotConnected
    data = json.load(response)
    telemetry_available = {}
    commands = {}
    for a in data.itervalues():
        for b in a:
            if b["apistring"].startswith("b."):
                name = "body_" + b["apistring"].rsplit(".", 1)[1]
            elif b["apistring"].startswith("tar."):
                name = "target_" + b["apistring"].rsplit(".", 1)[1]
            elif b["apistring"].startswith("f.") or b["apistring"].startswith("mj.") or \
                    b["apistring"].startswith("v.set"):
                command = b["apistring"].rsplit(".", 1)[1]
                commands[command] = b["apistring"]
                continue
            else:
                name = b["apistring"].rsplit(".", 1)[1]
            telemetry_available[name] = b["apistring"]
    return telemetry_available

try:
    telemetry = _get_api_listing()
except KSPNotConnected:
    telemetry = None
    print("Could not construct telemetry information - no contact with KSP")


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
    except urllib2.URLError as e:
        utils.log("Query string: {}".format(query_string))
        utils.log(e)
        raise KSPNotConnected
    json_response = json.load(raw_response)
    return json_response[data]
