"""
Function  : atmosphere.py
Title     : Atmosphere functions ISA deviation
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - International Standard Atmosphere (ISA) based in:
    - Reference: Blake, BOEING CO. Flight Operations Engineering - Jet Transport Performance Methods. 7th ed. Boeing Co.,Everett,Estados Unidos,1989
    - Chapter 4, page 4-1
Inputs:
    - Altitude [ft]
    - Delta ISA [deg C]
Outputs:
    - T = temperature [K]
    - p = pressure [Pascal] 
    - rho = density [kg/m3] 
    - a = sound speed [kts]
TODO's:
    - 

"""
########################################################################################
"IMPORTS"
########################################################################################
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def atmosphere_ISA_deviation(h,delta_ISA):
    h = h

    h1 = 11 # [km]
    L0 = -6.5e-3

    T0 = 288.15 # [K]
    p0 = 1.01325e5 # [Pa]
    rho0 = 1.2250 # [kg/m3]

    T1 = T0+L0*h1*1e3

    lambda_rate = 0.0019812 

    C1 = 5.25588
    C2 = 0.22336
    C3 = 36089.24
    C4 = 20805.7

    tropopause = (71.5 + delta_ISA)/lambda_rate

    if h<=tropopause:
        # at or below Troposphere:
        theta = (T0 - (lambda_rate*h) + delta_ISA)/T0
        delta = ((T0 - lambda_rate*h)/T0)**C1
    elif h>tropopause:
        # above Troposphere:
        theta = (T1 + delta_ISA)/T0
        delta = C2*np.exp((C3 - h)/C4)

    sigma = sigma = delta/theta
    a = 661.4786*np.sqrt(theta) # [kts]

    T_ISA = theta*T0
    P_ISA = delta*p0
    rho_ISA = sigma*rho0

    return theta,delta,sigma,T_ISA,P_ISA,rho_ISA,a
########################################################################################
"""MAIN"""
########################################################################################


########################################################################################
"""TEST"""
########################################################################################
# h = 2500
# delta_ISA = 0
# print(atmosphere_ISA_deviation(h,delta_ISA))