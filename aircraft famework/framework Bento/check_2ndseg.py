"""" 
Title     : WEW2Bento
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
from atmosphere import atmosphere
from cd0_Torenbeek import cd0_Torenbeek
from Drag_flap import Drag_flap
from CDWINDMILLTOREN import CDWINDMILLTOREN
########################################################################################


def check_2ndseg(AirportElevation,wS,bw,wMAC,tcmed,
    neng,bflap,FusDiam,clmaxt,
    W,VTS,VTSweep,ediam,ebypass,dflecflaptakeoff,k_ind_inc,Swet_tot):
    #--------------------------------------------------------------------------
    # Required T/W  for 2nd segment climb 
    #--------------------------------------------------------------------------
    g       = 9.80665
    rad     = np.pi/180
    ft2m    = 0.3048
    m2ft    = 1./ft2m
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------

    atm    = atmosphere(AirportElevation*m2ft,0)
    ro     = atm.ro # densidade [kg/m�]
    va     = atm.va # velocidade do som [m/s]
    #--------------------------------------------------------------------------
    cl2seg              = clmaxt/1.44
    V                   = np.sqrt((W*g)/(cl2seg*wS*0.50*ro))
    M                   = V/va
    M                   = max(0.20,M)
    V                   = M*va
    q                   = (1/2)*ro*V*V
    cl2seg              = (W*g)/(q*wS)
    CD0_airp_inc        = cd0_Torenbeek(M,wS,bw,wMAC,tcmed,FusDiam,AirportElevation*m2ft,Swet_tot)
    CD_airp             = CD0_airp_inc + k_ind_inc*(cl2seg**2)
    # Drag increase due to flaps and rudder deflection
    dcdflapetakeoff     = Drag_flap(dflecflaptakeoff,bflap)
    dcdrudder           = 0.0020*np.cos(rad*VTSweep)*(VTS/wS) 
    dcdwindmilli        = CDWINDMILLTOREN(M,ediam,ebypass)
    #
    cd2seg              = CD_airp+dcdflapetakeoff+dcdrudder+(dcdwindmilli/wS)
    ld2seg              = cl2seg/cd2seg
    #
    w2seg = 1
    if neng ==2:
        w2seg =2*(1/ld2seg+np.arctan(0.024))
    elif neng ==3:
        w2seg =(3/2)*(1/ld2seg+np.arctan(0.027))
    elif neng ==4:
        w2seg =(4/3)*(1/ld2seg+np.arctan(0.03))
 
    return(w2seg)