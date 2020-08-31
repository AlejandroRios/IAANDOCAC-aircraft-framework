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
########################################################################################

def oswaldf(Mach,AR,phi14,afilam,tcmed,nedebasa):
    # Oswald's factor calculation
    # Reference: Prof. Dieter Scholz Hamburg Angewandte Wissenschaft
    #               Universitaet
    rad  = np.pi/180
    #
    aux1 = 1+0.12*Mach**6
    aux2 = 0.1*(3*nedebasa+1)/((4+AR)**0.8)
    fy   = 0.005*(1+1.5*(afilam-0.6)**2)
    aux3 = (0.142+ fy*AR*((10*tcmed)**0.33))/(np.cos(phi14*rad)**2)
    e    = 1/(aux1*(1+aux2+aux3))


    return(e)