"""" 
Title     : Section Clmax
Written by: Alejandro Rios
Date      : 05/11/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
Mach
AirportElevation
PROOT
Craiz
PKINK
Cquebra
PTIP
Cponta

Outputs:
clmax_airfoil
flagsuc
"""
########################################################################################
import numpy as np
import os
from atmosphere import atmosphere
########################################################################################
"""Constants declaration"""
########################################################################################
def temperature(h):
    temps = 518.67
    if  0 <= h and h < 36089:
        satheta = 1.0 - h/145442
    elif 36089 <= h and h < 65617:
        satheta = 0.751865
    elif 65617 <= h and h < 104987:
        satheta = 0.682457 + h/945374
    elif 104987 <= h and h < 154199:
        satheta = 0.482561 + h/337634
    elif 154199 <= h and h < 167323:
        satheta = 0.939268
    elif 167323 <= h and h < 232940:
        satheta = 1.434843 - h/337634
        
    temps=temps*satheta
    return(temps)