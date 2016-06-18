#!/usr/bin/env python3
"""This file contains the interface to interact with KOS."""

import telnetlib
import telnetlib3
import struct
from basagc import config

def get_connection():
    return KOSConnection()
    
class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass

class KOSConnection:

    connection = None
    
    def __init__(self):
        self.connection = None
        KOSConnection.connection = self

    def start_connection(self):
        connection = telnetlib.Telnet()
        try:
            connection.open(host=config.IP, port=config.KOS_PORT)
        except ConnectionRefusedError:
            raise KSPNotConnected
        print(connection.read_until(b"> "))
        #naws_command = b"255 250 31 80 25 255 240"
        #connection.get_socket().send(naws_command)
        #self.connection = connection
        #self.connection.write(b"xterm\n") 
        #print(self.connection.read_until(b"> "))
        #self.connection.write(b"1\n")
        #self.connection.write(b"PRINT THROTTLE.\n")

    def check_connection(self):
        if KOSConnection.connection is None:
            try:
                self.start_connection()
            except KSPNotConnected:
                return False
        else:
            return True

    def set_throttle(percent):
        throttle_value = percent / 100
        command = b"LOCK THROTTLE TO {}\n".format(str(throttle_value))
        self.connection.write(command)