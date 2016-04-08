#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""This module contains internal routines used by the guidance computer."""

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
#  Includes code and images from the Virtual AGC Project
#  (http://www.ibiblio.org/apollo/index.html) by Ronald S. Burkey
#  <info@sandroid.org>


def charin(keypress, state, dsky, computer):
    
    def handle_control_register_load():
        
        """ Handles control register loading
        :return: None
        """

        # we are expecting a numeric digit as input
        if keypress.isalpha():
            dsky.operator_error("Expecting numeric input")
            return
        # otherwise, add the input to buffer
        elif state["register_index"] == 0:
            state["display_location_to_load"].digits[1].display(keypress)
            state["register_index"] += 1
        elif state["register_index"] == 1:
            state["display_location_to_load"].digits[2].display(keypress)
            state["register_index"] = 0
            state["input_data_buffer"] += keypress
    
    def handle_data_register_load():
    
        """ Handles data register loading
        :return: None
        """
    
        if state["register_index"] == 0:
            if keypress == "+":
                state["display_location_to_load"].sign.plus()
            elif keypress == "-":
                state["display_location_to_load"].sign.minus()
            else:
                state["display_location_to_load"].digits[0].display(keypress)
                state["register_index"] += 1
        elif state["register_index"] >= 1 <= 5:
            state["display_location_to_load"].digits[state["register_index"]].display(keypress)
            if state["register_index"] >= 4:
                state["register_index"] = 0
            else:
                state["register_index"] += 1
        state["input_data_buffer"] += keypress

    def handle_expected_data():
    
        """ Handles expected data entry.
        :return: None
        """
    
        if keypress == "P":
            dsky.stop_blink()
            utils.log("Proceeding without input, calling {}(proceed)".format(state["object_requesting_data"]))
            state["object_requesting_data"]("proceed")
            state["input_data_buffer"] = ""
            return
    
        # if we receive ENTER, the load is complete and we will call the
        # program or verb requesting the data load
        elif keypress == "E":
            dsky.stop_blink()
            utils.log("Data load complete, calling {} ({})".format(
                state["object_requesting_data"],
                state["input_data_buffer"]
            ))
            state["object_requesting_data"](state["input_data_buffer)"])
            state["input_data_buffer"] = ""
            return
    
        if state["display_location_to_load"] in dsky.data_registers.items():
            handle_data_register_load()
    
        # if isinstance(state["display_location_to_load, DataRegister):
        #     state["handle_data_register_load(keypress)
    
        elif state["display_location_to_load"] in dsky.control_registers.items():
            handle_control_register_load()
    
        # if the user as entered anything other than a numeric d,
        # trigger a OPR ERR and recycle program
        elif keypress.isalpha():
            # if a program is running, recycle it
            # INSERT TRY HERE!!!
            # computer.get_state("running_program").terminate()
            # INSERT EXCEPT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if a verb is running, recycle it
            # computer.get_state("running_verb").terminate()
            dsky.operator_error("Expecting numeric input")
            return
        else:
            state["input_data_buffer"] += keypress
        
            if state["display_location_to_load"] in dsky.data_registers.items():
                state["display_location_to_load"].display(sign="", value=state["input_data_buffer"])
            else:
                state["display_location_to_load"].display(state["input_data_buffer"])
            # state["is_noun_being_loaded = True
            return

    def handle_verb_entry():
    
        """ Handles verb entry
        :return: None
        """
    
        if keypress == "C":  # user has pushed CLEAR
            state["verb_position"] = 0
            state["requested_verb"] = ""
            dsky.control_registers["verb"].digits[1].display("blank")
            dsky.control_registers["verb"].digits[2].display("blank")
            return
    
        if keypress == "N":  # user has finished entering verb
            state["is_verb_being_loaded"] = False
            state["is_noun_being_loaded"] = True
            state["verb_position"] = 0
        elif keypress == "E":
            state["is_verb_being_loaded"] = False
            state["verb_position"] = 0
        elif keypress.isalpha():
            dsky.operator_error("Expected a number for verb choice")
            return
        elif state["verb_position"] == 0:
            dsky.set_register(value=keypress, register="verb", digit=0)
            state["requested_verb"] = keypress
            state["verb_position"] = 1
        elif state["verb_position"] == 1:
            dsky.set_register(value=keypress, register="verb", digit=1)
            state["requested_verb"] += keypress
            state["verb_position"] = 2

    def handle_noun_entry():
    
        """ Handles noun entry.
        :return: None
        """
    
        if keypress == "C":  # user has pushed CLEAR
            state["noun_position"] = 0
            state["requested_noun"] = ""
            dsky.control_registers["noun"].digits[1].display("blank")
            dsky.control_registers["noun"].digits[2].display("blank")
            return
    
        if keypress == "N":  # user has finished entering noun
            state["is_noun_being_loaded"] = False
            state["is_verb_being_loaded"] = True
            state["noun_position"] = 0
        elif keypress == "E":
            state["is_noun_being_loaded"] = False
            state["noun_position"] = 0
        elif keypress.isalpha():
            dsky.operator_error("Expected a number for noun choice")
            return
        elif state["noun_position"] == 0:
            dsky.control_registers["noun"].digits[0].display(keypress)
            state["requested_noun"] = keypress
            state["noun_position"] = 1
        elif state["noun_position"] == 1:
            dsky.control_registers["noun"].digits[1].display(keypress)
            state["requested_noun"] += keypress
            state["noun_position"] = 2

    def handle_entr_keypress():
    
        """ Handles ENTR keypress
        :return: None
        """
    
        computer.execute_verb()

    def handle_reset_keypress():
    
        """ Handles RSET keypress
        :return: None
        """
    
        computer.reset_alarm_codes()
        dsky.reset_annunciators()

    def handle_noun_keypress():
    
        """ Handles NOUN keypress
        :return: None
        """
    
        state["is_verb_being_loaded"] = False
        state["is_noun_being_loaded"] = True
        state["requested_noun"] = ""
        state["control_registers"]["noun"].blank()

    def handle_verb_keypress():
    
        """ Handles VERB keypress
        :return: None
        """
    
        state["is_noun_being_loaded"] = False
        state["is_verb_being_loaded"] = True
        state["requested_verb"] = ""
        dsky.blank_register("verb")

    def handle_key_release_keypress():
    
        """ Handles KEY REL keypress
        :return: None
        """
        if state["backgrounded_update"]:
            if state["display_lock"]:
                state["display_lock"].terminate()
            dsky.annunciators["key_rel"].stop_blink()
            state["backgrounded_update"].resume()
            state["backgrounded_update"] = None
            state["is_verb_being_loaded"] = False
            state["is_noun_being_loaded"] = False
            state["is_data_being_loaded"] = False
            state["verb_position"] = 0
            state["noun_position"] = 0
            state["requested_verb"] = 0
            state["requested_noun"] = 0
            return
    
        # if the computer is off, we only want to accept the PRO key input,
        # all other keys are ignored
        if computer.is_powered_on is False:
            if keypress == "P":
                computer.on()
            else:
                utils.log("Key {} ignored because gc is off".format(keypress))


    
    if state["is_expecting_data"]:
        handle_expected_data()
        return
    
    if keypress == "R":
        handle_reset_keypress()
        return
    
    if keypress == "K":
        handle_key_release_keypress()
        return
    
    if state["display_lock"]:
        state["display_lock"].background()
    
    if state["is_verb_being_loaded"]:
        handle_verb_entry()
    
    elif state["is_noun_being_loaded"]:
        handle_noun_entry()
    
    if keypress == "E":
        handle_entr_keypress()
    
    if keypress == "V":
        handle_verb_keypress()
    
    if keypress == "N":
        handle_noun_keypress()
    
    if keypress == "C":
        pass  # TODO

