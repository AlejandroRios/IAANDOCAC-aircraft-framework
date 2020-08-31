"""" 
Title     : WEW2Bento
Written by: Alejandro Rios
Date      : 04/12/19
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

def DCD_LDG(MTOW_kg,wS,DFLAP,DFLAP_MAX):

    K=(0.57 - 0.26*DFLAP/DFLAP_MAX)*0.001

    DCDLDG = K*((MTOW_kg)**0.785)/wS;

    return(DCDLDG)