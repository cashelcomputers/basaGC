#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    This file contains config information common to the whole package
"""
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
#  Includes code and images from the Virtual AGC Project
# (http://www.ibiblio.org/apollo/index.html) by Ronald S. Burkey
# <info@sandroid.org>

TEST_STRING = "Foobar"
VERSION = "0.3.2a"
IMAGES_DIR = "./images/"
IP = "http://127.0.0.1:8085"
URL = IP + "/telemachus/datalink?"
PORT = 26000
DISPLAY_UPDATE_INTERVAL = 1000
HOST = "127.0.0.1"
COMP_ACTY_FLASH_DURATION = 50

ID_VERBBUTTON = 10
ID_NOUNBUTTON = 11
ID_PLUSBUTTON = 12
ID_MINUSBUTTON = 13
ID_ZEROBUTTON = 0
ID_ONEBUTTON = 1
ID_TWOBUTTON = 2
ID_THREEBUTTON = 3
ID_FOURBUTTON = 4
ID_FIVEBUTTON = 5
ID_SIXBUTTON = 6
ID_SEVENBUTTON = 7
ID_EIGHTBUTTON = 8
ID_NINEBUTTON = 9
ID_CLRBUTTON = 14
ID_PROBUTTON = 15
ID_KEYRELBUTTON = 16
ID_ENTRBUTTON = 17
ID_RSETBUTTON = 18

KEY_IDS = {
    10: "V",
    11: "N",
    12: "+",
    13: "-",
    14: "C",
    15: "P",
    16: "K",
    17: "E",
    18: "R",
}

# DSKY_KEYCODES = {
#     "0": "10000",
#     "1": "00001",
#     "2": "00010",
#     "3": "00011",
#     "4": "00100",
#     "5": "00101",
#     "6": "00110",
#     "7": "00111",
#     "8": "01000",
#     "9": "01001",
#     "verb": "10001",
#     "reset": "10010",
#     "key_release": "11001",
#     "+": "11010",
#     "-": "11011",
#     "enter": "11100",
#     "clear": "11110",
#     "noun": "11111",
#     "proceed": "10101",
# }
#
# COMPUTER_KEYCODES = {value:key for key, value in DSKY_KEYCODES.items()}
# DSKY_POLL_INTERVAL = 1000
#
# OUT_CODES = {
#     "blank": "00000",
#     "0": "10101",
#     "1": "00011",
#     "2": "11001",
#     "3": "11011",
#     "4": "01111",
#     "5": "11110",
#     "6": "11100",
#     "7": "10011",
#     "8": "11101",
#     "9": "11111",
# }
# IN_CODES = {value:key for key, value in OUT_CODES.items()}

BODIES = {
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
OCTAL_BODIES = {int(oct(int(value))): key for key, value in BODIES.iteritems()}
