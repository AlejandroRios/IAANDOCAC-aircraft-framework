"""" 
Title     : Section Clmax
Written by: Alejandro Rios
Date      : 05/11/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
Mach
AirportElevation
PROOT
Craiz
PKINK
Cquebra
PTIP
Cponta

Outputs:
clmax_airfoil
flagsuc
"""
########################################################################################
import numpy as np
import os
from atmosphere import atmosphere
from temperature import temperature
########################################################################################
"""Constants declaration"""
########################################################################################
def cf_flat_plate(Re,Mach,Altitude):
    xt        = 0.05
    T         = temperature(Altitude)
    #Transition
    Rex = Re * xt
    if Rex <= 0:
        Rex = 0.0001

    theta = .671*xt/np.sqrt(Rex)
    xeff = (27.78*theta*(Re**0.2))**1.25
    Rext = Re*(1-xt+xeff)

    Cfturb = 0.455/((np.log10(Rext))**2.58)  # Original formula
#        Cfturb = 0.455/(((log10(Rext))^2.58)*((1+0.144*Mach*Mach)^0.65))
    Cflam = 1.328/np.sqrt(Rex)
    Cfstart = 0.455/((np.log10(Re*xeff))**2.58)
    cfval = Cflam*xt + Cfturb*(1-xt+xeff) - Cfstart*xeff
    # Mach Effects
    Tw = 1.0 + .178*Mach*Mach
    T1 = 1.0 + .035*Mach*Mach + .45*(Tw-1)
#
    mu1 = (T1**1.5) * (T+216)/(T*T1+216)
    R1 = 1/(mu1*T1)
    CfRatio = 1/(T1*(R1**0.2))
    cf_val = cfval*CfRatio
#         fprintf('\n Mach = #4.2f \n Altitude = #i ft \n Transition at #5.3f \n',Mach,Altitude,xt)
#         fprintf('\n cf = #7.5f \n',cfval)
            
    return(cf_val)