#!/usr/bin/env python3
"""
This module contains code for the DSKY (the guidance computer/user interface). It should be considered to be the
interface between the computer and the gui toolkit.
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

from basagc import utils


class DSKY:
    """ This class models the DSKY.
    """
    
    dsky_instance = None
    
    def __init__(self, computer, ui):
    
        """ Class constructor.
        :type ui: object
        :param computer: the instance of the guidance computer
        :return: None
        """
        
        DSKY.dsky_instance = self
        self.computer = computer
        output_widgets = ui.get_output_widgets()
        self.annunciators = output_widgets[0]
        self._control_registers = output_widgets[1]
        self._data_registers = output_widgets[2]
        # self.keyboard = Keyboard(ui)
        
        self.registers = {
            "program": {
                "1": self._control_registers["program"].digits[0],
                "2": self._control_registers["program"].digits[1],
            },
            "verb": {
                "1": self._control_registers["verb"].digits[0],
                "2": self._control_registers["verb"].digits[1],
            },
            "noun": {
                "1": self._control_registers["noun"].digits[0],
                "2": self._control_registers["noun"].digits[1],
            },
            "data": {
                "1": {
                    "sign": self._data_registers[1].digits[0],
                    "1": self._data_registers[1].digits[1],
                    "2": self._data_registers[1].digits[2],
                    "3": self._data_registers[1].digits[3],
                    "4": self._data_registers[1].digits[4],
                    "5": self._data_registers[1].digits[5],
                },
                "2": {
                    "sign": self._data_registers[1].digits[0],
                    "1": self._data_registers[2].digits[1],
                    "2": self._data_registers[2].digits[2],
                    "3": self._data_registers[2].digits[3],
                    "4": self._data_registers[2].digits[4],
                    "5": self._data_registers[2].digits[5],
                },
                "3": {
                    "sign": self._data_registers[1].digits[0],
                    "1": self._data_registers[3].digits[1],
                    "2": self._data_registers[3].digits[2],
                    "3": self._data_registers[3].digits[3],
                    "4": self._data_registers[3].digits[4],
                    "5": self._data_registers[3].digits[5],
                },
            },
        }
    
    def blank_register(self, register):
        
        """blanks the register"""
        
        if register not in self.registers:
            utils.log("No such register: {}".format(register))
            return
        for digit in self.registers[register].values():
            print(digit)
            digit.display("b")
    
    def blink_register(self, register):
        
        """
        Blinks the named register.
        :param register: the name of the register to blink
        :return: None
        """
        
        # check if we are to blink a control register
        for digit in self.registers[register].digits:
            digit.blink_data[is_blinking_lit] = False
            digit.blink_data[is_blinking] = True
            digit.display("b")
            
            # bind andstart the timer
            digit.blink_timer.timeout.connect(self._blink_event)
            digit.blink_timer.start(500)
    
    def _blink_event(self):
        """alternates the digit between a value and blank ie to flash the digit."""
    
        # digit displaying the number, switch to blank
        if self.is_blinking_lit:
            self.display(10)
            self.is_blinking_lit = False
        else:
            # digit displaying blank, change to number
            self.display(self.last_value)
            self.is_blinking_lit = True

    def set_register(self, value, register, digit=None):
        
        # registers are verb, noun, program, data_1, data_2, data_3
        if register in ["verb", "noun", "program"]:
            if digit:
                self.registers[register][str(digit)].display(value)
                return
            for index in len(self.registers[register].values()):
                print(index, digit)
                digit.display(value[index - 1])
        elif register == "data_1":
            if digit:
                self.registers[register]["1"][str(digit)].display(value)
                return
            for index, digit in enumerate(self.registers["data"]["1"].values(), start=1):
                digit.display(value[index - 1])
        elif register == "data_2":
            if digit:
                self.registers[register]["2"][str(digit)].display(value)
                return
            for index, digit in enumerate(self.registers["data"]["2"].values(), start=1):
                digit.display(value[index - 1])
        elif register == "data_3":
            if digit:
                self.registers[register]["3"][str(digit)].display(value)
                return
            for index, digit in enumerate(self.registers["data"]["3"].values(), start=1):
                digit.display(value[index - 1])

    def set_annunciator(self, name, set_to=True):
        
        try:
            if set_to:
                self.annunciators[name].on()
            else:
                self.annunciators[name].off()
        except KeyError:
            utils.log("You tried to change a annunciator that doesnt exist :(", "WARNING")
            
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

        self.registers["verb"].start_blink()
        self.registers["noun"].start_blink()

    def verb_noun_flash_off(self):

        """ Starts the verb/noun flash.
        :return: None
        """

        for digit in list(self.control_registers["verb"].digits.values()):
            digit.stop_blink()
        for digit in list(self.control_registers["noun"].digits.values()):
            digit.stop_blink()

    def stop_blink(self):

        """ Stops the verb/noun flash
        :return: None
        """

        self.is_expecting_data = False
        for d in self.control_registers.values():
            d.stop_blink()
        # for d in self.control_registers["noun"]:
        #     d.stop_blink()

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

    def reset_annunciators(self):
        
        for annunciator in self.annunciators:
            self.annunciators[annunciator].off()

class Digit:
    
    def __init__(self, widget):
        
        self.widget = widget
        self.is_blinking_lit = True
        self.current_display = None
        self.value_to_blink = None
        self.blink_timer = QtCore.QTimer()
        self.blink_timer.timeout.connect(self.flip)
        self.setText("")
        self.display(10)
        self.last_value = None
        self.is_blinking = False
    
    def set_tooltip(self, tooltip):
        self.setToolTip(tooltip)
    
    def start_blink(self):
        
        """ Starts the digit blinking.
        :return: None
        """
        self.is_blinking_lit = False
        self.is_blinking = True
        self.display(10)
        self.blink_timer.start(500)
    
    def stop_blink(self):
        self.is_blinking = False
        self.blink_timer.stop()
    
    def flip(self):
        
        """alternates the digit between a value and blank ie to flash the digit."""
        
        # digit displaying the number, switch to blank
        if self.is_blinking_lit:
            self.display(10)
            self.is_blinking_lit = False
        else:
            # digit displaying blank, change to number
            self.display(self.last_value)
            self.is_blinking_lit = True
    
    def display(self, number_to_display):

        
        # if we are flashing, only need to change stored digit
        if self.is_blinking:
            if self.is_blinking_lit:
                self.last_value = number_to_display
        else:
            # stores the last value displayed, in case we need to flash
            self.last_value = self.current_display
            
            # store the value we shall be displaying
            self.current_display = number_to_display
        
        

