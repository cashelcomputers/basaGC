#!/usr/bin/env python

computer = None

def average_g():
    """The purpose of the Powered Flight Navigation Sub-
    routine is to compute the vehicle state vector during periods
    of powered flight steering. During such periods the effects of
    gravity and thrusting are taken into account. In order to achieve
    a short computation time the integration of the effects of gravity
    is achieved by simple averaging of the gravity acceleration vec-
    tor. The effect of thrust acceleration is measured by the IMU
    Pulsed Integrating Pendulous Accelerometers (PIPA) in the form
    of velocity increments (Av) over the computation time interval
    (At). The computations are, therefore, in terms of discrete in-
    crements of velocity rather than instantaneous accelerations.
    The repetitive computation cycle time At is set at 2 seconds to
    maintain accuracy and to be compatible with the basic powered
    flight cycle.
    """
    # Note that in KSP, position vectors are relative to your current craft (I 
    # think), so we are going to simulate a position vector using lat, long and 
    # altitude above sea level
    latitude = computer.memory.get_memory("latitude")
    longitude = computer.memory.get_memory("longitude")
    altitude = computer.memory.get_memory("asl")
    
    velocity_x = computer.memory.get_memory("surface_velocity_x")
    velocity_y = computer.memory.get_memory("surface_velocity_y")
    velocity_z = computer.memory.get_memory("surface_velocity_z")
    
    time_ = computer.memory.get_memory("ut")
    
    computer.state_vector.position_vector["lat"] = latitude
    computer.state_vector.position_vector["long"] = longitude
    computer.state_vector.position_vector["alt"] = altitude
    
    computer.state_vector.velocity_vector.x = velocity_x
    computer.state_vector.velocity_vector.y = velocity_y
    computer.state_vector.velocity_vector.z = velocity_z
    
    computer.state_vector.time = time_

def routine_30():
    
    def receive_data(data):
        
        """ control will pass to here upon data being loaded by user """
        
        if data not in ("00001", "00002", "proceed"):
            computer.dsky.operator_error("Invalid data entered, expecting either '00001' or '00002', got {}".format(data))
        if data != "proceed":
            computer.option_codes["00002"] = data
            routine_30()
            
    # --> is another extended verb active?
    if computer.dsky.state["current_verb"] >= 40:
        computer.dsky.operator_error("Cannot run two extended verbs at the same time")
        return
    
    # --> is average g routine on?
    if computer.state["run_average_g_routine"]:
        
        # --> compute apoapsis, periapsis and TFF
        # I think TFF (Time to FreeFall) means orbital period?
        
        # --> is TFF computable (i.e is periapsis < 300,000ft in Earth orbit or
        # --> 35,000ft in Lunar orbit?
        
        # --> yes:
        # --> set TF periapsis = 0 and compute TFF
        
        # --> no:
        # --> set TFF = -59859 and compute TF periapsis
        
        # we ignore this test and "compute" the required data anyways
        pass
    else:
        # --> set CMC assumed (vehicle) option to 00001
        if computer.option_codes["00002"] == "":
            computer.option_codes["00002"] = "00001"
        # set V04N12 and request data entry
        computer.dsky.set_noun(12)
        computer.dsky.control_registers["verb"].display("04")
        computer.dsky.registers[1].display(value="00002")
        computer.dsky.registers[2].display(value=computer.option_codes["00002"])
        computer.dsky.request_data(receive_data, computer.dsky.registers[3])
    
    




























