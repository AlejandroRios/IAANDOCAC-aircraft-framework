"""" 
Function  : @ingroup Methods-Geometry-Two_Dimensonal-Cross_Section-Airfoil
Title     : Airfoil Sobieski coefficients
Written by: Alejandro Rios
Date      : Sep/2019
Language  : Python
Aeronautical Institute of Technology
"""
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
from scipy.optimize import differential_evolution
import scipy as sp
import os
# ----------------------------------------------------------------------
#  Compute Airfoil Parametres
# ----------------------------------------------------------------------
## @ingroup Methods-Costs-Industrial_Costs
# def airfoil_sobieski_coefficients(airfoil_name):
"""Compute Sobieski coefficients

Assumptions:
No assumptions

Source:
"", Sobieski

Inputs:
airfoil dime (.dat)     [-]     Airfoil .dat coordinates


Outputs:
Sobieski coefficientes:
r0          [-] 
t_c         [-]     thick to chord ratio
X_tcmax     [m]     X position of tcmax  
theta       [-]
epsilon     [-]
Ycmax       [-]
YCtcmax     [-]
X_Ycmax     [-]
xp          [-]
yu          [-]
yl          [-]

Properties Used:
N/A
"""


########################################################################################
"""Importing Data"""
########################################################################################
def airfoil_preprocessing(airfoil,panel_number):
    # panel_number  = '101'
    delimiter = '1'
    xfoil_run_file  = 'xfoil_preproc.txt'

    panel_number = str(panel_number)
    ########################################################################################
    """Xfoil run file writting"""
    ########################################################################################
    # Create the airfoil
    fid = open(xfoil_run_file,"w")
    fid.write("DELI" + delimiter + "\n")

    # fid.write("PLOP \n")
    # fid.write("G \n\n")

    fid.write("load \n")
    fid.write("" + airfoil + ".dat" "\n\n")
    fid.write("PPAR\n")
    fid.write("N " + panel_number + "\n")
    fid.write("\n\n")
    fid.write("SAVE \n")
    fid.write("" + airfoil + ".dat" "\n")
    fid.write("Y \n")

    fid.close()

    ########################################################################################
    """Xfoil Execution"""
    ########################################################################################
    os.system("xfoil < xfoil_preproc.txt > NUL.dat")

    if os.path.exists(xfoil_run_file):
        os.remove(xfoil_run_file)

    if os.path.exists(':00.bl'):
        os.remove(':00.bl')

    if os.path.exists('NUL.dat'):
        os.remove('NUL.dat')








