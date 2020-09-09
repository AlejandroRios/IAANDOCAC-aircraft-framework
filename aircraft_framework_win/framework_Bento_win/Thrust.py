"""
Function  : Thrust.py
Title     : Static thrust at given condition
Written by: Alejandro Rios
Date      : November/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculate thrust for different static conditions

Future implementations:
    - 

Inputs:
    - Static thrust
    - Bypass ratio
    - Altitude
    - Mach number
Outputs:
    - Thrust
"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
from atmosphere import atmosphere
########################################################################################
"""Constants declaration"""
########################################################################################

def Thrust(T0,BPR,h_ft,M):
# Calculo da tracao do motor
# Ref: Howe - Aircraft Conceptual Design Synthesis
#--------------------------------------------------------------------------
    atm    = atmosphere(h_ft,0)
    rho=atm.ro
    sigma=rho/1.225

    if M < 0.40:
        K1=1
        K2=0
        K3=-0.60
        K4=-0.04
    else:
        K1=0.88
        K2=-0.016
        K3=-0.30
        K4=0

    slinha=0.70

    if h_ft > 36089:
        slinha=1

    tau_factor=(K1 + K2*BPR + (K3 + K4*BPR)*M)*(sigma**slinha)
    T=T0*tau_factor

    return(T)