#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from basagc import gui, computer

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    
    ui = gui.GUI(main_window)
    computer = computer.Computer(ui)
    main_window.setWindowTitle('basaGC');
    main_window.show()

    sys.exit(app.exec_())

