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

# from PyQt5.QtCore import QTimer

from PyQt5.QtCore import pyqtSignal

import config
import utils
import verbs


class NumericDigit:
    """ A numeric digit.
    """

    def __init__(self):

        """ Class constructor.
        :return: None
        """
        self.current_value = None
        self.is_blinking = False
        self.is_blinking_lit = True
        self.blink_value = None
        self.last_value = None
        # setup blink timers
        # self.blink_timer = QTimer()
        # self.blink_timer.timeout.connect(self._blink)

        self.current_value = "blank"

    def set_tooltip(self, tooltip):

        """ Sets the wxPython tooltip to the provided value.
        :param tooltip: The tooltip to display.
        :return: None
        """

        #self.widget.SetToolTipString(tooltip)

    def start_blink(self, value=None):

        """ Starts the digit blinking.
        :param value: Value to blink with
        :return: None
        """

        if value:
            self.blink_value = value
        else:
            self.blink_value = self.current_value
        self.is_blinking = True

        self.blink_timer.Start(500)

    def _blink(self, event):

        if self.is_blinking_lit:
            self.display("blank")
            self.is_blinking_lit = False
        else:
            self.display(self.blink_value)
            self.is_blinking_lit = True

    def stop_blink(self):

        """ Stops the digit blinking.
        :return: None
        """

        self.blink_timer.Stop()
        self.display(self.blink_value)
        self.blink_value = None

    def blank(self):

        """ Blanks the digit.
        :return: None
        """

        self.last_value = self.current_value
        self.display("blank")

    def display(self, new_value):

        """ Displays the required number on the digit.
        :param new_value: the value to display (string)
        :return: None
        """

        if new_value == "0":
            self.widget.setPixmap(self._digit_0)
        elif new_value == "1":
            self.widget.setPixmap(self._digit_1)
        elif new_value == "2":
            self.widget.setPixmap(self._digit_2)
        elif new_value == "3":
            self.widget.setPixmap(self._digit_3)
        elif new_value == "4":
            self.widget.setPixmap(self._digit_4)
        elif new_value == "5":
            self.widget.setPixmap(self._digit_5)
        elif new_value == "6":
            self.widget.setPixmap(self._digit_6)
        elif new_value == "7":
            self.widget.setPixmap(self._digit_7)
        elif new_value == "8":
            self.widget.setPixmap(self._digit_8)
        elif new_value == "9":
            self.widget.setPixmap(self._digit_9)
        elif new_value == "blank":
            self.widget.setPixmap(self._digit_blank)
        elif new_value == "b":
            self.widget.setPixmap(self._digit_blank)
        self.current_value = new_value
        if self.is_blinking:
            if new_value != "blank":
                self.blink_value = new_value


class SignDigit:
    """ A class for a plus or minus digit.
    """

    def __init__(self):

        """ Class constructor.
        :param dsky: the DSKY instance to use
        :param panel: wxPython panel to display on
        :return: None
        """

    def set_tooltip(self, tooltip):

        """ Sets the wxPython tooltip to the provided value.
        :param tooltip: The tooltip to display.
        :return: None
        """

        # TODO: emit signal

    def plus(self):

        """ Sets the digit to "+"
        :return: None
        """

        # TODO: emit signal

    def minus(self):

        """ Sets the digit to "-"
        :return: None
        """

        # TODO: emit signal

    def blank(self):

        """ Blanks the digit.
        :return: None
        """

        # TODO: emit signal


class Annunciator:
    """ A class for annunciators.
    """

    def __init__(self, name=None):

        """ Class constructor.
        :param dsky: the DSKY instance to use
        :param panel: wxPython panel to display on
        :param name: Name of the annunciator
        :return: None
        """

        self.name = name
        self.is_lit = False
        self.requested_state = False

        # setup blink timer
        # self.blink_timer = QTimer()
        # self.blink_timer.timeout.connect(self._blink)

    def start_blink(self, interval=500):

        """ Starts the annunciator blinking.
        :param interval: the blink interval
        :return: None
        """

        self.blink_timer.start(interval)

    def stop_blink(self):

        """ Stops the annunciator blinking.
        :return: None
        """

        self.blink_timer.stop()
        self.off()

    def _blink(self, event):
        """ Blinks indicator """

        if self.is_lit:
            self.off()
        else:
            self.on()

    def on(self):

        """ Illuminates the annunciator.
        :return: None
        """

        # TODO: emit signal
        self.is_lit = True

    def off(self):

        """ Deluminates the annunciator.
        :return: None
        """

        # TODO: emit signal
        self.is_lit = False


