#!/usr/bin/env python3
""" This module contains all programs (major modes) used by the guidance computer."""

import inspect
import sys
import math
from collections import OrderedDict

from pudb import set_trace  # lint:ok
from PyQt5.QtCore import QTimer

import basagc.maneuver
from basagc import config

from basagc import utils

from basagc.maneuver import Burn
from basagc.telemachus import get_telemetry, KSPNotConnected, check_connection


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
    
    '''
    Prelaunch or service - Initialization program
    
    '''
    
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
        if check_connection() == False:
            Program.computer.program_alarm(111)
            self.terminate()
            return
        Program.computer.imu.on()
        
            
        self.timer.start(10000)

    def timeout(self):
        '''
        called when timer hits 0
        :returns: None
        '''
        Program.computer.imu.set_fine_align()
        Program.computer.execute_program("02")


class Program02(Program):
    '''
    Waits until liftoff is detected, blanks display and starts P11
    '''

    def __init__(self):
        
        """ Class constructor.
        :return: None
        """
        super().__init__(description="Prelaunch or service - Gyrocompassing program", number="02")
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

    def execute(self):

        """ Executes the program.
        :return: None
        """
        super().execute()
        Program.computer.add_to_mainloop(self.check_for_liftoff)

    def check_for_liftoff(self):
        if get_telemetry("verticalSpeed") > 1:
            utils.log("Liftoff discrete")
            Program.computer.remove_from_mainloop(self.check_for_liftoff)

            # Clear display
            for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
                Program.computer.dsky.blank_register(register)
            # pause for 1 second, then run P11
            self.timer.start(1000)

    def timeout(self):
        self.timer.stop()
        Program.computer.execute_program("11")

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
        try:
            get_telemetry("universalTime")
        except KSPNotConnected:
            self.terminate()
            return

        # --> call average G integration with ΔV integration
        # self.computer.run_average_g_routine = True

        # --> terminate gyrocompassing
        if "02" in self.computer.running_programs:
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
        # sequence of events:
        # V37E15E
        # Flashing V01N30 displays target octal ID
        # PRO to accept, V21 to change
        # Display blanks for 5 seconds at TIG - 105 seconds
        # Display V16N95
        # at TIG - 10 seconds: Flashing V99
        # if proceed: execute maneuver

        # FIXME: this program should only *calculate* the maneuver, the actual execution of the burn should be
        # FIXME: performed by P40

        # TODO: scale final altitude based on crafts TWR
        # TODO: request twr from user

        super().__init__(description="TMI Calculate", number="15")
        self.delta_v_first_burn = 0.0
        self.time_to_transfer = 0.0
        self.orbiting_body = None
        self.phase_angle_required = 0.0
        self.time_of_ignition_first_burn = 0.0
        self.delta_time_to_burn = 0.0
        self.phase_angle_difference = 0.0
        self.target_name = ""
        self.departure_body = None
        self.departure_altitude = 0
        self.destination_altitude = 0
        self.grav_param = 0.0
        self.orbital_period = 0
        self.departure_body_orbital_period = 0
        self.first_burn = None
        self.second_burn = None

    def execute(self):

        """ Entry point for the program
        :return: None
        """

        super().execute()
        
        # if no connection to KSP, do P00DOO abort
        if not check_connection():
            self.computer.poodoo_abort(111)
            self.terminate()
            return
        self.departure_body = get_telemetry("body")
        self.orbiting_body = get_telemetry("body")

        
        # check that orbital parameters are within range to conduct burn
        if not self._check_orbital_parameters():
            return
        self.target_name = self._check_target()
        
        #self.computer.noun_data["30"] = config.OCTAL_BODY_NAMES[self.target_name]
        self.computer.execute_verb(verb="01", noun="30")
        self.computer.dsky.request_data(requesting_object=self._accept_target_input, display_location="data_1",
                             is_proceed_available=True)

    def terminate(self):
        '''
        Terminates the program.
        :returns: None
        '''

        utils.log("Removing burn data", log_level="DEBUG")
        self.computer.remove_burn(self.first_burn)
        self.computer.remove_burn(self.second_burn)
        super().terminate()

    def _accept_target_input(self, target):

        """ Called by P15 after user as entered target choice.
        :param target: string of octal target code
        :return: None
        """

        if target == "proceed":
            self.target_name = self.target_name.lstrip("0")
        elif target[0] == ("+" or "-"):
            self.computer.operator_error("Expected octal input, decimal input provided")
            self.execute()
            return
        #elif target not in list(config.OCTAL_BODY_IDS.values()):
            #utils.log("{} {} is not a valid target".format(target, type(target)))
            #self.computer.poodoo_abort(223, message="Target not valid")
            #return TODO: add this back in
        else:
            self.target_name = config.OCTAL_BODY_IDS[target.lstrip("0")]
        # calculate the maneuver and add recalculation job to gc main loop
        self.calculate_maneuver()

    def calculate_maneuver(self):

        """ Calculates the maneuver parameters and creates a Burn object
        :return: Nothing
        """

        # load target
        telemachus_target_id = config.TELEMACHUS_BODY_IDS[self.target_name]
        target_apoapsis = float(get_telemetry("body_ApA", body_number=telemachus_target_id))

        # set destination altitude
        # self.destination_altitude = 11400000  # for impact
        self.destination_altitude = 15000000

        # obtain parameters to calculate burn
        self.departure_altitude = get_telemetry("altitude")
        self.orbital_period = get_telemetry("period")
        self.departure_body_orbital_period = get_telemetry("body_period", body_number=config.TELEMACHUS_BODY_IDS[
            "Kerbin"])
        self.grav_param = get_telemetry("body_gravParameter", body_number=config.TELEMACHUS_BODY_IDS[
            self.orbiting_body])
        current_phase_angle = get_telemetry("body_phaseAngle", body_number=telemachus_target_id)

        # calculate the first and second burn Δv parameters
        self.delta_v_first_burn, self.computer.moi_burn_delta_v = basagc.maneuver.calculate_delta_v_hohmann(self.departure_altitude,
                                                                                                 self.destination_altitude)

        # calculate the time to complete the Hohmann transfer
        self.time_to_transfer = basagc.maneuver.time_to_transfer(self.departure_altitude, self.destination_altitude,
                                                                 self.grav_param)

        # calculate the correct phase angle for the start of the burn
        # note that the burn impulse is calculated as a instantaneous burn, to be correct the burn should be halfway
        # complete at this calculated time

        self.phase_angle_required = basagc.maneuver.phase_angle(self.departure_altitude, self.destination_altitude,
                                                                self.grav_param)

        # calculate the current difference in phase angle required and current phase angle
        self.phase_angle_difference = current_phase_angle - self.phase_angle_required
        # if self.phase_angle_difference < 0:
        #     self.phase_angle_difference = 180 + abs(self.phase_angle_difference)

        # calculate time of ignition (TIG) HOW MANY SECONDS IN FUTURE
        self.delta_time_to_burn = self.phase_angle_difference / ((360 / self.orbital_period) -
                                                                 (360 / self.departure_body_orbital_period))
        print("FFFF" + str(self.delta_time_to_burn))

        # if the time of ignition is less than 120 seconds in the future, schedule the burn for next orbit
        if self.delta_time_to_burn <= 120:
            utils.log("Time of ignition less that 2 minutes in the future, starting burn during next orbit")
            self.delta_time_to_burn += get_telemetry("period")

        #calculate the universal time of node
        self.time_of_node = get_telemetry("universalTime") + self.delta_time_to_burn
        # convert the raw value in seconds to HMS
        delta_time = utils.seconds_to_time(self.delta_time_to_burn)

        # log the maneuver calculations
        utils.log("P15 calculations:")
        utils.log("Phase angle required: {}, Δv for burn: {} m/s, time to transfer: {}".format(
            round(self.phase_angle_required, 2),
            int(self.delta_v_first_burn),
            utils.seconds_to_time(self.time_to_transfer)))
        utils.log("Current Phase Angle: {:.2f}, difference: {:.2f}".format(
            current_phase_angle,
            self.phase_angle_difference))
        print(get_telemetry("universalTime") + self.delta_time_to_burn)
        utils.log("Time to burn: {} hours, {} minutes, {} seconds".format(
            int(delta_time["hours"]),
            int(delta_time["minutes"]),
            delta_time["seconds"]))

        self.duration_of_burn = self.burn_time()
        self.time_of_ignition = self.time_of_node - (self.duration_of_burn / 2)
        
        print(self.time_of_ignition_first_burn)
        # create a Burn object for the outbound burn
        self.first_burn = Burn(delta_v=self.delta_v_first_burn,
                               direction="prograde",
                               time_of_ignition=self.time_of_ignition,
                               time_of_node=self.time_of_node,
                               calling_program=self)


        
        # load the Burn object into computer
        self.computer.add_burn_to_queue(self.first_burn, execute=False)

        # display burn parameters and go to poo
        self.computer.execute_verb(verb="06", noun="95")
        # self.computer.go_to_poo()

    def burn_time(self):
        initial_mass_str = self.computer.noun_data["25"][0] + "." + self.computer.noun_data["25"][1]
        initial_mass = float(initial_mass_str)
        thrust_string = self.computer.noun_data["31"][0] + "." + self.computer.noun_data["31"][1]
        thrust = float(thrust_string)
        specific_impulse = float(self.computer.noun_data["38"][0])
        exhaust_velocity = specific_impulse * 9.81
        delta_v = self.delta_v_first_burn
        burn_duration = (initial_mass * exhaust_velocity / thrust) * (1 - math.exp(-delta_v / exhaust_velocity))
        print()
        print("-" * 40)
        print("Initial mass: {} tonnes".format(initial_mass))
        print("Thrust: {} kN".format(thrust))
        print("Specific Impulse: {} seconds".format(specific_impulse))
        print("Exhaust Velocity: {:.2f} kg/s".format(exhaust_velocity))

        print("Burn Duration: {:.1f} seconds".format(burn_duration))
        return burn_duration
        
    
    def recalculate_phase_angles(self):
    
        """ This function is to be placed in the GC main loop to recalculate maneuver parameters.
        :return: nothing
        """
    
        # update current phase angle
        telemachus_body_id = config.TELEMACHUS_BODY_IDS[config.OCTAL_BODY_NAMES[self.target_name]]
        current_phase_angle = get_telemetry("body_phaseAngle",
                                            body_number=telemachus_body_id)
    
        # recalculate phase angle difference
        phase_angle_difference = current_phase_angle - self.phase_angle_required
        if phase_angle_difference < 0:
            phase_angle_difference = 180 + abs(phase_angle_difference)
        self.delta_time_to_burn = phase_angle_difference / ((360 / self.orbital_period) - (360 / self.departure_body_orbital_period))
        print(self.delta_time_to_burn)
        # delta_time = utils.seconds_to_time(self.delta_time_to_burn)
        # velocity_at_cutoff = get_telemetry("orbitalVelocity") + self.delta_v_first_burn

    def _check_orbital_parameters(self):

        """ Checks to see if current orbital parameters are within an acceptable range to plot maneuver
        :return: Bool
        """

        # check if orbit is circular
        if get_telemetry("eccentricity") > 0.003:
            self.computer.poodoo_abort(224)
            return False

        # check if orbit is excessively inclined
        target_inclination = get_telemetry("target_inclination")
        vessel_inclination = get_telemetry("inclination")
        if (vessel_inclination > (target_inclination - 0.5)) and (vessel_inclination > (target_inclination + 0.5)):
            self.computer.poodoo_abort(225)
            return False
        else:
            return True

    def _check_target(self):

        """Checks if a target exists, it not, returns the default target, else returns the selected target number
        Returns: octal target code
        :rtype: str

        """

        if get_telemetry("target_name") == "No Target Selected.":
            utils.log("No target selected in KSP, defaulting to Mun", log_level="WARNING")
            return "Mun"
        else:
            return get_telemetry("target_name")

