"""" 
Title     : Cruise long range
Written by: Alejandro Rios
Date      : 03/12/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
hp: pressure-altitude [ft]
ISADEV: ISA temperature deviation

Outputs:
atm(1)=temperatura isa [K]
atm(2)=teta 
atm(3)=delta
atm(4)=sigma
atm(5)=pressure [KPa]
atm(6)=air density [Kg/m2]
atm(7)=sound speed [m/s]
atm(8)= air viscosity

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
from atmosphere import atmosphere
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