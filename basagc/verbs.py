#!/usr/bin/env python3
""" This module contains classes of all of the verbs used by basaGC."""
from pudb import set_trace

import inspect
import logging
import sys
from collections import OrderedDict

from PyQt5.QtCore import QTimer

from basagc import config, nouns, programs, utils, dsky
from basagc.telemachus import KSPNotConnected, TelemetryNotAvailable

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


class NounNotAcceptableError(Exception):

    """ This exception is raised when the noun selected is not available with the verb selected."""
    pass

# ------------------------BEGIN BASE CLASS DEFINITIONS---------------------------
class Verb:

    """ Base class for verbs
    """
    
    computer = None
    
    def __init__(self, name, verb_number, noun=None):

        """ Class constructor.
        :param name: the name (or description) of the verb
        :type name: string
        :param verb_number: the number of the verb. Valid ranges are 01 to 99 with some verb numbers not used
        :type verb_number: str
        """
        
        self.computer = Verb.computer
        self.dsky = dsky.DSKY.dsky_instance
        self.name = name
        self.number = verb_number
        self.illegal_nouns = []
        self.data = []
        self.noun = noun

    def _format_output_data(self, data):

        """ Formats data for output to the DSKY.
        :param data: data to display
        :type data: dict
        :return: DSKY formatted output
        :rtype: list of strings
        """

        raw_data = [data[1], data[2], data[3]]
        out_data = []
        for item in raw_data:
            if not item:
                continue
            output = ""
            if data["is_octal"]:
                output = "b"
                output += item.zfill(5)
            elif item[0] == "-":
                output += item.zfill(6)
            elif item[0].isdigit():
                output = "+"
                output += item.zfill(5)
            out_data.append(output)
        return out_data

    def execute(self):

        """ Executes the verb
        :return:
        """

        if self.noun in self.illegal_nouns:
            raise NounNotAcceptableError
        utils.log("Executing Verb {}: {}".format(self.number, self.name))
        self.dsky.current_verb = self

    # def _activity(self, event):
    #
    #     """ Flashes the COMP ACTY annunciator. Not currently used.
    #     :param event:
    #     :return:
    #     """
    #
    #     #dsky.flash_comp_acty()
    #     pass

    def terminate(self):

        """ Terminates the verb
        """

        Verb.computer.dsky.current_verb = None

    def receive_data(self, data):

        """ Allows the verb to receive requested data from the DSKY.
        :param data: the data sent by DSKY
        """

        utils.log("{} received data: {}".format(self, data))
        self.data = data
        self.execute()


class ExtendedVerb(Verb):

    """ Base class for extended verbs (40 through 99 inclusive)
    """

    def __init__(self, name, verb_number):
        super(ExtendedVerb, self).__init__(name, verb_number, noun=None)


class DataVerb(Verb):

    """ Base class for Data verbs
    """

    def __init__(self, name, verb_number, noun):

        """ Class constructor
        :param name: name (description) of verb
        :type name: string
        :param verb_number: the verb number
        :type verb_number: str
        :return: None
        """

        super(DataVerb, self).__init__(name, verb_number, noun)
        self.noun = noun


class DisplayVerb(DataVerb):

    """ Base class for display verbs (verbs 01 through 07 inclusive)
    """

    def __init__(self, name, verb_number, noun):

        """ Class constructor
        :param name: name (description) of verb
        :type name: string
        :param verb_number: the verb number
        :type verb_number: str
        :return: None
        """

        super(DisplayVerb, self).__init__(name, verb_number, noun)

    def execute(self):

        """ Executes the verb
        :return: None
        """

        super(DisplayVerb, self).execute()



