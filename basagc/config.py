#!/usr/bin/env python3

""" This file contains config information common to the whole package."""

import os

from collections import OrderedDict

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
LOOP_TIMER_INTERVAL = 50
SLOW_LOOP_TIMER_INTERVAL = 2000
ENABLE_COMP_ACTY_FLASH = True

LOG_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]

current_log_level = "DEBUG"

DIRECTIONS = [
    "prograde",
    "retrograde",
    "normalplus",
    "normalminus",
    "radialplus",
    "radialminus",
]

TELEMACHUS_BODY_IDS = {
    "Kerbol": "0",
    "Kerbin": "1",
    "Mun": "2",
    "Minmus": "3",
    "Moho": "4",
    "Eve": "5",
    "Duna": "6",
    "Ike": "7",
    "Jool": "8",
    "Laythe": "9",
    "Vall": "10",
    "Bop": "11",
    "Tylo": "12",
    "Gilly": "13",
    "Pol": "14",
    "Dres": "15",
    "Eeloo": "16",
}

_UNSORTED_ALARM_CODES = {
    110: "Error contacting KSP",
    111: "Telemetry not available",
    115: "No burn data loaded",
    120: "No phase angle data available",
    223: "Invalid target selected",
    224: "Orbit not circular",
    225: "Vessel and target orbits inclination too far apart",
    226: "Time of ignition less than 2 minutes in the future",
    310: "Program hasn't been finished yet, watch this space :)",
    410: "Autopilot error",
}

ALARM_CODES = OrderedDict(sorted(_UNSORTED_ALARM_CODES.items()))
OCTAL_BODY_IDS = {}

for key, value in TELEMACHUS_BODY_IDS.items():
    value = oct(int(value))
    value = value[2:]
    OCTAL_BODY_IDS[value] = key


# OCTAL_BODY_IDS = {key: str(int(oct(int(value)))) for key, value in TELEMACHUS_BODY_IDS.items()}  # FIXME: abomination
OCTAL_BODY_NAMES = {value: key for key, value in OCTAL_BODY_IDS.items()}

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




