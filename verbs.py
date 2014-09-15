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

import wx
import logging

import nouns
import config
import computer as Computer

memory = None
computer = None
dsky = None
frame = None

log = logging.getLogger("Verbs")


INVALID_VERBS = [
    0,
    8,
    9,
    10,
    18,
    19,
    20,
    26,
    28,
    29,
    38,
    39,
    68,
    76,
    77,
    79,
    84,
    95,
    98,
]

def format_output_data(data):
    
    output = []
    raw_data = [data[1], data[2], data[3]]
    
    for item in raw_data:
        if data["is_octal"] == True:
            output.append("")
        elif item < 0:
            #item = ~item + 1
            output.append("-")
            item = abs(item)
        else:
            output.append("+")
        d = str(item).zfill(5)
        output.append(d)
    return output

class NounNotAcceptableError(Exception):
    pass
    
#------------------------BEGIN BASE CLASS DEFINITIONS---------------------------

class Verb(object):
    def __init__(self, name, verb_number):
        self.name = name
        self.number = verb_number
        self.illegal_nouns = []
        self.activity_timer = wx.Timer(frame)
        frame.Bind(wx.EVT_TIMER, self._activity, self.activity_timer)
        self.data = ""
    
    def execute(self):
        computer.dsky.state["current_verb"] = self.number
    
    def _activity(self, event):
        #dsky.flash_comp_acty()
        pass
        
    def terminate(self):
        raise NotImplementedError
    
    def receive_data(self, data):
        print("{} received data: {}".format(self, data))
        self.data = data
        self.execute()

class DataVerb(Verb):
    def __init__(self, name, verb_number, components, registers, is_single_precision=True):
        super(DataVerb, self).__init__(name, verb_number)
        self.components = components
        self.registers = registers
        self.is_single_precision = is_single_precision

class DisplayVerb(DataVerb):
    def __init__(self, name, verb_number, components, registers, is_single_precision=True):
        super(DisplayVerb, self).__init__(name, verb_number, components, registers, is_single_precision)
    
    def execute(self):
        #raise NotImplementedError
        if computer.dsky.state["requested_noun"] in self.illegal_nouns:
            raise NounNotAcceptableError
            return

class MonitorVerb(DisplayVerb):
    def __init__(self, name, verb_number, components, registers, is_single_precision=True):
        
        super(MonitorVerb, self).__init__(name, verb_number, components, registers, is_single_precision)
        self.timer = wx.Timer(frame)
        frame.Bind(wx.EVT_TIMER, self._update_display, self.timer)
    
    def _send_output(self):
        """ Sends the requested output to the DSKY """
        if computer.dsky.state["requested_noun"] in self.illegal_nouns:
            raise NounNotAcceptableError
            return
        noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
        try:
            data = noun_function()
        except nouns.NounNotImplementedError:
            dsky.operator_error("Noun {} not implemented yet. Sorry about that...".format(dsky.state["requested_noun"]))
            self.terminate()
            return
        except Computer.KSPNotConnected:
            print("KSP not connected, terminating V{}".format(self.number))
            computer.program_alarm(110, required_action="program_alarm")
            self.terminate()
            raise
            return
        output = format_output_data(data)
        computer.dsky.registers[1].display(output[0], output[1])
        computer.dsky.registers[2].display(output[2], output[3])
        computer.dsky.registers[3].display(output[4], output[5])
        dsky.flash_comp_acty()
        
    def start_monitor(self):
        """ Starts the timer to monitor the verb """
        if dsky.state["backgrounded_update"] is not None:
            dsky.state["backgrounded_update"].terminate()
        dsky.state["display_lock"] = self
        
        try:
            self._send_output()
        except Computer.KSPNotConnected:
            return
        
        self.timer.Start(config.DISPLAY_UPDATE_INTERVAL)
        
        
    def _update_display(self, event):
        """ a simple wrapper to call the display update method """
        if not self.activity_timer.IsRunning():
            self.activity_timer.Start(1000)
        self._send_output()
    
    def terminate(self):
        print("Terminating V{}".format(self.number))
        dsky.annunciators["key_rel"].off()
        dsky.state["display_lock"] = None
        dsky.state["backgrounded_update"] = None
        self.timer.Stop()
        self.activity_timer.Stop()
    
    def background(self):
        dsky.state["backgrounded_update"] = self
        dsky.state["display_lock"] = None
        self.timer.Stop()
        dsky.annunciators["key_rel"].on()
        self.activity_timer.Stop()
    
    def resume(self):
        dsky.state["display_lock"] = self
        dsky.state["backgrounded_update"] = None
        self.start_monitor()

