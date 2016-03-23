#!/usr/bin/env python3
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

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

import new_gui


#from . import new_gui
import burn
import config
import utils

import verbs
import nouns
import programs
import telemachus


class TestGui(QMainWindow, new_gui.Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

class Computer:

    """ This object models the core of the guidance computer.
    """

    def __init__(self, gui):

        """ Class constructor.
        :param gui: the wxPython frame object
        :return: None
        """

        # init Qt

        utils.log(message="\n\n" + config.SHORT_LICENCE + "\n", log_level="INFO")

        # this has to go here, so we can init the widgets first
        import dsky
        self.gui = gui
        self.dsky = dsky.DSKY(self.gui, self)

        self.loop_timer = QTimer()
        self.loop_timer.timeout.connect(self.main_loop)
        self.is_powered_on = False
        self.main_loop_table = []
        # self.gui.Bind(wx.EVT_CLOSE, self.quit)
        self.alarm_codes = [0, 0, 0]
        self.running_program = None
        self.noun_data = {
            "30": [],
        }
        self.next_burn = None
        self._burn_queue = []
        self.is_ksp_connected = None
        self.ksp_paused_state = None
        self.is_direction_autopilot_engaged = False
        self.is_thrust_autopilot_engaged = False
        self.moi_burn_delta_v = 0.0  # a bit of a hack, need to rethink this


        burn.gc = self
        telemachus.gc = self
        verbs.gc = self
        verbs.dsky = self.dsky
        verbs.frame = self.gui
        nouns.gc = self
        nouns.dsky = self.dsky
        nouns.frame = self.gui
        programs.gc = self
        programs.dsky = self.dsky

        self.nouns = nouns.nouns
        self.verbs = verbs.verbs
        self.programs = programs.programs

        self.option_codes = {
            "00001": "",
            "00002": "",
            "00003": "",
            "00004": "",
            "00007": "",
            "00024": "",
        }
        print("FOO")
        self.on()


    def add_burn_to_queue(self, burn_object, execute=True):

        """ Adds a Burn object to the computer burn queue. If no burn is assigned to next_burn, load new burn to
        next_burn
        :param burn_object: a Burn object that contains parameters for the burn
        :param execute: if true, execute the added burn
        :return: None
        """

        self._burn_queue.append(burn_object)
        if not self.next_burn:
            self.next_burn = self._burn_queue.pop()
        if execute:
            self.next_burn.execute()

    def remove_burn(self, this_burn):

        """ Removes a given Burn object from the computers burn queue
        :param this_burn: the Burn object to remove
        :return: None
        """

        if this_burn == self.next_burn:
            self.next_burn = None
        if this_burn in self._burn_queue:
            self._burn_queue.remove(this_burn)

    def burn_complete(self):

        """ Removes a completed burn and loads next queued burn if available.
        :return: None
        """
        utils.log("Removing {} from burn queue".format(self.next_burn))
        self.next_burn = None
        if self._burn_queue:
            utils.log("Adding {} as next burn".format(self._burn_queue[0]))
            self.next_burn = self._burn_queue.pop()

    def disable_direction_autopilot(self):

        """ Disables the directional autopilot
        :return: None
        """

        telemachus.disable_smartass()
        self.is_direction_autopilot_engaged = False
        utils.log("Autopilot disabled", log_level="INFO")

    def quit(self, event=None):

        """ Quits basaGC.
        :param event: wxPython event (not used)
        :return: None
        """

        # disables SMARTASS
        try:
            telemachus.disable_smartass()
        except TypeError:
            pass
        # if self.loop_timer.is_running:
        #     self.loop_timer.stop()
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
            self.dsky.annunciators["no_att"].on()
        else:
            utils.log("Retrieved telemetry listing", log_level="INFO")
        self.loop_timer.start(config.LOOP_TIMER_INTERVAL)
        self.is_powered_on = True
        for display_item in self.dsky.static_display:
            display_item.on()

    def main_loop(self):

        """ The guidance computer main loop.
        :return: None
        """

        # Check if we have a connection to KSP
        self.check_ksp_connection()

        # check KSP paused state
        self.check_paused_state()

        # if self.run_average_g_routine:
        #     routines.average_g()
        for item in self.main_loop_table:
            item()

    def go_to_poo(self):

        """ Executes program 00. Name comes from NASA documentation :)
        :return: None
        """

        poo = self.programs["00"]()
        poo.execute()

    def execute_verb(self, verb, noun=None, **kwargs):

        """ Executes the specified verb, optionally with the specified noun.
        :param verb: The verb to execute
        :param noun: The noun to supply to the verb
        :return: None
        """
        if noun is not None:
            self.dsky.set_noun(noun)
        verb = str(verb)
        noun = str(noun)
        self.dsky.control_registers["verb"].display(verb)
        if int(verb) < 40:
            verb_to_execute = self.verbs[verb](noun)
        else:
            verb_to_execute = self.verbs[verb]()
        verb_to_execute.execute(**kwargs)

    def reset_alarm_codes(self):

        """ Resets the alarm codes.
        :return: None
        """

        self.alarm_codes[2] = self.alarm_codes[0]
        self.alarm_codes[0] = 0
        self.alarm_codes[1] = 0

    def program_alarm(self, alarm_code):

        """ Sets the program alarm codes in memory and turns the PROG annunciator on.
        :param alarm_code: a 3 or 4 digit octal int of the alarm code to raise
        :return: None
        """
        utils.log("PROGRAM ALARM {}: {}".format(str(alarm_code), config.ALARM_CODES[alarm_code]), log_level="ERROR")
        alarm_code += 1000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()

    def poodoo_abort(self, alarm_code):

        """ Terminates the faulty program, and executes Program 00 (P00)
        :param alarm_code: a 3 digit octal int of the alarm code to raise
        :return: None
        """

        alarm_message = config.ALARM_CODES[alarm_code]
        alarm_code += 2000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()
        try:
            self.running_program[-1].terminate()
        except programs.ProgramTerminated:
            # this should happen if the program terminated successfully
            utils.log("P00DOO ABORT {}: {}".format(str(alarm_code), alarm_message), log_level="ERROR")
        poo = self.programs["00"]()
        poo.execute()

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
        :return: None
        """

        if not telemachus.check_connection():
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
                telemachus.get_api_listing()

    def check_paused_state(self):

        """ Checks the paused state of KSP, and illuminates STBY annunciator and logs state as necessary.
        :return: None
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

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = TestGui()
ui.setupUi(MainWindow)
computer = Computer(ui)
MainWindow.show()
sys.exit(app.exec_())