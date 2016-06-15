#!/usr/bin/env python3
"""This module contains code that interacts with KSP via the selected interface."""

from basagc import config
from basagc import utils

if config.KSP_INTERFACE == "kos":
    from basagc.interfaces import kos as ksp_interface
elif config.KSP_INTERFACE == "krpc":
    from basagc.interfaces import krpc as ksp_interface
else:
    from basagc.interfaces import telemachus as ksp_interface

connection = None

def connect():
    global connection
    connection = ksp_interface.get_connection()
    try:
        connection.start_connection()
    except ksp_interface.KSPNotConnected:
        utils.log("Could not connect to KSP :(", "WARNING")
        return
    utils.log("KSP connection OK")
    
def check_connection():

    """ Checks if there is a connection available to KSP
    Returns True if so, False otherwise
    """

    try:
        connection.check_connection()
    except ksp_interface.KSPNotConnected:
        return False
    else:
        return True

def get_telemetry(telemetry_type, telemetry, body=None, once_only=False, refssmat=None, **kwargs):
    return connection.get_telemetry(telemetry_type, telemetry, body, once_only, refssmat, **kwargs)


def send_command(command, data):
    return connection.send_command(command, data)