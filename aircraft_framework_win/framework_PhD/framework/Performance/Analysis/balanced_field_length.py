"""
File name : Balanced field length function
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - Balanced length field function
    - Reference: Torenbeek. 1982 and Gudmunsson 2014
    - Chapter 5, page 169, equation 5-91 and Chapter 17 equation 17-1
Inputs:
    - aicraft data
    - airport data
Outputs:
    -
TODO's:
    - where does Tmax and Tavg equations comes from?
    - why no GRAVITY in eq. BLF?

"""
# =============================================================================
# IMPORTS
# =============================================================================
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
import numpy as np
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def balanced_field_length(aircraft_data, airport_data):
    '''
    Note: for project design the case of delta_gamma2 = 0 presents most
    interest, as the corresponding weight is limited by the second segment
    climb requirement (Torenbeek, 1982)
    '''
    # Aircraft data import
    CL_max_takeoff = aircraft_data['CL_maximum_takeoff']
    weight_takeoff = aircraft_data['maximum_takeoff_weight']  # [N]
    wing_surface = aircraft_data['wing_surface']  # [m2]
    T_avg = aircraft_data['average_thrust']  # [N]

    # Airport data import
    airfield_elevation = airport_data['elevation']  # [ft]
    delta_ISA = airport_data['delta_ISA']  # [deg C]

    # horizontal distance from airfield surface requirement according to FAR 25 - [m]
    h_takeoff = 10.7
    delta_gamma2 = 0.024
    delta_S_takeoff = 200  # [m]
    g = 9.807  # [m/s2]
    CL_2 = 0.694*CL_max_takeoff
    mu = 0.01*CL_max_takeoff + 0.02
    _, _, sigma, _, _, rho, _ = atmosphere_ISA_deviation(
        airfield_elevation, delta_ISA)  # [kg/m3]

    aux1 = 0.863/(1 + (2.3*delta_gamma2))
    aux2 = ((weight_takeoff/wing_surface)/(rho*g*CL_2)) + h_takeoff

    # To high takeoff weight will made this coeficient less than mu resulting in a negative
    # landing field, when that happend this code will use twice the takeoff weight as coefficient
    # to continue with the iteration
    if T_avg/weight_takeoff > mu:
        aux3 = (1/((T_avg/weight_takeoff)-mu)) + 2.7
    else:
        aux3 = weight_takeoff*2

    aux4 = delta_S_takeoff/np.sqrt(sigma)

    return aux1*aux2*aux3 + aux4  # [m]
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
