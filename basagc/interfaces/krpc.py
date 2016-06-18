#!/usr/bin/env python3
"""This file contains the interface to interact with kRPC."""

import krpc as krpclib

from basagc import config

class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass



def get_connection():
    return KRPCConnection.connection if KRPCConnection.connection else KRPCConnection()

class KRPCConnection:

    connection = None

    def __init__(self):

        KRPCConnection.connection = self
        self.connection = None
        self.streams = []
        self.control = None
        self.orbit = None
        self.vessel = None
        self.space_center = None

    def start_connection(self):

        try:
            self.connection = krpclib.connect(name='basaGC', rpc_port=config.KRPC_PORT)
        except krpclib.error.NetworkError:
            raise KSPNotConnected
        self.vessel = self.connection.space_center.active_vessel
        self.control = self.vessel.control
        self.orbit = self.vessel.orbit
        self.space_center = self.connection.space_center

    def check_connection(self):
        if self.connection is None:
            try:
                self.start_connection()
            except KSPNotConnected:
                return False
        else:
            return True

    def get_telemetry(self, telemetry_type, telemetry, body=None, once_only=False, refssmat=None, *args, **kwargs):

        if refssmat:
            vessel = self.connection.space_center.active_vessel
            refssmat = getattr(self.orbit.body, refssmat)
        data = None
        if telemetry_type == "orbit":
            data = self.orbit
        elif telemetry_type == "orbit_body":  # the parameters of the body being orbited
            data = self.orbit.body
        elif telemetry_type == "vessel":
            if refssmat:
                data = self.vessel(getattr(self.vessel, refssmat))
            data = self.vessel
        elif telemetry_type == "flight":
            data = self.space_center.active_vessel.flight(refssmat)
        elif telemetry_type == "body":  # the parameters of a given body
            data = self.space_center.bodies[body]
        elif telemetry_type == "body_orbit":  # the orbit parameters of a body
            data = self.space_center.bodies[body].orbit
        elif telemetry_type == "space_center":
            data = self.space_center
        else:
            return False

        if once_only:
            return getattr(data, telemetry)  # just return the data
        else:  # return a function that returns the telemetry
            if callable(getattr(data, telemetry)):
                return self.connection.add_stream(data, *args, **kwargs,)
            else:
                return self.connection.add_stream(getattr, data, telemetry)


    def send_command(self, command, data):

        # sas
        if command == "sas_mode":
            data = getattr(self.space_center.SASMode, data)
        try:
            setattr(self.control, command, data)
        except AttributeError:
            return False
        return True