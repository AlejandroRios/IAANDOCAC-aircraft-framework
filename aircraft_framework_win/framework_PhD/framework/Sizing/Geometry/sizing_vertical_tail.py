"""
File name :
Author    : 
Email     : aarc.88@gmail.com
Date      : 
Last edit :
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    -
Inputs:
    -
Outputs:
    -
TODO's:
    -

"""
# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global deg_to_rad
deg_to_rad = np.pi/180
kg_to_lb = 2.20462

def size_vertical_tail(
    wing_area,
    horizontal_tail['position'] ,
    horizontal_tail_data,
    mach,
    altitude):

    vertical_tail_twist = 0
    vertical_tail_dihedral = 90
    vertical_tail_span = np.sqrt(vertical_tail['aspect_ratio']*vertical_tail['area'])
    vertical_tail_center_chord = (2*vertical_tail['area'])/(vertical_tail_span*(1+vertical_tail['taper_ratio']))
    vertical_tail_tip_chord = vertical_tail['taper_ratio']*vertical_tail_center_chord
    vertical_tail_root_chord = vertical_tail_tip_chord/vertical_tail['taper_ratio']
    vertical_tail_mean_geometrical_chord = vertical_tail['area']/vertical_tail_span
    vertical_tail_mean_aerodynamic_chord = 2/3 * vertical_tail_center_chord * (1 + vertical_tail['taper_ratio'] + vertical_tail['taper_ratio']**2)/(1 + vertical_tail['taper_ratio'])
    vertical_tail_mean_aerodynamic_chord_yposition = (2*vertical_tail_span)/(6*(1+2*vertical_tail['taper_ratio'])/(1+vertical_tail['taper_ratio']))
    vertical_tail_sweep_leading_edge = 1/(deg_to_rad*(np.arctan(np.tan(deg_to_rad*vertical_tail_sweep_c_4) + 1/(vertical_tail['aspect_ratio']*(1 - vertical_tail['taper_ratio'])/(1 + vertical_tail['taper_ratio'])))))
    vertical_tail_sweep_c_2 = 1/(deg_to_rad*(np.arctan(np.tan(deg_to_rad*vertical_tail_sweep_c_4) - 1/(vertical_tail['aspect_ratio']*(1 - vertical_tail['taper_ratio'])/(1 + vertical_tail['taper_ratio'])))))
    vertical_tail_sweep_trailing_edge = 1/(deg_to_rad*(np.arctan(np.tan(deg_to_rad*vertical_tail['sweep']) - 3/(vertical_tail['aspect_ratio']*(1 - vertical_tail['taper_ratio'])/(1 + vertical_tail['taper_ratio'])))))

    vertical_tail_root_thickness = 0.11
    vertical_tail_tip_thickness = 0.11
    vertical_tail_mean_thickness = (vertical_tail_root_chord + 3*vertical_tail_tip_thickness)/4
    vertical_tail_wetted_area = 2*vertical_tail['area']*(1 + 0.25*vertical_tail_root_thickness*(1 + (vertical_tail_root_thickness/vertical_tail_tip_thickness)*vertical_tail['taper_ratio'])/(1 + vertical_tail['taper_ratio']))

    if horizontal_tail['position']  == 1:
        kv = 1  # vertical tail mounted in the fuselage
    else:
        zh = 0.95*vertical_tail_span
        kv = 1 + 0.15*((horizontal_tail['area']*zh)/(vertical_tail['area']*vertical_tail_span))

    theta, delta, sigma, T_ISA, P_ISA, rho_ISA, a = atmosphere_ISA_deviation(
        altitude, 0)

    V_dive = mach*a
    aux_1 = (vertical_tail['area']**0.2 * V_dive)/(1000*np.sqrt(np.cos(vertical_tail_sweep_c_2*deg_to_rad)))
    vertical_tail_weight = kv*vertical_tail['area']*(62*aux_1 - 2.5)
    vertical_tail_weight = vertical_tail_weight*kg_to_lb
    return
# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
