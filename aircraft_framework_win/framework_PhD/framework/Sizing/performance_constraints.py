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
    - 

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Performance.balanced_length_field import balanced_lenght_field
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def takeoff_field_length_check(TOFL):
    weight_takeoff = 55000
    wing_surface = 100
    CL_max_takeoff = 2.4
    h_airfield = 2500
    delta_ISA = 19.9530

    # This should come from another module instead of being calculated here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ##############################################################################################################
    lb_2_kg = 0.45359237
    bypass_ratio = 5.0
    maximum_rate = 22000
    thrust_altitude_factor = 0.8
    number_engines = 2
    _,_,sigma,_,_,_,_ = atmosphere_ISA_deviation(h_airfield,delta_ISA)
    T_max = (0.95 * maximum_rate * (sigma**thrust_altitude_factor) * lb_2_kg)/2
    T_avg = 0.75 *  ((5 + bypass_ratio)/(4 + bypass_ratio)) * T_max

    flag = 0
    iter = 0 
    while flag == 0:
        FL = balanced_lenght_field(weight_takeoff,wing_surface,CL_max_takeoff,T_avg,h_airfield,delta_ISA)
        if FL > TOFL:
            weight_takeoff = weight_takeoff - 10
        else:
            flag = 1           

    return weight_takeoff

def landing_field_length_check():
    return

def second_segment_climb_check():
    return

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
TOFL = 2560
weight_takeoff_f = takeoff_constraint(TOFL)
print(weight_takeoff_f)

