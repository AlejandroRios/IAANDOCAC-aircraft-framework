"""" 
Title     : WEW2Bento
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
from cd0_Torenbeek import cd0_Torenbeek
########################################################################################

def CDWINDMILLTOREN(jmach,ediam,ebypass):
    # Windmilling drag(Torenbeek)
    #
    VN               = 0.92 
    if ebypass < 3.5:
        VN = 0.42

    AN=np.pi*ediam*ediam/4
    term1=2/(1+0.16*jmach*jmach)
    cdwindmilli=0.0785*(ediam*ediam)+term1*AN*VN*(1-VN)


    return(cdwindmilli)