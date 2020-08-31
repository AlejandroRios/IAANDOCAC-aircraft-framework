"""" 
Function  : cruise_longrange.py
Title     : Cruise long range
Written by: Alejandro Rios
Date      : Dezember/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the fuel mass burned during cruise

Future implementations:
    - 

Inputs:
    - Cruise altitude
    - Cruise mass
    - Wing aspect ratio
    - Wing area
    - Wing MAC
    - Cruise range
    - MMO
    - Wing taper ratio
    - Engine position ???
    - Wing sweep angle at c/4
    - Fuselage diameter
    - Specific fuel consumption at cruise altitude
    - Altitude for which TSFC is referenced [ft]
    - Mach number for which TSFC is referenced
    - Engine bypass ratio
    - t/c root
    - t/c break
    - t/c tip
    - Total airplane wetted area


Outputs:
    - mass burned during cruise ???
    - Mach number
    - Time during cruise phase
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
def cruzeiro_longrange(Hft,masscruzi,
    arw,sw,wMAC,rangem,MMO,
    afilam, nedebasa,phi14,df,ctref,Href,Mref,BPR,tcroot,tcbreak,tctip,
    Swet_tot):

    tcmed = (0.50*(tcroot+tcbreak) + 0.50*(tcbreak+tctip))/2 # average section max. thickness of the wing
    atm   = atmosphere(Hft,0)
    rhoi  = atm.ro
    vsomi = atm.va
    mld   = -10000
 
    for NMach in np.arange(0.65,MMO+0.01,0.01):
        ecruise = oswaldf(NMach, arw, phi14, afilam, tcmed, nedebasa)
        # Long-range lift coefficient
        vcruzi  = NMach*vsomi
        bw      = np.sqrt(arw*sw) # wingspan
        CD0     = cd0_Torenbeek(NMach,sw,bw,wMAC,tcmed,df,Hft,Swet_tot)
        cl_long = masscruzi*9.81/(0.50*rhoi*sw*vcruzi*vcruzi)
        #cdw     = cdwave(NMach,cl_long,phi14,tcmed) # wave drag
        #CDw=CDW_DELFT(NMach,tcmed,cl_long,phi14,afilam,arw)
        CDw=CDW_SHEVELL(phi14,MMO,NMach)
        k       = 1/(np.pi*arw*ecruise)
        cd      = CD0 + k*(cl_long**2) + CDw
        mldcalc = NMach*cl_long/cd
        
        if mldcalc > mld:
            mld       = mldcalc
            Mach_calc = NMach
        #     Machmax = NMach
            ct=TSFC(ctref,Href,Mref,BPR,Hft,NMach)
            masfrac   = np.exp((rangem*cd*ct)/(3600*cl_long*vcruzi))
            massfin   = masscruzi/masfrac
            mcombc    = masscruzi-massfin 
            time_cru  = rangem/(3600*Mach_calc*vsomi)  # [h]
            
        # for
    #fprintf(' \n Machmax: #4.2f L/D max : #5.2f \n', Machmax, mld/Machmax)
    # function

    return(mcombc,Mach_calc,time_cru)