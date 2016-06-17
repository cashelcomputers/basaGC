#!/usr/bin/env python3

""" This file contains config information common to the whole package."""

import os

from collections import OrderedDict

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROGRAM_NAME = "basaGC"
VERSION = "2.2.0"
LICENCE_FILE = os.path.join(BASE_DIR, "licence")
IMAGES_DIR = os.path.join(BASE_DIR, "assets/")
IP = "127.0.0.1"
PORT = "8085"
URL = "http://" + IP + ":" + PORT + "/telemachus/datalink?"
DISPLAY_UPDATE_INTERVAL = 500
COMP_ACTY_FLASH_DURATION = 100
LOOP_TIMER_INTERVAL = 100
SLOW_LOOP_TIMER_INTERVAL = 2000
ENABLE_COMP_ACTY_FLASH = True
KSP_INTERFACE = "krpc"
KRPC_PORT = 50002
KOS_PORT = 5410

LOG_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]

current_log_level = "INFO"

REFSSMAT = {
    "planet_non_rotating": "non_rotating_reference_frame",
    "planet_rotating": "reference_frame",
    "vessel": "reference_frame",
    "vessel_orbital": "orbital_reference_frame",
    "surface_velocity": "surface_velocity_reference_frame",
    "surface": "surface_reference_frame",
    }

SAS_DIRECTIONS = [
    "stability_assist",  # normal SAS ie attitude hold
    "prograde",
    "retrograde",
    "normal",
    "anti_normal",
    "radial",
    "anti_radial",
    "maneuver",  # node
    "target",
    "anti_target",
]

_UNSORTED_ALARM_CODES = {
    110: "Error contacting KSP",
    111: "Telemetry not available",
    115: "No burn data loaded",
    116: "Program doesn't exist",
    120: "No phase angle data available",
    223: "Invalid target selected",
    224: "Orbit not circular",
    225: "Vessel and target orbits inclination too far apart",
    226: "Time of ignition less than 2 minutes in the future",
    310: "Program hasn't been finished yet, watch this space :)",
    410: "Autopilot error",
    501: "Uplink file does not exist, aborting uplink",
}

ALARM_CODES = OrderedDict(sorted(_UNSORTED_ALARM_CODES.items()))

PROGRAM_DESCRIPTION = "basaGC is a implementation of the Apollo Guidance Computer (AGC) for Kerbal Space Program." + (
                      "\n\nbasaGC includes code and images from the Virtual AGC Project ") + (
                      "(http://www.ibiblio.org/apollo/index.html) by Ronald S. Burkey <info@sandroid.org>")

with open(LICENCE_FILE) as f:
    LICENCE = f.readlines()
LICENCE = "".join(LICENCE)

SHORT_LICENCE = "basaGC is free software; you can redistribute it and/or modify it under the terms of the GNU " + (
                "General Public License as published by the Free Software Foundation; either version 2 of the ") + (
                "License, or (at your option) any later version.\n\nThis program is distributed in the hope that ") + (
                "it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of ") + (
                "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for ") + (
                "more details.\n\nYou should have received a copy of the GNU General Public License along with ") + (
                "this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, ") + (
                "Fifth Floor, Boston, MA 02110-1301, USA.")

COPYRIGHT = "(C) 2014-2016 Tim Buchanan (cashelcomputers@gmail.com)"
WEBSITE = "https://github.com/cashelcomputers/basaGC/"
DEVELOPERS = "Tim Buchanan"
ICON = os.path.join(BASE_DIR, "icon.png")




