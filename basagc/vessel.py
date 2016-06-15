#!/usr/bin/env python3

""" This file contains class definition of a vessel."""

from basagc import ksp
from basagc import config
from basagc import vector
from basagc.interfaces import krpc
from basagc import computer

class Vessel:

    def __init__(self):

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.connection = krpc.get_connection().connection
        self.computer = None
        self.autopilot = None


    def update_state_vector(self):

        vessel_direction = ksp.get_telemetry("vessel", "direction", refssmat=config.REFSSMAT["surface"])()

        # Get the direction of the vessel in the horizon plane
        horizon_direction = (0, vessel_direction[1], vessel_direction[2])

        # Compute the pitch - the angle between the vessels direction and the direction in the horizon plane
        pitch = vector.angle_between_vectors(vessel_direction, horizon_direction)
        if vessel_direction[0] < 0:
            pitch = -pitch

        # Compute the heading - the angle between north and the direction in the horizon plane
        north = (0, 1, 0)
        heading = vector.angle_between_vectors(north, horizon_direction)
        if horizon_direction[2] < 0:
            heading = 360 - heading

        # Compute the roll
        # Compute the plane running through the vessels direction and the upwards direction
        up = (1,0,0)
        plane_normal = vector.cross_product(vessel_direction, up)

        # Compute the upwards direction of the vessel

        vessel_up = self.connection.space_center.transform_direction(
            (0, 0, -1), self.connection.vessel.reference_frame, self.connection.vessel.surface_reference_frame)

        # Compute the angle between the upwards direction of the vessel and the plane
        roll = vector.angle_between_vector_and_plane(vessel_up, plane_normal)
        # Adjust so that the angle is between -180 and 180 and
        # rolling right is +ve and left is -ve
        if vessel_up[0] > 0:
            roll *= -1
        elif roll < 0:
            roll += 180
        else:
            roll -= 180

        self.pitch = pitch
        self.roll = roll
        self.yaw = heading

        print('pitch = % 5.1f, heading = % 5.1f, roll = % 5.1f' % (pitch, heading, roll))