class DataRegister:
    """ A class for the data registers
    """

    def __init__(self, name):

        """ Class constructor.
        :param dsky: the DSKY instance to use
        :return: None
        """
        self.display_signal = pyqtSignal()
        self.name = name
        self.sign = SignDigit()
        self.digits = [
            NumericDigit(),
            NumericDigit(),
            NumericDigit(),
            NumericDigit(),
            NumericDigit(),
        ]

    def display(self, value):

        """ Displays a given value on the whole data register (including sign).
        :param value: The value to display
        :return: None
        """

        # some value length checks
        value_length = len(value)
        if value_length > 6:
            utils.log("Too many digits passed to display(), got {} digits".format(value_length), log_level="ERROR")
            return
        elif value_length == 5:
            utils.log("display() received only 5 digits, assuming sign is blank", log_level="WARNING")

        elif value_length < 5:
            utils.log("display() received {} digits, padding with zeros to the left".format(value_length),
                      log_level="WARNING")
            value.zfill(5)

        self.display_signal = pyqtSignal({
            "type": "update_data_register",
            "register": self.name,
            "digit_sign": value[0],
            "digit_1": value[1],
            "digit_2": value[2],
            "digit_3": value[3],
            "digit_4": value[4],
            "digit_5": value[5],
        })
        self.display_signal.emit()

        # if value[0] == "-":
        #     self.sign.minus()
        #     value = value[1:]
        # elif value[0] == "+":
        #     self.sign.plus()
        #     value = value[1:]
        # elif value[0] == "b":
        #     self.sign.blank()
        #     value = value[1:]
        # else:
        #     self.sign.blank()

        # display each digit
        for index, digit in enumerate(value):
            self.digits[index].display(digit)

    def blank(self):

        """ Blanks the whole data register.
        :return: None
        """

        self.sign.blank()
        for digit in self.digits:
            digit.display("blank")

    def set_tooltip(self, tooltip):

        """ Sets the wxPython tooltip to the provided value.
        :param tooltip: The tooltip to display.
        :return: None
        """
        pass
        for digit in self.digits:
            pass
            # TODO: emit signal

    def start_blink(self):
        pass
        for digit in self.digits:
            pass
            # TODO: emit signal

    def stop_blink(self):

        pass
        for digit in self.digits:
            pass
            # TODO: emit signal


class ControlRegister:
    """ A class for the control registers.
    """

    def __init__(self, name):

        """ Class constructor.
        :param dsky: the DSKY instance to use
        :param name: Name of the control register.
        :return: None
        """

        self.display_signal = pyqtSignal()
        self.name = name
        self.digits = {
            1: NumericDigit(),
            2: NumericDigit(),
        }

    def display(self, value):

        """ Displays the given value on the whole control register.
        :param value: The value to display.
        :return:
        """

        self.display_signal = pyqtSignal({
            "type": "update_control_register",
            "register": self.name,
            "digit_1": value[0],
            "digit_2": value[1]
        })
        self.display_signal.emit()

    def blank(self):

        """ Blanks the whole control register.
        :return: None
        """

        self.display(["blank", "blank"])

    def start_blink(self):
        for digit in list(self.digits.values()):
            pass
            # TODO: emit signal

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
        # self.display_update_timer = wx.Timer(frame)
        # frame.Bind(wx.EVT_TIMER, self.display_update, self.display_update_timer)
        # self.comp_acty_timer = wx.Timer(frame)
        # frame.Bind(wx.EVT_TIMER, self.stop_comp_acty_flash, self.comp_acty_timer)
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
            "uplink_acty": Annunciator(name="uplink_acty"),
            "temp": Annunciator(name="temp"),
            "no_att": Annunciator(name="no_att"),
            "gimbal_lock": Annunciator(name="gimbal_lock"),
            "stby": Annunciator(name="stby"),
            "prog": Annunciator(name="prog"),
            "key_rel": Annunciator(name="key_rel"),
            "restart": Annunciator(name="restart"),
            "opr_err": Annunciator(name="opr_err"),
            "tracker": Annunciator(name="tracker"),
            "comp_acty": Annunciator(name="comp_acty"),
        }

        self.registers = {
            1: DataRegister(name="data_register_1"),
            2: DataRegister(name="data_register_2"),
            3: DataRegister(name="data_register_3"),
        }

        self.control_registers = {
            "program": ControlRegister("program"),
            "verb": ControlRegister("verb"),
            "noun": ControlRegister("noun"),
        }

        # self.keyboard = {
        #     "verb": KeyPress(),
        #     "noun": KeyPress(),
        #     "plus": KeyPress(),
        #     "minus": KeyPress(),
        #     0: KeyPress(),
        #     1: KeyPress(),
        #     2: KeyPress(),
        #     3: KeyPress(),
        #     4: KeyPress(),
        #     5: KeyPress(),
        #     6: KeyPress(),
        #     7: KeyPress(),
        #     8: KeyPress(),
        #     9: KeyPress(),
        #     "clear": KeyPress(),
        #     "proceed": KeyPress(),
        #     "key_release": KeyPress(),
        #     "enter": KeyPress(),
        #     "reset": KeyPress(),
        # }


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
        if not is_proceed_available:
            if isinstance(display_location, DataRegister):
                for register in list(self.registers.values()):
                    register.blank()
            else:
                display_location.blank()

    def verb_noun_flash_on(self):

        """ Starts the verb/noun flash.
        :return: None
        """

        self.control_registers["verb"].digits[1].start_blink()
        self.control_registers["verb"].digits[2].start_blink()
        self.control_registers["noun"].digits[1].start_blink()
        self.control_registers["noun"].digits[2].start_blink()

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
        for d in list(self.control_registers["verb"].digits.values()):
            d.stop_blink()
        for d in list(self.control_registers["noun"].digits.values()):
            d.stop_blink()

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

        if isinstance(self.display_location_to_load, DataRegister):
            self._handle_data_register_load(keypress)

        elif isinstance(self.display_location_to_load, ControlRegister):
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

            if isinstance(self.display_location_to_load, DataRegister):
                self.display_location_to_load.display(sign="", value=self.input_data_buffer)
            else:
                self.display_location_to_load.display(value=self.input_data_buffer)
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
            self.control_registers["verb"].digits[1].display(keypress)
            self.requested_verb = keypress
            self.verb_position = 1
        elif self.verb_position == 1:
            self.control_registers["verb"].digits[2].display(keypress)
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
            self.control_registers["noun"].digits[1].display(keypress)
            self.requested_noun = keypress
            self.noun_position = 1
        elif self.noun_position == 1:
            self.control_registers["noun"].digits[2].display(keypress)
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
        for annunciator in list(self.annunciators.values()):
            if annunciator.blink_timer.IsRunning():
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
