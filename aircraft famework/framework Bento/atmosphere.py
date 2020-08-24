"""" 
Function  : atmosphere.py
Title     : Atmosphere
Written by: Alejandro Rios
Date      : Octover/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the atosphere characteristics

Future implementations:
    - 

Inputs:
    - hp: pressure-altitude [ft]
    - ISADEV: ISA temperature deviation

Outputs:
    - atm(1)=temperature isa [K]
    - atm(2)=teta 
    - atm(3)=delta
    - atm(4)=sigma
    - atm(5)=pressure [KPa]
    - atm(6)=air density [Kg/m3]
    - atm(7)=sound speed [m/s]
    - atm(8)= air dynamic viscosity [kg/ms]
      Ref: (Sutherland, W. (1893), "The viscosity of gases and molecular force", Philosophical Magazine, S. 5, 36, pp. 507-531 (1893).)

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
########################################################################################
class structtype():
    pass
atm = structtype()
########################################################################################
"""Constants declaration"""
g = 9.80665   # gravity
temp = 288.2 # temperature [K]
rho = 1.225   # density [Kg/m3]
pres = 101325 # pressure
gama = 1.4    # cp/cv
R=286.9     # gas constant
########################################################################################
def atmosphere(hp,ISADEV):

    if hp <= 36089:
        TAEs = temp-0.0019812*hp
        delta = (TAEs/temp)**5.2561 # delta
    else:
        TAEs = 216.65
        delta = 0.223358*np.exp(-0.000048063*(hp-36089)) #delta

    atm.TAE = TAEs+ISADEV # temperatura isa
    atm.teta = atm.TAE/temp 
    atm.delta = delta
    atm.sigma = delta/atm.teta
    atm.p=pres*delta/1000 # pressure
    atm.ro=rho*atm.sigma #densidade
    atm.va=np.sqrt(gama*R*atm.TAE)# velocidade do som

    # mi0=18.27E-06
    # Tzero=291.15 # Reference temperature
    # Ceh= 120 # C = Sutherland's constant for the gaseous material in question
    # atm.visc=mi0*((atm.TAE+Ceh)/(Tzero+Ceh))*((atm.TAE/Tzero)**1.5)

    mi0 = 1.716E-5
    S = 110.4
    Tzero = 288.2
    atm.visc= mi0*((atm.TAE/Tzero)**(3/2)) * ((atm.TAE + S)/(Tzero + S))
    return(atm)