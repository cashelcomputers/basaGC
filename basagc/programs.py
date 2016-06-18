#!/usr/bin/env python3
""" This module contains all programs (major modes) used by the guidance computer."""

import inspect
import sys
import math
from collections import OrderedDict


from PyQt5.QtCore import QTimer

from basagc import config
if config.DEBUG:
    from pudb import set_trace  # lint:ok

from basagc import utils, maneuver

from basagc.maneuver import Burn
from basagc import ksp


class Program(object):

    """ Major mode base class.
    """
    computer = None

    def __init__(self, description, number):

        """ Class constructor.
        :param description: description of the program
        :param number: program number
        :return: None
        """
        self.computer = Program.computer
        self.description = description
        self.number = number

    def execute(self):

        """ Executes the program.
        :return: None
        """

        utils.log("Executing Program {}: {}".format(self.number, self.description))
        self.computer.flash_comp_acty(500)
        self.computer.dsky.set_register(self.number, "program")
        self.computer.running_program = self

    def terminate(self):

        """Terminates the program"""

        if self.computer.running_program == self:
            self.computer.running_program = None

    def restart(self):

        """ Restarts the program if required by program alarms.
        :return: None
        """

        self.execute()

    def __str__(self):
        return "Program {} ({}) ".format(self.number, self.description)


class Program00(Program):

    """ AGC Idling.
    :return: None
    """

    def __init__(self):

        """ Class constructor.
        :return: None
        """

        super(Program00, self).__init__(description="AGC Idling", number="00")


class Program01(Program):

    """
    Prelaunch or service - Initialization program

    """
    
    def __init__(self):
        
        """ Class constructor.
        :return: None
        """
        super().__init__(description="Prelaunch or service - Initialization program", number="01")
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

    def execute(self):

        """ Executes the program.
        :return: None
        """
        
        super().execute()
        if not ksp.check_connection():
            Program.computer.poodoo_abort(111)
            self.terminate()
            return
        #Program.computer.imu.on()
        self.timer.start(10000)

    def timeout(self):
        """
        called when timer hits 0
        :returns: None
        """

        #Program.computer.imu.set_fine_align()
        Program.computer.execute_program("02")

class Program02(Program):
    
    def __init__(self):
        
        super().__init__(description="Prelaunch or service - Gyrocompassing program", number="02")
        self.turn_start_altitude = None
        self.turn_end_altitude = None
        self.target_altitude = None
        self.computer = Program.computer
        self.ut_of_launch = 0.0


    def execute(self):
        #set_trace()
        now = ksp.get_telemetry("space_center", "ut")
        self.ut_of_launch = now + 5
        self.computer.noun_data["06"] = 5
        # enable SAS
        ksp.send_command("sas", True)
        self.computer.execute_verb(verb="16", noun="06")
        self.computer.add_to_mainloop(self.countdown_monitor)
        
    def countdown_monitor(self):
        #set_trace()
        now = ksp.get_telemetry("space_center", "ut")
        delta_time = self.ut_of_launch - now
        self.computer.noun_data["06"] = round(delta_time, 2)
        if delta_time <= 0.1:
            print("LIFTOFF!!!!!!1!")
            #set_trace()
            #self.computer.terminate_verb(verb="16")
            self.computer.dsky.current_verb.terminate()
            self.computer.remove_from_mainloop(self.countdown_monitor)
            # Clear display
            for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
                self.computer.dsky.blank_register(register)
            Program.computer.execute_program("11")
        
        
#class Program02(Program):
    #'''
    #Waits until liftoff is detected, blanks display and starts P11
    #'''

    #def __init__(self):
        #
        #""" Class constructor.
        #:return: None
        #"""
        #super().__init__(description="Prelaunch or service - Gyrocompassing program", number="02")
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.timeout)

    #def execute(self):

        #""" Executes the program.
        #:return: None
        #"""
        #super().execute()
        #Program.computer.add_to_mainloop(self.check_for_liftoff)

    #def check_for_liftoff(self):
        #if get_telemetry("verticalSpeed") > 1:
            #utils.log("Liftoff discrete")
            #Program.computer.remove_from_mainloop(self.check_for_liftoff)

            ## Clear display
            #for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
                #Program.computer.dsky.blank_register(register)
            ## pause for 1 second, then run P11
            #self.timer.start(1000)

    #def timeout(self):
        #self.timer.stop()
        #Program.computer.execute_program("11")

