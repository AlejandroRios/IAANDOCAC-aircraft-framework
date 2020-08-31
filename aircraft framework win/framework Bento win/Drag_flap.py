"""
Function  : Drag_flap.py
Title     : Drag due to flap
Written by: Alejandro Rios
Date      : September/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates drag due to flap deflection

Future implementations:
    - 

Inputs:
    - deflec: flap deflection [degrees]
    - flap span
Outputs:
    - Drag coefficient due to flap deflection

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
def Drag_flap(deflec,bflap):
    #
    # Ref: Drag Force and Drag Coefficient
    # Sadraey M., Aircraft Performance Analysis, VDM Verlag Dr. Mueller, 2009
    #**************************************************************************
    # Input:
    # deflec: flap deflection [degrees]
    # longtras: chordwise location of aft spar
    #**************************************************************************
    # Considerations:
    # Internal flap: double sllotted
    # External flap: single slotted
    #**************************************************************************
    # A_int = 0.0011
    # B_int = 1
    # A_ext = 0.00018
    # B_ext = 2
    # cflap=1 -(longtras +0.02)
    # # 
    # cdflap_int = cflap*A_int*(deflec^B_int)
    # cdflap_ext = cflap*A_ext*(deflec^B_ext)
    # cdflap     = cdflap_int + cdflap_ext
    # 
    # clear A_int B_int A_ext B_ext 
    cdflap = 0.0023*bflap*deflec

    return(cdflap)