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
########################################################################################

def CDW_SHEVELL(phi14,MMO,M):
#--------------------------------------------------------------------------
    rad=np.pi/180
    A=0.00057
    B=3.34821
    # A=0.001171
    # B=3.543
    #--------------------------------------------------------------------------
    # MMO=0.77
    # phi14=17.5
    # M=0.70
    #
    MDD=MMO+0.03
    auxcos=(np.cos(rad*phi14))**3
    T1=0.002/(A*auxcos)
    T1 = B + np.arctan(T1)
    Mcrit= B*MDD/T1

    DCDw= auxcos*A*np.tan(B*(M/Mcrit) - B)

    return(DCDw)