"""" 
Function  : CDWINDMILLTOREN.py
Title     : CD windmill Torenbeek
Written by: Alejandro Rios
Date      : Dezember/2019
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - Windmill drag calculation according to Torenbeek

Future implementations:
    - 

Inputs:
    - Mach number
    - Engine diameter
    - Engine bypass
Outputs:
    - Delta CD due to windmill

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
from atmosphere import atmosphere
from cd0_Torenbeek import cd0_Torenbeek
########################################################################################
"""Function definition"""
########################################################################################
def CDWINDMILLTOREN(jmach,ediam,ebypass):
    VN               = 0.92 
    if ebypass < 3.5:
        VN = 0.42

    AN=np.pi*ediam*ediam/4
    term1=2/(1+0.16*jmach*jmach)
    cdwindmilli=0.0785*(ediam*ediam)+term1*AN*VN*(1-VN)

    return(cdwindmilli)