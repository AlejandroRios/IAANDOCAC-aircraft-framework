"""" 
Title     : Atmosphere
Written by: Alejandro Rios
Date      : 30/10/19
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
class structtype():
    pass

atm = structtype()
########################################################################################
"""Constants declaration"""

g=9.80665 #gravidadde
temp=288.15 #temperatura
rho=1.225 # densidade
pres=101325 # pressao
gama=1.4 # cp/cv
R=29.26 # constante dos gases
########################################################################################

def atmosphere(hp,ISADEV):

    if hp <= 36089:
        TAEs=temp-0.0019812*hp
        delta=(TAEs/temp)**5.2561#delta
    else:
        TAEs=216.65
        delta=0.223358*np.exp(-0.000048063*(hp-36089)) #delta


    atm.TAE=TAEs+ISADEV # temperatura isa
    atm.teta=atm.TAE/temp 
    atm.delta = delta
    atm.sigma=delta/atm.teta
    atm.p=pres*delta/1000 # pressure
    atm.ro=rho*atm.sigma #densidade
    atm.va=np.sqrt(gama*g*R*atm.TAE)# velocidade do som

    mi0=18.27E-06
    Tzero=291.15 # Reference temperature
    Ceh= 120 # C = Sutherland's constant for the gaseous material in question
    atm.visc=mi0*((atm.TAE+Ceh)/(Tzero+Ceh))*((atm.TAE/Tzero)**1.5)

    return(atm)