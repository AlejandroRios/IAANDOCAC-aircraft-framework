"""
Function  : second_segment_climb.py
Title     : Second segment climb function
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function calculates the thrust to weight ratio following the requiremnts
      of climb to second segment with one-engine-inoperative accoring to FAR 25.121.
      For this case the climb gradient expressed as a percentage takes a value of 0.024.
      The lading gear is up and takeoff flaps are deployed
      References: FAR 25.121 and ROSKAM 1997 - Part 1, pag. 146 

    - 
Inputs:
    - aircraft_data
Outputs:
    - 
TODO's:
    - 

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

def second_segment_climb(aircraft_data,airport_data):
    '''
    '''
    engines_number = aircraft_data['engines_number'] 
    CL_maximum_takeoff = aircraft_data['CL_maximum_takeoff']
    CD_takeoff = zero_fidelity_drag_coefficient(aircraft_data)

    L_to_D = CL_maximum_takeoff/CD_takeoff

    aux1 = (engines_number/(engines_number-1))
    aux2 = (1/L_to_D) + 0.024

    thrust_to_weight_takeoff = aux1*aux2
    return thrust_to_weight_takeoff
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
