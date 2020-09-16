"""
Function  : balanced_lenght_field.py
Title     :
Written by: 
Date      : 
Last edit :
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - CL maximum for take of configuration
    - 
Inputs:
    -
Outputs:
    - 
TODO's:
    - where does Tmax equation comes from?
    - max. engine rate of what???
    - Codigos José no gravity. Dimensional analysis inconsistency!

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

def balanced_lenght_field(weight_takeoff,wing_surface,CL_max_takeoff,T_avg,h_airfield,delta_ISA):
    '''
    Note: for project design the case of delta_gamma2 = 0 presents most interest, as the corresponding weight
    is limited by the second segment climb requirement (Torenbeek, 1982) 
    '''
    h_takeoff = 10.7 # horizontal distance from airfield surface requirement according to FAR 25 - [m] 
    delta_gamma2 = 0
    delta_S_takeoff = 200 
    g = 9.81
    CL_2 = 0.694*CL_max_takeoff 
    mu = 0.01*CL_max_takeoff + 0.02
    _,_,sigma,_,_,rho,_ = atmosphere_ISA_deviation(h_airfield,delta_ISA)
   

    aux1 = 0.863/(1 + (2.3*delta_gamma2))
    aux2 = ((weight_takeoff/wing_surface)/(rho*g*CL_2)) + h_takeoff
    aux3 = (1/((T_avg/weight_takeoff)-mu)) + 2.7
    aux4 = delta_S_takeoff/np.sqrt(sigma)

    return aux1*aux2*aux3 + aux4
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################

# weight_takeoff = 55000
# wing_surface = 100
# CL_max_takeoff = 2.4
# h_airfield = 2500
# delta_ISA = 19.9530

# # This should come from another module instead of being calculated here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ##############################################################################################################
# lb_2_kg = 0.45359237
# bypass_ratio = 5.0
# maximum_rate = 22000
# thrust_altitude_factor = 0.8
# number_engines = 2
# _,_,sigma,_,_,_,_ = atmosphere_ISA_deviation(h_airfield,delta_ISA)
# T_max = (0.95 * maximum_rate * (sigma**thrust_altitude_factor) * lb_2_kg)/2
# T_avg = 0.75 *  ((5 + bypass_ratio)/(4 + bypass_ratio)) * T_max
# ##############################################################################################################

# BFL = balanced_lenght_field(weight_takeoff,wing_surface,CL_max_takeoff,T_avg,h_airfield,delta_ISA)

