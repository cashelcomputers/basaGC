#!/usr/bin/env python3
"""This file contains the guts of the guidance computer"""

from PyQt5.QtCore import QTimer

from basagc import config
from basagc import dsky
from basagc import nouns
from basagc import programs
from basagc import routines
from basagc import telemachus
from basagc import utils
from basagc import verbs


class Computer:

    """ This object models the core of the guidance computer.
    """

    computer_instance = None

    def __init__(self, ui):

        """ Class constructor.
        :param gui: the wxPython frame object
        :return: None
        """

        Computer.computer_instance = self
        verbs.Verb.computer = self

        utils.log(message="\n\n" + config.SHORT_LICENCE + "\n", log_level="INFO")
        self.ui = ui

        self.dsky = dsky.DSKY(self, self.ui)
        self.keyboard_state = {
            "input_data_buffer": "",
            "register_index": 0,
            "is_verb_being_loaded": False,
            "is_noun_being_loaded": False,
            "is_data_being_loaded": False,
            "verb_position": 0,
            "noun_position": 0,
            "requested_verb": 0,
            "requested_noun": 0,
            "current_verb": 0,
            "current_noun": 0,
            "current_program": 0,
            "display_lock": None,
            "backgrounded_update": None,
            "is_expecting_data": False,
            "is_expecting_proceed": False,
            "object_requesting_data": None,
            "display_location_to_load": None,
            "set_keyboard_state_setter": self.set_keyboard_state,
        }
        self.main_loop_timer = QTimer()
        self.main_loop_timer.timeout.connect(self.main_loop)
        self.is_powered_on = False
        self.main_loop_table = []
        self.alarm_codes = [0, 0, 0]
        self.running_programs = []
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
        self.jobs = []

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

        self.on()

    def get_verbs(self):

        verbs_dict = OrderedDict()
        clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        for class_tuple in clsmembers:
            if class_tuple[0][-1].isdigit():
                verbs_dict[class_tuple[0][-2:]] = class_tuple[1]

    def charin(self, keypress):
        routines.charin(keypress, self.keyboard_state, self.dsky, self)

    def register_charin(self):
        self.ui.register_key_event_handler(self.charin)

    def set_keyboard_state(self, state_name, new_value):
        self.keyboard_state[state_name] = new_value

    def add_burn_to_queue(self, burn_object, execute=True):

        """ Adds a Burn object to the computer burn queue. If no burn is
        assigned to next_burn, load new burn to next_burn
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

    def quit(self):

        """ Quits basaGC.
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
            telemachus.get_api_listing()
        except telemachus.KSPNotConnected:
            utils.log("Cannot retrieve telemetry listing - no connection to KSP", log_level="WARNING")
            self.dsky.annunciators["no_att"].on()
        else:
            utils.log("Retrieved telemetry listing", log_level="INFO")

        # register key handler with qt ui
        self.register_charin()

        self.main_loop_timer.start(config.LOOP_TIMER_INTERVAL)
        self.is_powered_on = True

    def main_loop(self):

        """ The guidance computer main loop.
        :return: None
        """

        # Check if we have a connection to KSP
        self.check_ksp_connection()

        # check KSP paused state
        self.check_paused_state()

        # run each item in process queue
        for item in self.main_loop_table:
            item()

    def go_to_poo(self):

        """ Executes program 00. Name comes from NASA documentation :)
        :return: None
        """

        poo = self.programs["00"]()
        poo.execute()

    def execute_verb(self):

        """ Executes the verb as stored in self.keyboard_state
        :return: None
        """
        verb = self.keyboard_state["requested_verb"]
        if self.keyboard_state["requested_noun"] == 0:
            noun = None
        else:
            noun = self.keyboard_state["requested_noun"]
        self.dsky.set_register(value=verb, register="verb")
        verb_to_execute = self.verbs[verb](noun)
        self.add_job(verb_to_execute)
        verb_to_execute.execute()

    def remove_job(self, job):
        utils.log("Removing job from jobs list: {}".format(job))
        self.jobs.remove(job)

    def add_job(self, job):
        utils.log("Adding job to jobs list: {}".format(job))
        self.jobs.append(job)

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
            self.running_program.terminate()
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
            paused_state = telemachus.get_telemetry("paused")
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

