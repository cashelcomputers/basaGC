#!/usr/bin/env python3

""" This file contains class definition of a vessel."""

from basagc import autopilot
from basagc import computer
from basagc import imu
from basagc import krpc_interface


class Vessel:

    def __init__(self, ui):

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.krpc_connection = krpc_interface.get_connection()
        try:
            self.krpc_connection.start_connection()
        except krpc_interface.NotInFlightScene:
            # add code here to regularly check for flight scene change
            pass
        except krpc_interface.KSPNotConnected:
            # add code here to regularly check for connection
            pass
        self.computer = computer.Computer(ui, vessel=self)
        self.autopilot = autopilot.Autopilot()
        self.imu = imu.IMU(vessel=self)

        # turn on the computer and IMU
        self.computer.on()
        self.imu.on()
