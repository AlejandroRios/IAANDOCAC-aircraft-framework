"""" 
Function  : cl_max_2D.py
Title     : Section Clmax
Written by: Alejandro Rios
Date      : November/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculate the 2D clmax for each aifoil of the wing segments and other local properties

Future implementations:
    - Redefine function to let use n-segments

Inputs:
    - Mach
    - Airport elevation
    - Airfoil names
    - Airfoil chords
Outputs:
    - Dictionary with airfoils Clmax values
"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
from atmosphere import atmosphere
from rxfoil import rxfoil
########################################################################################
"""Function definition"""
########################################################################################
def cl_max_2d(mach,airport_elevation,airfoil_names,airfoil_chords):
    # Constants declaration
    ft2m    = 0.3048
    m2ft    = 1./ft2m
    hp = airport_elevation
    ISADEV = 0
    flagsuc = 0 # success flag, initially ok

    atm        = atmosphere(hp,ISADEV)

    airfoils = {1:{},
                2:{},
                3:{}}

    for i in range(len(airfoils)):
        j = i+1
        airfoils[j]['name'] = airfoil_names[i]
        airfoils[j]['chord'] = airfoil_chords[i]
        airfoils[j]['reynolds'] = str((atm.ro*mach*atm.va*airfoil_chords[i])/atm.visc)

    #--------------------------------------------------------------------------
    # reynolds   = atm.ro*mach*atm.va/mi

    aoa_ini    = '0'
    aoa_fin    = '20'  
    delta_aoa = '1'


    for i in airfoils:
        airfoil = i

        airfoil_name = airfoils[airfoil]['name']
        mach = str(mach)
        reynolds = airfoils[airfoil]['reynolds']
            
        Cl_max,_,_,_,_,_ = rxfoil(airfoil_name,reynolds,mach,aoa_ini,aoa_fin,delta_aoa)
        airfoils[airfoil]['Clmax'] = Cl_max


    return(airfoils)



