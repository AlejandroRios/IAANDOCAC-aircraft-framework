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
# class structtype():
#     pass

# airfoils = structtype()
# wing = structtype()
# Airfoils ----------------------------------------------------------------
def cl_max_2d(mach,airport_elevation,airfoil_names,airfoil_chords):
    airfoils = {1:{},
                2:{},
                3:{}}





    for i in range(len(airfoils)):
        j = i+1
        airfoils[j]['name'] = airfoil_names[i]
        airfoils[j]['chord'] = airfoil_chords[i]



    ########################################################################################
    """Importing Modules"""
    ########################################################################################
    import numpy as np
    from atmosphere import atmosphere
    from rxfoil import rxfoil
    ########################################################################################
    """Constants declaration"""
    ########################################################################################
    ft2m    = 0.3048
    m2ft    = 1./ft2m

    mach = 0.15
    hp = 1000
    ISADEV = 0

    ########################################################################################

    flagsuc = 0 # success flag, initially ok
    # Conversion factors
    #--------------------------------------------------------------------------

    atm        = atmosphere(hp,ISADEV)
    # ***** air viscosity (begin)******
    mi0    = 18.27E-06
    Tzero  = 291.15 # Reference temperature
    Ceh    = 120 # C = Sutherland's constant for the gaseous material in question
    mi     = mi0*((atm.TAE+Ceh)/(Tzero+Ceh))*((atm.TAE/Tzero)**1.5)
    #--------------------------------------------------------------------------
    reynolds   = atm.ro*mach*atm.va/mi

    aoa_ini    = '0'
    aoa_fin    = '20'  
    delta_aoa = '1'


    for i in airfoils:
        airfoil = i

        airfoil_name = airfoils[airfoil]['name']
        mach = str(mach)
        reynolds = str(reynolds)
            
        Cl_max,_,_,_,_,_ = rxfoil(airfoil_name,reynolds,mach,aoa_ini,aoa_fin,delta_aoa)
        airfoils[airfoil]['Clmax'] = Cl_max


    return(airfoils)



