#!/usr/bin/env python3

""" This file contains class definition of a vessel."""

from basagc import autopilot
from basagc import computer
from basagc import imu
from basagc import ksp
from basagc import programs


class Vessel:

    def __init__(self, ui):

        # vessel parameters
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.mass = 0.0  # in tons
        self.krpc_connection = ksp.get_connection()
        try:
            self.krpc_connection.start_connection()
        except ksp.NotInFlightScene:
            # add code here to regularly check for flight scene change
            pass
        except ksp.KSPNotConnected:
            # add code here to regularly check for connection
            pass
        self.computer = computer.Computer(ui, vessel=self)
        self.autopilot = autopilot.Autopilot(vessel=self)
        self.imu = imu.IMU(vessel=self)
        programs._vessel = self


        # turn on the computer and IMU
        self.computer.on()
        self.imu.on()
