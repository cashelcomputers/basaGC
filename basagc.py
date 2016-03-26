#!/usr/bin/env python3
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
#  by Ronald S. Burkey <info@sandroid.org> (thanks Ronald!)

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from basagc import gui, computer

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    
    ui = gui.GUI(MainWindow)
    computer = computer.Computer(ui)
    ui.CHARIN = computer.dsky.charin
    MainWindow.show()
    
    sys.exit(app.exec_())
