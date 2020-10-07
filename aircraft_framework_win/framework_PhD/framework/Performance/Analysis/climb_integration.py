"""
Function  : 
Title     :
Written by: 
Date      : 
Last edit :
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - 
Inputs:
    -
Outputs:
    - 
TODO's:
    - 

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Attributes.Airspeed.airspeed import V_cas_to_mach, mach_to_V_cas, crossover_altitude
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Performance.Engine.engine_performance import turbofan

from framework.Performance.Analysis.climb_to_altitude import rate_of_climb_calculation
from framework.baseline_aircraft import baseline_aircraft
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def climb_integration():
    rate_of_climb = 500

    time_climb1 = 0
    time_climb2 = 0
    time_climb3 = 0

    transition_altitude = crossover_altitude(climb_mach,climb_V_cas,delta_ISA)

    time = 0
    distance = 0
    fuel1 = 0
    fuel2 = 0
    fuel3 = 0

    if final_altitude >= transition_altitude:
        flag1 = 1
        flag2 = 1
        flag3 = 1

    if (final_altitude >= 10000 and final_altitude < transition_altitude):
        flag1 = 1
        flag2 = 1
        flag3 = 0

    if final_altitude< 10000:
        flag1 = 1
        flag2 = 0
        flag3 = 0
    
    if flag1 == 1:

        # Climb to 10000 ft with 250 KCAS

        if final_altitude <= 10000:
            final_altitude = final_altitude
        else:
            final_altitude = 10000

        initial_altitude = initial_altitude + 1500



        state0 = [0.0,0.0,0.0]

        




    return


def climb(satate,t,climb_V_cas,climb_mach,altitude,delta_ISA):
    mass = state[1]

    _,_,_,_,_,rho_ISA,_  = atmosphere_ISA_deviation(altitude,delta_ISA)
    throttle_position = 0.95
    aircraft_data = baseline_aircraft()
    number_engines = aircraft_data['number_of_engines']

    
    
    if V_cas > 0:
        mach = V_cas_to_mach(V_cas,altitude,delta_ISA)
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)
        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)

    else:
        mach = climb_mach
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)
        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)
    
    distance_d

    



    

    return[]
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################