class MonitorVerb(DisplayVerb):

    """ Base class for Monitor verbs (verbs 11 through 17 inclusive)
    """

    def __init__(self, name, verb_number, noun):

        super(MonitorVerb, self).__init__(name, verb_number, noun)
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_display)
        self.is_tooltips_set = False

    def _send_output(self):

        """ Sends the requested output to the DSKY """

        # check if the display update interval needs to be changed
        if self.timer.interval() != config.DISPLAY_UPDATE_INTERVAL:
            # stop and start the timer to change the update interval
            self.timer.stop()
            self.timer.start(config.DISPLAY_UPDATE_INTERVAL)

        if self.noun is None:
            self.noun = Verb.computer.dsky.requested_noun
        if self.noun in self.illegal_nouns:
            raise NounNotAcceptableError
        noun_function = Verb.computer.nouns[self.noun]()
        try:
            data = noun_function.return_data()
        except nouns.NounNotImplementedError:
            self.computer.operator_error("Noun {} not implemented yet. Sorry about that...".format(dsky.requested_noun))
            self.terminate()
            return
        except KSPNotConnected:
            utils.log("KSP not connected, terminating V{}".format(self.number),
                      log_level="ERROR")
            Verb.computer.program_alarm(110)
            self.terminate()
            raise
        except TelemetryNotAvailable:
            utils.log("Telemetry not available, terminating V{}".format(self.number),
                      log_level="ERROR")
            Verb.computer.program_alarm(111)
            self.terminate()
            raise
        if not data:
            # if the noun returns False, the noun *should* have already raised a program alarm, so we just need to
            # terminate and return
            self.terminate()
            return
        output = self._format_output_data(data)
        
        # set tooltips
        if not self.is_tooltips_set:
            Verb.computer.dsky.data_registers[1].set_tooltip(data["tooltips"][0])
            Verb.computer.dsky.data_registers[2].set_tooltip(data["tooltips"][1])
            Verb.computer.dsky.data_registers[3].set_tooltip(data["tooltips"][2])
            self.is_tooltips_set = True

        # display data on DSKY registers
        for index, display_line in enumerate(output, start=1):
            Verb.computer.dsky.data_registers[index].display(display_line)

        dsky.flash_comp_acty()

    def start_monitor(self):

        """ Starts the timer to monitor the verb """

        # if dsky.backgrounded_update is not None:
        #     dsky.backgrounded_update.terminate()
        dsky.display_lock = self

        try:
            self._send_output()
        except KSPNotConnected:
            return
        except TelemetryNotAvailable:
            return

        self.timer.start(config.DISPLAY_UPDATE_INTERVAL)

    def execute(self):
        super(MonitorVerb, self).execute()

    def _update_display(self):

        """ a simple wrapper to call the display update method """

        # if not self.activity_timer.active():
        #     self.activity_timer.Start(1000)
        self._send_output()

    def terminate(self):

        """ Terminates the verb
        :return: None
        """

        utils.log("Terminating V{}".format(self.number))
        dsky.annunciators["key_rel"].off()
        dsky.display_lock = None
        # dsky.backgrounded_update = None
        self.timer.stop()
        self.noun = None
        # self.activity_timer.Stop()
        # reset tooltips to ""
        Verb.computer.dsky.data_registers[1].set_tooltip("")
        Verb.computer.dsky.data_registers[2].set_tooltip("")
        Verb.computer.dsky.data_registers[3].set_tooltip("")

    def background(self):

        """ Backgrounds verb display updates
        :return: None
        """

        dsky.backgrounded_update = self
        dsky.display_lock = None
        self.timer.stop()
        dsky.annunciators["key_rel"].start_blink()

    def resume(self):

        """ Resumes verb display updates
        :return: None
        """

        dsky.display_lock = self
        dsky.backgrounded_update = None
        dsky.control_registers["verb"].display(self.number)
        dsky.control_registers["noun"].display(self.noun)
        self.start_monitor()


class LoadVerb(DataVerb):

    """ Base class for Load verbs (verbs 21 through 25 inclusive)
    """

    def __init__(self, name, verb_number, noun):
        """ Class constructor
        :param name: name (description) of verb
        :type name: string
        :param verb_number: the verb number
        :type verb_number: int
        :return: None
        """

        super(LoadVerb, self).__init__(name, verb_number, noun)

    def accept_input(self, data):
        """ Accepts data provided by user via DSKY
        :param data: the data
        :return: None
        """
        Verb.computer.noun_data[self.noun].append(data)

        utils.log(data)

#---------------------------BEGIN VERB CLASS DEFINITIONS------------------------

# no verb 00


class Verb01(DisplayVerb):

    """ Displays Octal component 1 in R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb01, self).__init__(name="Display Octal component 1 in R1", verb_number="01", noun=noun)
        
    def execute(self):

        super(Verb01, self).execute()
        noun_function = Verb.computer.nouns[self.noun]()
        noun_data = noun_function.return_data()
        if noun_data is False:
            # No data returned from noun, noun should have raised a program alarm, all we need to do it quit here
            return
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.set_register(output[0], "data_1")
        #Verb.computer.dsky.data_registers[1].display(output[0])


class Verb02(DisplayVerb):

    """ Displays Octal component 2 in R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb02, self).__init__(name="Display Octal component 2 in R1", verb_number="02", noun=noun)

    #def execute(self):
        #super(Verb2, self).execute()
        #if self.data == None:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #noun_function(calling_verb=self, base=8)
            #return
        #else:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #self.noun_data = noun_function(calling_verb=self, data=self.data, base=8)
            #output = _format_output_data(self.noun_data)
            #computer.dsky.data_registers[1].display(output[2], output[3])
            #self.data = None