class LoadVerb(DataVerb):
    def __init__(self, name, verb_number, components, registers):
        super(LoadVerb, self).__init__(name, verb_number, components, registers, is_single_precision=True)

#---------------------------BEGIN VERB CLASS DEFINITIONS------------------------

# no verb 00

class Verb1(DisplayVerb):
    def __init__(self):
        super(Verb1, self).__init__(name="Display Octal component 1 in R1", verb_number=1, components=(1,), registers=(1,))
    #def execute(self):
        #super(Verb1, self).execute()
        #if self.data == None:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #noun_function(calling_verb=self, base=8)
            #return
        #else:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #self.noun_data = noun_function(calling_verb=self, data=self.data, base=8)
            #output = format_output_data(self.noun_data)
            #computer.dsky.registers[1].display(output[0], output[1])
            #self.data = None

class Verb2(DisplayVerb):
    def __init__(self):
        super(Verb2, self).__init__(name="Display Octal component 2 in R1", verb_number=2, components=(2,), registers=(1,))
    
    #def execute(self):
        #super(Verb2, self).execute()
        #if self.data == None:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #noun_function(calling_verb=self, base=8)
            #return
        #else:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #self.noun_data = noun_function(calling_verb=self, data=self.data, base=8)
            #output = format_output_data(self.noun_data)
            #computer.dsky.registers[1].display(output[2], output[3])
            #self.data = None

class Verb3(DisplayVerb):
    def __init__(self):
        super(Verb3, self).__init__(name="Display Octal component 3 in R1", verb_number=3, components=(3,), registers=(1,))
    
    #def execute(self):
        #super(Verb3, self).execute()
        #if self.data == None:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #noun_function(calling_verb=self, base=8)
            #return
        #else:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #self.noun_data = noun_function(calling_verb=self, data=self.data, base=8)
            #output = format_output_data(self.noun_data)
            #computer.dsky.registers[1].display(output[4], output[5])
            #self.data = None
        
class Verb4(DisplayVerb):
    def __init__(self):
        super(Verb4, self).__init__(name="Display Octal components 1, 2 in R1, R2", verb_number=4, components=(1, 2), registers=(1, 2))
        
    def execute(self):
        
        super(Verb4, self).execute()
        noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
        noun_data = noun_function(calling_verb=self)
        output = format_output_data(self.noun_data)
        computer.dsky.registers[1].display(output[0], output[1])
        computer.dsky.registers[2].display(output[2], output[3])
        
class Verb5(DisplayVerb):
    def __init__(self):
        super(Verb5, self).__init__(name="Display Octal components 1, 2, 3 in R1, R2, R3", verb_number=5, components=(1, 2, 3), registers=(1, 2, 3))
        self.illegal_nouns = []
    def execute(self):
        print("Executing V05")
        super(Verb5, self).execute()
        noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
        noun_data = noun_function(calling_verb=self)
        output = format_output_data(noun_data)
        computer.dsky.registers[1].display(output[0], output[1])
        computer.dsky.registers[2].display(output[2], output[3])
        computer.dsky.registers[3].display(output[4], output[5])

