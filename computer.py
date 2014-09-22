#!/usr/bin/env python2

import multiprocessing as mp
import logging
import urllib2
import json

import config
import timer
import display
import dsky
import verbs
import nouns
import programs
import lib
import routines

memory_log = logging.getLogger("MEMORY")


class Computer(object):
    def __init__(self, gui):
        self.gui = gui
        self.dsky = dsky.DSKY(self.gui, self)
        self.loop_timer = timer.Timer(interval=0.5, function=self.main_loop)
        self.out_queue = mp.Queue()
        self.in_queue = mp.Queue()
        self.DSPTAB = display.init_DSPTAB()
        self.is_powered_on = False
        self.memory = Memory(self)
        self.state_vector = lib.StateVector()
        self.loop_items = []

        self.state = {
            # "is_powered_on": False,
            # "is_verb": False,
            #"is_noun": False,
            #"display_lock": None,
            #"is_noun_table_initialised": False,
            #"is_verb_table_initialised": False,
            #"interrupt_inhibit": False,
            "alarm_codes": [0, 0, 0],
            "running_programs": [],
            #"running_verb": None,
            "run_average_g_routine": False,
        }

        verbs.memory = self.memory
        verbs.computer = self
        verbs.dsky = self.dsky
        verbs.frame = self.gui
        nouns.memory = self.memory
        nouns.computer = self
        nouns.dsky = self.dsky
        nouns.frame = self.gui
        programs.gc = self
        programs.dsky = self.dsky
        routines.computer = self

        self.nouns = [
            None,
            nouns.noun01,
            nouns.noun02,
            nouns.noun03,
            None,
            nouns.noun05,
            nouns.noun06,
            nouns.noun07,
            nouns.noun08,
            nouns.noun09,
            nouns.noun10,
            nouns.noun11,
            nouns.noun12,
            nouns.noun13,
            nouns.noun14,
            nouns.noun15,
            nouns.noun16,
            nouns.noun17,
            nouns.noun18,
            None,
            nouns.noun20,
            nouns.noun21,
            nouns.noun22,
            None,
            nouns.noun24,
            nouns.noun25,
            nouns.noun26,
            nouns.noun27,
            None,
            nouns.noun29,
            nouns.noun30,
            nouns.noun31,
            nouns.noun32,
            nouns.noun33,
            nouns.noun34,
            nouns.noun35,
            nouns.noun36,  # implemented!
            nouns.noun37,
            nouns.noun38,
            nouns.noun39,
            nouns.noun40,
            nouns.noun41,
            nouns.noun42,
            nouns.noun43,
            nouns.noun44,
            nouns.noun45,
            nouns.noun46,
            nouns.noun47,
            nouns.noun48,
            nouns.noun49,
            nouns.noun50,
            nouns.noun51,
            nouns.noun52,
            nouns.noun53,
            nouns.noun54,
            nouns.noun55,
            nouns.noun56,
            None,
            nouns.noun58,
            nouns.noun59,
            nouns.noun60,
            nouns.noun61,
            nouns.noun62,
            nouns.noun63,
            nouns.noun64,
            nouns.noun65,
            nouns.noun66,
            nouns.noun67,
            nouns.noun68,
            nouns.noun69,
            nouns.noun70,
            nouns.noun71,
            None,
            nouns.noun73,
            nouns.noun74,
            nouns.noun75,
            None,
            None,
            nouns.noun78,
            nouns.noun79,
            nouns.noun80,
            nouns.noun81,
            nouns.noun82,
            nouns.noun83,
            nouns.noun84,
            nouns.noun85,
            nouns.noun86,
            nouns.noun87,
            nouns.noun88,
            nouns.noun89,
            nouns.noun90,
            nouns.noun91,
            nouns.noun92,
            nouns.noun93,
            nouns.noun94,
            nouns.noun95,
            nouns.noun96,
            nouns.noun97,
            nouns.noun98,
            nouns.noun99,
        ]
        self.verbs = [
            None,  # 0
            verbs.Verb1(),  # implemented!
            verbs.Verb2(),  # implemented!
            verbs.Verb3(),  # implemented!
            verbs.Verb4(),  # implemented!
            verbs.Verb5(),  # implemented!
            verbs.Verb6(),  # implemented!
            verbs.Verb7(),
            None,  # 8
            None,  # 9
            None,  # 10
            verbs.Verb11(),
            verbs.Verb12(),
            verbs.Verb13(),
            verbs.Verb14(),
            verbs.Verb15(),
            verbs.Verb16(),
            verbs.Verb17(),
            None,  # 18
            None,  # 19
            None,  # 20
            verbs.Verb21(),
            verbs.Verb22(),
            verbs.Verb23(),
            verbs.Verb24(),
            verbs.Verb25(),
            None,
            verbs.Verb27(),
            None,  # 28
            None,  # 29
            verbs.Verb30(),
            verbs.Verb31(),
            verbs.Verb32(),  # partially implemented
            verbs.Verb33(),  # partially implemented
            verbs.Verb34(),  # partially implemented
            verbs.Verb35(),  # implemented!
            verbs.Verb36(),
            verbs.Verb37(),
            None,  # 38
            None,  # 39
            verbs.Verb40(),
            verbs.Verb41(),
            verbs.Verb42(),
            verbs.Verb43(),
            verbs.Verb44(),
            verbs.Verb45(),
            verbs.Verb46(),
            verbs.Verb47(),
            verbs.Verb48(),
            verbs.Verb49(),
            verbs.Verb50(),
            verbs.Verb51(),
            verbs.Verb52(),
            verbs.Verb53(),
            verbs.Verb54(),
            verbs.Verb55(),
            verbs.Verb56(),
            verbs.Verb57(),
            verbs.Verb58(),
            verbs.Verb59(),
            verbs.Verb60(),
            verbs.Verb61(),
            verbs.Verb62(),
            verbs.Verb63(),
            verbs.Verb64(),
            verbs.Verb65(),
            verbs.Verb66(),
            verbs.Verb67(),
            None,  # 68
            verbs.Verb69(),
            verbs.Verb70(),
            verbs.Verb71(),
            verbs.Verb72(),
            verbs.Verb73(),
            verbs.Verb74(),
            verbs.Verb75(),
            None,  # 76
            None,  # 77
            verbs.Verb78(),
            None,  # 79
            verbs.Verb80(),
            verbs.Verb81(),
            verbs.Verb82(),
            verbs.Verb83(),
            None,  # 84
            verbs.Verb85(),
            verbs.Verb86(),
            verbs.Verb87(),
            verbs.Verb88(),
            verbs.Verb89(),
            verbs.Verb90(),
            verbs.Verb91(),
            verbs.Verb92(),
            verbs.Verb93(),
            verbs.Verb94(),
            None,  # 95
            verbs.Verb96(),
            verbs.Verb97(),
            None,  # 98
            verbs.Verb99(),
        ]
        print(self.verbs[82])
        self.programs = {
            "01": programs.Program01(name="Prelaunch or Service - Initialization Program", number=01),
            "11": programs.Program11(name="Change Program (Major Mode)", number=11),
        }
        self.routines = {
            "average_g": routines.average_g,
            30: routines.routine_30,
        }
        self.option_codes = {
            "00001": "",
            "00002": "",
            "00003": "",
            "00004": "",
            "00007": "",
            "00024": "",
        }

    def on(self):
        self.loop_timer.start()
        self.is_powered_on = True
        for display_item in self.dsky.static_display:
            display_item.on()

    def main_loop(self):
        if self.state["run_average_g_routine"]:
            routines.average_g()
        for item in self.loop_items:
            item()

    def execute_verb(self, verb, noun=None):
        if noun is not None:
            self.dsky.set_noun(noun)
        self.dsky.control_registers["verb"].display(str(verb))
        self.verbs[verb].execute()

    def reset_alarm_codes(self):
        self.state["alarm_codes"][2] = self.state["alarm_codes"][0]
        self.state["alarm_codes"][0] = 0
        self.state["alarm_codes"][1] = 0

    def program_alarm(self, alarm_code, required_action):

        """ sets the program alarm codes in memory and turns the PROG
            annunciator on
            alarm_code should be a 3 or 4 digit octal int
        """
        if required_action == "program_alarm":
            if self.state["alarm_codes"][0] != 0:
                self.state["alarm_codes"][1] = self.state["alarm_codes"][0]
            self.state["alarm_codes"][0] = 1000 + alarm_code
            self.state["alarm_codes"][2] = self.state["alarm_codes"][0]
            self.dsky.annunciators["prog"].on()
        elif required_action == "P00DOO":
            # insert terminate program and goto P00
            print("P00D00 program abort not implemented yet... watch this space...")
        elif required_action == "program_restart":
            # insert terminate and restart program
            print("Program fresh start not implemented yet... watch this space...")
        elif required_action == "computer_restart":
            # insert computer reboot
            #self.fresh_start()
            pass
