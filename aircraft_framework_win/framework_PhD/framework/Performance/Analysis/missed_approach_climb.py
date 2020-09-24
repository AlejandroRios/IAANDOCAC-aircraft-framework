"""
Function  : missed_approach_climb.py
Title     : Missed approach limb function
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function calculates the thrust to weight ratio following the requiremnts
      of missed climb approach with one-engine-inoperative accoring to FAR 25.121.
      For this case the climb gradient expressed as a percentage takes a value of 0.021 (for two engine aircraft).
      The lading gear is up and takeoff flaps are deployed
      References: FAR 25.121 and ROSKAM 1997 - Part 1, pag. 142 
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

def missed_approach_climb_OEI(aircraft_data,airport_data,maximum_takeoff_weight):
    '''
    '''
    engines_number = aircraft_data['engines_number'] 
    CL_maximum_landing = aircraft_data['CL_maximum_landing']
    maximum_landing_weight = aircraft_data['maximum_landing_weight'] # [N]
    phase = 'climb'
    CD_landing = zero_fidelity_drag_coefficient(aircraft_data,CL_maximum_landing,phase)

    L_to_D = CL_maximum_landing/CD_landing
    if engines_number == 2:
        steady_gradient_of_climb = 0.021 # 2.4% for two engines airplane
    elif engines_number == 3:
        steady_gradient_of_climb = 0.024 # 2.4% for two engines airplane
    elif engines_number == 4:
        steady_gradient_of_climb = 0.027 # 2.4% for two engines airplane

    aux1 = (engines_number/(engines_number-1))
    aux2 = (1/L_to_D) + steady_gradient_of_climb 
    aux3 = maximum_landing_weight/maximum_takeoff_weight
    thrust_to_weight_landing = aux1*aux2*aux3
    return thrust_to_weight_landing

def missed_approach_climb_AEO(aircraft_data,airport_data,maximum_takeoff_weight):
    '''
    '''
    phase = 'descent'
    CL_maximum_landing = aircraft_data['CL_maximum_landing']
    CD_landing = zero_fidelity_drag_coefficient(aircraft_data,CL_maximum_landing,phase)
    maximum_landing_weight = aircraft_data['maximum_landing_weight'] # [N]

    L_to_D = CL_maximum_landing/CD_landing

    steady_gradient_of_climb = 0.032 # 2.4% for two engines airplane

    aux1 = (1/L_to_D) + steady_gradient_of_climb 
    aux2 = maximum_landing_weight/maximum_takeoff_weight
    thrust_to_weight_landing = aux1 * aux2
    return thrust_to_weight_landing
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