class Program40(Program):
    
    '''
    Controls a SPS (Service Propulsion System) burn.
    '''
    
    def __init__(self):
        '''
        instance constructor.
        :returns: None
        '''
        super().__init__(description="SPS Burn", number="40")
        self.burn = self.computer.next_burn

    def execute(self):
        '''
        Executes the program
        :returns: None
        '''
        super().execute()
        # if TIG < 2 mins away, abort burn
        if utils.seconds_to_time(self.burn.time_until_ignition)["minutes"] < 2:
            self.computer.remove_burn(self.computer.next_burn)
            self.computer.poodoo_abort(226)
            return
        # if time to ignition if further than a hour away, display time to ignition
        print(self.burn.time_until_ignition)
        if utils.seconds_to_time(self.burn.time_until_ignition)["hours"] > 0:
            utils.log("TIG > 1 hour away")
            self.computer.execute_verb(verb="16", noun="33")
            self.computer.main_loop_table.append(self._ten_minute_monitor)
        else:
            utils.log("TIG < 1 hour away, enabling burn")
            self.burn.execute()

    def _ten_minute_monitor(self):
        '''
        Part of the sequence of P40
        :returns: None
        '''
        if utils.seconds_to_time(self.burn.time_until_ignition)["minutes"] < 10:
            self.computer.main_loop_table.remove(self._ten_minute_monitor)
            self.burn.execute()

    def terminate(self):
        '''
        Terminates the program.
        :returns: None
        '''
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
