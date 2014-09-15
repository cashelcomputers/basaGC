#!/usr/bin/env python2

import simplevector

class StateVector(object):
    def __init__(self):
        self.position_vector = {
            "lat": 0.0,
            "long": 0.0, 
            "alt": 0.0,
        }
        self.velocity_vector = simplevector.Vector(0, 0, 0)
        self.time = 0.0

class Attitude(object):
    def __init__(self, pitch=0.0, roll=0.0, yaw=0.0):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
