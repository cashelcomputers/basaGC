import math

from pudb import set_trace

from basagc import config, telemachus, utils
from basagc.config import TELEMACHUS_BODY_IDS
from basagc.telemachus import get_telemetry

computer = None

def time_to_transfer(departure_orbit, destination_orbit, grav_param):
    """
    Calculates the time to transfer from one orbit to another,
    :param departure_orbit: departure orbit altitude
    :param destination_orbit: destination orbit altitude
    :param grav_param: orbiting body gravitational parameter
    :return: a float in seconds of the time to transfer
    """
    tH = math.pi * math.sqrt(math.pow(departure_orbit + destination_orbit, 3) / (8 * grav_param))
    return tH


def phase_angle(departure_orbit, destination_orbit, grav_param):
    """ Calculates the required phase angle for transfer.
    :param departure_orbit: departure orbit altitude
    :param destination_orbit: destination orbit altitude
    :param grav_param: orbiting body gravitational parameter
    :return: the required phase angle
    """

    tH = time_to_transfer(departure_orbit, destination_orbit, grav_param)
    required_phase_angle = 180 - math.sqrt(grav_param / destination_orbit) * (tH / destination_orbit) * 180 / math.pi
    return required_phase_angle


def calculate_delta_v_hohmann(departure_altitude, destination_altitude, departure_body="Kerbin"):
    """
    Given a circular orbit at altitude departure_altitude and a target orbit at altitude
    destination_altitude, return the delta-V budget of the two burns required for a Hohmann
    transfer.

    departure_altitude and destination_altitude are in meters above the surface.
    returns a float of the burn delta-v required, positive means prograde, negative means retrograde

    :param departure_body:
    :param departure_altitude: departure orbit altitude
    :param destination_altitude: destination orbit altitude
    """

    departure_planet_radius = get_telemetry("body_radius", body_number=TELEMACHUS_BODY_IDS[departure_body])
    r1 = departure_altitude + departure_planet_radius
    r2 = destination_altitude + departure_planet_radius
    mu = float(get_telemetry("body_gravParameter", body_number=TELEMACHUS_BODY_IDS[departure_body]))
    sqrt_r1 = math.sqrt(r1)
    sqrt_r2 = math.sqrt(r2)
    sqrt_2_sum = math.sqrt(2 / (r1 + r2))
    sqrt_mu = math.sqrt(mu)
    delta_v_1 = sqrt_mu / sqrt_r1 * (sqrt_r2 * sqrt_2_sum - 1)
    delta_v_2 = sqrt_mu / sqrt_r2 * (1 - sqrt_r1 * sqrt_2_sum)
    return delta_v_1, delta_v_2


