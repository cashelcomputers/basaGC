#!/usr/bin/env python3
"""This file contains the implementation of the autopilot."""

from basagc import ksp

def disable_smartass():
    ksp.send_command("command=mj.smartassoff")

def set_throttle(percent):
    if percent == 0:
        throttle_magnitude = 0
    else:
        throttle_magnitude = percent / 100.0
    command_string = "command=" + commands["setThrottle"] + "[" + str(throttle_magnitude) + "]"
    send_command_to_ksp("command=)