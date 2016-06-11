#!/usr/bin/env python3
"""This module contains a class to model the IMU found on Apollo spacecraft."""

from basagc.interfaces.telemachus import check_connection, get_telemetry
from basagc import utils, config
if config.DEBUG:
    from pudb import set_trace  # lint:ok

class IMU:
    '''
    This class models the IMU used in Apollo spacecraft.
    '''
    def __init__(self, computer):
        '''
        Class init
        :param computer: the instance of the computer
        :type computer: Computer object
        :returns: None
        '''
        
        self.computer = computer
        self._is_on = False
        self.is_course_aligned = False
        self.is_fine_aligned = False
        self.gyro_angles = {
            "inner": 0.0,  # Y axis, aka pitch
            "middle": 0.0,  # Z axis, aka heading
            "outer": 0.0,  # X axis, aka roll
            }

    def on(self):
        '''
        Turns the IMU on
        :returns: True if successful, False otherwise
        '''
        if check_connection() == False:
            utils.log("Cannot connect to KSP", "WARNING")
        else:
            self.set_coarse_align()


        # add check for gimbal lock to computer main loop


    def update_gyro_angles(self):
        '''
        Gets the latest attitude from KSP and sets those values in IMU
        :returns: None
        '''

        self.gyro_angles["inner"] = get_telemetry("pitch")
        self.gyro_angles["middle"] = get_telemetry("heading")
        self.gyro_angles["outer"] = get_telemetry("roll")

    def check_for_gimbal_lock(self):
        '''
        Checks if middle gimbal is approaching gimbal lock, only applies to fine align mode
        :returns: False if ok, True if approaching gimbal lock
        '''
        if self.is_fine_aligned:
            # check if approaching gimbal lock
            if (70 <= self.gyro_angles["middle"] <= 85) or \
                (95 <= self.gyro_angles["middle"] <= 110) or \
                (250 <= self.gyro_angles["middle"] <= 265) or \
                (275 <= self.gyro_angles["middle"] <= 290):
                    self.computer.dsky.set_annunciator("gimbal_lock")
            else:
            # if middle gimbal = 90 +- 5 or 270 +- 5, gimbal lock has occured
                if (85 < self.gyro_angles["middle"] < 95) or \
                    (265 < self.gyro_angles["middle"] <= 275):
                        self.set_coarse_align()

    def set_coarse_align(self):
        '''
        Sets coarse align mode.
        :returns: None
        '''
        self.is_fine_aligned = False
        self.is_course_aligned = True
        self.computer.dsky.set_annunciator("no_att")
        if self.update_gyro_angles in self.computer.main_loop_table:
            self.computer.main_loop_table.remove(self.update_gyro_angles)
        if self.check_for_gimbal_lock in self.computer.main_loop_table:
            self.computer.main_loop_table.remove(self.check_for_gimbal_lock)
        utils.log("IMU coarse align set")

    def set_fine_align(self):
        '''
        Sets fine align mode.
        :returns: None
        '''
        # if no connection to KSP, stop fine align and go back to coarse align
        if check_connection() == False:
            utils.log("IMU: cannot complete fine align, no connection to KSP", log_level="ERROR")
            return
        self.is_fine_aligned = True
        self.is_course_aligned = False
        self.computer.dsky.set_annunciator("gimbal_lock", False)
        self.computer.dsky.set_annunciator("no_att", False)
        #self.computer.main_loop_table.append(self.update_gyro_angles)
        #self.computer.main_loop_table.append(self.check_for_gimbal_lock)
        utils.log("IMU fine align set")