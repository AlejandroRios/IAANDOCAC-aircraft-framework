"""
Function  : airspeed.py
Title     : Airspeed conversor function
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module performs speed transformations.
    - Reference: Gudmundsson, General Aviation Aircraft Design: Applied Methods and Procedures, 2013
    - pag 770
    - Reference: Blake, BOEING CO. Flight Operations Engineering - Jet Transport Performance Methods. 7th ed. Boeing Co.,Everett,Estados Unidos,1989
    - Chapter 6, page 6-12
    - Chapter 30, page 30-2
Inputs:
    - Altitude [m]
    - Delta ISA [deg C]
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
def mach_to_V_cas(mach,h,delta_ISA):
    """
    Description:
        - 
    Inputs:
        - Altitude [m]
        - Delta ISA [deg C]
        - Mach number
    Outputs:
        - Calibated airspeed [knots]
    """
    _,delta,_,_,_,_,_ = atmosphere_ISA_deviation(h,delta_ISA)

    speed_of_sound = 661.4786 # sea level [knots]
    aux1 = ((0.2 * (mach**2) + 1)**3.5) - 1
    aux2 =  (delta*aux1 + 1)**(1/3.5)
    return speed_of_sound * np.sqrt(5 *(aux2 - 1))

def mach_to_V_true(mach,h,delta_ISA):
    """
    Description:
        - 
    Inputs:
        - Altitude [m]
        - Delta ISA [deg C]
        - Mach number
    Outputs:
        - true airspeed [knots]
    """
    theta,_,_,_,_,_,_ = atmosphere_ISA_deviation(h,delta_ISA)
    speed_of_sound = 661.4786 # sea level [knots]



    return speed_of_sound * mach * np.sqrt(theta)




def V_cas_to_mach(V_cas,h,delta_ISA):
    """
    Description:
        - 
    Inputs:
        - Altitude [m]
        - Delta ISA [deg C]
        - Calibated airspeed [knots]
    Outputs:
        - Mach number
    """

    _,delta,_,_,_,_,_ = atmosphere_ISA_deviation(h,delta_ISA)
    speed_of_sound = 661.4786 # sea level [knots]

    aux1 = ((1 + 0.2*((V_cas/speed_of_sound)**2))**3.5) - 1
    aux2 = ((1/delta)*aux1 + 1)**((1.4-1)/1.4)
    return np.sqrt(5 * (aux2-1))

########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
