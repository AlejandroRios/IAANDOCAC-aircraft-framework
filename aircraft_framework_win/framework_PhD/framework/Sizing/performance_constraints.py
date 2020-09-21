"""
Function  : performance_constraints.py
Title     : Performance constraints
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - 
Inputs:
    -
Outputs:
    - 
TODO's:
    - Add sigma effect of engine

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Performance.balanced_field_length import balanced_field_length
from framework.Performance.landing_field_length import landing_field_length
from framework.Performance.second_segment_climb import second_segment_climb
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation

from framework.baseline_aircraft import *
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def takeoff_field_length_check(aircraft_data,airport_data):
    airport_field_length = airport_data['takeoff_field_length']
    weight_takeoff = aircraft_data['maximum_takeoff_weight']

    flag = 0
    while flag == 0:

        aircraft_data['maximum_takeoff_weight'] =  weight_takeoff
        field_length_computed = balanced_field_length(aircraft_data,airport_data)

        if field_length_computed > airport_field_length:
            weight_takeoff = weight_takeoff - (10*9.81)
        else:
            flag = 1      

    print(field_length_computed)     

    return weight_takeoff

def landing_field_length_check(aircraft_data,airport_data):
    airport_field_length = airport_data['landing_field_length']
    weight_landing = aircraft_data['maximum_landing_weight']

    flag = 0
    while flag == 0:
        aircraft_data['maximum_landing_weight'] =  weight_landing
        field_length_computed = landing_field_length(aircraft_data,airport_data)

        if field_length_computed > airport_field_length:
            weight_landing = weight_landing-(10*9.81)
        else:
            flag = 2
    return weight_landing

def second_segment_climb_check(aircraft_data,airport_data):

    weight_takeoff = aircraft_data['maximum_takeoff_weight']
    thrust_takeoff = aircraft_data['maximum_engine_thrust']

    flag = 0
    while flag == 0:
        thrust_to_weight_takeoff_required= second_segment_climb(aircraft_data,airport_data)
        thrust_to_weight_takeoff = thrust_takeoff/weight_takeoff

        if thrust_to_weight_takeoff < thrust_to_weight_takeoff_required:
            weight_takeoff = weight_takeoff-(10*9.81)
        else:
            flag = 2
    return weight_takeoff


def landing_climb_check():
    return

def approach_climb_check():
    return

def residual_rate_of_climb_check():
    return

def maximum_cruise_speed_check():
    return

def drag_divergence_check():
    return
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################

airport_data = baseline_airport()
aircraft_data = baseline_aircraft()

weight_takeoff_f = takeoff_field_length_check(aircraft_data,airport_data)
print('weight BFL requirement:',weight_takeoff_f/9.81)

weight_landing_f = landing_field_length_check(aircraft_data,airport_data)

print('weight landing field requirement:',weight_landing_f/9.81 )


second_segment_clb =  second_segment_climb_check(aircraft_data,airport_data)

print('second segment requirement:',second_segment_clb/9.81)