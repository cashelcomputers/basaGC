#!/usr/bin/env python3
"""This module contains a class to model the IMU found on Apollo spacecraft."""

from basagc import utils, config, krpc_interface
from basagc import vector
from basagc import krpc_interface

if config.DEBUG:
    pass

class IMU:
    """
    This class models the IMU used in Apollo spacecraft.
    """
    def __init__(self, vessel):
        """
        Class init
        :param computer: the instance of the computer
        :type computer: Computer object
        :returns: None
        """
        
        self.vessel = vessel
        self.computer = vessel.computer
        self.krpc_connection = krpc_interface.get_connection()
        self._is_on = False
        self.is_coarse_aligned = False
        self.is_fine_aligned = False

        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0

    def get_pitch_roll_yaw(self):
        return self.pitch, self.roll, self.yaw

    def on(self):
        """
        Turns the IMU on
        :returns: True if successful, False otherwise
        """
        self._is_on = True
        if krpc_interface.get_connection().check_connection():
            self.computer.add_to_mainloop(self._update_state_vector)
        return True

    def off(self):
        """
        Turns the IMU off
        :returns: True if successful, False otherwise
        """
        self._is_on = False
        return True


    def _update_state_vector(self):
        """
        Gets the latest attitude from KSP and sets those values in IMU
        :returns: None
        """

        # if we have lost connection to KSP, terminate state vector updates
        if not krpc_interface.get_connection().check_connection():
            self.computer.remove_from_mainloop(self._update_state_vector)
        vessel_direction = self.krpc_connection.vessel.direction(self.krpc_connection.vessel.surface_reference_frame)

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
        up = (1, 0, 0)
        plane_normal = vector.cross_product(vessel_direction, up)

        # Compute the upwards direction of the vessel

        vessel_up = self.krpc_connection.space_center.transform_direction(
            (0, 0, -1), self.krpc_connection.vessel.reference_frame,
            self.krpc_connection.vessel.surface_reference_frame)

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


    # def _check_for_gimbal_lock(self):
    #     '''
    #     Checks if middle gimbal is approaching gimbal lock, only applies to fine align mode
    #     :returns: False if ok, True if approaching gimbal lock
    #     '''
    #     if self.is_fine_aligned:
    #         # check if approaching gimbal lock
    #         if (70 <= self.gyro_angles["middle"] <= 85) or \
    #             (95 <= self.gyro_angles["middle"] <= 110) or \
    #             (250 <= self.gyro_angles["middle"] <= 265) or \
    #             (275 <= self.gyro_angles["middle"] <= 290):
    #                 self.computer.dsky.set_annunciator("gimbal_lock")
    #         else:
    #         # if middle gimbal = 90 +- 5 or 270 +- 5, gimbal lock has occured
    #             if (85 < self.gyro_angles["middle"] < 95) or \
    #                 (265 < self.gyro_angles["middle"] <= 275):
    #                     self.set_coarse_align()

    def set_coarse_align(self):
        """
        Sets coarse align mode.
        :returns: None
        """
        self.is_fine_aligned = False
        self.is_coarse_aligned = True
        self.computer.dsky.set_annunciator("no_att")
        # if self.update_gyro_angles in self.computer.main_loop_table:
        #     self.computer.main_loop_table.remove(self.update_gyro_angles)
        # if self.check_for_gimbal_lock in self.computer.main_loop_table:
        #     self.computer.main_loop_table.remove(self.check_for_gimbal_lock)
        utils.log("IMU coarse align set")

    def set_fine_align(self):
        """
        Sets fine align mode.
        :returns: None
        """
        # if no connection to KSP, stop fine align and go back to coarse align
        # if check_connection() == False:
        #     utils.log("IMU: cannot complete fine align, no connection to KSP", log_level="ERROR")
        #     return
        self.is_fine_aligned = True
        self.is_coarse_aligned = False
        self.computer.dsky.set_annunciator("gimbal_lock", False)
        self.computer.dsky.set_annunciator("no_att", False)
        #self.computer.main_loop_table.append(self.update_gyro_angles)
        #self.computer.main_loop_table.append(self.check_for_gimbal_lock)
        utils.log("IMU fine align set")