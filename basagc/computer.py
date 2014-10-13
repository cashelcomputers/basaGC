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
from basagc import lib
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
        self.state_vector = lib.StateVector()
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

        self.nouns = [
            None,
            nouns.noun01,
            nouns.noun02,
            nouns.noun03,
            None,
            nouns.noun05,
            nouns.noun06,
            nouns.noun07,
            nouns.noun08,
            nouns.noun09,
            nouns.noun10,
            nouns.noun11,
            nouns.noun12,
            nouns.noun13,
            nouns.noun14,
            nouns.noun15,
            nouns.noun16,
            nouns.noun17,
            nouns.noun18,
            None,
            nouns.noun20,
            nouns.noun21,
            nouns.noun22,
            None,
            nouns.noun24,
            nouns.noun25,
            nouns.noun26,
            nouns.noun27,
            None,
            nouns.noun29,
            nouns.noun30,
            nouns.noun31,
            nouns.noun32,
            nouns.noun33,
            nouns.noun34,
            nouns.noun35,
            nouns.noun36,  # implemented!
            nouns.noun37,
            nouns.noun38,
            nouns.noun39,
            nouns.noun40,
            nouns.noun41,
            nouns.noun42,
            nouns.noun43,
            nouns.noun44,
            nouns.noun45,
            nouns.noun46,
            nouns.noun47,
            nouns.noun48,
            nouns.noun49,
            nouns.noun50,
            nouns.noun51,
            nouns.noun52,
            nouns.noun53,
            nouns.noun54,
            nouns.noun55,
            nouns.noun56,
            None,
            nouns.noun58,
            nouns.noun59,
            nouns.noun60,
            nouns.noun61,
            nouns.noun62,
            nouns.noun63,
            nouns.noun64,
            nouns.noun65,
            nouns.noun66,
            nouns.noun67,
            nouns.noun68,
            nouns.noun69,
            nouns.noun70,
            nouns.noun71,
            None,
            nouns.noun73,
            nouns.noun74,
            nouns.noun75,
            None,
            None,
            nouns.noun78,
            nouns.noun79,
            nouns.noun80,
            nouns.noun81,
            nouns.noun82,
            nouns.noun83,
            nouns.noun84,
            nouns.noun85,
            nouns.noun86,
            nouns.noun87,
            nouns.noun88,
            nouns.noun89,
            nouns.noun90,
            nouns.noun91,
            nouns.noun92,
            nouns.noun93,
            nouns.noun94,
            nouns.noun95,
            nouns.noun96,
            nouns.noun97,
            nouns.noun98,
            nouns.noun99,
        ]
        self.verbs = [
            None,  # 0
            verbs.Verb1(),  # implemented!
            verbs.Verb2(),  # implemented!
            verbs.Verb3(),  # implemented!
            verbs.Verb4(),  # implemented!
            verbs.Verb5(),  # implemented!
            verbs.Verb6(),  # implemented!
            verbs.Verb7(),
            None,  # 8
            None,  # 9
            None,  # 10
            verbs.Verb11(),
            verbs.Verb12(),
            verbs.Verb13(),
            verbs.Verb14(),
            verbs.Verb15(),
            verbs.Verb16(),
            verbs.Verb17(),
            None,  # 18
            None,  # 19
            None,  # 20
            verbs.Verb21(),
            verbs.Verb22(),
            verbs.Verb23(),
            verbs.Verb24(),
            verbs.Verb25(),
            None,
            verbs.Verb27(),
            None,  # 28
            None,  # 29
            verbs.Verb30(),
            verbs.Verb31(),
            verbs.Verb32(),  # partially implemented
            verbs.Verb33(),  # partially implemented
            verbs.Verb34(),  # partially implemented
            verbs.Verb35(),  # implemented!
            verbs.Verb36(),
            verbs.Verb37(),
            None,  # 38
            None,  # 39
            verbs.Verb40(),
            verbs.Verb41(),
            verbs.Verb42(),
            verbs.Verb43(),
            verbs.Verb44(),
            verbs.Verb45(),
            verbs.Verb46(),
            verbs.Verb47(),
            verbs.Verb48(),
            verbs.Verb49(),
            verbs.Verb50(),
            verbs.Verb51(),
            verbs.Verb52(),
            verbs.Verb53(),
            verbs.Verb54(),
            verbs.Verb55(),
            verbs.Verb56(),
            verbs.Verb57(),
            verbs.Verb58(),
            verbs.Verb59(),
            verbs.Verb60(),
            verbs.Verb61(),
            verbs.Verb62(),
            verbs.Verb63(),
            verbs.Verb64(),
            verbs.Verb65(),
            verbs.Verb66(),
            verbs.Verb67(),
            None,  # 68
            verbs.Verb69(),
            verbs.Verb70(),
            verbs.Verb71(),
            verbs.Verb72(),
            verbs.Verb73(),
            verbs.Verb74(),
            verbs.Verb75(),
            None,  # 76
            None,  # 77
            verbs.Verb78(),
            None,  # 79
            verbs.Verb80(),
            verbs.Verb81(),
            verbs.Verb82(),
            verbs.Verb83(),
            None,  # 84
            verbs.Verb85(),
            verbs.Verb86(),
            verbs.Verb87(),
            verbs.Verb88(),
            verbs.Verb89(),
            verbs.Verb90(),
            verbs.Verb91(),
            verbs.Verb92(),
            verbs.Verb93(),
            verbs.Verb94(),
            None,  # 95
            verbs.Verb96(),
            verbs.Verb97(),
            None,  # 98
            verbs.Verb99(),
        ]

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