class Verb03(DisplayVerb):

    """ Displays Octal component 3 in R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb03, self).__init__(name="Display Octal component 3 in R1", verb_number="03", noun=noun)

    #def execute(self):
        #super(Verb3, self).execute()
        #if self.data == None:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #noun_function(calling_verb=self, base=8)
            #return
        #else:
            #noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
            #self.noun_data = noun_function(calling_verb=self, data=self.data, base=8)
            #output = _format_output_data(self.noun_data)
            #computer.dsky.data_registers[1].display(output[4], output[5])
            #self.data = None


class Verb04(DisplayVerb):

    """ Displays Octal components 1, 2 in R1, R2
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb04, self).__init__(name="Display Octal components 1, 2 in R1, R2", verb_number="04", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        super(Verb04, self).execute()
        noun_function = Verb.computer.nouns[Verb.computer.dsky.state["requested_noun"]]
        noun_data = noun_function(calling_verb=self)
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.data_registers[1].display(output[0])
        Verb.computer.dsky.data_registers[2].display(output[1])


class Verb05(DisplayVerb):

    """ Displays Octal components 1, 2, 3 in R1, R2, R3
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb05, self).__init__(name="Display Octal components 1, 2, 3 in R1, R2, R3", verb_number="05", noun=noun)
        self.illegal_nouns = []

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        super(Verb05, self).execute()
        noun_function = Verb.computer.nouns[Verb.computer.dsky.requested_noun]()
        noun_data = noun_function.return_data()
        if not noun_data:
            # No data returned from noun, noun should have raised a program alarm, all we need to do it quit here
            return
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.data_registers[1].display(output[0])
        Verb.computer.dsky.data_registers[2].display(output[1])
        Verb.computer.dsky.data_registers[3].display(output[2])


class Verb06(DisplayVerb):

    """ Displays Decimal in R1 or in R1, R2 or in R1, R2, R3
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb06, self).__init__(name="Display Decimal in R1 or in R1, R2 or in R1, R2, R3", verb_number="06",
                                    noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        super(Verb06, self).execute()
        noun_function = Verb.computer.nouns[self.noun]()
        noun_data = noun_function.return_data()
        if not noun_data:
            # No data returned from noun, noun should have raised a program alarm, all we need to do it quit here
            return
        output = self._format_output_data(noun_data)
        print(noun_data["tooltips"][0])
        Verb.computer.dsky.set_tooltip("data_1", noun_data["tooltips"][0])
        Verb.computer.dsky.set_tooltip("data_2", noun_data["tooltips"][1])
        Verb.computer.dsky.set_tooltip("data_3", noun_data["tooltips"][2])

        Verb.computer.dsky.set_register(output[0], "data_1")
        Verb.computer.dsky.set_register(output[1], "data_2")
        Verb.computer.dsky.set_register(output[2], "data_3")

        # if self.data is None:
        #     noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
        #     noun_function(calling_verb=self, base=10)
        #     return
        # else:
        #     noun_function = computer.nouns[computer.dsky.state["requested_noun"]]
        #     noun_data = noun_function()
        #     output = _format_output_data(noun_data)
        #     computer.dsky.data_registers[1].display(sign=output[0], value=output[1])
        #     computer.dsky.data_registers[2].display(sign=output[2], value=output[3])
        #     computer.dsky.data_registers[3].display(sign=output[4], value=output[5])
            #self.data = None


# class Verb07(DisplayVerb):
# 
#     """ Displays Double Precision Decimal in R1, R2 (test only)
#     """
# 
#     def __init__(self, noun):
# 
#         """ Class constructor
#         :return: None
#         """
# 
#         super(Verb07, self).__init__(name="Display Double Precision Decimal in R1, R2 (test only)", verb_number="07",
#                                     noun=noun)

# no verb 8

# no verb 9

# no verb 10


class Verb11(MonitorVerb):

    """ Monitors Octal component 1 in R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb11, self).__init__(name="Monitor Octal component 1 in R1", verb_number="11", noun=noun)


class Verb12(MonitorVerb):

    """ Monitors Octal component 2 in R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb12, self).__init__(name="Monitor Octal component 2 in R1", verb_number="12", noun=noun)


