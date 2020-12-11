"""
File name : Missed approach limb function
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function calculates the thrust to weight ratio following the requiremnts
      of missed climb approach with one-engine-inoperative accoring to FAR 25.121.
      For this case the climb gradient expressed as a percentage takes a value of 0.021 (for two engine aircraft).
      The lading gear is up and takeoff flaps are deployed
      References: FAR 25.121 and ROSKAM 1997 - Part 1, pag. 142 
Inputs:
    - aircraft_data
Outputs:
    - 
TODO's:
    - 

"""
########################################################################################
"IMPORTS"
########################################################################################
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient
from framework.Aerodynamics.aerodynamic_coefficients_ANN import aerodynamic_coefficients_ANN
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

def missed_approach_climb_OEI(aircraft_data,airport_data,maximum_takeoff_weight):
    '''
    '''
    engines_number = aircraft_data['number_of_engines']
    CL_maximum_landing = aircraft_data['CL_maximum_landing']
    maximum_landing_weight = aircraft_data['maximum_landing_weight'] # [N]
    wing_surface = aircraft_data['wing_surface']
    airfield_elevation = airport_data['elevation']
    airfield_delta_ISA = airport_data['delta_ISA']
    phase = 'climb'

    _,_,_,_,_,rho,a = atmosphere_ISA_deviation(airfield_elevation,airfield_delta_ISA) # [kg/m3]


    

    V = 1.3*np.sqrt(2*maximum_landing_weight/(CL_maximum_landing*wing_surface*rho))
    mach = V/a
    CD_landing,_ = aerodynamic_coefficients_ANN(aircraft_data,airfield_elevation,mach,CL_maximum_landing)
    CD_landing = zero_fidelity_drag_coefficient(aircraft_data,CL_maximum_landing,phase)


    L_to_D = CL_maximum_landing/CD_landing
    if engines_number == 2:
        steady_gradient_of_climb = 0.021 # 2.4% for two engines airplane
    elif engines_number == 3:
        steady_gradient_of_climb = 0.024 # 2.4% for two engines airplane
    elif engines_number == 4:
        steady_gradient_of_climb = 0.027 # 2.4% for two engines airplane

    aux1 = (engines_number/(engines_number-1))
    aux2 = (1/L_to_D) + steady_gradient_of_climb 
    aux3 = maximum_landing_weight/maximum_takeoff_weight
    thrust_to_weight_landing = aux1*aux2*aux3
    return thrust_to_weight_landing

def missed_approach_climb_AEO(aircraft_data,airport_data,maximum_takeoff_weight):
    '''
    '''
    maximum_landing_weight = aircraft_data['maximum_landing_weight'] # [N]
    CL_maximum_landing = aircraft_data['CL_maximum_landing']
    wing_surface = aircraft_data['wing_surface']

    airfield_elevation = airport_data['elevation']
    airfield_delta_ISA = airport_data['delta_ISA']
    phase = 'descent'


    _,_,_,_,_,rho,a = atmosphere_ISA_deviation(airfield_elevation,airfield_delta_ISA) # [kg/m3]
    V = 1.3*np.sqrt(2*maximum_landing_weight/(CL_maximum_landing*wing_surface*rho))
    mach = V/a

    CD_landing,_ = aerodynamic_coefficients_ANN(aircraft_data,airfield_elevation,mach,CL_maximum_landing)
    # CD_landing = zero_fidelity_drag_coefficient(aircraft_data,CL_maximum_landing,phase)
    maximum_landing_weight = aircraft_data['maximum_landing_weight'] # [N]



    L_to_D = CL_maximum_landing/CD_landing

    steady_gradient_of_climb = 0.032 # 2.4% for two engines airplane

    aux1 = (1/L_to_D) + steady_gradient_of_climb 
    aux2 = maximum_landing_weight/maximum_takeoff_weight
    thrust_to_weight_landing = aux1 * aux2
    return thrust_to_weight_landing
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