class Verb6(DisplayVerb):
    def __init__(self):
        super(Verb6, self).__init__(name="Display Decimal in R1 or in R1, R2 or in R1, R2, R3", verb_number=6, components=(1, 2, 3), registers=(1, 2, 3))

        
    def execute(self):
        super(Verb6, self).execute()
        if self.data == None:
            noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            noun_function(calling_verb=self, base=10)
            return
        else:
            noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            self.noun_data = noun_function(calling_verb=self, data=self.data, base=10)
            output = format_output_data(self.noun_data)
            computer.dsky.registers[1].display(output[0], output[1])
            computer.dsky.registers[2].display(output[2], output[3])
            computer.dsky.registers[3].display(output[4], output[5])
            self.data = None
        
class Verb7(DisplayVerb):
    def __init__(self):
        super(Verb7, self).__init__(name="Display Double Precision Decimal in R1, R2 (test only)", verb_number=7, components=(1,), registers=(1, 2), is_single_precision=False)

# no verb 8

# no verb 9

# no verb 10

class Verb11(MonitorVerb):
    def __init__(self):
        super(Verb11, self).__init__(name="Monitor Octal component 1 in R1", verb_number=11, components=(1,), registers=(1,))

class Verb12(MonitorVerb):
    def __init__(self):
        super(Verb12, self).__init__(name="Monitor Octal component 2 in R1", verb_number=12, components=(2,), registers=(1,))

class Verb13(MonitorVerb):
    def __init__(self):
        super(Verb13, self).__init__(name="Monitor Octal component 3 in R1", verb_number=13, components=(3,), registers=(1,))

class Verb14(MonitorVerb):
    def __init__(self):
        super(Verb14, self).__init__(name="Monitor Octal components 1, 2 in R1, R2", verb_number=14, components=(1, 2), registers=(1, 2))
        
class Verb15(MonitorVerb):
    def __init__(self):
        super(Verb15, self).__init__(name="Monitor Octal components 1, 2, 3 in R1, R2, R3", verb_number=15, components=(1, 2, 3), registers=(1, 2, 3))

class Verb16(MonitorVerb): # implemented, needs testing
    def __init__(self):
        super(Verb16, self).__init__(name="Monitor Decimal in R1 or in R1, R2 or in R1, R2, R3", verb_number=16, components=(1, 2, 3), registers=(1, 2, 3))

    def execute(self):
        self.start_monitor()

class Verb17(MonitorVerb):
    def __init__(self):
        super(Verb17, self).__init__(name="Monitor Double Precision Decimal in R1, R2 (test only)", verb_number=17, components=(1,), registers=(1, 2), is_single_precision=False)

# no verb 18

# no verb 19

# no verb 20

class Verb21(LoadVerb):
    def __init__(self):
        super(Verb21, self).__init__(name="Load component 1 into R1", verb_number=21, components=(1,), registers=(1,))

class Verb22(LoadVerb):
    def __init__(self):
        super(Verb22, self).__init__(name="Load component 2 into R2", verb_number=22, components=(2,), registers=(2,))

class Verb23(LoadVerb):
    def __init__(self):
        super(Verb23, self).__init__(name="Load component 3 into R3", verb_number=23, components=(3,), registers=(3,))

class Verb24(LoadVerb):
    def __init__(self):
        super(Verb24, self).__init__(name="Load component 1, 2 into R1, R2", verb_number=24, components=(1, 2), registers=(1, 2))
        
class Verb25(LoadVerb):
    def __init__(self):
        super(Verb25, self).__init__(name="Load component 1, 2, 3 into R1, R2, R3", verb_number=25, components=(1, 2, 3), registers=(1, 2, 3))

# no verb 26

class Verb27(LoadVerb):
    def __init__(self):
        super(Verb27, self).__init__(name="Display fixed memory", verb_number=27, components=(1,), registers=(1,))

# no verb 28

# no verb 29

class Verb30(Verb):
    def __init__(self):
        super(Verb30, self).__init__(name="Request Executive", verb_number=30)