class Program11(Program):

    """ Earth Orbit Insertion Monitor.
    :return: None
    """

    def __init__(self):

        """ Class constructor.
        :return: None
        """

        super().__init__(description="Earth Orbit Insertion Monitor", number="11")

    def execute(self):

        """ Executes the program.
        :return: None
        """

        super().execute()
        utils.log("Program 11 executing", log_level="INFO")

        # test if KSP is connected
        #if check_connection() == False:
            #return

        # --> call average G integration with ΔV integration
        # self.computer.run_average_g_routine = True

        # --> terminate gyrocompassing
        if "02" in self.computer.running_programs:
            utils.log("Late termination of P02")
            self.computer.programs["02"].terminate()

        # --> compute initial state vector
        # self.computer.routines["average_g"]()

        # --> Display on DSKY:
        # --> V06 N62 (we are going to use V16N62 though, so we can have a updated display
        # --> R1: Velocity
        # --> R2: Rate of change of vehicle altitude
        # --> R3: Vehicle altitude in km to nearest .1 km
        self.computer.execute_verb(verb="16", noun="62")


class Program15(Program):

    """ Calculates TMI burn
    :return: None
    """

    def __init__(self):

        """ Class constructor.
        :return: None
        """

        super().__init__(description="TMI Calculate", number="15")
        

    def execute(self):

        """ Entry point for the program
        :return: None
        """

        super().execute()
        
        # if no connection to KSP, do P00DOO abort
        #if not check_connection():
            #self.computer.poodoo_abort(111)
            #self.terminate()
            #return
        #
        ## check that orbital parameters are within range to conduct burn
        #is_orbit_ok = maneuver.HohmannTransfer.check_orbital_parameters()
        #if is_orbit_ok == False:
            #self.computer.poodoo_abort(is_orbit_ok[1])
            #return
        
        # get mass
        mass = ksp.get_telemetry("vessel", "mass") / 1000  # in tons
        fractional_part, whole_part  = math.modf(mass)
        Program.computer.noun_data["25"][0] = str(int(whole_part)).zfill(5)
        Program.computer.noun_data["25"][1] = str(int(fractional_part * 100000))
        
        # get thrust
        thrust = ksp.get_telemetry("vessel", "max_thrust") / 1000  # in kN
        fractional_part, whole_part  = math.modf(thrust)
        Program.computer.noun_data["31"][0] = str(int(whole_part)).zfill(5)
        Program.computer.noun_data["31"][1] = str(int(fractional_part * 100000)).zfill(5)

        # get isp
        isp = ksp.get_telemetry("vessel", "specific_impulse")
        Program.computer.noun_data["38"][0] = str(int(isp)).zfill(5)

        # do it!
        self.calculate_maneuver()

    def calculate_maneuver(self):

        """ Calculates the maneuver parameters and creates a Burn object
        :return: Nothing
        """
        self.maneuver = maneuver.HohmannTransfer()
        self.maneuver.execute()
        # display burn parameters and go to poo
        self.computer.execute_verb(verb="06", noun="95")
        self.computer.go_to_poo()

