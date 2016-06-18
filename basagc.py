#!/usr/bin/env python3

import argparse
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from basagc import config  # need to import this first to set debug flag


# def tracefunc(frame, event, arg, indent=[0]):
#     if event == "call":
#         indent[0] += 2
#         print("-" * indent[0] + "> call function", frame.f_code.co_name)
#     elif event == "return":
#         print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
#         indent[0] -= 2
#     return tracefunc
#
#
# import sys
#
# sys.settrace(tracefunc)

if __name__ == "__main__":

    # arg parser for debug flag
    parser = argparse.ArgumentParser(description='basaGC: AGC for KSP')
    parser.add_argument('-d','--debug', help='Set debug mode on', required=False, action='store_true')
    args = parser.parse_args()
    if args.debug:
        config.DEBUG = True
        config.current_log_level = "DEBUG"
        print("================DEBUG MODE================")
        
    from basagc import vessel, gui  # import the rest
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    
    ui = gui.GUI(main_window)

    vessel = vessel.Vessel(ui)
    main_window.setWindowTitle('basaGC')
    main_window.show()

    sys.exit(app.exec_())

