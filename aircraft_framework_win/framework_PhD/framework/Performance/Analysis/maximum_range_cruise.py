"""
Function  : maximum_range_cruise
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
from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient
from framework.Attributes.Airspeed.airspeed import V_cas_to_V_true, mach_to_V_true
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient

import numpy as np
import matplotlib.pyplot as plt
from framework.baseline_aircraft import baseline_aircraft
import operator
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
# def maximum_range_cruise_speed():
global gravity
gravity = 9.80665

def maximum_range_mach(mass,cruise_altitude,delta_ISA):
    aircraft_data = baseline_aircraft()
    wing_surface = aircraft_data['wing_surface']

    VMO = 340
    altitude = cruise_altitude
    mach_maximum_operating = 0.82 


    VMO = V_cas_to_V_true(VMO-10,altitude,delta_ISA)

    initial_mach = 0.2

    mach = np.linspace(initial_mach,2,100)

    V_tas = mach_to_V_true(mach,altitude,delta_ISA)

    _,_,_,_,_,rho_ISA,a = atmosphere_ISA_deviation(altitude,delta_ISA)

    CL_required = (2*mass*gravity)/(rho_ISA*V_tas*V_tas*wing_surface)

    phase = 'cruise'

    CD = zero_fidelity_drag_coefficient(aircraft_data,CL_required,phase)

    MLD = mach*(CL_required/CD)

    index, value = max(enumerate(MLD), key=operator.itemgetter(1))

    mach_maximum_cruise = mach[index]

    V_maximum = mach_to_V_true(mach_maximum_cruise,altitude,delta_ISA)

    if V_maximum > VMO:
        V_maximum = VMO
        mach_maximum_cruise = V_maximum/a

    return mach_maximum_cruise
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
