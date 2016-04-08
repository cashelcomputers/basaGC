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

from basagc import utils, verbs, routines


class DSKY:
    """ This class models the DSKY.
    """

    def __init__(self, computer, ui):
    
        """ Class constructor.
        :type ui: object
        :param computer: the instance of the guidance computer
        :return: None
        """

        self.computer = computer
        output_widgets = ui.get_output_widgets()
        self.annunciators = output_widgets[0]
        self.control_registers = output_widgets[1]
        self.data_registers = output_widgets[2]
        self.keyboard = Keyboard(ui)

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

        self.control_registers["verb"].start_blink()
        self.control_registers["noun"].start_blink()

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
