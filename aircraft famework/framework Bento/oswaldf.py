"""
Function  : oswaldf.py
Title     : Oswald factor function
Written by: Alejandro Rios
Date      : Dezember/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the oswald factor

Future implementations:
    - 

Inputs:
    - Mach number
    - Wing aspect ratio
    - Wing sweep angle c/4
    - Wing taper ratio
    - Wing mean thickness
    - Engine wing position
Outputs:
    - Oswald factor
"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
########################################################################################
"""Function definition"""
########################################################################################
def oswaldf(Mach,AR,phi14,afilam,tcmed,nedebasa):
    # Oswald's factor calculation
    # Reference: Prof. Dieter Scholz Hamburg Angewandte Wissenschaft
    #               Universitaet
    rad  = np.pi/180
    #
    aux1 = 1+0.12*Mach**6
    aux2 = 0.1*(3*nedebasa+1)/((4+AR)**0.8)
    fy   = 0.005*(1+1.5*(afilam-0.6)**2)
    aux3 = (0.142+ fy*AR*((10*tcmed)**0.33))/(np.cos(phi14*rad)**2)
    e    = 1/(aux1*(1+aux2+aux3))
    return(e)