class Burn:

    """ This object models a burn maneuver """

    def __init__(self, delta_v, direction, time_of_ignition, time_of_node, recalc_function=None, calling_program=None):

        """ Class constructor

        :param delta_v: delta_v required for burn
        :type delta_v: float
        :param direction: direction of burn
        :type direction: str (should be in config.DIRECTIONS)
        :param time_of_ignition: Time of Ignition, relative to Mission Elapsed Time
        :type time_of_ignition: float
        :return: None
        """

        self.recalc_function = recalc_function
        self.delta_v_required = delta_v
        self.direction = direction
        self.time_of_ignition = time_of_ignition
        self.time_of_node = time_of_node
        self.is_display_blanked = False
        self.is_verb_99_executed = False
        self.time_until_ignition = self.calculate_time_to_ignition()
        self.velocity_at_cutoff = self._calculate_velocity_at_cutoff()
        self.is_directional_autopilot_engaged = False
        self.is_thrust_autopilot_engaged = False
        self.is_active = False
        self.initial_speed = 0.0
        self.accumulated_delta_v = 0.0
        self._is_thrust_reduced = False
        self.calling_program = calling_program

    def execute(self):

        """ Entry point to execute this burn.
        :return: None
        """

        # check if direction is valid
        if self.direction not in config.DIRECTIONS:
            computer.program_alarm(410)
            return
        # load the course start time monitor into the computers main loop
        computer.execute_verb(verb="16", noun="40")
        computer.main_loop_table.append(self._coarse_start_time_monitor)
        self.add_maneuver_node()

    def add_maneuver_node(self):
        ut = self.time_of_node
        self.maneuver_node = telemachus.add_maneuver_node(
            ut=ut,
            delta_v=(0.0, 0.0, self.delta_v_required)
            )
        print(self.maneuver_node)

    def terminate(self):

        """ Terminates the burn, disabling autopilot if running
        :return: None
        """
        self._disable_directional_autopilot()

        # if the throttle is open, close it
        telemachus.cut_throttle()

        computer.remove_burn(self)

    def _coarse_start_time_monitor(self):

        self.time_until_ignition = self.calculate_time_to_ignition()

        # at TIG - 105 seconds:
        # ensure we only blank display first time through the loop
        if int(self.time_until_ignition) == 105 and not self.is_display_blanked:
            computer.dsky.current_verb.terminate()
            for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
                computer.dsky.blank_register(register)
            self.is_display_blanked = True
        # at TIG - 100 seconds, reenable display and enable directional autopilot
        if int(self.time_until_ignition) <= 100 and self.is_display_blanked:
            # restore the displayed program number
            computer.dsky.set_register(computer.running_program.number, "program")
            computer.execute_verb(verb="16", noun="40")
            self.is_display_blanked = False
            self._enable_directional_autopilot()

        # at TIG - 10, execute verb 99
        if int(self.time_until_ignition) <= 10:
            computer.main_loop_table.remove(self._coarse_start_time_monitor)
            computer.execute_verb(verb="99", object_requesting_proceed=self._accept_enable_engine)

    def _accept_enable_engine(self, data):
        if data == "proceed":
            utils.log("Go for burn!", log_level="INFO")
        else:
            return
        computer.main_loop_table.append(self._fine_start_time_monitor)
        computer.execute_verb(verb="16", noun="40")

    def _fine_start_time_monitor(self):

        self.time_until_ignition = self.calculate_time_to_ignition()
        if float(self.time_until_ignition) < 0.1:
            utils.log("Engine Ignition", log_level="INFO")
            self._begin_burn()
            computer.main_loop_table.remove(self._fine_start_time_monitor)

    def _begin_burn(self):

        self.initial_speed = get_telemetry("orbitalVelocity")

        # start thrusting
        telemachus.set_throttle(100)
        computer.main_loop_table.append(self._thrust_monitor)

    def _thrust_monitor(self):

        # recalculate accumulated delta-v so far
        self.accumulated_delta_v = self._calculate_accumulated_delta_v()

        if self.accumulated_delta_v > (self.delta_v_required - 10) and not self._is_thrust_reduced:
            utils.log("Throttling back to 10%", log_level="DEBUG")
            telemachus.set_throttle(10)
            self._is_thrust_reduced = True

        if self.accumulated_delta_v > (self.delta_v_required - 0.5):
            telemachus.cut_throttle()
            utils.log("Closing throttle, burn complete!", log_level="DEBUG")
            computer.dsky.current_verb.terminate()
            computer.execute_verb(verb="06", noun="14")
            computer.main_loop_table.remove(self._thrust_monitor)
            computer.burn_complete()
            self.terminate()
            computer.go_to_poo()

        # utils.log("Accumulated Δv: {}, Δv to go: {}".format(accumulated_speed[0], delta_v_required -
        #                                                     accumulated_speed[0]))

    def _calculate_velocity_at_cutoff(self):
        return get_telemetry("orbitalVelocity") + self.delta_v_required

    def calculate_time_to_ignition(self):

        """ Calculates the time to ignition in seconds
        :return: time to ignition in seconds
        :rtype : float
        """
        current_time = get_telemetry("universalTime")
        return self.time_of_ignition - current_time

    def _calculate_accumulated_delta_v(self):
        current_speed = get_telemetry("orbitalVelocity")
        return current_speed - self.initial_speed

    def _disable_directional_autopilot(self):

        try:
            telemachus.disable_smartass()
        except:
            return False
        else:
            utils.log("Directional autopilot disabled", log_level="INFO")
            return True

    def _enable_directional_autopilot(self):
        
        telemachus.set_mechjeb_smartass("node")
        utils.log("Directional autopilot enabled", log_level="INFO")
        return True
