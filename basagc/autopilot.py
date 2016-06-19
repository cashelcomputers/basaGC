#!/usr/bin/env python3
"""This file contains the implementation of the autopilot."""

from basagc import utils
from basagc import config

#def disable_smartass():
    #ksp.send_command("command=mj.smartassoff")

#def set_throttle(percent):
    #if percent == 0:
        #throttle_magnitude = 0
    #else:
        #throttle_magnitude = percent / 100.0
    #command_string = "command=" + commands["setThrottle"] + "[" + str(throttle_magnitude) + "]"
    #send_command_to_ksp("command=)

class Autopilot:
    
    def __init__(self, vessel):
        self.mode = None
        self.mode_choices = ["sas", "auto", "off"]  # auto means craft under direct control of script
        self.is_enabled = True
        self.vessel = vessel
        self.send_command = vessel.krpc_connection.send_command

    def enable_autopilot(self, mode, direction=None):
        if mode not in self.mode_choices:
            utils.log('Selected autopilot mode "{}" not available.'.format(mode))
            return False
        self.mode = mode
        if mode == "sas":
            self.send_command("sas", True)
            if direction:
                # check that direction is valid
                if direction not in config.SAS_DIRECTIONS:
                    utils.log("Invalid selection for SAS mode: {}".format(direction))
                    return False
                self.send_command("sas_mode", direction)
        elif mode == "auto":
            # config krpc autopilot
            pass  # TODO: implement
        