class Verb31(Verb):
    def __init__(self):
        super(Verb31, self).__init__(name="Request waitlist", verb_number=31)

class Verb32(Verb):
    def __init__(self):
        super(Verb32, self).__init__(name="Recycle program", verb_number=32)
    
    def execute(self):
        if isinstance(dsky.state["backgrounded_update"], MonitorVerb):
            dsky.state["backgrounded_update"].terminate()
        else:
            print("V32 called, but nothing to recycle!")
    
class Verb33(Verb):
    def __init__(self):
        super(Verb33, self).__init__(name="Proceed without DSKY inputs", verb_number=33)
    
    def execute(self):
        if isinstance(dsky.state["backgrounded_update"], MonitorVerb):
            dsky.state["backgrounded_update"].terminate()
        else:
            print("V33 called, but nothing to proceed with!")

class Verb34(Verb):
    def __init__(self):
        super(Verb34, self).__init__(name="Terminate function", verb_number=34)
    
    def execute(self):
        if isinstance(dsky.state["backgrounded_update"], MonitorVerb):
            dsky.state["backgrounded_update"].terminate()
        else:
            print("V34 called, but nothing to terminate!")

class Verb35(Verb): # Implemented
    
    """Lamp test"""
    
    def __init__(self):
        super(Verb35, self).__init__(name="Test lights", verb_number=35)
        global frame
        self.stop_timer = wx.Timer(frame)
        self.loop_counter = 0
        frame.Bind(wx.EVT_TIMER, self.stop_timer_event, self.stop_timer)
    
    def execute(self):
        # commands the annunciators
        for annunciator in dsky.annunciators.itervalues():
            annunciator.on()
        #commands the data registers
        for register in dsky.registers.itervalues():
            register.sign.plus()
            for digit in register.digits:
                digit.display(8)
        #commands the control registers
        for name, register in dsky.control_registers.iteritems():
            if name == "program":
                for digit in register.digits.itervalues():
                    digit.display(8)
            else:
                for digit in register.digits.itervalues():
                    digit.display(8)
                    digit.start_blink()
        self.stop_timer.Start(5000, oneShot=True)
        
    def terminate(self):
        print("Hit terminate")
        for annunciator in dsky.annunciators.itervalues():
            annunciator.off()
        for name, register in dsky.control_registers.iteritems():
            if name == "program":
                for digit in register.digits.itervalues():
                    digit.display("blank")
            else:
                for digit in register.digits.itervalues():
                    digit.stop_blink()
                    digit.display(8)
    
    def stop_timer_event(self, event):
        print("Stopping V35 timer")
        self.terminate()

class Verb36(Verb):
    def __init__(self):
        super(Verb36, self).__init__(name="Request fresh start", verb_number=36)
    
    def execute(self):
        computer.fresh_start()

class Verb37(Verb):
    def __init__(self):
        super(Verb37, self).__init__(name="Change program (Major Mode)", verb_number=37)
        #self.data.append("")
        
    def execute(self):
        dsky.state["object_requesting_data"] = self
        dsky.control_registers["noun"].blank()
        dsky.request_data(requesting_object=self, location=dsky.control_registers["noun"])
    
    def receive_data(self, data):
        
        computer.programs[int(data)].execute()
    
    def data_load_done(self):
        dsky.verb_noun_flash_off()
        data = self.data.pop()
        number_of_digits = len(data)
        if number_of_digits != 2:
            dsky.operator_error("Expected exactly two digits, received {}".format(number_of_digits))
            self.terminate()
            return
        computer.programs[int(data)].execute()

#-------------------------------BEGIN EXTENDED VERBS----------------------------

class Verb40(Verb):
    def __init__(self):
        super(Verb40, self).__init__(name="Zero CDUs", verb_number=40)
    
    def execute(self):
        computer.program_alarm(666, required_action=config.PROGRAM_ALARM)

