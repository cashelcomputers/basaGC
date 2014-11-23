#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""This file contains the guts of the guidance computer"""

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

import wx

import utils
import telemachus
#import config
#import display
import dsky
import verbs
import nouns
import programs
import routines
from sortedcontainers import SortedDict
from telemachus import check_connection, get_telemetry
import telemachus


class Computer(object):

    """ This object models the core of the guidance computer.
    """

    def __init__(self, gui):

        """ Class constructor.
        :param gui: the wxPython frame object
        :return: None
        """

        self.gui = gui
        self.dsky = dsky.DSKY(self.gui, self)
        self.loop_timer = utils.Timer(interval=0.5, function=self.main_loop)
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
        self.noun_data = {
            "30": None,
        }
        self.is_ksp_connected = None
        self.ksp_paused_state = None

        telemachus.gc = self
        verbs.computer = self
        verbs.dsky = self.dsky
        verbs.frame = self.gui
        nouns.gc = self
        nouns.dsky = self.dsky
        nouns.frame = self.gui
        programs.gc = self
        programs.dsky = self.dsky
        routines.computer = self

        self.nouns = SortedDict({
            "09": nouns.Noun09(),
            "17": nouns.Noun17(),
            "30": nouns.Noun30(),
            "33": nouns.Noun33(),
            "36": nouns.Noun36(),
            "43": nouns.Noun43(),
            "44": nouns.Noun44(),
            "50": nouns.Noun50(),
            "62": nouns.Noun62(),
        })
        self.verbs = SortedDict({
            "01": verbs.Verb1,
            "02": verbs.Verb2,
            "03": verbs.Verb3,
            "04": verbs.Verb4,
            "05": verbs.Verb5,
            "06": verbs.Verb6,
            "07": verbs.Verb7,
            "11": verbs.Verb11,
            "12": verbs.Verb12,
            "13": verbs.Verb13,
            "14": verbs.Verb14,
            "15": verbs.Verb15,
            "16": verbs.Verb16,
            "17": verbs.Verb17,
            "21": verbs.Verb21,
            "22": verbs.Verb22,
            "23": verbs.Verb23,
            "24": verbs.Verb24,
            "25": verbs.Verb25,
            "32": verbs.Verb32,
            "33": verbs.Verb33,
            "34": verbs.Verb34,
            "35": verbs.Verb35,
            "36": verbs.Verb36,
            "37": verbs.Verb37,
            "75": verbs.Verb75,
            "82": verbs.Verb82,
            "99": verbs.Verb99,
        })

        self.programs = SortedDict({
            "00": programs.Program00(),
            "11": programs.Program11(),
            "15": programs.Program15(),
        })

        # self.routines = {
        #     "average_g": routines.average_g,
        #     30: routines.routine_30,
        # }

        self.option_codes = {
            "00001": "",
            "00002": "",
            "00003": "",
            "00004": "",
            "00007": "",
            "00024": "",
        }
        self.on()

    def quit(self, event=None):

        """ Quits basaGC.
        :param event: wxPython event (not used)
        :return: None
        """

        if self.loop_timer.is_running:
            self.loop_timer.stop()
        self.gui.Destroy()

    def on(self):

        """ Turns the guidance computer on.
        :return: None
        """
        utils.log("Computer booting...", log_level="INFO")

        # attempt to load telemetry listing
        try:
            telemachus.telemetry = telemachus.get_api_listing()
        except telemachus.KSPNotConnected:
            utils.log("Cannot retrieve telemetry listing - no connection to KSP", log_level="WARNING")
        else:
            utils.log("Retrieved telemetry listing", log_level="INFO")
        self.loop_timer.start()
        self.is_powered_on = True
        for display_item in self.dsky.static_display:
            display_item.on()

    def main_loop(self):

        """ The guidance computer main loop. Not used for much yet.
        :return: None
        """

        # Check if we have a connection to KSP
        self.check_ksp_connection()

        # check KSP paused state
        self.check_paused_state()


        # if self.run_average_g_routine:
        #     routines.average_g()
        for item in self.loop_items:
            item()

    def execute_verb(self, verb, noun=None):

        """ Executes the specified verb, optionally with the specified noun.
        :param verb: The verb to execute
        :param noun: The noun to supply to the verb
        :return: None
        """

        if noun is not None:
            self.dsky.set_noun(noun)
        verb = str(verb)
        noun = str(noun)
        self.dsky.control_registers["verb"].display(str(verb))
        verb_to_execute = self.verbs[verb](noun)
        verb_to_execute.execute()

    def reset_alarm_codes(self):

        """ Resets the alarm codes.
        :return: None
        """

        self.alarm_codes[2] = self.alarm_codes[0]
        self.alarm_codes[0] = 0
        self.alarm_codes[1] = 0

    def program_alarm(self, alarm_code, message=None):

        """ Sets the program alarm codes in memory and turns the PROG annunciator on.
        :param alarm_code: a 3 or 4 digit octal int of the alarm code to raise
        :param message: optional message to print to log
        :return: None
        """
        alarm_code += 1000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()
        if message:
            utils.log("PROGRAM ALARM {}: {}".format(str(alarm_code), message), log_level="ERROR")

    def poodoo_abort(self, alarm_code, message=None):

        """ Terminates the faulty program, and executes Program 00 (P00)
        :param alarm_code: a 3 or 4 digit octal int of the alarm code to raise
        :param message: optional message to print to log
        :return: None
        """

        alarm_code += 2000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()
        try:
            self.running_programs[-1].terminate()
        except programs.ProgramTerminated:
            # this should happen if the program terminated successfully
            utils.log("P00DOO ABORT {}: {}".format(str(alarm_code), message), log_level="ERROR")
        self.programs["00"].execute()

    def program_restart(self, alarm_code, message=None):

        """ Triggers a program restart.
        :param alarm_code: a 3 or 4 digit octal int of the alarm code to raise
        :param message: optional message to print to log
        :return: None
        """

        # TODO: insert terminate and restart program
        utils.log("Program fresh start not implemented yet... watch this space...")
        if message:
            utils.log(message, log_level="ERROR")

    def computer_restart(self, alarm_code, message=None):

        """ Triggers a guidance computer hardware restart. The most severe of the errors!
        :param alarm_code: a 3 or 4 digit octal int of the alarm code to raise
        :param message: optional message to print to log
        :return: None
        """

        # insert computer reboot
        # self.fresh_start()
        if message:
            utils.log(message, log_level="CRITICAL")
        pass

    def servicer(self):

        """ For future use. The servicer updates the spacecrafts state vector.
        """

        pass

    def check_ksp_connection(self):

        """ checks if we have a connection to Telemachus / KSP
        Returns nothing.
        """

        if not check_connection():
            if self.is_ksp_connected:
                # we have just lost the connection, illuminate NO ATT annunciator and log it
                self.dsky.annunciators["no_att"].on()
                utils.log("No connection to KSP, navigation functions unavailable", log_level="ERROR")
                self.is_ksp_connected = False
        else:
            if not self.is_ksp_connected:
                # have just regained connection, deluminate NO ATT annunciator and log it
                self.dsky.annunciators["no_att"].off()
                utils.log("Connection to KSP established", log_level="INFO")
                self.is_ksp_connected = True
            if not telemachus.telemetry:
                telemachus.telemetry = telemachus.get_api_listing()

    def check_paused_state(self):

        """ Checks the paused state of KSP, and illuminates STBY annunciator and logs state as necessary.
        """

        if self.is_ksp_connected:
            paused_state = get_telemetry("paused")
            # if the paused state hasn't changed, skip any annunciator changes
            if paused_state != self.ksp_paused_state:
                if paused_state == 0:
                    self.dsky.annunciators["stby"].off()
                    utils.log("KSP unpaused, all systems go", log_level="INFO")
                elif paused_state == 1:
                    self.dsky.annunciators["stby"].on()
                    utils.log("KSP paused", log_level="INFO")
                elif paused_state == 2:
                    self.dsky.annunciators["stby"].on()
                    utils.log("No power to Telemachus antenna", log_level="WARNING")
                elif paused_state == 3:
                    self.dsky.annunciators["stby"].on()
                    utils.log("Telemachus antenna off", log_level="WARNING")
                elif paused_state == 4:
                    self.dsky.annunciators["stby"].on()
                    utils.log("No Telemachus antenna found", log_level="WARNING")
                self.ksp_paused_state = paused_state

