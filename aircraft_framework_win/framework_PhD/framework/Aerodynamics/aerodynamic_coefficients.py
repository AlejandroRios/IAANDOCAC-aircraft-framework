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
from framework.baseline_aircraft import *
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def zero_fidelity_drag_coefficient(aircraft_data,CL,phase):

    wing_aspect_ratio = aircraft_data['wing_aspect_ratio']
    
    e = 0.7
    CD_0 = 0.0001

    Delta_CD_flap = 0.03 # for flap 35 degrees and CL = 1.7
    Delta_CD_slat = 0
    Delta_CD_gear = 0.015
    if phase == "takeoff":
        Delta_CD_flap = 0.03 # for flap 35 degrees and CL = 1.7
        Delta_CD_slat = 0
        Delta_CD_gear = 0.015
        CD_induced = (CL**2)/(np.pi*wing_aspect_ratio*e)
        CD_profile = CD_0 + Delta_CD_flap + Delta_CD_slat + Delta_CD_gear
        CD = CD_profile + CD_induced
    elif phase == "landing":
        Delta_CD_flap = 0.03 # for flap 35 degrees and CL = 1.7
        Delta_CD_slat = 0
        Delta_CD_gear = 0.015
        CD_induced = (CL**2)/(np.pi*wing_aspect_ratio*e)
        CD_profile = CD_0 + Delta_CD_flap + Delta_CD_slat + Delta_CD_gear
        CD = CD_profile + CD_induced
    elif phase == "climb":
        CD_induced = (CL**2)/(np.pi*wing_aspect_ratio*e)
        CD_profile = CD_0
        CD = CD_profile + CD_induced
    elif phase == "descent":
        CD_induced = (CL**2)/(np.pi*wing_aspect_ratio*e)
        CD_profile = CD_0
        CD = CD_profile + CD_induced
    elif phase == "cruise":
        CD_induced = (CL**2)/(np.pi*wing_aspect_ratio*e)
        CD_profile = CD_0
        CD = CD_profile + CD_induced
    return CD
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
# aircraft_data = baseline_aircraft()
# zero_fidelity_drag_coefficient(aircraft_data)