class Verb41(Verb):
    def __init__(self):
        super(Verb41, self).__init__(name="Coarse align CDUs", verb_number=41)
    
    def execute(self):
        computer.program_alarm(69, required_action=config.COMPUTER_FRESH_START)
    
class Verb42(Verb):
    def __init__(self):
        super(Verb42, self).__init__(name="Fine align IMU", verb_number=42)

class Verb43(Verb):
    def __init__(self):
        super(Verb43, self).__init__(name="Load IMU attitude error meters (test only)", verb_number=43)

class Verb44(Verb):
    def __init__(self):
        super(Verb44, self).__init__(name="Set surface flag", verb_number=44)
        
class Verb45(Verb):
    def __init__(self):
        super(Verb45, self).__init__(name="Reset surface flag", verb_number=45)

class Verb46(Verb):
    def __init__(self):
        super(Verb46, self).__init__(name="Establish G&C control", verb_number=46)

class Verb47(Verb):
    def __init__(self):
        super(Verb47, self).__init__(name="Move LM state vector into CM state vector", verb_number=47)

class Verb48(Verb):
    def __init__(self):
        super(Verb48, self).__init__(name="Request DAP data load (R03)", verb_number=48)

class Verb49(Verb):
    def __init__(self):
        super(Verb49, self).__init__(name="Request crew defined maneuver (R62)", verb_number=49)

class Verb50(Verb):
    def __init__(self):
        super(Verb50, self).__init__(name="Please perform", verb_number=50)

class Verb51(Verb):
    def __init__(self):
        super(Verb51, self).__init__(name="Please mark", verb_number=51)
        
class Verb52(Verb):
    def __init__(self):
        super(Verb52, self).__init__(name="Mark on offset landing site", verb_number=52)
        
class Verb53(Verb):
    def __init__(self):
        super(Verb53, self).__init__(name="Please perform alternate LOS mark", verb_number=53)
        
class Verb54(Verb):
    def __init__(self):
        super(Verb54, self).__init__(name="Request rendezvous backup sighting mark routine (R23)", verb_number=54)
        
class Verb55(Verb):
    def __init__(self):
        super(Verb55, self).__init__(name="Increment AGC time (decimal)", verb_number=55)
        
class Verb56(Verb):
    def __init__(self):
        super(Verb56, self).__init__(name="Terminate tracking (P20)", verb_number=56)
        
class Verb57(Verb):
    def __init__(self):
        super(Verb57, self).__init__(name="Display update state of FULTKFLG", verb_number=57)
        
class Verb58(Verb):
    def __init__(self):
        super(Verb58, self).__init__(name="Enable auto maneuver in P20", verb_number=58)
        
class Verb59(Verb):
    def __init__(self):
        super(Verb59, self).__init__(name="Please calibrate", verb_number=59)

class Verb60(Verb):
    def __init__(self):
        super(Verb60, self).__init__(name="Set astronaut total attitude (N17) to present attitude", verb_number=60)

class Verb61(Verb):
    def __init__(self):
        super(Verb61, self).__init__(name="Display DAP attitude error", verb_number=61)
        
class Verb62(Verb):
    def __init__(self):
        super(Verb62, self).__init__(name="Display total attitude error WRT N22", verb_number=62)
        
class Verb63(Verb):
    def __init__(self):
        super(Verb63, self).__init__(name="Display total astronaut attitude error WRT N17", verb_number=63)
        
class Verb64(Verb):
    def __init__(self):
        super(Verb64, self).__init__(name="Request S-Band antenna routine", verb_number=64)
        
class Verb65(Verb):
    def __init__(self):
        super(Verb65, self).__init__(name="Optical verification of prelaunch alignment", verb_number=65)
        
class Verb66(Verb):
    def __init__(self):
        super(Verb66, self).__init__(name="Vehicles attached, move this vehicle state vector to other vehicle state vector", verb_number=66)
        
class Verb67(Verb):
    def __init__(self):
        super(Verb67, self).__init__(name="Display W Matrix", verb_number=67)
        
