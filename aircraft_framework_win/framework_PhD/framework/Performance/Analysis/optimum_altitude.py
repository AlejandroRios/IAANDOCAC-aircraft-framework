"""
Function  : optimum_altitude.py
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
    - Informar Fregnani erro no código do matlab. V_CAS to mach dando valores incosistentes

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Attributes.Airspeed.airspeed import V_cas_to_mach, mach_to_V_cas, crossover_altitude

from framework.Performance.Engine.engine_performance import turbofan

from framework.Performance.Analysis.climb_to_altitude import rate_of_climb_calculation
from framework.Performance.Analysis.buffet_altitude_constraint import buffet_altitude

from framework.baseline_aircraft import baseline_aircraft
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

global gravity
gravity = 9.80665

def optimum_altitude(initial_altitude,limit_altitude,mass,
    climb_V_cas,climb_mach,delta_ISA):

    transition_altitude = crossover_altitude(climb_mach,climb_V_cas,delta_ISA)
    altitude_step = 100
    residual_rate_of_climb = 300

    time = 0
    distance = 0
    fuel = 0
    rate_of_climb = 9999

    # Climb to 10000 ft with 250KCAS
    initial_altitude = initial_altitude + 1500 # 1500 [ft]
    altitude = initial_altitude
    final_altitude = 10000
    throttle_position = 0.95

    optimum_specific_rate = 0

    aircraft_data = baseline_aircraft()
    number_engines = aircraft_data['number_of_engines']


    while (rate_of_climb>residual_rate_of_climb and altitude<final_altitude):
        V_cas = 250
        mach = V_cas_to_mach(V_cas,altitude,delta_ISA)
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)

        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)

        delta_time = altitude_step/rate_of_climb
        time = time + delta_time
        distance = distance + (V_tas/60)*delta_time
        delta_fuel = (fuel_flow/60)*delta_time
        fuel = fuel+delta_fuel
        mass = mass-delta_fuel
        altitude = altitude + altitude_step

        specific_rate = V_tas/fuel_flow
        if specific_rate>optimum_specific_rate:
            optimum_specific_rate = specific_rate
            optimum_altitude = altitude

    # Climb to transition altitude at constat CAS

    delta_altitude = 0
    initial_altitude = 10000 + delta_altitude
    altitude = initial_altitude
    final_altitude = transition_altitude

    while (rate_of_climb>residual_rate_of_climb and altitude<=final_altitude):
        mach = V_cas_to_mach(V_cas,altitude,delta_ISA)
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position)
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)

        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)

        delta_time = altitude_step/rate_of_climb
        time = time + delta_time
        distance = distance + (V_tas/60)*delta_time
        delta_fuel = (fuel_flow/60)*delta_time
        fuel = fuel+delta_fuel
        mass = mass-delta_fuel
        altitude = altitude + altitude_step

        specific_rate = V_tas/fuel_flow
        if specific_rate>optimum_specific_rate:
            optimum_specific_rate = specific_rate
            optimum_altitude = altitude


    # Climb to transition altitude at constant mach
    final_altitude = limit_altitude
    mach = climb_mach


    buffet_altitude_limit = buffet_altitude(mass,altitude,limit_altitude,climb_mach)

    while (rate_of_climb>residual_rate_of_climb and altitude<=final_altitude):

        V_cas  = mach_to_V_cas(mach,altitude,delta_ISA)
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position)
        thrust_to_weight = number_engines*thrust_force/(mass*gravity)

        rate_of_climb,V_tas = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)

        delta_time = altitude_step/rate_of_climb
        time = time + delta_time
        distance = distance + (V_tas/60)*delta_time
        delta_fuel = (fuel_flow/60)*delta_time
        fuel = fuel+delta_fuel
        mass = mass-delta_fuel
        altitude = altitude + altitude_step
    
        specific_rate = V_tas/fuel_flow
        if specific_rate>optimum_specific_rate:
            optimum_specific_rate = specific_rate
            optimum_altitude = altitude

    
    final_altitude = altitude - altitude_step
    
    if buffet_altitude_limit < final_altitude:
        final_altitude = buffet_altitude_limit
    
    optimum_altitude = final_altitude
    return optimum_altitude,rate_of_climb,optimum_specific_rate


########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
# initial_altitude = 0
# limit_altitude = 41000
# mass = 43112 # [kg]
# climb_V_cas = 280
# climb_mach = 0.78
# delta_ISA = 0

# optimum_altitude,rate_of_climb,optimum_specific_rate =  maximum_altitude(initial_altitude,limit_altitude,mass,
#     climb_V_cas,climb_mach,delta_ISA)

# print(optimum_altitude,rate_of_climb,optimum_specific_rate)