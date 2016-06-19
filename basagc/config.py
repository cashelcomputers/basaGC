#!/usr/bin/env python3

""" This file contains config information common to the whole package."""

import os
from collections import OrderedDict

###############################################################################
# PROGRAM CONFIGURATION - DO NOT EDIT
###############################################################################

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROGRAM_NAME = "basaGC"
VERSION = "pre-3.0.0"
LICENCE_FILE = os.path.join(BASE_DIR, "licence")
IMAGES_DIR = os.path.join(BASE_DIR, "assets/")
ICON = os.path.join(IMAGES_DIR, "icon.png")
IP = "127.0.0.1"
KRPC_PORT = 50000
COMP_ACTY_FLASH_DURATION = 100  # in milliseconds
LOOP_TIMER_INTERVAL = 100  # in milliseconds
SLOW_LOOP_TIMER_INTERVAL = 2000  # in milliseconds

###############################################################################
# PROGRAM OPTIONS - OK TO EDIT
###############################################################################

ENABLE_COMP_ACTY_FLASH = True
LAUNCH_LEAD_TIME = 20  # countdown starts at T-20s
DISPLAY_UPDATE_INTERVAL = 500  # in milliseconds

###############################################################################
# PROGRAM CONSTANTS - DO NOT EDIT
###############################################################################

LOG_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]



CURRENT_LOG_LEVEL = "INFO"

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

###############################################################################
# PROGRAM META - DO NOT EDIT
###############################################################################

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





