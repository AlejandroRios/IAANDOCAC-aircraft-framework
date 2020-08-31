"""" 
Function  : CDW_SHEVELL.py
Title     : Wave drag 
Written by: Alejandro Rios
Date      : Dezember/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - Wave drag calculation according to Shevell

Future implementations:
    - 

Inputs:
    - Quarter-chord wing sweepback angle
    - Maximum Mach number
    - Mach number
Outputs:
    - Delta CD due to wave drag

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
########################################################################################
"""Function definition"""
########################################################################################
def CDW_SHEVELL(phi14,MMO,M):
    rad=np.pi/180
    A=0.00057
    B=3.34821
    MDD=MMO+0.03
    auxcos=(np.cos(rad*phi14))**3
    T1=0.002/(A*auxcos)
    T1 = B + np.arctan(T1)
    Mcrit= B*MDD/T1
    DCDw= auxcos*A*np.tan(B*(M/Mcrit) - B)

    return(DCDw)