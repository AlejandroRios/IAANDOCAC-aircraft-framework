"""
Function  : DCD_LDG.py
Title     : Delta CD during landing
Written by: Alejandro Rios
Date      : Dezember/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the delta CD associated to flaps deflected during landing

Future implementations:
    - 

Inputs:
    - MTOW
    - Wing Area
    - Flap deflection
    - Maximum flap deflection
Outputs:
    - Delta CD flap deflection landing

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
########################################################################################
"""Function definition"""
########################################################################################

def DCD_LDG(MTOW_kg,wS,DFLAP,DFLAP_MAX):

    K=(0.57 - 0.26*DFLAP/DFLAP_MAX)*0.001

    DCDLDG = K*((MTOW_kg)**0.785)/wS;

    return(DCDLDG)