class Program31(Program):
    """
    Mun Orbital Insertion (MOI) burn calculator
    """
    def __init__(self):
        
        """ Class constructor.
        :return: None
        """
        super().__init__(description="MOI Burn Calculator", number="31")
        self.delta_v = Program.computer.moi_burn_delta_v
        self.time_of_node = get_telemetry("timeOfPeriapsisPassage")
        self.time_of_ignition = None

    def update_parameters(self):
        
        self.delta_v = Program.computer.moi_burn_delta_v
        self.time_of_node = get_telemetry("timeOfPeriapsisPassage")

        initial_mass = float(self.computer.noun_data["25"][0] + "." + self.computer.noun_data["25"][1])
        thrust = float(self.computer.noun_data["31"][0] + "." + self.computer.noun_data["31"][1])
        specific_impulse = float(self.computer.noun_data["38"][0])
        self.duration_of_burn = maneuver.calc_burn_duration(initial_mass, thrust, specific_impulse, self.delta_v)
        self.time_of_ignition = self.time_of_node - (self.duration_of_burn / 2)
        
    def execute(self):  # FIXME: this needs to be refactored into something better, just trying to get it working now
        
        self.computer.execute_verb(verb="21", noun="25")
        self.computer.dsky.request_data(requesting_object=self._accept_initial_mass_whole_part, display_location="data_1")
        
    def _accept_initial_mass_whole_part(self, mass):
        Program.computer.noun_data["25"][0] = mass
        self.computer.execute_verb(verb="22", noun="25")
        self.computer.dsky.request_data(requesting_object=self._accept_initial_mass_fractional_part, display_location="data_2")
        
    def _accept_initial_mass_fractional_part(self, mass):
        Program.computer.noun_data["25"][1] = mass
        self.computer.execute_verb(verb="21", noun="31")
        self.computer.dsky.request_data(requesting_object=self._accept_thrust_whole_part, display_location="data_1")

    def _accept_thrust_whole_part(self, thrust):
        Program.computer.noun_data["31"][0] = thrust
        self.computer.execute_verb(verb="22", noun="31")
        self.computer.dsky.request_data(requesting_object=self._accept_thrust_fractional_part, display_location="data_2")

    def _accept_thrust_fractional_part(self, thrust):
        Program.computer.noun_data["31"][1] = thrust
        self.computer.execute_verb(verb="21", noun="38")
        self.computer.dsky.request_data(requesting_object=self._accept_isp, display_location="data_1")

    def _accept_isp(self, isp):
        Program.computer.noun_data["38"][0] = isp
        self.calculate_maneuver()

    def calculate_maneuver(self):
        self.update_parameters()
        self.burn = Burn(delta_v=self.delta_v,
                         direction="retrograde",
                         time_of_ignition=self.time_of_of_ignition,
                         time_of_node=self.time_of_node,
                         calling_program=self)

        # load the Burn object into computer
        self.computer.add_burn_to_queue(self.burn, execute=False)

        ## display burn parameters and go to poo
        self.computer.execute_verb(verb="06", noun="95")
        self.computer.go_to_poo()

class Program40(Program):

    """
    Controls a SPS (Service Propulsion System) burn.
    """
    
    def __init__(self):
        """
        instance constructor.
        :returns: None
        """
        super().__init__(description="SPS Burn", number="40")
        self.burn = self.computer.next_burn

    def execute(self):
        """
        Executes the program
        :returns: None
        """
        super().execute()
        # if TIG < 2 mins away, abort burn
        if utils.seconds_to_time(self.burn.time_until_ignition)["minutes"] < 2:
            self.computer.remove_burn()
            self.computer.poodoo_abort(226)
            return
        # if time to ignition if further than a hour away, display time to ignition
        if utils.seconds_to_time(self.burn.time_until_ignition)["hours"] > 0:
            utils.log("TIG > 1 hour away")
            self.computer.execute_verb(verb="16", noun="33")
            self.computer.main_loop_table.append(self._ten_minute_monitor)
        else:
            utils.log("TIG < 1 hour away, enabling burn")
            self.burn.execute()

    def _ten_minute_monitor(self):
        """
        Part of the sequence of P40
        :returns: None
        """
        if utils.seconds_to_time(self.burn.time_until_ignition)["minutes"] < 10:
            self.computer.main_loop_table.remove(self._ten_minute_monitor)
            self.burn.execute()

    def terminate(self):
        """
        Terminates the program.
        :returns: None
        """
        super().terminate()
        self.burn.terminate()

class ProgramNotImplementedError(Exception):

    """ This exception is raised when the selected program hasn't been implemented yet.
    """

    pass


programs = OrderedDict()
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for class_tuple in clsmembers:
    if class_tuple[0][-1].isdigit():
        programs[class_tuple[0][-2:]] = class_tuple[1]