class Verb13(MonitorVerb):

    """ Monitors Octal component 3 in R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb13, self).__init__(name="Monitor Octal component 3 in R1", verb_number="13", noun=noun)


class Verb14(MonitorVerb):

    """ Monitors Octal components 1, 2 in R1, R2
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb14, self).__init__(name="Monitor Octal components 1, 2 in R1, R2", verb_number="14", noun=noun)


class Verb15(MonitorVerb):

    """ Monitors Octal components 1, 2, 3 in R1, R2, R3
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb15, self).__init__(name="Monitor Octal components 1, 2, 3 in R1, R2, R3", verb_number="15", noun=noun)


class Verb16(MonitorVerb):

    """ Monitors Decimal in R1 or in R1, R2 or in R1, R2, R3
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb16, self).__init__(name="Monitor Decimal in R1 or in R1, R2 or in R1, R2, R3", verb_number="16",
                                     noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """
        super(Verb16, self).execute()
        self.start_monitor()


class Verb17(MonitorVerb):

    """ Monitors Double Precision Decimal in R1, R2 (test only)
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb17, self).__init__(name="Monitor Double Precision Decimal in R1, R2 (test only)", verb_number="17",
                                     noun=noun)

# no verb 18

# no verb 19

# no verb 20


class Verb21(LoadVerb):

    """ Loads component 1 into R1
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb21, self).__init__(name="Load component 1 into R1", verb_number="21", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        dsky.request_data(self.accept_input, dsky.data_registers[1])

    # def accept_input(self, data):
    #
    #     """ Accepts data provided by user via DSKY
    #     :param data: the data
    #     :return: None
    #     """
    #     Verb.computer.noun_data[self.noun].append(data)
    #
    #     utils.log(data)


