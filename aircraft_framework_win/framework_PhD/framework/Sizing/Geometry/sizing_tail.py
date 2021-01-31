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
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def sizing_tail():
    relaxation = 0.7
    kink_distance = (wing['span']/2)*wing_semi_span_kink

    # Calc of cg here

    delta_horizontal_tail = 10000
    delta_vertical_tail = 10000
    margin = aircraft['static_margin']*wing['mean_aerodynamic_chord']

    while delta_horizontal_tail > 0.025 or delta_vertical_tail > 0.025:
        airfoil_aerodynamic_center_reference = 0.25

        neutral_point_xposition = wing_leading_edge_xposition + wing['mean_aerodynamic_chord_yposition']  * \
            np.tan(wing_sweeo_leading_edge*deg_to_rad) + \
            airfoil_aerodynamic_center_reference*wing['mean_aerodynamic_chord_yposition'] 
        distance_xnp_xcg = neutral_point_xposition - center_of_gravity_after_xposition
        delta_distance = distance_xnp_xcg - margin
        wing_leading_edge_xposition_new = wing_leading_edge_xposition - delta_distance
        wing_leading_edge_xposition = wing_leading_edge_xposition_new

        # Iteration cycle for vertical tail
        vertical_tail_aerodynamic_center_xposition = 0.95*fuselage['length'] - vertical_tail_center_chord + vertical_tail_mean_aerodynamic_chord_yposition * \
            np.tan(vertical_tail['sweep']_leading_edge*deg_to_rad) + \
            vertical_tail_aerodynamic_center_xposition*vertical_tail_mean_aerodynamic_chord

        distance_vtxac_xcg = vertical_tail_aerodynamic_center_xposition - \
            center_of_gravity_after_xposition

        vertical_tail_area_new = (
            wing_area*vertical_tail['volume']*wing['span'])/distance_vtxac_xcg

        delta_vertical_tail_area = np.abs(
            vertical_tail['area'] - vertical_tail_area_new)

        vertical_tail['area'] = relaxation*vertical_tail_area_new + \
            (1-relaxation)*vertical_tail['area']

        vertical_tail_parameters = size_vertical_tail(
            wing_area,
            horizontal_tail_data,
            mach,
            altitude)

        # Iteration cycle for horizontal tail
        if horizontal_tail['position']  == 1:
            horizontal_tail_aerodynamic_center_xposition = 0.95*fuselage['length'] - horizontal_tail_center_chord + horizontal_tail_mean_aerodynamic_chord_yposition * \
                np.tan(horizontal_tail_sweep_leading_edge*deg_to_rad) + \
                horizontal_tail['aerodynamic_center'] * \
                horizontal_tail_mean_aerodynamic_chord
        else:
            horizontal_tail_aerodynamic_center_xposition = 0.95*fuselage['length'] - vertical_tail_center_chord + vertical_tail_span * \
                np.tan(vertical_tail['sweep']_leading_edge*deg_to_rad) + \
                horizontal_tail['aerodynamic_center'] * \
                horizontal_tail_mean_aerodynamic_chord + horizontal_tail_mean_aerodynamic_chord_yposition * \
                np.tan(horizontal_tail_sweep_leading_edge*deg_to_rad)

        distance_htxac_xcg = horizontal_tail_aerodynamic_center_xposition - \
            center_of_gravity_after_xposition

        horizontal_tail_area_new = (
            horizontal_tail['volume']*wing_area*wing['mean_aerodynamic_chord'])/distance_htxac_xcg

        delta_horizontal_tail_area = np.abs(
            horizontal_tail['area'] - horizontal_tail_area_new)

        horizontal_tail['area'] = relaxation*horizontal_tail_area_new + \
            (1-relaxation)*horizontal_tail['area']

        horizontal_tail_parameters = sizing_horizontal_tail(HTarea, HTAR, HTTR, PHT, wS, wSweep14, lf, vtSweepLE,
                                                            vtct, vtc0, vtb, htac_rel, Mach, Ceiling)
        
        # Calc of cg again here
        

    return

# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
