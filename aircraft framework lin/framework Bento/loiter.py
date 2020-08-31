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
from oswaldf import oswaldf
from cd0_Torenbeek import cd0_Torenbeek
from CDW_SHEVELL import CDW_SHEVELL
from atmosphere import atmosphere
from TSFC import TSFC
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