"""
Function  : TSFC.py
Title     : Thrust specific fuel consumption
Written by: Alejandro Rios
Date      : November/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculates the thrust specific fuel consumption

Future implementations:
    - 

Inputs:
    - Specific fuel consumption at cruise
    - Reference altitude
    - Mach number for which TSFC is referenced
    - Bypass ratio
    - Flight condition altitude
    - Mach number at loiter
Outputs:
    - Thrust
"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
from atmosphere import atmosphere
########################################################################################
"""Function definition"""
########################################################################################

def TSFC(c_ref,href_ft,Mref,BPR,h_ft,M):
    # Calculo do consumo especifico do motor
    # Valores de refer�ncia s�o para a MMO na altitude de cruzeiro
    # Ref: Howe - Aircraft Conceptual Design Synthesis
    #--------------------------------------------------------------------------
    # Passo 1: Ajusta parametro para condicao de referencia
    atm=atmosphere(href_ft,0)
    rho=atm.ro
    sigma_ref=rho/1.225
    T1=(1-0.15*(BPR**0.65))
    T2=(1+0.28*(1+0.063*BPR*BPR)*Mref)
    c_linha= c_ref/(T1*T2*(sigma_ref**0.08))
    # Passo 2: Calculo no ponto desejado
    atm=atmosphere(h_ft,0)
    sigma=atm.ro/1.225
    T2=(1+0.28*(1+0.063*BPR*BPR)*M)
    c=c_linha*T1*T2*(sigma**0.08)

    return(c)