class Memory(object):
    """This object represents the guidance computer's memory."""

    # memory_log = logging.getLogger("Memory")

    def __init__(self, computer):

        """Constructor for the Memory object."""

        print("Init memory")
        self._init_storage()
        self._init_symbols()
        self.computer = computer

    def _init_symbols(self):
        self.TEPHEM = 0

    def reset(self):

        """ Resets the contents of memory """

        print("Resetting memory contents...")
        self._init_storage()

    def _init_storage(self):

        """ Initialises memory storage """

        self.REFSMMAT_flag = False

        self._storage = {
            "is_paused": MemoryData("Paused", False, "p.paused"),
            "is_rcs": MemoryData("RCS", False, "v.rcsValue"),
            "is_sas": MemoryData("SAS", False, "v.sasValue"),
            "is_lights": MemoryData("Lights", False, "v.lightValue"),
            "ut": MemoryData("Universal Time", 0, "t.universalTime"),
            "relative_velocity": MemoryData("Relative Velocity", 0.0, "o.relativeVelocity"),
            "periapsis": MemoryData("Periapsis", 0.0, "o.PeA"),
            "apoapsis": MemoryData("Apoapsis", 0.0, "o.ApA"),
            "time_to_periapsis": MemoryData("Time To Periapsis", 0.0, "o.timeToPe"),
            "time_to_apoapsis": MemoryData("Time To Apoapsis", 0.0, "o.timeToAp"),
            "inclination": MemoryData("Orbital Inclination", 0.0, "o.inclination"),
            "eccentricity": MemoryData("Orbital Eccentricity", 0.0, "o.eccentricity"),
            "orbital_period": MemoryData("Orbital Period", 0.0, "o.period"),
            "argument_of_periapsis": MemoryData("Argument of Periapsis", 0.0, "o.argumentOfPeriapsis"),
            "time_to_transition_1": MemoryData("Time To Transition One", 0.0, "o.timeToTransition1"),
            "time_to_transition_2": MemoryData("Time To Transition Two", 0.0, "o.timeToTransition2"),
            "semi_major_axis": MemoryData("Semi-Major Axis", 0.0, "o.sma"),
            "longitude_of_ascending_node": MemoryData("Longitude Of Ascending Node", 0.0, "o.lan"),
            "mean_anomaly_at_epoch": MemoryData("Mean Anomaly At Epoch", 0.0, "o.maae"),
            "time_of_periapsis_passage": MemoryData("Time Of Periapsis Passage", 0.0, "o.timeOfPeriapsisPassage"),
            "true_anomaly": MemoryData("True Anomaly", 0.0, "o.trueAnomaly"),
            "temperature": MemoryData("Temperature Sensor", 0, "s.sensor.temp"),
            "gravity": MemoryData("Gravity Sensor", 0, "s.sensor.grav"),
            "pressure": MemoryData("Pressure Sensor", 0, "s.sensor.pres"),
            "acceleration": MemoryData("Acceleration Sensor", 0, "s.sensor.acc"),
            "asl": MemoryData("Altitude Above Sea Level", 0.0, "v.altitude"),
            "agl": MemoryData("Altitude Above Ground Level", 0.0, "v.heightFromTerrain"),
            "terrain_height": MemoryData("Terrain Height", 0.0, "v.terrainHeight"),
            "met": MemoryData("Mission Elapsed Time", 0.0, "v.missionTime"),
            "surface_velocity": MemoryData("Surface Velocity", 0.0, "v.surfaceVelocity"),
            "surface_velocity_x": MemoryData("Surface Velocity X", 0.0, "v.surfaceVelocityx"),
            "surface_velocity_y": MemoryData("Surface Velocity Y", 0.0, "v.surfaceVelocityy"),
            "surface_velocity_z": MemoryData("Surface Velocity Z", 0.0, "v.surfaceVelocityz"),
            "angular_velocity": MemoryData("Angular Velocity", 0.0, "v.angularVelocity"),
            "orbital_velocity": MemoryData("Orbital Velocity", 0.0, "v.orbitalVelocity"),
            "surface_speed": MemoryData("Surface Speed", 0.0, "v.surfaceSpeed"),
            "vertical_speed": MemoryData("Vertical Speed", 0.0, "v.verticalSpeed"),
            "atmo_density": MemoryData("Atmospheric Density", 0.0, "v.atmosphericDensity"),
            "longitude": MemoryData("Longitude", 0.0, "v.long"),
            "latitude": MemoryData("Latitude", 0.0, "v.lat"),
            "dynamic_pressure": MemoryData("Dynamic Pressure", 0.0, "v.dynamicPressure"),
            "name": MemoryData("Vessel Name", "", "v.name"),
            "orbiting_body_name": MemoryData("Orbiting Body Name", "", "v.body"),
            "angle_to_prograde": MemoryData("Angle To Prograde", 0.0, "v.angleToPrograde"),
            "pitch": MemoryData("Pitch", 0.0, "n.pitch"),
            "roll": MemoryData("Roll", 0.0, "n.roll"),
            "yaw": MemoryData("Yaw", 0.0, "n.heading"),
            "raw_pitch": MemoryData("Raw Pitch", 0.0, "n.rawpitch"),
            "raw_roll": MemoryData("Raw Roll", 0.0, "n.rawroll"),
            "raw_yaw": MemoryData("Raw Yaw", 0.0, "n.rawheading"),
        }



    def get_data_from_ksp(self, data):

        """ Contacts KSP for the requested data. Saves the data to storage """

        # for item in data:
        #query_string += item + "=" + self._storage[item].query_string + "&"
        #query_string = query_string[:-1]
        query_string = data + "=" + self._storage[data].query_string
        try:
            raw_response = urllib2.urlopen(config.URL + query_string)
        except urllib2.URLError as e:
            print("Unable to contact KSP, reason: {}".format(e.reason))
            raise KSPNotConnected
        json_response = json.load(raw_response)
        for key, value in json_response.iteritems():
            self._storage[key].set_value(value)
        return json_response

    def get_memory(self, data):

        """Gets the contents of memory as specified by data. data should be a
           list of storage locations"""
        try:
            self.get_data_from_ksp(data)
        except KSPNotConnected:
            self.computer.program_alarm(300, "program_alarm")
            raise
        # return_data = {request: self._storage[request].get_value() for request in data}
        #return return_data
        return self._storage[data].value


class MemoryData(object):
    """ This class represents a individual memory item in gc memory """

    def __init__(self, name, value, query_string):
        """ Class constructor """

        self.name = name
        self.value = value
        self.query_string = query_string

    def set_value(self, new_value):
        """ Memory data setter """

        self.value = new_value

    def get_value(self):
        """ Memory data getter """

        return self.value


class KSPNotConnected(Exception):
    """ This exception should be raised when there is not connection to KSP """
    pass

