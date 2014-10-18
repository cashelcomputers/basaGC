"""This file contains the guts of the guidance computer,
"""

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
#  Includes code and images from the Virtual AGC Project
#  (http://www.ibiblio.org/apollo/index.html) by Ronald S. Burkey
#  <info@sandroid.org>

import multiprocessing as mp
import logging

import wx

from basagc import telemachus
from basagc import dsky
from basagc import config
from basagc import timer
from basagc import display
from basagc import verbs
from basagc import nouns
from basagc import programs
from basagc import utils
from basagc import routines

# import config
# import timer
# import display
# import dsky
# import verbs
# import nouns
# import programs
# import lib
# import routines


memory_log = logging.getLogger("MEMORY")


class Computer(object):
    def __init__(self, gui):
        self.gui = gui
        self.dsky = dsky.DSKY(self.gui, self)
        self.loop_timer = timer.Timer(interval=0.5, function=self.main_loop)
        self.out_queue = mp.Queue()
        self.in_queue = mp.Queue()
        self.is_powered_on = False
        self.state_vector = utils.StateVector()
        self.loop_items = []
        self.gui.Bind(wx.EVT_CLOSE, self.quit)
        self.alarm_codes = [0, 0, 0]
        self.running_programs = []
        self.run_average_g_routine = False
        self.target = ""
        self.loaded_data = {
            "verb": 0,
            "noun": 0,
            1: "",
            2: "",
            3: "",
        }
        self.target = ""

        telemachus.gc = self
        verbs.telemetry = telemachus.telemetry
        verbs.computer = self
        verbs.dsky = self.dsky
        verbs.frame = self.gui
        nouns.telemetry = telemachus.telemetry
        nouns.computer = self
        nouns.dsky = self.dsky
        nouns.frame = self.gui
        programs.gc = self
        programs.dsky = self.dsky
        routines.computer = self

        self.nouns = {
            "09": nouns.noun09,
            "17": nouns.noun17,
            "36": nouns.noun36,
            "43": nouns.noun43,
            "44": nouns.noun44,
            "50": nouns.noun50,
            "62": nouns.noun62,
        }
        self.verbs = {
            "01": verbs.Verb1(),
            "02": verbs.Verb2(),
            "03": verbs.Verb3(),
            "04": verbs.Verb4(),
            "05": verbs.Verb5(),
            "06": verbs.Verb6(),
            "07": verbs.Verb7(),
            "11": verbs.Verb11(),
            "12": verbs.Verb12(),
            "13": verbs.Verb13(),
            "14": verbs.Verb14(),
            "15": verbs.Verb15(),
            "16": verbs.Verb16(),
            "17": verbs.Verb17(),
            "21": verbs.Verb21(),
            "22": verbs.Verb22(),
            "23": verbs.Verb23(),
            "24": verbs.Verb24(),
            "25": verbs.Verb25(),
            "32": verbs.Verb32(),
            "33": verbs.Verb33(),
            "34": verbs.Verb34(),
            "35": verbs.Verb35(),
            "36": verbs.Verb36(),
            "37": verbs.Verb37(),
            "75": verbs.Verb75(),
            "82": verbs.Verb82(),
            "99": verbs.Verb99(),
        }

        self.programs = {
            "01": programs.Program01(name="Prelaunch or Service -"
                                          "Initialization Program", number=01),
            "11": programs.Program11(name="Change Program (Major Mode)",
                                     number=11),
            "15": programs.Program15(name="TMI initiate/cutoff", number=15),
        }

        self.routines = {
            "average_g": routines.average_g,
            30: routines.routine_30,
        }

        self.option_codes = {
            "00001": "",
            "00002": "",
            "00003": "",
            "00004": "",
            "00007": "",
            "00024": "",
        }
        self.on()

    def quit(self, event):
        if self.loop_timer.is_running:
            self.loop_timer.stop()
        self.gui.Destroy()


    def on(self):
        self.loop_timer.start()
        self.is_powered_on = True
        for display_item in self.dsky.static_display:
            display_item.on()

    def main_loop(self):
        # try:
        #     if self.telemetry.get_memory("is_paused") in [1, 2, 3, 4]:
        #         self.dsky.annunciators["no_att"].on()
        # except KSPNotConnected:
        #     self.dsky.annunciators["no_att"].on()
        if self.run_average_g_routine:
            routines.average_g()
        for item in self.loop_items:
            item()

    def execute_verb(self, verb, noun=None):
        if noun is not None:
            self.dsky.set_noun(noun)
        self.dsky.control_registers["verb"].display(str(verb))
        self.verbs[verb].execute()

    def reset_alarm_codes(self):
        self.alarm_codes[2] = self.alarm_codes[0]
        self.alarm_codes[0] = 0
        self.alarm_codes[1] = 0

    def program_alarm(self, alarm_code):

        """ sets the program alarm codes in memory and turns the PROG
            annunciator on
            alarm_code should be a 3 or 4 digit octal int
        """
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = 1000 + alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()

    def poodoo_abort(self, alarm_code):

        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = 2000 + alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()
        for program in self.running_programs:
            program.terminate()
        self.programs["00"].execute()

    def program_restart(self, alarm_code):
        # insert terminate and restart program
        print("Program fresh start not implemented yet... watch this"
              "space...")

    def computer_restart(self, alarm_code):
        # insert computer reboot
        # self.fresh_start()
        pass
