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
#  Includes code and images from the Virtual AGC Project (http://www.ibiblio.org/apollo/index.html)
#  by Ronald S. Burkey <info@sandroid.org>import wx
import logging

import wx

import config
import verbs


dsky_log = logging.getLogger("DSKY")
debug_computer = None

class DSKY(object):

    def __init__(self, gui, computer):

        """The constructor for the DSKY object."""

        self.computer = computer

        global frame
        frame = gui

        #self.display_update_timer = wx.Timer(frame)
        #frame.Bind(wx.EVT_TIMER, self.display_update, self.display_update_timer)
        self.comp_acty_timer = wx.Timer(frame)
        frame.Bind(wx.EVT_TIMER, self.stop_comp_acty_flash, self.comp_acty_timer)
        self.input_data_buffer = ""
        self.register_index = 0

        self._init_state()

        self.static_display = [

            DSKY.Annunciator(self, image_on="rProgOn.jpg", image_off="rProgOff.jpg", panel=frame.panel_1),
            DSKY.Annunciator(self, image_on="VerbOn.jpg", image_off="VerbOff.jpg", panel=frame.panel_1),
            DSKY.Annunciator(self, image_on="NounOn.jpg", image_off="NounOff.jpg", panel=frame.panel_1),
            DSKY.Seperator(frame.panel_1),
            DSKY.Seperator(frame.panel_1),
            DSKY.Seperator(frame.panel_1),
        ]
        self.annunciators = {
            "uplink_acty":  DSKY.Annunciator(self, name="uplink_acty", image_on="UplinkActyOn.jpg", image_off="UplinkActyOff.jpg"),
            "temp":         DSKY.Annunciator(self, name="temp", image_on="TempOn.jpg", image_off="TempOff.jpg"),
            "no_att":       DSKY.Annunciator(self, name="no_att", image_on="NoAttOn.jpg", image_off="NoAttOff.jpg"),
            "gimbal_lock":  DSKY.Annunciator(self, name="gimbal_lock", image_on="GimbalLockOn.jpg", image_off="GimbalLockOff.jpg"),
            "stby":         DSKY.Annunciator(self, name="stby", image_on="StbyOn.jpg", image_off="StbyOff.jpg"),
            "prog":         DSKY.Annunciator(self, name="prog", image_on="ProgOn.jpg", image_off="ProgOff.jpg"),
            "key_rel":      DSKY.Annunciator(self, name="key_rel", image_on="KeyRelOn.jpg", image_off="KeyRelOff.jpg"),
            "restart":      DSKY.Annunciator(self, name="restart", image_on="RestartOn.jpg", image_off="RestartOff.jpg"),
            "opr_err":      DSKY.Annunciator(self, name="opr_err", image_on="OprErrOn.jpg", image_off="OprErrOff.jpg"),
            "tracker":      DSKY.Annunciator(self, name="tracker", image_on="TrackerOn.jpg", image_off="TrackerOff.jpg"),
            "no_dap":       DSKY.Annunciator(self, name="no_dap", image_on="BlankOff.jpg", image_off="BlankOff.jpg"),
            "alt":          DSKY.Annunciator(self, name="alt", image_on="BlankOff.jpg", image_off="BlankOff.jpg"),
            "prio_disp":    DSKY.Annunciator(self, name="prio_disp", image_on="BlankOff.jpg", image_off="BlankOff.jpg"),
            "vel":          DSKY.Annunciator(self, name="vel", image_on="BlankOff.jpg", image_off="BlankOff.jpg"),
            "comp_acty":    DSKY.Annunciator(self, name="comp_acty", image_on="CompActyOn.jpg", image_off="CompActyOff.jpg", panel=frame.panel_1),
        }
        self.registers = {
            1: DSKY.DataRegister(self),
            2: DSKY.DataRegister(self),
            3: DSKY.DataRegister(self),
        }
        self.control_registers = {
            "program": DSKY.ControlRegister(self, "program", "rProgOn.jpg", "rProgOff.jpg"),
            "verb": DSKY.ControlRegister(self, "verb", "VerbOn.jpg", "VerbOff.jpg"),
            "noun": DSKY.ControlRegister(self, "noun", "NounOn.jpg", "NounOff.jpg"),
        }
        self.keyboard = {
            "verb": DSKY.KeyButton(config.ID_VERBBUTTON, "VerbUp.jpg", self),
            "noun": DSKY.KeyButton(config.ID_NOUNBUTTON, "NounUp.jpg", self),
            "plus": DSKY.KeyButton(config.ID_PLUSBUTTON, "PlusUp.jpg", self),
            "minus": DSKY.KeyButton(config.ID_MINUSBUTTON, "MinusUp.jpg", self),
            0: DSKY.KeyButton(config.ID_ZEROBUTTON, "0Up.jpg", self),
            1: DSKY.KeyButton(config.ID_ONEBUTTON, "1Up.jpg", self),
            2: DSKY.KeyButton(config.ID_TWOBUTTON, "2Up.jpg", self),
            3: DSKY.KeyButton(config.ID_THREEBUTTON, "3Up.jpg", self),
            4: DSKY.KeyButton(config.ID_FOURBUTTON, "4Up.jpg", self),
            5: DSKY.KeyButton(config.ID_FIVEBUTTON, "5Up.jpg", self),
            6: DSKY.KeyButton(config.ID_SIXBUTTON, "6Up.jpg", self),
            7: DSKY.KeyButton(config.ID_SEVENBUTTON, "7Up.jpg", self),
            8: DSKY.KeyButton(config.ID_EIGHTBUTTON, "8Up.jpg", self),
            9: DSKY.KeyButton(config.ID_NINEBUTTON, "9Up.jpg", self),
            "clear": DSKY.KeyButton(config.ID_CLRBUTTON, "ClrUp.jpg", self),
            "proceed": DSKY.KeyButton(config.ID_PROBUTTON, "ProUp.jpg", self),
            "key_release": DSKY.KeyButton(config.ID_KEYRELBUTTON, "KeyRelUp.jpg", self),
            "enter": DSKY.KeyButton(config.ID_ENTRBUTTON, "EntrUp.jpg", self),
            "reset": DSKY.KeyButton(config.ID_RSETBUTTON, "RsetUp.jpg", self),
        }
    def operator_error(self, message=None):

        """Called when the astronaut has entered invalid keyboard input."""
        if message:
            print("OPERATOR ERROR: " + message)
        self.annunciators["opr_err"].blink_timer.Start(500)

    def _init_state(self):
        self.state = {
            "is_verb_being_loaded": False,
            "is_noun_being_loaded": False,
            "is_data_being_loaded": False,
            "register_focus": None,
            "verb_position": 0,
            "noun_position": 0,
            "requested_verb": 0,
            "requested_noun": 0,
            "current_verb": 0,
            "current_noun": 0,
            "current_program": 0,
            "display_lock": None,
            "backgrounded_update": None,
            "is_display_released": True,
            "is_expecting_data": False,
            "object_requesting_data": None,
            "display_location_to_load": None,
            "data_load_index": None,
        }

    def stop_comp_acty_flash(self, event):
        self.annunciators["comp_acty"].off()

    def request_data(self, requesting_object, location):
        print("{} requesting data".format(requesting_object))
        self.verb_noun_flash_on()
        self.state["object_requesting_data"] = requesting_object
        self.state["is_expecting_data"] = True
        self.state["display_location_to_load"] = location
        if isinstance(location, DSKY.DataRegister):
            for register in self.registers.itervalues():
                register.blank()
        else:
            location.blank()

    def verb_noun_flash_on(self):

        self.control_registers["verb"].digits[1].start_blink()
        self.control_registers["verb"].digits[2].start_blink()
        self.control_registers["noun"].digits[1].start_blink()
        self.control_registers["noun"].digits[2].start_blink()
        #for digit in self.control_registers["verb"].digits.itervalues():
            ##digit.blink_value = digit.value
            #digit.start_blink(digit.value)
        #for digit in self.control_registers["noun"].digits.itervalues():
            ##digit.blink_value = digit.value
            #digit.start_blink(digit.value)

    def verb_noun_flash_off(self):
        for digit in self.control_registers["verb"].digits.itervalues():
            digit.stop_blink()
        for digit in self.control_registers["noun"].digits.itervalues():
            digit.stop_blink()

    class Digit(object):

        def __init__(self, dsky):

            self.dsky = dsky
            global frame
            self.state = None

        #def blank(self):
            #self.widget.SetBitmap(self.blank)
            #pass



    class Seperator(object):
        def __init__(self, panel):
            self.image_on = wx.Image(config.IMAGES_DIR + "SeparatorOn.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_off = wx.Image(config.IMAGES_DIR + "Separator.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.widget = wx.StaticBitmap(panel, wx.ID_ANY, self.image_off)

        def on(self):
            self.widget.SetBitmap(self.image_on)
            self.state = True

        def off(self):
            self.widget.SetBitmap(self.image_off)
            self.state = False

    class NumericDigit(Digit):

        def __init__(self, dsky, panel=None):
            self.dsky = dsky
            super(DSKY.NumericDigit, self).__init__(self.dsky)
            self.digit_0 = wx.Image(config.IMAGES_DIR + "7Seg-0.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_1 = wx.Image(config.IMAGES_DIR + "7Seg-1.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_2 = wx.Image(config.IMAGES_DIR + "7Seg-2.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_3 = wx.Image(config.IMAGES_DIR + "7Seg-3.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_4 = wx.Image(config.IMAGES_DIR + "7Seg-4.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_5 = wx.Image(config.IMAGES_DIR + "7Seg-5.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_6 = wx.Image(config.IMAGES_DIR + "7Seg-6.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_7 = wx.Image(config.IMAGES_DIR + "7Seg-7.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_8 = wx.Image(config.IMAGES_DIR + "7Seg-8.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.digit_9 = wx.Image(config.IMAGES_DIR + "7Seg-9.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.blank_digit = wx.Image(config.IMAGES_DIR + "7SegOff.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.current_value = None
            self.is_blinking = False
            self.is_blinking_lit = True
            self.blink_value = None
            self.last_value = None


            # setup blink timers
            self.blink_timer = wx.Timer(frame)
            frame.Bind(wx.EVT_TIMER, self._blink, self.blink_timer)

            if panel:
                self.widget = wx.StaticBitmap(panel, wx.ID_ANY, self.blank_digit)
            else:
                self.widget = wx.StaticBitmap(frame, wx.ID_ANY, self.blank_digit)
            self.current_value = "blank"

        def set_tooltip(self, tooltip):
            self.widget.SetToolTipString(tooltip)

        def start_blink(self, value=None):
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
            self.blink_timer.Stop()
            self.display(self.blink_value)
            self.blink_value = None

        def blank(self):
            self.last_value = self.current_value
            self.display("blank")

        def display(self, new_value):
            if new_value == 0:
                self.widget.SetBitmap(self.digit_0)
            elif new_value == 1:
                self.widget.SetBitmap(self.digit_1)
            elif new_value == 2:
                self.widget.SetBitmap(self.digit_2)
            elif new_value == 3:
                self.widget.SetBitmap(self.digit_3)
            elif new_value == 4:
                self.widget.SetBitmap(self.digit_4)
            elif new_value == 5:
                self.widget.SetBitmap(self.digit_5)
            elif new_value == 6:
                self.widget.SetBitmap(self.digit_6)
            elif new_value == 7:
                self.widget.SetBitmap(self.digit_7)
            elif new_value == 8:
                self.widget.SetBitmap(self.digit_8)
            elif new_value == 9:
                self.widget.SetBitmap(self.digit_9)
            elif new_value == "blank":
                self.widget.SetBitmap(self.blank_digit)
            self.current_value = new_value
            if self.is_blinking:
                if new_value != "blank":
                    self.blink_value = new_value

            #if new_value == 0:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap, self.digit_0)
            #elif new_value == 1:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_1))
            #elif new_value == 2:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_2))
            #elif new_value == 3:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_3))
            #elif new_value == 4:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_4))
            #elif new_value == 5:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_5))
            #elif new_value == 6:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_6))
            #elif new_value == 7:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_7))
            #elif new_value == 8:
                #self.dsky.display_update_queue.appendleft((self.widget.SetBitmap, self.digit_8))
            #elif new_value == 9:
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.digit_9))
            #elif new_value == "blank":
                #self.dsky.display_update_queue.appendleft(self.widget.SetBitmap(self.blank))


    class SignDigit(Digit):

        def __init__(self, dsky, panel=None):
            self.dsky = dsky
            #super(DSKY.SignDigit, self).__init__(self.dsky)
            self.image_plus = wx.Image(config.IMAGES_DIR + "PlusOn.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_minus = wx.Image(config.IMAGES_DIR + "MinusOn.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.blank = wx.Image(config.IMAGES_DIR + "PlusMinusOff.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            if panel:
                self.widget = wx.StaticBitmap(panel, wx.ID_ANY, self.blank)
            else:
                self.widget = wx.StaticBitmap(frame, wx.ID_ANY, self.blank)

        def set_tooltip(self, tooltip):
            self.widget.SetToolTipString(tooltip)

        def display(self, value):
            if value == "blank":
                self.widget.SetBitmap(self.blank)

        def plus(self):
            self.widget.SetBitmap(self.image_plus)

        def minus(self):
            self.widget.SetBitmap(self.image_minus)

        def blank(self):
            self.widget.SetBitmap(self.blank)

    class Annunciator(object):
        def __init__(self, dsky, image_on, image_off, image_orange=None, panel=None, name=None):

            self.dsky = dsky
            self.name = name
            self.image_on = wx.Image(config.IMAGES_DIR + image_on, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.image_off = wx.Image(config.IMAGES_DIR + image_off, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            if image_orange:
                self.image_orange = wx.Image(config.IMAGES_DIR + image_orange, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.is_lit = False
            self.requested_state = False
            #self.old_state = None

            # setup blink timer
            self.blink_timer = wx.Timer(frame)
            frame.Bind(wx.EVT_TIMER, self.blink, self.blink_timer)

            if panel:
                self.widget = wx.StaticBitmap(panel, wx.ID_ANY, self.image_off)
            else:
                self.widget = wx.StaticBitmap(frame, wx.ID_ANY, self.image_off)

        def start_blink(self, interval=500):
            self.blink_timer.Start(interval)

        def stop_blink(self):
            self.blink_timer.Stop()

        def blink(self, event):
            """ Blinks indicator """

            if self.is_lit:
                self.off()
            else:
                self.on()

        def on(self):
            self.widget.SetBitmap(self.image_on)
            self.is_lit = True

        def off(self):
            self.widget.SetBitmap(self.image_off)
            self.is_lit = False

        #def _on(self):
            #self.widget.SetBitmap(self.image_on)
            #self.is_lit = True

        #def _off(self):
            #self.widget.SetBitmap(self.image_off)
            #self.is_lit = False

    class DataRegister(object):
        def __init__(self, dsky):
            self.dsky = dsky
            self.sign = DSKY.SignDigit(dsky, panel=frame.panel_1)
            self.digits = [
                DSKY.NumericDigit(dsky, panel=frame.panel_1),
                DSKY.NumericDigit(dsky, panel=frame.panel_1),
                DSKY.NumericDigit(dsky, panel=frame.panel_1),
                DSKY.NumericDigit(dsky, panel=frame.panel_1),
                DSKY.NumericDigit(dsky, panel=frame.panel_1),
            ]

        def display(self, value, sign=""):
            if sign == "-":
                self.sign.minus()
            elif sign == "+":
                self.sign.plus()
            elif sign == "":
                self.sign.widget.SetBitmap(self.sign.blank)
            for index, digit in enumerate(value):
                self.digits[index].display(int(digit))

        def blank(self):
            self.sign.display("blank")
            for digit in self.digits:
                digit.display("blank")

        def set_tooltip(self, tooltip):
            for digit in self.digits:
                digit.widget.SetToolTipString(tooltip)

    class ControlRegister(object):
        def __init__(self, dsky, name, image_on, image_off):
            self.dsky = dsky
            self.name = name
            self.image_on = image_on
            self.image_off = image_off
            self.digits = {
                1: DSKY.NumericDigit(dsky, panel=frame.panel_1),
                2: DSKY.NumericDigit(dsky, panel=frame.panel_1),
            }

        def display(self, value):

            if len(value) == 1:
                self.digits[1].display(int(value))
            else:
                self.digits[1].display(int(value[0]))
                self.digits[2].display(int(value[1]))

            #for index, digit in enumerate(self.digits, start=1):
                #try:
                    #self.digits[index].display(int(value[index]))
                #except IndexError:
                    #print(value, index)
                    #print("Too many values to display, silently ignoring further data")

        def blank(self):
            for digit in self.digits.itervalues():
                digit.display("blank")

    class KeyButton(object):

        def __init__(self, wxid, image, dsky):
            self.dsky = dsky
            self.image = wx.Bitmap(config.IMAGES_DIR + image, wx.BITMAP_TYPE_ANY)
            self.widget = wx.BitmapButton(frame, wxid, self.image)

        def press(self, event):

            """Called when a keypress event has been received.
            :param event: wx event
            """
            keypress = event.GetId()

            # set up the correct key codes for non-numeric keys
            if keypress in config.KEY_IDS:
                keypress = config.KEY_IDS[keypress]

            # call the actual handler
            self.dsky.charin(keypress)
            return

    def charin(self, keypress):
        """
        Handles key input from DSKY keyboard.
        :param keypress: holds the key code
        """

        def stop_blink():
            self.state['is_expecting_data'] = False
            for d in self.control_registers["verb"].digits.itervalues():
                d.stop_blink()
            for d in self.control_registers["noun"].digits.itervalues():
                d.stop_blink()

        def handle_data_register_load():
            if self.register_index == 0:
                if keypress == "+":
                    self.state["display_location_to_load"].sign.plus()
                elif keypress == "-":
                    self.state["display_location_to_load"].sign.minus()
                else:
                    self.state["display_location_to_load"].digits[0].display(keypress)
                    self.register_index += 1
            elif self.register_index >= 1 <= 5:
                self.state["display_location_to_load"].digits[self.register_index].display(keypress)
                if self.register_index >= 4:
                    self.register_index = 0
                else:
                    self.register_index += 1
            self.input_data_buffer += str(keypress)


        def handle_control_register_load():
            # we are expecting a numeric digit as input
            if keypress > 9:
                self.operator_error("Expecting numeric input")
                return
            # otherwise, add the input to buffer
            elif self.register_index == 0:
                self.state["display_location_to_load"].digits[1].display(keypress)
                self.register_index += 1
            elif self.register_index == 1:
                self.state["display_location_to_load"].digits[2].display(keypress)
                self.register_index = 0
            self.input_data_buffer += str(keypress)

        def handle_expected_data():

            if keypress == "P":
                stop_blink()
                print("Proceeding without input, calling {}(proceed)".format(
                    self.state["object_requesting_data"]))
                self.state["object_requesting_data"]("proceed")
                self.input_data_buffer = ""
                return

            # if we receive ENTER, the load is complete and we will call the
            # program or verb requesting the data load
            elif keypress == "E":
                stop_blink()
                print("Data load complete, calling {}({})".format(
                    self.state["object_requesting_data"],
                    self.input_data_buffer))
                self.state["object_requesting_data"](self.input_data_buffer)
                self.input_data_buffer = ""
                return

            if isinstance(self.state["display_location_to_load"], DSKY.DataRegister):
                handle_data_register_load()

            elif isinstance(self.state["display_location_to_load"], DSKY.ControlRegister):
                handle_control_register_load()

            # if the user as entered anything other than a numeric d,
            # trigger a OPR ERR and recycle program
            elif keypress > 9:
                # if a program is running, recycle it
                # INSERT TRY HERE!!!
                #computer.get_state("running_program").terminate()
                # INSERT EXCEPT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # if a verb is running, recycle it
                #computer.get_state("running_verb").terminate()
                self.operator_error("Expecting numeric input")
                return
            else:

                self.input_data_buffer += str(keypress)

                if isinstance(self.state["display_location_to_load"],
                              DSKY.DataRegister):
                    self.state["display_location_to_load"].display(
                        sign="", value=self.input_data_buffer)
                else:
                    self.state["display_location_to_load"].display(
                        value=self.input_data_buffer)
                #self.state["is_noun_being_loaded"] = True
                return

        def handle_verb_entry():

            if keypress == "C": # user has pushed CLEAR
                self.state["verb_position"] = 0
                self.state["requested_verb"] = 0
                self.control_registers["verb"].digits[1].display("blank")
                self.control_registers["verb"].digits[2].display("blank")
                return

            if keypress == "N":  # user has finished entering verb
                self.state["is_verb_being_loaded"] = False
                self.state["is_noun_being_loaded"] = True
            elif keypress == "E":
                self.state["is_verb_being_loaded"] = False
            elif keypress >= 10:
                self.operator_error("Expected a number for verb choice")
                return
            elif self.state["verb_position"] == 0:
                self.control_registers["verb"].digits[1].display(keypress)
                self.state["requested_verb"] = keypress * 10
                self.state["verb_position"] = 1
            elif self.state["verb_position"] == 1:
                self.control_registers["verb"].digits[2].display(keypress)
                self.state["requested_verb"] += keypress
                self.state["verb_position"] = 0

        def handle_noun_entry():

            if keypress == "C":  # user has pushed CLEAR
                self.state["noun_position"] = 0
                self.state["requested_noun"] = 0
                self.control_registers["noun"].digits[1].display("blank")
                self.control_registers["noun"].digits[2].display("blank")
                return

            if keypress == "V" or keypress == "E":
                self.state["is_noun_being_loaded"] = False
            elif keypress >= 10:
                self.operator_error("Expected a number for noun choice")
                return
            elif self.state["noun_position"] == 0:
                self.control_registers["noun"].digits[1].display(keypress)
                self.state["requested_noun"] = keypress * 10
                self.state["noun_position"] = 1
            elif self.state["noun_position"] == 1:
                self.control_registers["noun"].digits[2].display(keypress)
                self.state["requested_noun"] += keypress
                self.state["noun_position"] = 0

        def handle_entr_keypress():
            self.state["is_verb_being_loaded"] = False
            self.state["is_noun_being_loaded"] = False
            if self.state["requested_verb"] in verbs.INVALID_VERBS:
                self.operator_error(
                    "Verb {} does not exist, please try a different verb".format(
                        self.state["requested_verb"]))
                return
            try:
                self.computer.verbs[int(self.state["requested_verb"])].execute()
            except NotImplementedError:
                self.operator_error(
                    "Verb {} is not implemented yet. Sorry about that...".format(
                        self.state["requested_verb"]))
            except verbs.NounNotAcceptableError:
                self.operator_error(
                    "Noun {} can't be used with verb {}".format(
                        self.state["requested_noun"],
                        self.state["requested_verb"]))
            # except IndexError:
            # print(type(self.state["requested_verb"]))
            #     print("Verb {} not in verb list".format(self.state["requested_verb"]))
            #     self.operator_error("Requested verb {} does not exist in list of verbs :(".format(self.state["requested_verb"]))
            return

        def handle_reset_keypress():
            self.computer.reset_alarm_codes()
            for annunciator in self.annunciators.itervalues():
                if annunciator.blink_timer.IsRunning():
                    annunciator.stop_blink()
                annunciator.off()

        def handle_noun_keypress():
            self.state["is_verb_being_loaded"] = False
            self.state["is_noun_being_loaded"] = True
            self.state["requested_noun"] = 0
            self.control_registers["noun"].blank()

        def handle_verb_keypress():
            self.state["is_noun_being_loaded"] = False
            self.state["is_verb_being_loaded"] = True
            self.state["requested_verb"] = 0
            self.control_registers["verb"].blank()

        def handle_key_release_keypress():
            if self.state["backgrounded_update"] is not None:
                self.annunciators["key_rel"].off()
                self.state["backgrounded_update"].resume()

        # if the computer is off, we only want to accept the PRO key input,
        # all other keys are ignored
        if self.computer.is_powered_on is False:
            if keypress == "P":
                self.computer.on()
            else:
                print("Key {} ignored because gc is off".format(keypress))
            return

        if keypress == "R":
            handle_reset_keypress()
        elif self.state["is_expecting_data"]:
            handle_expected_data()
        elif keypress == "E":
            handle_entr_keypress()
        elif keypress == "V":
            handle_verb_keypress()
        elif keypress == "N":
            handle_noun_keypress()
        elif self.state["is_verb_being_loaded"]:
            handle_verb_entry()
        elif self.state["is_noun_being_loaded"]:
            handle_noun_entry()
        elif keypress == "K":
            handle_key_release_keypress()
        elif keypress == "C":
            pass  # TODO


        # # if a verb has the display lock, background it
        # if self.state["display_lock"] is not None:
        #     self.state["display_lock"].background()
    def flash_comp_acty(self):
        self.annunciators["comp_acty"].on()
        self.comp_acty_timer.Start(config.COMP_ACTY_FLASH_DURATION, oneShot=True)

    def set_noun(self, noun):
        self.state["requested_noun"] = noun
        self.control_registers["noun"].display(str(noun))
