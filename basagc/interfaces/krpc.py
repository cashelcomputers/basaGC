#!/usr/bin/env python3
"""This file contains the interface to interact with kRPC."""

import krpc

class KSPNotConnected(Exception):
    """ This exception should be raised when there is no connection to KSP """
    pass