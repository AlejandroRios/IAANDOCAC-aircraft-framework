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
from cf_flat_plate import cf_flat_plate
########################################################################################
"""Constants declaration"""
########################################################################################


def cd0_Torenbeek(nmach,swm2,bw,wMAC,tc,df,h,swetm2):
    # Calculo do CD0 de acordo com metodo proposto por Torenbeek:
    # Torenbee, E., "Advanced Aircraft Design," 1st Edition, 2013, pg 123-125.
    # Entradas:
    # nmach:  numero de Mach
    # mtowlb: peso maximo de decolagem em libras
    # swm2:   area da asa em metros ao quadrado
    # bw:     envergadura da asa em metros
    # afil:   afilamento da asa
    # tc:     espessura relativa media da asa
    # df:     diametro da fuselagem em metros
    # h:      altitude em pes
    #--------------------------------------------------------------------------
    ISADEV = 0
    atm        = atmosphere(h,ISADEV)
    ni    = atm.visc/atm.ro
    V     = nmach*atm.va
    #
    reybar = V*swetm2/bw/ni
    # rphi = 4 para avioes ah helice = 3,5 para avioes ah jato
    #
    rphi   = 3.5
    sfront = np.pi*df**2/4 +2*(wMAC*tc*bw/2)
    #
    knid=1+255*(reybar**-0.35) # Page 104 Torenbeek (jet airplanes)
    # CD0=0.044*(reybar^(-1/6))*knid*(swetm2+rphi*sfront)
    # CD0=CD0/swm2
    cfval=cf_flat_plate(reybar,nmach,h)
    CD0=cfval*knid*(swetm2+rphi*sfront)/swm2
    return(CD0)