class Verb22(LoadVerb):

    """ Loads component 2 into R2
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb22, self).__init__(name="Load component 2 into R2", verb_number="22", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        dsky.request_data(self.accept_input, dsky.data_registers[2])


class Verb23(LoadVerb):

    """ Loads component 3 into R3
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb23, self).__init__(name="Load component 3 into R3", verb_number="23", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        Verb.computer.dsky.request_data(requesting_object=self.accept_input, display_location=dsky.data_registers[3])

    def accept_input(self, data):

        """ Accepts data provided by user via DSKY
        :param data: the data
        :return: None
        """

        Verb.computer.loaded_data["verb"] = self.number
        Verb.computer.loaded_data["noun"] = dsky.current_noun
        Verb.computer.loaded_data[3] = data
        if Verb.computer.object_requesting_data:
            Verb.computer.object_requesting_data()


class Verb24(LoadVerb):

    """ Loads component 1, 2 into R1, R2
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb24, self).__init__(name="Load component 1, 2 into R1, R2", verb_number="24", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        pass


class Verb25(LoadVerb):

    """ Loads component 1, 2, 3 into R1, R2, R3
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb25, self).__init__(name="Load component 1, 2, 3 into R1, R2, R3", verb_number="25", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        pass
#
# # no verb 26
#
# class Verb27(LoadVerb):
#     def __init__(self):
#         super(Verb27, self).__init__(name="Display fixed telemetry", verb_number=27, components=(1,), registers=(1,))

# no verb 28

# no verb 29

# class Verb30(Verb):
#     def __init__(self):
#         super(Verb30, self).__init__(name="Request Executive", verb_number=30)
#
# class Verb31(Verb):
#     def __init__(self):
#         super(Verb31, self).__init__(name="Request waitlist", verb_number=31)


class Verb32(Verb):

    """ Recycle program
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb32, self).__init__(name="Recycle program", verb_number="32", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        if isinstance(dsky.state["backgrounded_update"], MonitorVerb):
            dsky.state["backgrounded_update"].terminate()  # TODO
        else:
            utils.log("V32 called, but nothing to recycle!")


class Verb33(Verb):

    """ Proceed without DSKY inputs
    """

    def __init__(self, noun):

        """ Class constructor
            :return: None
            """

        super(Verb33, self).__init__(name="Proceed without DSKY inputs", verb_number="33", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        if isinstance(dsky.state["backgrounded_update"], MonitorVerb):
            dsky.state["backgrounded_update"].terminate()
        else:
            utils.log("V33 called, but nothing to proceed with!")


class Verb34(Verb):

    """ Terminate function
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb34, self).__init__(name="Terminate function", verb_number="34", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        if dsky.backgrounded_update:
            utils.log("Terminating backgrounded update")
            dsky.backgrounded_update.terminate()
            if dsky.annunciators["key_rel"].blink_timer.active():
                dsky.annunciators["key_rel"].stop_blink()
        if Verb.computer.running_program:
            utils.log("Terminating active program {}".format(Verb.computer.running_program.number))
            # have to use try block to catch and ignore expected ProgramTerminated exception
            try:
                Verb.computer.running_program.terminate()
            except programs.ProgramTerminated:
                pass
        else:
            utils.log("V34 called, but nothing to terminate!")


class Verb35(Verb):

    """Lamp test"""

    def __init__(self):

        """ Class constructor
        :return: None
        """

        super(Verb35, self).__init__(name="Test lights", verb_number="35")
        self.flash_timer = QTimer()

    def execute(self):

        """ Executes the verb.
        :return: None
        """
        # commands the annunciators

        for annunciator in self.dsky.annunciators.values():
            annunciator.on()
        # commands the data registers
        for register in ["1", "2", "3"]:
            self.dsky.set_register(value="+88888", register="data_{}".format(register))
        # commands the control registers
        for register in ["verb", "noun", "program"]:
            self.dsky.set_register(value="88", register=register)
        # blinks the verb/noun registers
        self.dsky.verb_noun_flash_on()
        self.dsky.annunciators["opr_err"].start_blink()
        self.dsky.annunciators["key_rel"].start_blink()
        self.flash_timer.singleShot(5000, self.terminate)
        self.computer.flash_comp_acty(500)
        
    def terminate(self):
        
        for annunciator in self.dsky.annunciators.values():
            annunciator.off()
        self.dsky.verb_noun_flash_off()
        self.dsky.set_register("88", "verb")
        self.dsky.set_register("88", "noun")
        self.dsky.annunciators["opr_err"].stop_blink()
        self.dsky.annunciators["key_rel"].stop_blink()
        self.dsky.set_register(value="bb", register="program")
        self.computer.remove_job(self)
        

class Verb36(Verb):

    """ Request fresh start
    """

    def __init__(self, noun):

        """ Class constructor
        :return: None
        """

        super(Verb36, self).__init__(name="Request fresh start", verb_number="36", noun=noun)

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        Verb.computerfresh_start()


class Verb37(Verb):

    """ Change program (Major Mode)
    """

    def __init__(self):

        """ Class constructor
        :return: None
        """

        super(Verb37, self).__init__(name="Change program (Major Mode)", verb_number="37")

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        super(Verb37, self).execute()
        self.dsky.request_data(requesting_object=self.receive_data, display_location="noun")

    def receive_data(self, data):

        """ Accepts data provided by user via DSKY
        :param data: the data from DSKY
        :return: None
        """
        if len(data) != 2:
            self.computer.operator_error("Expected exactly two digits, received {} digits".format(len(data)))
            self.terminate()
            return
        Verb.computer.execute_program(data)

#-------------------------------BEGIN EXTENDED VERBS----------------------------

# class Verb40(Verb):
#     def __init__(self):
#         super(Verb40, self).__init__(name="Zero CDUs", verb_number=40)
#
#     def execute(self):
#         pass
#
# class Verb41(Verb):
#     def __init__(self):
#         super(Verb41, self).__init__(name="Coarse align CDUs", verb_number=41)
#
#     def execute(self):
#         pass
#
# class Verb42(Verb):
#     def __init__(self):
#         super(Verb42, self).__init__(name="Fine align IMU", verb_number=42)
#
# class Verb43(Verb):
#     def __init__(self):
#         super(Verb43, self).__init__(name="Load IMU attitude error meters (test only)", verb_number=43)
#
# class Verb44(Verb):
#     def __init__(self):
#         super(Verb44, self).__init__(name="Set surface flag", verb_number=44)
#
# class Verb45(Verb):
#     def __init__(self):
#         super(Verb45, self).__init__(name="Reset surface flag", verb_number=45)
#
# class Verb46(Verb):
#     def __init__(self):
#         super(Verb46, self).__init__(name="Establish G&C control", verb_number=46)
#
# class Verb47(Verb):
#     def __init__(self):
#         super(Verb47, self).__init__(name="Move LM state vector into CM state vector", verb_number=47)
#
# class Verb48(Verb):
#     def __init__(self):
#         super(Verb48, self).__init__(name="Request DAP data load (R03)", verb_number=48)
#
# class Verb49(Verb):
#     def __init__(self):
#         super(Verb49, self).__init__(name="Request crew defined maneuver (R62)", verb_number=49)
#
# class Verb50(Verb):
#     def __init__(self):
#         super(Verb50, self).__init__(name="Please perform", verb_number=50)
#
# class Verb51(Verb):
#     def __init__(self):
#         super(Verb51, self).__init__(name="Please mark", verb_number=51)
#
# class Verb52(Verb):
#     def __init__(self):
#         super(Verb52, self).__init__(name="Mark on offset landing site", verb_number=52)
#
# class Verb53(Verb):
#     def __init__(self):
#         super(Verb53, self).__init__(name="Please perform alternate LOS mark", verb_number=53)
#
# class Verb54(Verb):
#     def __init__(self):
#         super(Verb54, self).__init__(name="Request rendezvous backup sighting mark routine (R23)", verb_number=54)
#
# class Verb55(Verb):
#     def __init__(self):
#         super(Verb55, self).__init__(name="Increment AGC time (decimal)", verb_number=55)
#
# class Verb56(Verb):
#     def __init__(self):
#         super(Verb56, self).__init__(name="Terminate tracking (P20)", verb_number=56)
#
# class Verb57(Verb):
#     def __init__(self):
#         super(Verb57, self).__init__(name="Display update state of FULTKFLG", verb_number=57)
#
# class Verb58(Verb):
#     def __init__(self):
#         super(Verb58, self).__init__(name="Enable auto maneuver in P20", verb_number=58)
#
# class Verb59(Verb):
#     def __init__(self):
#         super(Verb59, self).__init__(name="Please calibrate", verb_number=59)
#
# class Verb60(Verb):
#     def __init__(self):
#         super(Verb60, self).__init__(name="Set astronaut total attitude (N17) to present attitude", verb_number=60)
#
# class Verb61(Verb):
#     def __init__(self):
#         super(Verb61, self).__init__(name="Display DAP attitude error", verb_number=61)
#
# class Verb62(Verb):
#     def __init__(self):
#         super(Verb62, self).__init__(name="Display total attitude error WRT N22", verb_number=62)
#
# class Verb63(Verb):
#     def __init__(self):
#         super(Verb63, self).__init__(name="Display total astronaut attitude error WRT N17", verb_number=63)
#
# class Verb64(Verb):
#     def __init__(self):
#         super(Verb64, self).__init__(name="Enable Autopilot", verb_number=64) # TODO
#
# class Verb65(Verb):
#     def __init__(self):
#         super(Verb65, self).__init__(name="Optical verification of prelaunch alignment", verb_number=65)
#
# class Verb66(Verb):
#     def __init__(self):
#        super(Verb66, self).__init__(name="Vehicles attached, move this vehicle state vector to other vehicle state "
#                                          "vector", verb_number=66)
#
# class Verb67(Verb):
#     def __init__(self):
#         super(Verb67, self).__init__(name="Display W Matrix", verb_number=67)
#
# #no Verb 68
#
# class Verb69(Verb):
#     def __init__(self):
#         super(Verb69, self).__init__(name="Cause restart", verb_number=69)
#
# class Verb70(Verb):
#     def __init__(self):
#         super(Verb70, self).__init__(name="Update liftoff time", verb_number=70)
#
# class Verb71(Verb):
#     def __init__(self):
#         super(Verb71, self).__init__(name="Universal update - block address", verb_number=71)
#
# class Verb72(Verb):
#     def __init__(self):
#         super(Verb72, self).__init__(name="Universal update - single address", verb_number=72)
#
# class Verb73(Verb):
#     def __init__(self):
#         super(Verb73, self).__init__(name="Update AGC time (octal)", verb_number=73)
#
# class Verb74(Verb):
#     def __init__(self):
#         super(Verb74, self).__init__(name="Initialize erasable dump via downlink", verb_number=74)


class Verb75(ExtendedVerb):

    """ Backup liftoff
    """

    def __init__(self):

        """ Class constructor
        :return: None
        """

        super(Verb75, self).__init__(name="Backup liftoff", verb_number="75")

    def execute(self):

        """ Executes the verb.
        :return: None
        """
        program = Verb.computer.programs["11"]()
        program.execute()

#no verb 76
#no verb 77

# class Verb78(Verb):
#     def __init__(self):
#         super(Verb78, self).__init__(name="Update prelaunch azimuth", verb_number=78)
#
# #no verb 79
#
# class Verb80(Verb):
#     def __init__(self):
#         super(Verb80, self).__init__(name="Update LM state vector", verb_number=80)
#
# class Verb81(Verb):
#     def __init__(self):
#         super(Verb81, self).__init__(name="Update CSM state vector", verb_number=81)


class Verb82(ExtendedVerb):

    """ Request orbital parameters display (R30)
    """

    def __init__(self):

        """ Class constructor
        :return: None
        """

        super(Verb82, self).__init__(name="Request orbital parameters display (R30)", verb_number="82")

    def execute(self):

        """ Executes the verb.
        :return: None
        """

        #super(Verb82, self).execute()
        #computer.routines[30]()
        Verb.computer.execute_verb(verb="16", noun="44")


# class Verb83(Verb):
#     def __init__(self):
#         super(Verb83, self).__init__(name="Request rendezvous parameter display (R31)", verb_number=83)
#
#
# #no verb 84
#
# class Verb85(Verb):
#     def __init__(self):
#         super(Verb85, self).__init__(name="Request rendezvous parameter display no. 2 (R34)", verb_number=85)
#
# class Verb86(Verb):
#     def __init__(self):
#         super(Verb86, self).__init__(name="Reject rendezvous backup sighting mark", verb_number=86)
#
# class Verb87(Verb):
#     def __init__(self):
#         super(Verb87, self).__init__(name="Set VHF range flag", verb_number=87)
#
# class Verb88(Verb):
#     def __init__(self):
#         super(Verb88, self).__init__(name="Reset VHF range flag", verb_number=88)
#
# class Verb89(Verb):
#     def __init__(self):
#         super(Verb89, self).__init__(name="Request rendezvous final attitude (R63)", verb_number=89)
#
# class Verb90(Verb):
#     def __init__(self):
#         super(Verb90, self).__init__(name="Request rendezvous out of plane display (R36)", verb_number=90)
#
# class Verb91(Verb):
#     def __init__(self):
#         super(Verb91, self).__init__(name="Display bank sum", verb_number=91)
#
# class Verb92(Verb):
#     def __init__(self):
#         super(Verb92, self).__init__(name="Operate IMU performance test (P07)", verb_number=92)
#
class Verb93(ExtendedVerb):
    def __init__(self):
        super(Verb93, self).__init__(name="Disable Autopilot", verb_number="93")

    def execute(self):
        Verb.computer.disable_direction_autopilot()
#
# class Verb94(Verb):
#     def __init__(self):
#         super(Verb94, self).__init__(name="Request rendezvous backup sighting mark routine (R23)", verb_number=94)
#
# #no verb 95
#
# class Verb96(Verb):
#     def __init__(self):
#         super(Verb96, self).__init__(name="Terminate integration and go to P00", verb_number=96)
#
# class Verb97(Verb):
#     def __init__(self):
#         super(Verb97, self).__init__(name="Perform engine fail procedure", verb_number=97)
#
# #no verb 98
#


class Verb99(ExtendedVerb):

    """ Please enable engine
    """

    def __init__(self):

        """ Class constructor
        :return: None
        """

        super(Verb99, self).__init__(name="Please enable engine", verb_number="99")

    def execute(self, object_requesting_proceed):

        """ Executes the verb.
        :return: None
        """

        # stop any display updates
        if self.dsky.current_verb:
            self.dsky.current_verb.terminate()
        super(Verb99, self).execute()



        # blank the DSKY
        for register in list(self.dsky.control_registers.values()):
            register.blank()
        for register in list(self.dsky.data_registers.values()):
            register.blank()

        # re-display the verb number since the register has been blanked
        self.dsky.control_registers["verb"].display("99")
        self.dsky.request_data(requesting_object=object_requesting_proceed, display_location=None,
                             is_proceed_available=True)


verbs = OrderedDict()
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for class_tuple in clsmembers:
    if class_tuple[0][-1].isdigit():
        verbs[class_tuple[0][-2:]] = class_tuple[1]

