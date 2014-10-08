#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

#  This file is part of basaGC (https://github.com/cashelcomputers/basaGC),
#  copyright 2014 Tim Buchanan, cashelcomputers (at) gmail.com
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
#  Includes code and images from the Virtual AGC Project (http://www.ibiblio.org/apollo/index.html)
#  by Ronald S. Burkey <info@sandroid.org>

import logging

import lib
import computer
import maneuvers
import config
from telemachus import get_telemetry, KSPNotConnected

gc = None
dsky = None
log = logging.getLogger("Programs")

class Program(object):

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def execute(self):
        dsky.flash_comp_acty()
        dsky.control_registers["program"].display(str(self.number))
        gc.running_programs.append(self.number)

    def terminate(self):
        while self.number in gc.running_programs: gc.running_programs.remove(self.number)


    #def init_program(self):
        #computer.state["running_program"] = self

    #@staticmethod
    #def format_output_data(data):

        #output = []
        #raw_data = []
        #for item in data:
            #raw_data.append(item)
        #raw_data = [data[1], data[2], data[3]]

        #for item in raw_data:
            #if data["is_octal"] == True:
                #output.append("")
            #elif item < 0:
                #item = ~item + 1
                #output.append("-")
            #else:
                #output.append("+")
            #d = str(item).zfill(5)
            #output.append(d)
        #return output

class Program00(Program):

    def __init__(self, name, number):
        super(Program00, self).__init__(name, number)

    def execute(self):
        #self.init_program()
        log.debug("Program 00 executing...")
        dsky.control_registers["program"].display("00")

class Program01(Program):
    def __init__(self, name, number):
        super(Program01, self).__init__(name, number)

    def execute(self):
        super(Program01, self).execute()
        log.info("Program 01 executing")

        # --> Command ISS zero CDU routine
        # --> wait about 10 seconds
        # nope

        # --> turn on NO ATT annunciator
        dsky.annunciators["no_att"].on()

        # --> Command course align in ISS. Course align to desired platform orientation

        # --. turn off NO ATT annunciator
        # here we will simply wait 5 secs then turn it off

class Program11(Program):
    def __init__(self, name, number):
        super(Program11, self).__init__(name, number)

    def execute(self):
        super(Program11, self).execute()
        log.info("Program 11 executing")

        # test if KSP is connected
        try:
            get_telemetry("ut")
        except KSPNotConnected:
            self.terminate()
            return


        # --> call average G integration with delta V integration
        gc.run_average_g_routine = True

        # --> terminate gyrocompassing
        if "02" in gc.running_programs:
            gc.programs["02"].terminate()

        # --> compute initial state vector
        # gc.routines["average_g"]()


        # --> Display on DSKY:
        # --> V06 N62 (we are going to use V16N62 though, so we can have a updated display
        # --> R1: Velocity
        # --> R2: Rate of change of vehicle altitude
        # --> R3: Vehicle altitude in km to nearest .1 km
        gc.execute_verb(verb=16, noun=62)


class Program15(Program):

    def __init__(self, name, number):
        super(Program15, self).__init__(name, number)
        self.delta_v_required = 0
        self.time_to_transfer = 0
        self.orbiting_body = None
        self.phase_angle = 0

    def execute(self):
        #dsky.request_data(requesting_object=self.set_target, location=dsky.registers[3])
        # departure_altitude = get_telemetry("asl")
        # destination_altitude = 12250000
        # print(maneuvers.hohmann(departure_altitude, destination_altitude))
        self.orbiting_body = get_telemetry("orbiting_body_name")
        if get_telemetry("eccentricity") > 0.001:
            gc.program_alarm(224)
            return
        gc.execute_verb(verb=23, noun=30)
        gc.object_requesting_data = self.select_target

    def select_target(self, target):
        if target[0] == ("+" or "-"):
            gc.program_alarm(222)
            return
        elif int(target) not in config.OCTAL_BODIES:
            gc.program_alarm(223)
            return
        target = config.OCTAL_BODIES[int(target)]
        destination_altitude = 0
        if target == "Mun":
            destination_altitude = 12250000
        departure_altitude = get_telemetry("asl")
        self.delta_v_required = maneuvers.hohmann(departure_altitude, destination_altitude)
        grav_param = get_telemetry("body_gravitational_parameter", body_number=config.BODIES[self.orbiting_body])
        self.time_to_transfer = maneuvers.time_to_transfer(departure_altitude, destination_altitude, grav_param)
        self.phase_angle = maneuvers.phase_angle(departure_altitude, destination_altitude, grav_param)
        print(self.phase_angle)

class ProgramNotImplementedError(Exception):
    pass























