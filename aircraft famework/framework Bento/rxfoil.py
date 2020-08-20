"""" 
Title     : Xfoil Python function
Written by: Alejandro Rios
Date      : 22/08/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
airfoil name
Reynolds number
AoA initial
AoA final
Delta AoA

Outputs:
Cl max.
Cd@Cl max.
Cl@Cd min.
Cd min.
Cl min.
Cd@Cl min.
"""

########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
########################################################################################
"""Constants declaration"""
########################################################################################

def rxfoil(airfoil,reynolds,mach,aoa_ini,aoa_fin,delta_aoa):
    # airfoil    = 'alexky'
    # NACA       = '0012'
    # aoa_ini    = '-10'
    # aoa_fin    = '20'  
    # delta_aoa = '1'
    panel_number  = '200'
    xfoil_run_file  = 'rxfoil_input.txt'
    # reynolds.str()
    iterations = '200'

    # saveFlnmAF = 'Save_Airfoil.txt'
    polar_file = 'Save_Polar.txt'

    ########################################################################################
    """Folder cleaning"""
    ########################################################################################
    if os.path.exists(polar_file):
        os.remove(polar_file)

    ########################################################################################
    """Xfoil run file writting"""
    ########################################################################################
    # Create the airfoil
    fid = open(xfoil_run_file,"w")
    fid.write("load \n")
    fid.write("" + airfoil + ".dat" "\n\n")
    
    fid.write("GDES \n")
    fid.write("CADD\n")
    fid.write("\n\n\n\n")
    fid.write("PANE \n")

    fid.write("PLOP\n")
    fid.write("G \n\n")

    fid.write("PPAR\n")
    fid.write("N " + panel_number + "\n")
    fid.write("\n\n")
    # fid.write("PSAV "  + saveFlnmAF + "\n")

    fid.write("OPER\n")
    fid.write("VISC" " " + reynolds + "\n")
    fid.write("M" " " + mach + "\n")
    fid.write("ITER" " " + iterations + "\n")
    fid.write("PACC \n")
    fid.write("\n\n")
    fid.write("ASEQ \n")
    fid.write("" + aoa_ini + "\n")
    fid.write("" + aoa_fin + "\n")
    fid.write("" + delta_aoa + "\n")
    fid.write("PACC \n")
    fid.write("PWRT 1 \n")
    fid.write("" + polar_file + "\n")

    fid.close()

    ########################################################################################
    """Xfoil Execution"""
    ########################################################################################
    os.system("xfoil < rxfoil_input.txt > NUL.dat")

    if os.path.exists(xfoil_run_file):
        os.remove(xfoil_run_file)

    ########################################################################################
    """Data extraction"""
    ########################################################################################

    file_path = "/home/alejandro/Documents/Github/GIT_IAANDOCAC/IAANDOCAC-aircraft-framework/aircraft famework/framework Bento/"
    file_name  = file_path  + polar_file
        
    # Load the data from the text file
    db= np.loadtxt(polar_file, skiprows=12)
    # df = pd.read_csv(polar_file, delimiter = ' ',skiprows=13, header = None, names=list('abcdefghi'))
    df = pd.DataFrame(db)
    df.columns = ['alpha','CL','CD','CDp','CM','Top_Xtr','Bot_Xtr','Top_Itr','Bot_Itr']

    # print(df.head())

    Cl_max = df['CL'].max()
    Cd_Cl_max = df.loc[df['CL'] == Cl_max, 'CD'].iloc[0]
    alpha_Cl_max = df.loc[df['CL'] == Cl_max, 'alpha'].iloc[0]

    Cd_min = df['CD'].min()
    Cl_Cd_min = df.loc[df['CD'] == Cd_min, 'CL'].iloc[0]
    alpha_Cd_min = df.loc[df['CD'] == Cd_min, 'alpha'].iloc[0]

    Cl_min = df['CL'].min()
    Cd_Cl_min = df.loc[df['CL'] == Cl_min, 'CD'].iloc[0]
    alpha_Cl_min = df.loc[df['CL'] == Cl_min, 'alpha'].iloc[0]

    ########################################################################################
    """Deleting files"""
    ########################################################################################

    if os.path.exists(':00.bl'):
        os.remove(':00.bl')

    if os.path.exists(polar_file):
        os.remove(polar_file)

    if os.path.exists('NUL.dat'):
        os.remove('NUL.dat')

    return(Cl_max,Cd_Cl_max,Cd_min,Cl_Cd_min,Cl_min,Cd_Cl_min )



airfoil    = 'PQ1'
reynolds = '3.5e6'
mach = '0.15'
aoa_ini = '0'
aoa_fin = '22'
delta_aoa = '1'

t = rxfoil(airfoil,reynolds,mach,aoa_ini,aoa_fin,delta_aoa)


print(t)