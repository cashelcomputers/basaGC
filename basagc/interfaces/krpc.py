#!/usr/bin/env python3
"""This file contains the interface to interact with kRPC."""

import krpc as krpclib

from basagc import config

class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass

def get_connection():
    return KRPCConnection()

class KRPCConnection:
    
    def __init__(self):
        self.connection = None
        self.streams = []

    def start_connection(self):

        try:
            self.connection = krpclib.connect(name='basaGC', rpc_port=config.KRPC_PORT)
        except krpclib.error.NetworkError:
            raise KSPNotConnected

    def check_connection(self):
        if self.connection == None:
            try:
                self.start_connection()
            except KSPNotConnected:
                return False
        else:
            return True

    def set_throttle(percent):
        pass

    def get_telemetry(self, telemetry_type, telemetry, stream, refssmat, **kwargs):

        if refssmat:
            vessel = self.connection.space_center.active_vessel
            print(dir(vessel.orbit.body))
            refssmat = getattr(vessel.orbit.body, refssmat)
            print(refssmat)
        data = None
        if telemetry_type == "orbit":
            data = self.connection.space_center.active_vessel.orbit
        elif telemetry_type == "orbit_body":
            data = self.connection.space_center.active_vessel.orbit.body
        elif telemetry_type == "vessel":
            data = self.connection.space_center.active_vessel
        elif telemetry_type == "flight":
            data = self.connection.space_center.active_vessel.flight(refssmat)
        else:
            return False

        if stream:
            if callable(getattr(data, telemetry)):
                return self.connection.add_stream(data, **kwargs,)
            else:
                return self.connection.add_stream(getattr, data, telemetry)
        else:
            return getattr(data, telemetry)
