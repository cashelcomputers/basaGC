#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from basagc import gui, computer

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    
    ui = gui.GUI(MainWindow)
    computer = computer.Computer(ui)
    # gui.CHARIN = computer.dsky.charin
    MainWindow.show()
    
    sys.exit(app.exec_())
