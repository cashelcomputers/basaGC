#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" This module contains code for the DSKY (the guidance computer/user interface)
"""
# This file is part of basaGC (https://github.com/cashelcomputers/basaGC),
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
#  Includes code and images from the Virtual AGC Project (http://www.ibiblio.org/apollo/index.html)
#  by Ronald S. Burkey <info@sandroid.org>import wx

from . import utils
from . import verbs


class DSKY:
    """ This class models the DSKY.
    """

    def __init__(self, computer):

        """ Class constructor.
        :param gui: QtPy5 window object
        :param computer: the instance of the guidance computer
        :return: None
        """

        self.computer = computer
        self.input_data_buffer = ""
        self.register_index = 0
        self.is_verb_being_loaded = False
        self.is_noun_being_loaded = False
        self.is_data_being_loaded = False
        self.verb_position = 0
        self.noun_position = 0
        self.requested_verb = 0
        self.requested_noun = 0
        self.current_verb = 0
        self.current_noun = 0
        self.current_program = 0
        self.display_lock = None
        self.backgrounded_update = None
        self.is_expecting_data = False
        self.is_expecting_proceed = False
        self.object_requesting_data = None
        self.display_location_to_load = None

        self.annunciators = {
            "uplink_acty": self.computer.ui.annunciators["uplink_acty"],
            "temp": self.computer.ui.annunciators["temp"],
            "no_att": self.computer.ui.annunciators["no_att"],
            "gimbal_lock": self.computer.ui.annunciators["gimbal_lock"],
            "stby": self.computer.ui.annunciators["stby"],
            "prog": self.computer.ui.annunciators["prog"],
            "key_rel": self.computer.ui.annunciators["key_rel"],
            "restart": self.computer.ui.annunciators["restart"],
            "opr_err": self.computer.ui.annunciators["opr_err"],
            "tracker": self.computer.ui.annunciators["tracker"],
            "comp_acty": self.computer.ui.annunciators["comp_acty"],
        }

        self.data_registers = {
            1: self.computer.ui.data_registers[1],
            2: self.computer.ui.data_registers[2],
            3: self.computer.ui.data_registers[3],
        }

        self.control_registers = {
            "program": self.computer.ui.control_registers["program"],
            "verb": self.computer.ui.control_registers["verb"],
            "noun": self.computer.ui.control_registers["noun"],
        }


    def operator_error(self, message=None):

        """ Called when the astronaut has entered invalid keyboard input.
        :param message: Optional message to send to log
        :return: None
        """

        if message:
            utils.log("OPERATOR ERROR: " + message)
        self.annunciators["opr_err"].blink_timer.start(500)

    def stop_comp_acty_flash(self, event):

        """ Stops the COMP ACTY annunciator from flashing.
        :param event: wxPython event (not used).
        :return: None
        """

        self.annunciators["comp_acty"].off()

    # def request_proceed_or_data(self, requesting_object, location):
    #
    #     utils.log("{} requesting PROCEED or data".format(requesting_object))
    #     self.verb_noun_flash_on()
    #     self.object_requesting_data = requesting_object
    #     self.is_expecting_data = True
    #     self.display_location_to_load = location
    #
    # def request_proceed(self, requesting_object):
    #     utils.log("{} requesting PROCEED or data".format(requesting_object))
    #     self.verb_noun_flash_on()
    #     self.object_requesting_data = requesting_object
    #     self.is_expecting_data = True

    def request_data(self, requesting_object, display_location, is_proceed_available=False):

        """ Requests data entry from the user.
        :param requesting_object: the object requesting the data
        :param display_location: the register that entered data will be displayed in
        :param is_proceed_available: True if the user can key in PROCEED instead of data
        :return: None
        """

        utils.log("{} requesting data".format(requesting_object))
        self.verb_noun_flash_on()
        self.object_requesting_data = requesting_object
        self.is_expecting_data = True
        self.display_location_to_load = display_location
        # if PROCEED is a valid option, don't blank the data register (user needs to be able to see value :)
        # if not is_proceed_available:
        #     if isinstance(display_location, DataRegister):
        #         for register in list(self.data_registers.values()):
        #             register.blank()
        #     else:
        display_location.blank()

    def verb_noun_flash_on(self):

        """ Starts the verb/noun flash.
        :return: None
        """

        self.control_registers["verb"].digits[0].start_blink()
        self.control_registers["verb"].digits[1].start_blink()
        self.control_registers["noun"].digits[0].start_blink()
        self.control_registers["noun"].digits[1].start_blink()

    def verb_noun_flash_off(self):

        """ Starts the verb/noun flash.
        :return: None
        """

        for digit in list(self.control_registers["verb"].digits.values()):
            digit.stop_blink()
        for digit in list(self.control_registers["noun"].digits.values()):
            digit.stop_blink()


    def charin(self, keypress):
        """
        Handles key input from DSKY keyboard.
        :param keypress: contains the key code
        """
        print("Computer received {}".format(keypress))
        if self.is_expecting_data:
            self._handle_expected_data(keypress)
            return

        if keypress == "R":
            self._handle_reset_keypress()
            return

        if keypress == "K":
            self._handle_key_release_keypress(keypress)
            return

        if self.display_lock:
            self.display_lock.background()

        if self.is_verb_being_loaded:
            self._handle_verb_entry(keypress)

        elif self.is_noun_being_loaded:
            self._handle_noun_entry(keypress)

        if keypress == "E":
            self._handle_entr_keypress(keypress)

        if keypress == "V":
            self._handle_verb_keypress()

        if keypress == "N":
            self._handle_noun_keypress()

        if keypress == "C":
            pass  # TODO


    def stop_blink(self):

        """ Stops the verb/noun flash
        :return: None
        """

        self.is_expecting_data = False
        for d in self.control_registers.values():
            d.stop_blink()
        # for d in self.control_registers["noun"]:
        #     d.stop_blink()

    def _handle_data_register_load(self, keypress):

        """ Handles data register loading
        :return: None
        """

        if self.register_index == 0:
            if keypress == "+":
                self.display_location_to_load.sign.plus()
            elif keypress == "-":
                self.display_location_to_load.sign.minus()
            else:
                self.display_location_to_load.digits[0].display(keypress)
                self.register_index += 1
        elif self.register_index >= 1 <= 5:
            self.display_location_to_load.digits[self.register_index].display(keypress)
            if self.register_index >= 4:
                self.register_index = 0
            else:
                self.register_index += 1
        self.input_data_buffer += keypress


    def _handle_control_register_load(self, keypress):

        """ Handles control register loading
        :return: None
        """

        # we are expecting a numeric digit as input
        if keypress.isalpha():
            self.operator_error("Expecting numeric input")
            return
        # otherwise, add the input to buffer
        elif self.register_index == 0:
            self.display_location_to_load.digits[1].display(keypress)
            self.register_index += 1
        elif self.register_index == 1:
            self.display_location_to_load.digits[2].display(keypress)
            self.register_index = 0
        self.input_data_buffer += keypress

    def _handle_expected_data(self, keypress):

        """ Handles expected data entry.
        :return: None
        """

        if keypress == "P":
            self.stop_blink()
            utils.log("Proceeding without input, calling {}(proceed)".format(
                self.object_requesting_data))
            self.object_requesting_data("proceed")
            self.input_data_buffer = ""
            return

        # if we receive ENTER, the load is complete and we will call the
        # program or verb requesting the data load
        elif keypress == "E":
            self.stop_blink()
            utils.log("Data load complete, calling {} ({})".format(
                self.object_requesting_data,
                self.input_data_buffer))
            self.object_requesting_data(self.input_data_buffer)
            self.input_data_buffer = ""
            return
        
        if self.display_location_to_load in self.data_registers.items():
            self._handle_data_register_load(keypress)
        
        # if isinstance(self.display_location_to_load, DataRegister):
        #     self._handle_data_register_load(keypress)

        elif self.display_location_to_load in self.control_registers.items():
            self._handle_control_register_load(keypress)

        # if the user as entered anything other than a numeric d,
        # trigger a OPR ERR and recycle program
        elif keypress.isalpha():
            # if a program is running, recycle it
            # INSERT TRY HERE!!!
            # computer.get_state("running_program").terminate()
            # INSERT EXCEPT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if a verb is running, recycle it
            #computer.get_state("running_verb").terminate()
            self.operator_error("Expecting numeric input")
            return
        else:
            self.input_data_buffer += keypress

            if self.display_location_to_load in self.data_registers.items():
                self.display_location_to_load.display(sign="", value=self.input_data_buffer)
            else:
                print(self.input_data_buffer)
                self.display_location_to_load.display(self.input_data_buffer)
            # self.is_noun_being_loaded = True
            return

    def _handle_verb_entry(self, keypress):

        """ Handles verb entry
        :return: None
        """

        if keypress == "C":  # user has pushed CLEAR
            self.verb_position = 0
            self.requested_verb = ""
            self.control_registers["verb"].digits[1].display("blank")
            self.control_registers["verb"].digits[2].display("blank")
            return

        if keypress == "N":  # user has finished entering verb
            self.is_verb_being_loaded = False
            self.is_noun_being_loaded = True
            self.verb_position = 0
        elif keypress == "E":
            self.is_verb_being_loaded = False
            self.verb_position = 0
        elif keypress.isalpha():
            self.operator_error("Expected a number for verb choice")
            return
        elif self.verb_position == 0:
            self.control_registers["verb"].digits[0].display(keypress)
            self.requested_verb = keypress
            self.verb_position = 1
        elif self.verb_position == 1:
            self.control_registers["verb"].digits[1].display(keypress)
            self.requested_verb += keypress
            self.verb_position = 2


    def _handle_noun_entry(self, keypress):

        """ Handles noun entry.
        :return: None
        """

        if keypress == "C":  # user has pushed CLEAR
            self.noun_position = 0
            self.requested_noun = ""
            self.control_registers["noun"].digits[1].display("blank")
            self.control_registers["noun"].digits[2].display("blank")
            return

        if keypress == "N":  # user has finished entering noun
            self.is_noun_being_loaded = False
            self.is_verb_being_loaded = True
            self.noun_position = 0
        elif keypress == "E":
            self.is_noun_being_loaded = False
            self.noun_position = 0
        elif keypress.isalpha():
            self.operator_error("Expected a number for noun choice")
            return
        elif self.noun_position == 0:
            self.control_registers["noun"].digits[0].display(keypress)
            self.requested_noun = keypress
            self.noun_position = 1
        elif self.noun_position == 1:
            self.control_registers["noun"].digits[1].display(keypress)
            self.requested_noun += keypress
            self.noun_position = 2

    def _handle_entr_keypress(self, keypress):

        """ Handles ENTR keypress
        :return: None
        """

        this_verb = None
        if self.requested_verb in verbs.INVALID_VERBS:
            self.operator_error(
                "Verb {} does not exist, please try a different verb".format(self.requested_verb))
            return
        try:

            if int(self.requested_verb) < 40:
                this_verb = self.computer.verbs[self.requested_verb](self.requested_noun)
            else:
                this_verb = self.computer.verbs[self.requested_verb]()
        except IndexError:
            utils.log("Verb {} not in verb list".format(self.requested_verb), "ERROR")
            self.operator_error()
        try:
            this_verb.execute()
        except NotImplementedError:
            self.operator_error(
                "Verb {} is not implemented yet. Sorry about that...".format(self.requested_verb))
        except verbs.NounNotAcceptableError:
            self.operator_error(
                "Noun {} can't be used with verb {}".format(self.requested_noun, self.requested_verb))

        return

    def _handle_reset_keypress(self):

        """ Handles RSET keypress
        :return: None
        """

        self.computer.reset_alarm_codes()
        for annunciator in self.annunciators.values():
            if annunciator.blink_timer.isActive():
                annunciator.stop_blink()
            annunciator.off()

    def _handle_noun_keypress(self):

        """ Handles NOUN keypress
        :return: None
        """

        self.is_verb_being_loaded = False
        self.is_noun_being_loaded = True
        self.requested_noun = ""
        self.control_registers["noun"].blank()

    def _handle_verb_keypress(self):

        """ Handles VERB keypress
        :return: None
        """

        self.is_noun_being_loaded = False
        self.is_verb_being_loaded = True
        self.requested_verb = ""
        self.control_registers["verb"].blank()

    def _handle_key_release_keypress(self, keypress):

        """ Handles KEY REL keypress
        :return: None
        """
        if self.backgrounded_update:
            if self.display_lock:
                self.display_lock.terminate()
            self.annunciators["key_rel"].stop_blink()
            self.backgrounded_update.resume()
            self.backgrounded_update = None
            self.is_verb_being_loaded = False
            self.is_noun_being_loaded = False
            self.is_data_being_loaded = False
            self.verb_position = 0
            self.noun_position = 0
            self.requested_verb = 0
            self.requested_noun = 0
            return

        # if the computer is off, we only want to accept the PRO key input,
        # all other keys are ignored
        if self.computer.is_powered_on is False:
            if keypress == "P":
                self.computer.on()
            else:
                utils.log("Key {} ignored because gc is off".format(keypress))

    def flash_comp_acty(self):

        """ Flashes the COMP ACTY annunciator.
        :return: None
        """

        pass
        # self.annunciators["comp_acty"].on()
        # self.comp_acty_timer.Start(config.COMP_ACTY_FLASH_DURATION, oneShot=True)

    def set_noun(self, noun):

        """ Sets the required noun.
        :param noun: Noun to set
        :return:
        """

        self.requested_noun = noun
        self.control_registers["noun"].display(noun)

    def key_button_input(self):
        self.computer.ui.key_press_signal.connect(self.foob)

