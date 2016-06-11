#!/usr/bin/env python3
"""This module contains code that interacts with KSP via the selected interface."""

from basagc import config
if config.KSP_INTERFACE == "kos":
    from basagc.interfaces import kos as ksp
elif config.KSP_INTERFACE == "krpc":
    from basagc.interfaces import krpc as ksp
else:
    from basagc.interfaces import telemachus as ksp

def check_connection():

    """ Checks if there is a connection available to KSP
    Returns True if so, False otherwise
    """

    try:
        ksp.check_connection()
    except ksp.KSPNotConnected:
        return False
    else:
        return True