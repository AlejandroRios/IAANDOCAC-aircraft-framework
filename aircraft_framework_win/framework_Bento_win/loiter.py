"""
Function  : loiter.py
Title     : Loiter 
Written by: Alejandro Rios
Date      : Dezember/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the amount of fuel burned during loiter

Future implementations:
    - 

Inputs:
    - Wait altitude at loiter
    - Mach at loiter
    - Mass after descent flight
    - Wait time at loiter
    - Specific fuel comsumption at loiter
    - Wing area
    - Wing aspect ratio
    - Wing sweep c/4
    - Wing taper ratio
    - Wing MAC
    - Wing mean thickness
    - Engine mount position
    - Fuselage diameter
    - Aircraft wetted surface
Outputs:
    - Mass of fuel burned during loiter

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
from oswaldf import oswaldf
from cd0_Torenbeek import cd0_Torenbeek
from CDW_SHEVELL import CDW_SHEVELL
from atmosphere import atmosphere
from TSFC import TSFC
########################################################################################
"""Function definition"""
########################################################################################
def loiter(altesp,Machesp,mesperai,tempespera,ctloiter,sw,
    arw,phi14,afilam,wMAC,tcmed,nedebasa,df,Swet_tot):
# This routine calculates the amount of fuel burned during loiter
#--------------------------------------------------------------------------
    dmfuelloiter = 1000
    mfuelloiter  = 50
    #vespera      = Machesp*vsom
    bw=np.sqrt(arw*sw)
    cd0=cd0_Torenbeek(Machesp,sw,bw,wMAC,tcmed,df,altesp,Swet_tot)      
    # Iteration is needed because Oswald's factor depends on speed
    while dmfuelloiter > 3:
        eesp       = oswaldf(Machesp, arw, phi14, afilam, tcmed, nedebasa)
        k          = 1/(np.pi*arw*eesp)
        cd=2*cd0
        cl=np.sqrt(cd0/k)
        ldmaxauton=cl/cd

        #Machesp = min(0.50,vespera/vsom)
        tempesperah=tempespera/60
        T1=(tempesperah/ldmaxauton)*ctloiter
        fmassesp = 1/np.exp(T1)
        newfuel=mesperai*(1-fmassesp)
        dmfuelloiter=abs(newfuel-mfuelloiter)
        mfuelloiter = newfuel

    return(mfuelloiter)