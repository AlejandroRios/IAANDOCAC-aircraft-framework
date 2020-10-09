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

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def climb_integration(mass,climb_mach,climb_V_cas,delta_ISA,final_altitude,initial_altitude):
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

    total_burned_fuel = []
    total_climb_time = []
    
    if flag1 == 1:

        # Climb to 10000 ft with 250 KCAS

        if final_altitude <= 10000:
            block_final_altitude = final_altitude
        else:
            block_final_altitude = 10000

        state0 = [0.0,mass,0.0]
        altitude = np.arange(initial_altitude, block_final_altitude, 1)
        state = odeint(climb, state0, altitude, args = (climb_V_cas,climb_mach,delta_ISA))
        # print(state)
        final_time = state[-1,0]
        final_mass = state[-1,1]
        final_distance = state[-1,2]
        burned_fuel = mass - final_mass
        total_burned_fuel.append(burned_fuel)
        total_climb_time.append(final_time)


    if flag2 == 1:

        mass = final_mass
        initial_altitude = 10000
        initial_distance = final_distance
        block_final_altitude = transition_altitude
        state0 = [0,mass,initial_distance]
        altitude = np.arange(initial_altitude,block_final_altitude, 1)
        state = odeint(climb, state0, altitude, args = (climb_V_cas,climb_mach,delta_ISA))
        final_time = state[-1,0]
        final_mass = state[-1,1]
        final_distance = state[-1,2]
        burned_fuel = mass - final_mass
        total_burned_fuel.append(burned_fuel)
        total_climb_time.append(final_time)

    if flag3 == 1:

        mass = final_mass
        initial_altitude = transition_altitude
        initial_distance = final_distance
        block_final_altitude = final_altitude
        state0 = [0,mass,initial_distance]
        altitude = np.arange(initial_altitude, block_final_altitude, 1)
        state = odeint(climb, state0, altitude, args = (climb_V_cas,climb_mach,delta_ISA))
        final_time = state[-1,0]
        final_mass = state[-1,1]
        final_distance = state[-1,2]
        burned_fuel = mass - final_mass
        total_burned_fuel.append(burned_fuel)
        total_climb_time.append(final_time)

    total_burned_fuel = sum(total_burned_fuel)
    total_climb_time = sum(total_climb_time)
    return final_distance,total_climb_time,total_burned_fuel,final_altitude


def climb(state,altitude,climb_V_cas,climb_mach,delta_ISA):
    mass = state[1]

    _,_,_,_,_,rho_ISA,_  = atmosphere_ISA_deviation(altitude,delta_ISA)
    throttle_position = 0.95
    aircraft_data = baseline_aircraft()
    number_engines = aircraft_data['number_of_engines']

    
    
    if climb_V_cas > 0:
        mach = V_cas_to_mach(climb_V_cas,altitude,delta_ISA)
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)
        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)

    else:
        mach = climb_mach
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)
        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)
    
    dist_dt=(V_tas/60)
    dis_dh = dist_dt/rate_of_climb
    dfuel_dt = (number_engines*fuel_flow/60)
    dW_dt=-dfuel_dt
    dW_dh=dW_dt*1/rate_of_climb
    dt_dh=1/rate_of_climb
    dout=np.array([dt_dh, dW_dh, dis_dh])

    dout = dout.reshape(3,)

    return dout
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
global gravity
gravity = 9.8067

# mass = 43112
# climb_mach = 0.78
# climb_V_cas = 280
# delta_ISA = 0
# final_altitude = 39000
# initial_altitude = 0
# print(climb_integration(mass,climb_mach,climb_V_cas,delta_ISA,final_altitude,initial_altitude))
# print(state)

