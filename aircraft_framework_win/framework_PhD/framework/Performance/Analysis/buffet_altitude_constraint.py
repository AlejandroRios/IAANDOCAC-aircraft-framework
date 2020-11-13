"""
Function  : buffet_altitude_constraint.py
Title     :
Written by: 
Date      : 
Last edit :
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module obtain the cruise altutude considering buffeting constraints
    - Reference: Ruijgrok, Elements of airplane performance 
    - Chapter 10, pag 261
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
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
import numpy as np

from framework.baseline_aircraft import baseline_aircraft
from framework.Attributes.Airspeed.airspeed import mach_to_V_tas
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
global gravity
gravity = 9.80665
def buffet_altitude(mass,altitude,limit_altitude,climb_mach):
    aircraft_data = baseline_aircraft()
    wing_surface = aircraft_data['wing_surface']
    step = 100
    load_factor = 1.3
    gamma = 1.4
    delta_ISA = 0

    wing_loading_constraint = 6000 # Typical values of wing loading for jet airplanes around 5749 [Pascal]
    _,_,_,_,P_ISA,_,_ = atmosphere_ISA_deviation(limit_altitude,delta_ISA)
    CL_constraint = ((2)/(gamma*P_ISA*climb_mach**2))*wing_loading_constraint

    CL = 0.1

    while CL<CL_constraint:
        theta,delta,sigma,T_ISA,P_ISA,rho_ISA,a = atmosphere_ISA_deviation(altitude,delta_ISA)
        CL = ((2*load_factor)/(gamma*P_ISA*climb_mach*climb_mach))*(mass*gravity/wing_surface)
        altitude = altitude+step

    return altitude


    # return buffet_altitude
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
# weight = 43112
# altitude = 10000
# limit_altitude = 41000
# climb_mach = 0.78
# print(buffet_altitude(weight,altitude,limit_altitude,climb_mach))