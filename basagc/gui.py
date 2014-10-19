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
#  by Ronald S. Burkey <info@sandroid.org>

import logging

import wx

import computer as Computer
import config


logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d/%m/%y %H:%M',
    filename='gc.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class LogViewerFrame(wx.Frame):

    """This frame provides a log viewer"""

    def __init__(self, *args, **kwds):
        kwds["style"] = wx.CLOSE_BOX | wx.MINIMIZE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.viewer = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.close_button = wx.Button(self.panel_2, wx.ID_CLOSE, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.close_button_event, self.close_button)

    def __set_properties(self):
        self.SetTitle("Log Viewer")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(config.ICON, wx.BITMAP_TYPE_PNG))
        self.SetIcon(_icon)
        self.SetSize((720, 450))
        self.close_button.SetFocus()

    def __do_layout(self):
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_3 = wx.FlexGridSizer(2, 1, 5, 0)
        grid_sizer_3.Add(self.viewer, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
        grid_sizer_3.Add(self.close_button, 0, wx.ADJUST_MINSIZE, 0)
        self.panel_2.SetSizer(grid_sizer_3)
        grid_sizer_3.AddGrowableRow(0)
        grid_sizer_3.AddGrowableCol(0)
        sizer_16.Add(self.panel_2, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_16)
        self.Layout()

    def close_button_event(self, event):
        self.Hide()


class GUI(wx.Frame):

    """This class provides the main DSKY GUI"""

    computer = None
    dsky = None
    keyboard = None
    annunciators = None

    def __init__(self, *args, **kwds):

        kwds["style"] = wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        self.log_viewer = LogViewerFrame(self)

        GUI.computer = Computer.Computer(self)
        GUI.dsky = GUI.computer.dsky
        GUI.keyboard = GUI.computer.dsky.keyboard
        GUI.annunciators = GUI.computer.dsky.annunciators

        self.VerbButton = GUI.keyboard["verb"].widget
        self.NounButton = GUI.keyboard["noun"].widget
        self.PlusButton = GUI.keyboard["plus"].widget
        self.MinusButton = GUI.keyboard["minus"].widget
        self.ZeroButton = GUI.keyboard[0].widget
        self.SevenButton = GUI.keyboard[7].widget
        self.FourButton = GUI.keyboard[4].widget
        self.OneButton = GUI.keyboard[1].widget
        self.EightButton = GUI.keyboard[8].widget
        self.FiveButton = GUI.keyboard[5].widget
        self.TwoButton = GUI.keyboard[2].widget
        self.NineButton = GUI.keyboard[9].widget
        self.SixButton = GUI.keyboard[6].widget
        self.ThreeButton = GUI.keyboard[3].widget
        self.ClrButton = GUI.keyboard["clear"].widget
        self.ProButton = GUI.keyboard["proceed"].widget
        self.KeyRelButton = GUI.keyboard["key_release"].widget
        self.EntrButton = GUI.keyboard["enter"].widget
        self.RsetButton = GUI.keyboard["reset"].widget

        # Menu Bar
        self.menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.settings_menuitem = wx.MenuItem(self.file_menu, wx.ID_ANY, "Settings...", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.settings_menuitem)
        self.show_log_menuitem = wx.MenuItem(self.file_menu, wx.ID_ANY, "Show Log...", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.show_log_menuitem)
        self.quit_menuitem = wx.MenuItem(self.file_menu, wx.ID_ANY, "Quit", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.quit_menuitem)
        self.menubar.Append(self.file_menu, "File")
        self.help_menu = wx.Menu()
        self.about_menuitem = wx.MenuItem(self.help_menu, wx.ID_ANY, "About...", "", wx.ITEM_NORMAL)
        self.help_menu.AppendItem(self.about_menuitem)
        self.menubar.Append(self.help_menu, "Help")
        self.SetMenuBar(self.menubar)
        # Menu Bar end

        self.bitmap_5 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameVertical.jpg",
            wx.BITMAP_TYPE_ANY))
        self.bitmap_6_copy = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameHorizontal.jpg",
            wx.BITMAP_TYPE_ANY))
        self.bitmap_6 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameHorizontal.jpg",
            wx.BITMAP_TYPE_ANY))
        self.bitmap_5_copy = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameVertical.jpg",
            wx.BITMAP_TYPE_ANY))
        self.bitmap_5_copy_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameVertical.jpg",
            wx.BITMAP_TYPE_ANY))
        self.bitmap_6_copy_copy = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameHorizontal.jpg",
            wx.BITMAP_TYPE_ANY))
        self.bitmap_6_copy_copy_copy = wx.StaticBitmap(self, wx.ID_ANY,
            wx.Bitmap(config.IMAGES_DIR + "FrameHorizontal.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_5_copy_2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(config.IMAGES_DIR + "FrameVertical.jpg",
            wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, GUI.keyboard["verb"].press, id=config.ID_VERBBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["noun"].press, id=config.ID_NOUNBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["plus"].press, id=config.ID_PLUSBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["minus"].press, id=config.ID_MINUSBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[0].press, id=config.ID_ZEROBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[7].press, id=config.ID_SEVENBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[4].press, id=config.ID_FOURBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[1].press, id=config.ID_ONEBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[8].press, id=config.ID_EIGHTBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[5].press, id=config.ID_FIVEBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[2].press, id=config.ID_TWOBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[9].press, id=config.ID_NINEBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[6].press, id=config.ID_SIXBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard[3].press, id=config.ID_THREEBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["clear"].press, id=config.ID_CLRBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["proceed"].press, id=config.ID_PROBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["key_release"].press, id=config.ID_KEYRELBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["enter"].press, id=config.ID_ENTRBUTTON)
        self.Bind(wx.EVT_BUTTON, GUI.keyboard["reset"].press, id=config.ID_RSETBUTTON)

        # menu binds
        self.Bind(wx.EVT_MENU, self.settings_menuitem_click, self.settings_menuitem)
        self.Bind(wx.EVT_MENU, self.show_log_menuitem_click, self.show_log_menuitem)
        self.Bind(wx.EVT_MENU, self.quit_menuitem_click, self.quit_menuitem)
        self.Bind(wx.EVT_MENU, self.about_menuitem_click, self.about_menuitem)

    def __set_properties(self):

        self.SetTitle("basaGC")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(config.ICON, wx.BITMAP_TYPE_PNG))
        self.SetIcon(_icon)
        self.panel_1.SetBackgroundColour(wx.Colour(160, 160, 160))
        self.VerbButton.SetMinSize((75, 75))
        self.NounButton.SetMinSize((75, 75))
        self.PlusButton.SetMinSize((75, 75))
        self.MinusButton.SetMinSize((75, 75))
        self.ZeroButton.SetMinSize((75, 75))
        self.SevenButton.SetMinSize((75, 75))
        self.FourButton.SetMinSize((75, 75))
        self.OneButton.SetMinSize((75, 75))
        self.EightButton.SetMinSize((75, 75))
        self.FiveButton.SetMinSize((75, 75))
        self.TwoButton.SetMinSize((75, 75))
        self.NineButton.SetMinSize((75, 75))
        self.SixButton.SetMinSize((75, 75))
        self.ThreeButton.SetMinSize((75, 75))
        self.ClrButton.SetMinSize((75, 75))
        self.ProButton.SetMinSize((75, 75))
        self.KeyRelButton.SetMinSize((75, 75))
        self.EntrButton.SetMinSize((75, 75))
        self.RsetButton.SetMinSize((75, 75))

    def __do_layout(self):

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10_copy_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_11_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_11_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1_copy = wx.GridSizer(7, 2, 9, 10)
        sizer_1.Add((20, 15), 0, 0, 0)
        sizer_2.Add((20, 20), 2, wx.EXPAND, 0)
        sizer_12.Add(self.bitmap_5, 0, 0, 0)
        sizer_13.Add(self.bitmap_6_copy, 0, 0, 0)
        sizer_13.Add((20, 5), 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["uplink_acty"].widget, 0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["temp"].widget, 0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["no_att"].widget, 0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["gimbal_lock"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["stby"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["prog"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["key_rel"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["restart"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["opr_err"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["tracker"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["no_dap"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["alt"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["prio_disp"].widget, 0, 0, 0)
        grid_sizer_1_copy.Add(GUI.annunciators["vel"].widget, 0, 0, 0)
        sizer_13.Add(grid_sizer_1_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13.Add((20, 5), 0, 0, 0)
        sizer_13.Add(self.bitmap_6, 0, 0, 0)
        sizer_12.Add(sizer_13, 0, 0, 0)
        sizer_12.Add(self.bitmap_5_copy, 0, 0, 0)
        sizer_2.Add(sizer_12, 0, 0, 0)
        sizer_2.Add((20, 20), 3, wx.EXPAND, 0)
        sizer_14.Add(self.bitmap_5_copy_1, 0, 0, 0)
        sizer_15.Add(self.bitmap_6_copy_copy, 0, 0, 0)
        sizer_9.Add(GUI.annunciators["comp_acty"].widget, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_9.Add((20, 20), 1, 0, 0)
        sizer_10.Add(GUI.dsky.static_display[0].widget, 0, 0, 0)
        sizer_11.Add(GUI.dsky.control_registers["program"].digits[1].widget, 0, 0, 0)
        sizer_11.Add(GUI.dsky.control_registers["program"].digits[2].widget, 0, 0, 0)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_6.Add((20, 14), 0, 0, 0)
        sizer_10_copy.Add(GUI.dsky.static_display[1].widget, 0, 0, 0)
        sizer_11_copy.Add(GUI.dsky.control_registers["verb"].digits[1].widget, 0, 0, 0)
        sizer_11_copy.Add(GUI.dsky.control_registers["verb"].digits[2].widget, 0, 0, 0)
        sizer_10_copy.Add(sizer_11_copy, 0, wx.EXPAND, 0)
        sizer_8.Add(sizer_10_copy, 1, wx.EXPAND, 0)
        sizer_8.Add((20, 20), 1, 0, 0)
        sizer_10_copy_1.Add(GUI.dsky.static_display[2].widget, 0, 0, 0)
        sizer_11_copy_1.Add(GUI.dsky.control_registers["noun"].digits[1].widget, 0, 0, 0)
        sizer_11_copy_1.Add(GUI.dsky.control_registers["noun"].digits[2].widget, 0, 0, 0)
        sizer_10_copy_1.Add(sizer_11_copy_1, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_10_copy_1, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_6.Add(GUI.dsky.static_display[3].widget, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_7_copy_1.Add(GUI.dsky.registers[1].sign.widget, 0, 0, 0)
        sizer_7_copy_1.Add(GUI.dsky.registers[1].digits[0].widget, 0, 0, 0)
        sizer_7_copy_1.Add(GUI.dsky.registers[1].digits[1].widget, 0, 0, 0)
        sizer_7_copy_1.Add(GUI.dsky.registers[1].digits[2].widget, 0, 0, 0)
        sizer_7_copy_1.Add(GUI.dsky.registers[1].digits[3].widget, 0, 0, 0)
        sizer_7_copy_1.Add(GUI.dsky.registers[1].digits[4].widget, 0, 0, 0)
        sizer_6.Add(sizer_7_copy_1, 0, wx.EXPAND, 0)
        sizer_6.Add(GUI.dsky.static_display[4].widget, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_7_copy.Add(GUI.dsky.registers[2].sign.widget, 0, 0, 0)
        sizer_7_copy.Add(GUI.dsky.registers[2].digits[0].widget, 0, 0, 0)
        sizer_7_copy.Add(GUI.dsky.registers[2].digits[1].widget, 0, 0, 0)
        sizer_7_copy.Add(GUI.dsky.registers[2].digits[2].widget, 0, 0, 0)
        sizer_7_copy.Add(GUI.dsky.registers[2].digits[3].widget, 0, 0, 0)
        sizer_7_copy.Add(GUI.dsky.registers[2].digits[4].widget, 0, 0, 0)
        sizer_6.Add(sizer_7_copy, 0, wx.EXPAND, 0)
        sizer_6.Add(GUI.dsky.static_display[5].widget, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_7.Add(GUI.dsky.registers[3].sign.widget, 0, 0, 0)
        sizer_7.Add(GUI.dsky.registers[3].digits[0].widget, 0, 0, 0)
        sizer_7.Add(GUI.dsky.registers[3].digits[1].widget, 0, 0, 0)
        sizer_7.Add(GUI.dsky.registers[3].digits[2].widget, 0, 0, 0)
        sizer_7.Add(GUI.dsky.registers[3].digits[3].widget, 0, 0, 0)
        sizer_7.Add(GUI.dsky.registers[3].digits[4].widget, 0, 0, 0)
        sizer_6.Add(sizer_7, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_6)
        sizer_15.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_15.Add(self.bitmap_6_copy_copy_copy, 0, 0, 0)
        sizer_14.Add(sizer_15, 0, 0, 0)
        sizer_14.Add(self.bitmap_5_copy_2, 0, 0, 0)
        sizer_2.Add(sizer_14, 0, 0, 0)
        sizer_2.Add((20, 20), 2, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add((20, 15), 0, 0, 0)
        sizer_3.Add((8, 20), 0, 0, 0)
        sizer_4.Add((20, 20), 1, 0, 0)
        sizer_4.Add(self.VerbButton, 0, 0, 0)
        sizer_4.Add((20, 5), 0, 0, 0)
        sizer_4.Add(self.NounButton, 0, 0, 0)
        sizer_4.Add((20, 20), 1, 0, 0)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_3.Add((8, 20), 0, 0, 0)
        sizer_5.Add(self.PlusButton, 0, 0, 0)
        sizer_5.Add((20, 5), 0, 0, 0)
        sizer_5.Add(self.MinusButton, 0, 0, 0)
        sizer_5.Add((20, 5), 0, 0, 0)
        sizer_5.Add(self.ZeroButton, 0, 0, 0)
        sizer_3.Add(sizer_5, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_5_copy.Add(self.SevenButton, 0, 0, 0)
        sizer_5_copy.Add((20, 5), 0, 0, 0)
        sizer_5_copy.Add(self.FourButton, 0, 0, 0)
        sizer_5_copy.Add((20, 5), 0, 0, 0)
        sizer_5_copy.Add(self.OneButton, 0, 0, 0)
        sizer_3.Add(sizer_5_copy, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_5_copy_1.Add(self.EightButton, 0, 0, 0)
        sizer_5_copy_1.Add((20, 5), 0, 0, 0)
        sizer_5_copy_1.Add(self.FiveButton, 0, 0, 0)
        sizer_5_copy_1.Add((20, 5), 0, 0, 0)
        sizer_5_copy_1.Add(self.TwoButton, 0, 0, 0)
        sizer_3.Add(sizer_5_copy_1, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_5_copy_2.Add(self.NineButton, 0, 0, 0)
        sizer_5_copy_2.Add((20, 5), 0, 0, 0)
        sizer_5_copy_2.Add(self.SixButton, 0, 0, 0)
        sizer_5_copy_2.Add((20, 5), 0, 0, 0)
        sizer_5_copy_2.Add(self.ThreeButton, 0, 0, 0)
        sizer_3.Add(sizer_5_copy_2, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_5_copy_3.Add(self.ClrButton, 0, 0, 0)
        sizer_5_copy_3.Add((20, 5), 0, 0, 0)
        sizer_5_copy_3.Add(self.ProButton, 0, 0, 0)
        sizer_5_copy_3.Add((20, 5), 0, 0, 0)
        sizer_5_copy_3.Add(self.KeyRelButton, 0, 0, 0)
        sizer_3.Add(sizer_5_copy_3, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        self.panel_1.SetSizer(sizer_6)
        sizer_4_copy.Add((20, 20), 1, 0, 0)
        sizer_4_copy.Add(self.EntrButton, 0, 0, 0)
        sizer_4_copy.Add((20, 5), 0, 0, 0)
        sizer_4_copy.Add(self.RsetButton, 0, 0, 0)
        sizer_4_copy.Add((20, 20), 1, 0, 0)
        sizer_3.Add(sizer_4_copy, 0, wx.EXPAND, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_1.Add(sizer_3, 1, 0, 0)
        sizer_1.Add((20, 15), 0, 0, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def start_verb_noun_flash(self):
        GUI.dsky.control_registers["verb"].start_blink()
        GUI.dsky.control_registers["noun"].start_blink()

    def stop_verb_noun_flash(self):
        GUI.dsky.control_registers["verb"].stop_blink()
        GUI.dsky.control_registers["noun"].stop_blink()

    def on(self):
        print("DSKY on")
        for item in GUI.dsky.static_display:
            item.on()

    def off(self):
        print("DSKY off")
        for item in GUI.dsky.static_display:
            item.off()

    def settings_menuitem_click(self, event):
        print "Event handler 'settings_menuitem_click' not implemented!"
        event.Skip()

    def show_log_menuitem_click(self, event):
        self.log_viewer.Show()

    def quit_menuitem_click(self, event):
        GUI.computer.quit()

    def about_menuitem_click(self, event):

        about_dialog = wx.AboutDialogInfo()

        #about_dialog.SetIcon(wx.Icon(config.ICON, wx.BITMAP_TYPE_PNG))
        about_dialog.SetName(config.PROGRAM_NAME)
        about_dialog.SetVersion(config.VERSION)
        about_dialog.SetDescription(config.PROGRAM_DESCRIPTION)
        about_dialog.SetCopyright(config.COPYRIGHT)
        about_dialog.SetWebSite(config.WEBSITE)
        about_dialog.SetLicence(config.LICENCE)
        about_dialog.AddDeveloper(config.DEVELOPERS)

        wx.AboutBox(about_dialog)


class basaGCApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        dsky = GUI(None, wx.ID_ANY, "")
        self.SetTopWindow(dsky)
        dsky.Show()
        return 1

#if __name__ == "__main__":

    #pydsky = pyDSKYApp(0)
    #pydsky.MainLoop()
