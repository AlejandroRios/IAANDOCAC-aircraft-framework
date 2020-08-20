"""" 
Title     : Crew Salary Function
Written by: Alejandro Rios
Date      : 30/10/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
MTOW

Outputs:
Cap_Sal
FO_Sal
"""

########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
########################################################################################
"""Constants declaration"""
########################################################################################

def crew_salary(MTOW):

    A0_CA=-2.2342E+03
    A1_CA=3.3898E+00
    A0_FO=-1.9221E+04
    A1_FO=2.6687E+00
    A0_FA=-1.1533E+04
    A1_FA=1.6012E+00

    Capt_Sal=A0_CA+A1_CA*MTOW
    FO_Sal  =A0_FO+A1_FO*MTOW
    FA_Sal  =A0_FA+A1_FA*MTOW

    return(Capt_Sal,FO_Sal,FA_Sal)



