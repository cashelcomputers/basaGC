#!/usr/bin/env python3
"""
This module is not currently used. It is kept around in case it might be needed in the future.
"""

import orbit
from basagc import config
from basagc.telemachus import get_telemetry

class Body(object):
    """This class represents a celestial body"""

    def __init__(self, name):
        self.name = name
        try:
            self.id_ = config.BODIES[name]
        except KeyError:
            utils.log("Body not known: {}".format(name))
            return
        self.orbit = orbit.Orbit(name)
        # if name != "Sun":
        #     self.parent_body = Body(get_telemetry("body"))
        # else:
        #     self.parent_body = None