#no Verb 68
        
class Verb69(Verb):
    def __init__(self):
        super(Verb69, self).__init__(name="Cause restart", verb_number=69)

class Verb70(Verb):
    def __init__(self):
        super(Verb70, self).__init__(name="Update liftoff time", verb_number=70)

class Verb71(Verb):
    def __init__(self):
        super(Verb71, self).__init__(name="Universal update - block address", verb_number=71)
        
class Verb72(Verb):
    def __init__(self):
        super(Verb72, self).__init__(name="Universal update - single address", verb_number=72)
        
class Verb73(Verb):
    def __init__(self):
        super(Verb73, self).__init__(name="Update AGC time (octal)", verb_number=73)
        
class Verb74(Verb):
    def __init__(self):
        super(Verb74, self).__init__(name="Initialize erasable dump via downlink", verb_number=74)
        
class Verb75(Verb):
    def __init__(self):
        super(Verb75, self).__init__(name="Backup liftoff", verb_number=75)
        
#no verb 76
#no verb 77
        
class Verb78(Verb):
    def __init__(self):
        super(Verb78, self).__init__(name="Update prelaunch azimuth", verb_number=78)
        
#no verb 79

class Verb80(Verb):
    def __init__(self):
        super(Verb80, self).__init__(name="Update LM state vector", verb_number=80)

class Verb81(Verb):
    def __init__(self):
        super(Verb81, self).__init__(name="Update CSM state vector", verb_number=81)
        
class Verb82(Verb):
    def __init__(self):
        super(Verb82, self).__init__(name="Request orbital paramters display (R30)", verb_number=82)
    
    def execute(self):
        #super(Verb82, self).execute()
        computer.routines[30]()
        
        
class Verb83(Verb):
    def __init__(self):
        super(Verb83, self).__init__(name="Request rendezvous paramter display (R31)", verb_number=83)
        

#no verb 84

class Verb85(Verb):
    def __init__(self):
        super(Verb85, self).__init__(name="Request rendezvous paramter display no. 2 (R34)", verb_number=85)
        
class Verb86(Verb):
    def __init__(self):
        super(Verb86, self).__init__(name="Reject rendezvous backup sighting mark", verb_number=86)
        
class Verb87(Verb):
    def __init__(self):
        super(Verb87, self).__init__(name="Set VHF range flag", verb_number=87)
        
class Verb88(Verb):
    def __init__(self):
        super(Verb88, self).__init__(name="Reset VHF range flag", verb_number=88)
        
class Verb89(Verb):
    def __init__(self):
        super(Verb89, self).__init__(name="Request rendezvous final attitude (R63)", verb_number=89)

class Verb90(Verb):
    def __init__(self):
        super(Verb90, self).__init__(name="Request rendezvous out of plane display (R36)", verb_number=90)

class Verb91(Verb):
    def __init__(self):
        super(Verb91, self).__init__(name="Display bank sum", verb_number=91)
        
class Verb92(Verb):
    def __init__(self):
        super(Verb92, self).__init__(name="Operate IMU performance test (P07)", verb_number=92)
        
class Verb93(Verb):
    def __init__(self):
        super(Verb93, self).__init__(name="Enable W Matrix initialization", verb_number=93)
        
class Verb94(Verb):
    def __init__(self):
        super(Verb94, self).__init__(name="Request rendezvous backup sighting mark routine (R23)", verb_number=94)
        
#no verb 95
        
class Verb96(Verb):
    def __init__(self):
        super(Verb96, self).__init__(name="Terminate integration and go to P00", verb_number=96)
        
class Verb97(Verb):
    def __init__(self):
        super(Verb97, self).__init__(name="Perform engine fail procedure", verb_number=97)
        
#no verb 98
        
class Verb99(Verb):
    def __init__(self):
        super(Verb99, self).__init__(name="Please enable engine", verb_number=99)
