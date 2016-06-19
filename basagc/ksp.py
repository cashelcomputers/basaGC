#!/usr/bin/env python3
"""This file contains the interface to interact with kRPC."""

import krpc

from basagc import config
from basagc import utils

class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass


class NotInFlightScene(Exception):
    """Should be raised when KSP is not in the flight scene"""
    pass

def get_telemetry(telemetry_type, telemetry, body=None, once_only=False, refssmat=None, *args, **kwargs):
    return get_connection().get_telemetry(telemetry_type, telemetry, body, once_only, refssmat, *args, **kwargs)

def get_connection():
    return KRPCConnection.connection if KRPCConnection.connection else KRPCConnection()

def send_command(command, data):
    utils.log("Use of depreciated function send_command()", log_level="DEBUG")
    return get_connection().send_command(command, data)

def check_connection():
    return get_connection().check_connection()

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
        self.is_connected = False

    def start_connection(self):

        try:
            self.connection = krpc.connect(name='basaGC', rpc_port=config.KRPC_PORT)
        except krpc.error.NetworkError:
            raise KSPNotConnected
        try:
            self.vessel = self.connection.space_center.active_vessel
            self.control = self.vessel.control
            self.orbit = self.vessel.orbit
        except krpc.error.RPCError:
            raise NotInFlightScene
        self.is_connected = True
        self.space_center = self.connection.space_center

    def check_connection(self):
        if self.connection is None:
            try:
                self.start_connection()
            except KSPNotConnected:
                self.is_connected = False
                return False
            self.is_connected = True
            return True
        else:
            return True

    def check_flight_scene(self):
        flight_scene = self.connection.krpc.current_game_scene
        if flight_scene == self.connection.krpc.GameScene.flight:
            return True
        else:
            return flight_scene

    def get_telemetry(self, telemetry_type, telemetry, body=None, once_only=False, refssmat=None, *args, **kwargs):

        flight_scene = self.check_flight_scene()
        if not flight_scene:
            utils.log("Cannot obtain telemetry: not in flight scene (currently in {} scene".format(flight_scene))
            return False
        #first, check if we have a active connection
        if not self.check_connection():
            utils.log("Cannot obtain telemetry: no connection to KSP")
            return False
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