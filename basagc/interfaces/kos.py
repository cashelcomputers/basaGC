#!/usr/bin/env python3
"""This file contains the interface to interact with KOS."""

import telnetlib

from basagc import config

class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass

def check_connection():
    connection = telnetlib.Telnet()
    try:
        connection.open(host=config.IP, port=config.KOS_PORT)
    except ConnectionRefusedError:
        raise KSPNotConnected
