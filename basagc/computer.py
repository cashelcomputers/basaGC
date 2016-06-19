#!/usr/bin/env python3
"""This file contains the guts of the guidance computer"""

import os

from PyQt5.QtCore import QTimer


from basagc import config
if config.DEBUG:
    from pudb import set_trace
from basagc import dsky
from basagc import nouns
from basagc import programs
from basagc import routines
from basagc import utils
from basagc import verbs
from basagc import maneuver


class Computer:

    """ This object models the core of the guidance computer.
    """

    computer_instance = None

    def __init__(self, ui, vessel):

        """ Class constructor.
        :param gui: the wxPython frame object
        :return: None
        """

        Computer.computer_instance = self
        verbs.Verb.computer = self

        nouns.vessel = vessel
        maneuver.computer = self

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
            "requested_verb": "",
            "requested_noun": "",
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

        # init slow loop (for less important tasks that can be ran approx 2 seconds)
        self.slow_loop_timer = QTimer()
        self.slow_loop_timer.timeout.connect(self.slow_loop)

        self.comp_acty_timer = QTimer()
        self.comp_acty_timer.timeout.connect(self._comp_acty_off)

        self.uplink_queue = []
        self.is_powered_on = False
        self.main_loop_table = []
        self.alarm_codes = [0, 0, 0]
        self.running_programs = []
        self.noun_data = {
            "06": "",  # time to event
            "30": ["00002"],
            "25": ["00000", "00000", ""],
            "31": ["00000", "00000"],
            "38": ["00000", "", ""],
        }
        self.memory = {
            "TIG": 0.0,
        }
        self.next_burn = None
        self.is_ksp_connected = False
        self.ksp_paused_state = None
        self.is_direction_autopilot_engaged = False
        self.is_thrust_autopilot_engaged = False
        self.moi_burn_delta_v = 0.0  # a bit of a hack, need to rethink this

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
        # register key handler with qt ui
        self.register_charin()

    def accept_uplink(self):
        try:
            uplink_file = open(os.path.join(config.BASE_DIR, "basagc/", "uplink.txt"), "r")
        except FileNotFoundError:  # lint:ok
            self.program_alarm(501)
            return
        self.dsky.set_annunciator("uplink_acty")
        uplink_data = uplink_file.read().strip()
        uplink_file.close()
        for char in uplink_data:
            if char == "\n":
                continue
            self.uplink_queue.append(char)
    
    def charin(self, keypress):
        """
        Receives a keypress event and passes it on to routines.charin
        :param keypress: the value of the key pressed
        :type keypress: str
        :returns: None
        """
        routines.charin(keypress, self.keyboard_state, self.dsky, self)

    def process_uplink_data(self):
        
        # check if any data ready to be uplinked
        if len(self.uplink_queue) > 0:
            char = self.uplink_queue.pop(0)
            self.charin(char)
            return True
        else:
            # self.dsky.set_annunciator("uplink_acty", False)
            return False

    def add_to_mainloop(self, func):
        self.main_loop_table.append(func)

    def remove_from_mainloop(self, func):
        if func in self.main_loop_table:
            self.main_loop_table.remove(func)
        else:
            utils.log("Cannot remove function from mainloop, function {} not found".format(func))

    def register_charin(self):
        """
        Registers the charin handler with the GUI
        :returns: None
        """
        self.ui.register_key_event_handler(self.charin)

    def set_keyboard_state(self, state_name, new_value):
        """
        setter for keyboard state
        :param state_name: the name of the state to change
        :type state_name: str
        :param new_value: the new value
        :type new_value: str
        :returns: None
        """
        self.keyboard_state[state_name] = new_value

    def add_burn(self, burn_object):

        """ Adds a Burn object to the computer burn queue. If no burn is
        assigned to next_burn, load new burn to next_burn
        :param burn_object: a Burn object that contains parameters for the burn
        :param execute: if true, execute the added burn
        :return: None
        """
        self.next_burn = burn_object
        #self.add_to_mainloop(burn_object._coarse_start_time_monitor)

    def enable_burn(self):
        self.next_burn.execute()

    def remove_burn(self):

        """ Removes a given Burn object from the computers burn queue
        :param this_burn: the Burn object to remove
        :return: None
        """
        self.next_burn = None


    #def burn_complete(self):

        #""" Removes a completed burn and loads next queued burn if available.
        #:return: None
        #"""
        #utils.log("Removing {} from burn queue".format(self.next_burn))
        #self.next_burn = None
        #if self._burn_queue:
            #utils.log("Adding {} as next burn".format(self._burn_queue[0]))
            #self.next_burn = self._burn_queue.pop()

    # def disable_direction_autopilot(self):
    #
    #     """ Disables the directional autopilot
    #     :return: None
    #     """
    #
    #     telemachus.disable_smartass()
    #     self.is_direction_autopilot_engaged = False
    #     utils.log("Autopilot disabled", log_level="INFO")

    # def quit(self):
    #
    #     """ Quits basaGC.
    #     :return: None
    #     """
    #
    #     # disables SMARTASS
    #     try:
    #         telemachus.disable_smartass()
    #     except TypeError:
    #         pass
    #     # if self.loop_timer.is_running:
    #     #     self.loop_timer.stop()
    #     self.gui.Destroy()

    def on(self):

        """ Turns the guidance computer on.
        :return: None
        """

        utils.log("Computer booting...", log_level="INFO")
        self.is_powered_on = True

        # start the loops
        self.main_loop_timer.start(config.LOOP_TIMER_INTERVAL)
        self.slow_loop_timer.start(config.SLOW_LOOP_TIMER_INTERVAL)

    def main_loop(self):

        """ The guidance computer main loop.
        :return: None
        """

        # check KSP paused state
        # self.check_paused_state()

        # run each item in process queue
        for item in self.main_loop_table:
            item()


    def slow_loop(self):
        """
        A slower loop to handle tasks that are less frequently run
        :returns:
        """
        # if not ksp.check_connection():
        #     self.dsky.annunciators["no_att"].on()
        if config.ENABLE_COMP_ACTY_FLASH:
            self.flash_comp_acty()
        

    def go_to_poo(self):

        """ Executes program 00. Name comes from NASA documentation :)
        :return: None
        """

        poo = self.programs["00"]()
        poo.execute()

    def execute_verb(self, verb=None, noun=None, **kwargs):

        """ Executes the verb as stored in self.keyboard_state
        :return: None
        """
        if not verb:
            verb = self.keyboard_state["requested_verb"]
        self.dsky.set_register(value=verb, register="verb")

        if not noun:
        # if verb doesn't exist, smack operator over head
            try:
                # if there is a noun entered by user, pass it to verb
                if self.keyboard_state["requested_noun"] == "":
                    verb_to_execute = self.verbs[verb](**kwargs)
                else:
                    verb_to_execute = self.verbs[verb](self.keyboard_state["requested_noun"], **kwargs)
            except KeyError:
                self.operator_error("Verb {} does not exist :(".format(verb))
                return
        else:
            verb_to_execute = self.verbs[verb](noun, **kwargs)

        self.flash_comp_acty(200)
        verb_to_execute.execute()

    def terminate_verb(self, verb):
        self.verbs[verb].terminate(self)

    def execute_program(self, program_number):
        """
        Executes the given program.Must have between 1 and 6 values to disp
        :param program_number: the program number to execute
        :type program_number: str
        :returns:
        """
        try:
            program = self.programs[program_number]()
        except KeyError:
            self.program_alarm(116)
            self.go_to_poo()
            return
        program.execute()
        
    
    def flash_comp_acty(self, duration=config.COMP_ACTY_FLASH_DURATION):
        """
        Flashes the Computer Activity annunciator.

        :returns:
        """
        self.dsky.annunciators["comp_acty"].on()
        self.comp_acty_timer.start(duration)

    def _comp_acty_off(self):
        """
        Turns off the comp acty annunciator
        :returns: None
        """
        self.dsky.annunciators["comp_acty"].off()
        self.comp_acty_timer.stop()
    
    def operator_error(self, message=None):

        """ Called when the astronaut has entered invalid keyboard input.
        :param message: Optional message to send to log
        :return: None
        """

        if message:
            utils.log("OPERATOR ERROR: " + message, log_level="ERROR")
        self.dsky.annunciators["opr_err"].blink_timer.start(500)
        
    #def remove_job(self, job):
        #utils.log("Removing job from jobs list: {}".format(job))
        #self.jobs.remove(job)

    #def add_job(self, job):
        #utils.log("Adding job to jobs list: {}".format(job))
        #self.jobs.append(job)

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

    def poodoo_abort(self, alarm_code, message=None):

        """ Terminates the faulty program, and executes Program 00 (P00)
        :param alarm_code: a 3 digit octal int of the alarm code to raise
        :return: None
        """

        # alarm_message = config.ALARM_CODES[alarm_code]
        alarm_code += 2000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()
        self.running_program.terminate()
        utils.log("P00DOO ABORT {}: {}".format(str(alarm_code), message), log_level="ERROR")
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