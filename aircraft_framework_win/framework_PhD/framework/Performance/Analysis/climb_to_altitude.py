"""
File name : Climb to altitude function
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function performs the calculation process to obtain the time, fuel anddistance for one altitude step og the step integration process
    - Reference: Blake, BOEING CO. Flight Operations Engineering - Jet Transport Performance Methods. 7th ed. Boeing Co.,Everett,Estados Unidos,1989
    - Chapter 30, page 30-11
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
from framework.Attributes.Atmosphere.atmosphere import atmosphere
from framework.Attributes.Airspeed.airspeed import mach_to_V_tas
from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient
import numpy as np


from framework.baseline_aircraft import *
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
global gravity
gravity = 9.80665
def rate_of_climb_calculation(thrust_to_weight,h,delta_ISA,mach,mass,aircraft_data):

    wing_surface = aircraft_data['wing_surface']

    knots_to_feet_minute = 101.268 
    knots_to_meters_second = 0.514444

    phase = "climb"

    V_tas = mach_to_V_tas(mach,h,delta_ISA)

    _,_,_,_,_,rho_ISA,_  = atmosphere_ISA_deviation(h,delta_ISA)

    CL = (2*mass*gravity)/(rho_ISA*((V_tas*knots_to_meters_second)**2)*wing_surface)

    CD = zero_fidelity_drag_coefficient(aircraft_data,CL,phase)

    L_to_D = CL/CD
    
    if mach > 0:
        acceleration_factor,_ = acceleration_factor_calculation(h,delta_ISA,mach)
        climb_path_angle = np.arcsin((thrust_to_weight - 1/(L_to_D))/(1 + acceleration_factor))
    else:
        _,acceleration_factor = acceleration_factor_calculation(h,delta_ISA,mach)
        climb_path_angle = np.arcsin((thrust_to_weight - 1/(L_to_D))/(1 + acceleration_factor))
    rate_of_climb = knots_to_feet_minute * V_tas * np.sin(climb_path_angle)
    return rate_of_climb, V_tas, climb_path_angle


def acceleration_factor_calculation(h,delta_ISA,mach):
    lambda_rate = 0.0019812 
    tropopause = (71.5 + delta_ISA)/lambda_rate

    T,_,_,_ = atmosphere(h)
    _,_,_,T_ISA,_,_,_  = atmosphere_ISA_deviation(h,delta_ISA)

    if h < tropopause:
        # For constant calibrated airspeed below the tropopause:
        acceleration_factor_V_CAS =  (0.7*mach**2)*(phi_factor(mach) - 0.190263*(T_ISA/T))
        # For constant Mach number below the tropopause:
        acceleration_factor_mach = (-0.13318*mach**2)*(T_ISA/T)
    elif h > tropopause:
        # For constant calibrated airspeed above the tropopause:
        acceleration_factor_V_CAS = (0.7*mach**2)*phi_factor(mach)
        # For constant Mach number above the tropopause:
        acceleration_factor_mach = 0

    return acceleration_factor_V_CAS, acceleration_factor_mach

def phi_factor(mach):
    aux1 = (1 + 0.2*mach**2)**3.5 - 1
    aux2 = (0.7*mach**2) * (1 + 0.2*mach**2)**2.5
    return aux1/aux2
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################


# aircraft_data = baseline_aircraft()