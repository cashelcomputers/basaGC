#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" This module contains the wxPython GUI. """
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
#  by Ronald S. Burkey <info@sandroid.org>

import sys

import new_gui
from PyQt5 import QtWidgets
from computer import Computer



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = new_gui.Ui_MainWindow(MainWindow)
    computer = Computer(ui)
    new_gui.CHARIN = computer.dsky.charin
    MainWindow.show()

    sys.exit(app.exec_())

# class HelpFrame(wx.Frame):
#         def on_close(self, event):
#         """Event handler for close button
#             :param event: Event object as passed by wxPython
#             """
#         self.SetTitle("")
#         self.viewer.Clear()
#         self.Hide()


# class SettingsFrame(wx.Frame):
#     """This frame provides a settings dialog"""
#     def ok_button_event(self, event):
#         """ Event handler for OK button.
#         :param event: wxPython event (not used)
#         :return:
#         """
#
#         ip_address = self.ip_field.GetValue()
#         port = self.port_field.GetValue()
#         log_level = self.log_level_combobox.GetValue()
#         display_update_interval = self.display_update_field.GetValue()
#         config.IP = ip_address
#         config.PORT = port
#         config.current_log_level = log_level
#         config.URL = "http://" + config.IP + ":" + config.PORT + "/telemachus/datalink?"
#         config.DISPLAY_UPDATE_INTERVAL = int(display_update_interval)
#         self.Hide()
#
#     def cancel_button_event(self, event):
#         """ Event handler for Cancel button.
#         :param event: wxPython event (not used)
#         :return:
#         """
#
#         self.Hide()

    # @staticmethod
    # def start_verb_noun_flash():
    #
    #     """ Starts the verb/noun flash.
    #     :return: None
    #     """
    #
    #     GUI.dsky.control_registers["verb"].start_blink()
    #     GUI.dsky.control_registers["noun"].start_blink()
    #
    # @staticmethod
    # def stop_verb_noun_flash():
    #
    #     """ Stops the verb/noun flash.
    #     :return: None
    #     """
    #
    #     GUI.dsky.control_registers["verb"].stop_blink()
    #     GUI.dsky.control_registers["noun"].stop_blink()

# def on(self):
#
#     """ Turns the DSKY on.
#     :return: None
#     """
#
#     utils.log("DSKY on")
#     for item in GUI.dsky.static_display:
#         item.on()
#
# def off(self):
#
#     """ Turns the DSKY off.
#     :return: None
#     """
#
#     utils.log("DSKY off")
#     for item in GUI.dsky.static_display:
#         item.off()
#
# def settings_menuitem_click(self, event):
#
#     """ Event handler for Settings menu item.
#     :param event: wxPython event (not used)
#     :return: None
#     """
#
#     self.settings_dialog.log_level_combobox.SetSelection(config.LOG_LEVELS.index(config.current_log_level))
#     self.settings_dialog.Show()
#
# def show_log_menuitem_click(self, event):
#
#     """ Event handler for "Show Log" menu item.
#     :param event: wxPython event (not used)
#     :return: None
#     """
#
#     self.log_viewer.Show()
#
# def quit_menuitem_click(self, event):
#
#     """ Event handler for Quit menu item.
#     :param event: wxPython event (not used)
#     :return: None
#     """
#
#     GUI.computer.quit()
#
# def about_menuitem_click(self, event):
#
#     """ Event handler for Help/About menu item.
#     :param event: wxPython event (not used)
#     :return: None
#     """
#
#     about_dialog = wx.AboutDialogInfo()
#
#     about_dialog.SetIcon(wx.Icon(config.ICON, wx.BITMAP_TYPE_PNG))
#     about_dialog.SetName(config.PROGRAM_NAME)
#     about_dialog.SetVersion(config.VERSION)
#     about_dialog.SetDescription(config.PROGRAM_DESCRIPTION)
#     about_dialog.SetCopyright(config.COPYRIGHT)
#     about_dialog.SetWebSite(config.WEBSITE)
#     about_dialog.SetLicence(config.LICENCE)
#     about_dialog.AddDeveloper(config.DEVELOPERS)
#
#     wx.AboutBox(about_dialog)
#
# def verbs_menuitem_click(self, event):
#     self.help_viewer.SetTitle("Verbs Listing")
#     verbs_list = ""
#     for verb_number, verb in list(self.computer.verbs.items()):
#         if int(verb_number) < 39:
#             this_verb = verb(None)
#         else:
#             this_verb = verb()
#         verbs_list += "Verb " + verb_number + ":\t" + this_verb.name + "\n"
#         del this_verb
#     self.help_viewer.viewer.SetValue(verbs_list)
#     self.help_viewer.Show()
#
# def nouns_menuitem_click(self, event):
#     self.help_viewer.SetTitle("Nouns Listing")
#     nouns_list = ""
#     for noun_number, noun in list(self.computer.nouns.items()):
#         this_noun = noun()
#         nouns_list += "Noun " + noun_number + ":\t" + this_noun.description + "\n"
#     self.help_viewer.viewer.SetValue(nouns_list)
#     self.help_viewer.Show()
#
# def programs_menuitem_click(self, event):
#     self.help_viewer.SetTitle("Programs Listing")
#     programs_list = ""
#     for program_number, program in list(self.computer.programs.items()):
#         this_program = program()
#         programs_list += "Program " + program_number + ":\t" + this_program.description + "\n"
#     self.help_viewer.viewer.SetValue(programs_list)
#     self.help_viewer.Show()
#
# def alarm_codes_menuitem_click(self, event):
#     self.help_viewer.SetTitle("Alarm Codes")
#     alarm_codes_list = ""
#     for alarm_code, description in list(config.ALARM_CODES.items()):
#         alarm_codes_list += "0X" + str(alarm_code) + ":\t" + description + "\n"
#     self.help_viewer.viewer.SetValue(alarm_codes_list)
#     self.help_viewer.Show()
