"""" 
Function  : cd0_Torenbeek.py
Title     : Section Clmax
Written by: Alejandro Rios
Date      : 05/11/19
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates CD0 in accordance with the method proposed by Torenbeek:
        Torenbee, E., "Advanced Aircraft Design," 1st Edition, 2013, pg 123-125.
    
Future implementations:
    - 

Inputs:
    - Mach number
    - MTOW                      [lb]
    - Wing area                 [m2]
    - Wing span                 [m]
    - Taper ratio
    - Wing thickness mean
    - Fuselage diamenter        [m]
    - Altitude                  [ft]
Outputs:
    - CD0
"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
import os
from atmosphere import atmosphere
from cf_flat_plate import cf_flat_plate
########################################################################################
"""Function definition"""
########################################################################################
def cd0_Torenbeek(nmach,swm2,bw,wMAC,tc,df,h,swetm2):
    ISADEV = 0
    atm   = atmosphere(h,ISADEV)
    ni    = atm.visc/atm.ro
    V     = nmach*atm.va
    #
    reybar = V*swetm2/bw/ni
    # rphi = 4 para avioes ah helice = 3,5 para avioes ah jato
    #
    rphi   = 3.5
    sfront = np.pi*df**2/4 +2*(wMAC*tc*bw/2)
    #
    knid=1+255*(reybar**-0.35) # Page 104 Torenbeek (jet airplanes)
    # CD0=0.044*(reybar^(-1/6))*knid*(swetm2+rphi*sfront)
    # CD0=CD0/swm2
    cfval=cf_flat_plate(reybar,nmach,h)
    CD0=cfval*knid*(swetm2+rphi*sfront)/swm2
    return(CD0)