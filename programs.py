#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright 2014 Tim Buchanan, cashelcomputers (at) gmail.com
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
import timer

computer = None
dsky = None
log = logging.getLogger("Programs")

class Program(object):
    
    def __init__(self, name, number):
        self.name = name
        self.number = number
    
    def execute(self):
        dsky.flash_comp_acty(300)
        dsky.control_registers["program"].display(str(self.number))
        computer.state["running_programs"].append(self.number)
    
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
        
        # --> zero CMC clock
        # the KSP clock only starts at liftoff, so nothing to be done
        
        # --> update TEPHEM with liftoff time
        computer.memory.TEPHEM = computer.memory.get_memory("ut")
        
        # --> call average G integration with delta V integration
        computer.state["run_average_g_routine"] = True
        
        # --> terminate gyrocompassing
        if "02" in computer.state["running_programs"]:
            computer.programs["02"].terminate()
        
        # --> compute initial state vector
        computer.routines["average_g"]()

        # --> compute REFSMMAT
        # we already know our REFSMMAT, no need to calculate
        
        # --> set REFSMMAT flag
        computer.memory.REFSMMAT_flag = True
        
        # --> store liftoff attitude
        
        pitch = computer.memory.get_memory("pitch")
        roll = computer.memory.get_memory("roll")
        yaw = computer.memory.get_memory("yaw")
        computer.memory.liftoff_attitude = lib.Attitude(pitch, roll, yaw)
        
        # --> call routine to load ICDU DACs with pitch, roll and yaw attitude
        # --> errors derived from present attitude and stored liftoff attitude
        # --> until present time equals TE1 (stored in erasable memory) at which
        # --> time the stored liftoff attitude is replaced by the solution to
        # --> the stored 6th order boost polynomial.
        # -->
        # --> At time TE1 + TE2 (TE2 is stored in erasable memory) shut off 
        # --> boost polynomial and hold attitude error needles constant at
        # --> terminatl error.
        # --> at 163.86 secs shut off routine to load ICDU DACs.
        # ignoring this part, not even sure what it means :)
        
        

class ProgramNotImplementedError(Exception):
    pass























