#!/usr/bin/env python3

""" This file contains class definition of a vessel."""

from basagc import ksp
from basagc import config
from basagc import vector
from basagc import autopilot
from basagc.interfaces import krpc
from basagc import computer
from basagc import imu

class Vessel:

    def __init__(self, ui):

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.krpc_connection = krpc.get_connection()
        self.computer = computer.Computer(ui, vessel=self)
        self.autopilot = autopilot.Autopilot()
        self.imu = imu.IMU(vessel=self)

        # turn on the computer and IMU
        self.computer.on()
        self.imu.on()

        # connect to ksp
        conn = krpc.get_connection()
        try:
            conn.start_connection()
        except krpc.KSPNotConnected:
            pass  # FIXME