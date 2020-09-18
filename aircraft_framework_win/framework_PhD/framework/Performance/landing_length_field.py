"""
Function  : landing_lenght_field.py
Title     :
Written by: 
Date      : 
Last edit :
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - 
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
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

def landing_length_field(aircraft_data,airport_data):
    '''
    '''
    # Aircraft data import
    CL_max_landing = aircraft_data['CL_maximum_landing']
    weight_landing = aircraft_data['maximum_landing_weight']
    wing_surface = aircraft_data['wing_surface']

    # Airport data import
    airfield_elevation = airport_data['elevation']
    delta_ISA = airport_data['delta_ISA']


    _,_,sigma,_,_,rho,_ = atmosphere_ISA_deviation(airfield_elevation,delta_ISA)
    
    gamma_bar = 0.1 # mean value of (D-T)/W
    h_landing = 15.3 # screen height in landing
    g = 9.81
    a_bar_g = 0.4 # mean_deceleration, between 0.4 to 0.5 for jets
    Delta_n = 0.1 # incremental_load_factor during flare
    f_land = 5/3 # landing safe factor FAR Part 91 


    aux1 = 1/gamma_bar
    aux2 = 1.69*((weight_landing/wing_surface)/(h_landing*rho*g*CL_max_landing))
    aux3 = (1/a_bar_g) * (1 - ((gamma_bar**2)/Delta_n)) + (gamma_bar/Delta_n)

    S_landing_h_landing = aux1 + aux2*aux3

    return S_landing_h_landing*h_landing*f_land
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
