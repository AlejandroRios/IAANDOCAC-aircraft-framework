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


def center_of_gravity():
    # == wing ==
    # Wing mean aerodynamic chord 37 - 42 percent
    if aircraft['slat_presence'] == 0:
        delta_xw = 0.5*(0.1 + wing['rear_spar'] )
    else:
        delta_xw = 0.5*(0.15 + wing['rear_spar'] )

    wing_center_of_gravity_xposition = wing_leading_edge_xposition + wing['mean_aerodynamic_chord_yposition']  * \
        np.tan(wing['sweep_leading_edge']*deg_to_rad) + \
        delta_xw*wing['mean_aerodynamic_chord']
    wing_moment = wing_weight*wing_center_of_gravity_xposition

    # == horizontal tail ==
    if horizontal_tail['position']  == 1:
        horizontal_tail_center_of_gravity_xposition = 0.95*fuselage['length'] - horizontal_tail_center_chord + \
            horizontal_tail_mean_aerodynamic_chord_yposition * \
            np.tan(horizontal_tail_sweep_leading_edge*deg_to_rad) + \
            0.3*horizontal_tail_mean_aerodynamic_chord
    else:
        horizontal_tail_center_of_gravity_xposition = 0.95*fuselage['length'] - vertical_tail_center_chord + \
            vertical_tail_span * \
            np.tan(vertical_tail_sweep_leading_edge*deg_to_rad)
    horizontal_tail_moment = horizontal_tail_weight * \
        horizontal_tail_center_of_gravity_xposition

    # == vertical tail ==
    vertical_tail_center_of_gravity_xposition = 0.98*fuselage['length'] - (vertical_tail_center_chord - (0.3*vertical_tail_mean_aerodynamic_chord + (
        vertical_tail_mean_aerodynamic_chord_yposition*np.tan(vertical_tail_sweep_leading_edge*deg_to_rad))))
    vertical_tail_moment = vertical_tail_weight * \
        vertical_tail_center_of_gravity_xposition

    # == fuselage ==
    if engine['position'] == 1:
        fuselage_center_of_gravity_xposition = 0.43*fuselage['length']
    elif engine['position'] == 2:
        fuselage_center_of_gravity_xposition = 0.47*fuselage['length']
    elif engine['position'] == 3:
        fuselage_center_of_gravity_xposition = 0.48*fuselage['length']
    elif engine['position'] == 4:
        fuselage_center_of_gravity_xposition = 0.43*fuselage['length']

    fuselage_moment = fuselage_weight*fuselage_center_of_gravity_xposition

    # == engines ==
    aircraft['number_of_engines']  = max(2, engine['position'])
    if engine['position'] == 1:
        engine_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge'] *
                                 deg_to_rad) - 0.1*engine['length']
        engine_2_center_of_gravity_xposition = 0
        engine_moment = aircraft['number_of_engines'] *engine_weight*engine_center_of_gravity_xposition
        engine_2_moment = 0

        # == propulsion system ==
        propulsion_system_center_of_gravity_xposition = wing_leading_edge_xposition + \
            engine_yposition*(wing['span']/2) * \
            np.tan(wing['sweep_leading_edge']*deg_to_rad)
        propulsion_system_moment = propulsion_system_weight * \
            propulsion_system_center_of_gravity_xposition
        propulsion_system_2_moment = 0

    elif engine['position'] == 2:
        engine_center_of_gravity_xposition = 0.98*fuselage['length'] - \
            vertical_tail_center_chord - engine['length'] + 0.3*engine_lenghth
        engine_2_center_of_gravity_xposition = 0
        engine_moment = aircraft['number_of_engines'] *engine_weight*engine_center_of_gravity_xposition
        engine_2_moment = 0

        # == propulsion system ==
        propulsion_system_center_of_gravity_xposition = engine_center_of_gravity_xposition
        propulsion_system_moment = propulsion_system_weight * \
            propulsion_system_center_of_gravity_xposition
        propulsion_system_2_moment = 0

    elif engine['position'] == 3:
        engine_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge']*deg_to_rad) - \
            0.25*engine['length'] + 0.3*engine_lenghth
        engine_2_center_of_gravity_xposition = fuselage['length'] - \
            vertical_tail_center_chord - engine['length'] + 0.3*engine['length']
        engine_moment = (2/3)*aircraft['number_of_engines'] *engine_weight * \
            engine_center_of_gravity_xposition
        engine_2_moment = (1/3)*aircraft['number_of_engines'] *engine_weight * \
            engine_2_center_of_gravity_xposition

        # == propulsion system ==
        propulsion_system_moment = (
            2/3)*propulsion_system_weight*engine_center_of_gravity_xposition
        propulsion_system_2_moment = (
            1/3)*propulsion_system_weight*engine_2_center_of_gravity_xposition

    elif engine['position'] == 4:
        engine_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge']*deg_to_rad) - \
            0.25*engine['length'] + 0.3*engine_lenghth
        engine_2_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge']*deg_to_rad) - \
            0.25*engine['length'] + 0.3*engine_lenghth
        engine_moment = 0.5*aircraft['number_of_engines'] *engine_weight * \
            engine_center_of_gravity_xposition
        engine_2_moment = 0.5*aircraft['number_of_engines'] *engine_weight * \
            engine_2_center_of_gravity_xposition

        # == propulsion system ==
        propulsion_system_moment = 0.5*propulsion_system_weight * \
            engine_center_of_gravity_xposition
        propulsion_system_moment2 = 0.5*propulsion_system_weight * \
            engine_2_center_of_gravity_xposition

    # == nacelles==

    if engine['position'] == 1:
        nacelle_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge'] *
                                 deg_to_rad) + 0.4*engine['length']
        nacelle_moment = nacelle_weight*nacelle_center_of_gravity_xposition
    elif engine['position'] == 2:
        nacelle_center_of_gravity_xposition = 0.97*fuselage['length'] - \
            vertical_tail_center_chord - engine['length'] + 0.35*engine['length']
        nacelle_moment = nacelle_weight*nacelle_center_of_gravity_xposition
    elif engine['position'] == 3:
        nacelle_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge'] *
                                 deg_to_rad) + 0.4*engine['length']
        nacelle_moment = nacelle_weight*nacelle_center_of_gravity_xposition
    elif engine['position'] == 4:  # CHECK THIS ONE!!!!
        nacelle_center_of_gravity_xposition = wing_leading_edge_xposition + engine_yposition * \
            (wing['span']/2)*np.tan(wing['sweep_leading_edge'] *
                                 deg_to_rad) + 0.4*engine['length']
        nacelle_moment = nacelle_weight*nacelle_center_of_gravity_xposition

    # == landing gear ==

    # nose landing gear
    nose_landing_gear_center_of_gravity_xposition = 0.5*fuselage['cockpit_length']
    nose_landing_gear_moment = nose_landing_gear_weight * \
        nose_landing_gear_center_of_gravity_xposition

    # main landing gear
    if wing['position'] == 1:
        main_landig_gear_center_of_gravity_xposition = wing_leading_edge_xposition + trunnion wing_xposition
    else:
        main_landig_gear_center_of_gravity_xposition = wing_center_of_gravity_xposition + \
            0.20*wing['mean_aerodynamic_chord']

    main_landig_gear_moment = main_landig_gear_weight * \
        main_landig_gear_center_of_gravity_xposition

    # == fuel system ==
    # fuel system
    fuel_system_center_of_gravity_xposition = wing_leading_edge_xposition - \
        wing['mean_aerodynamic_chord_yposition']  * \
        np.tan(wing['sweep_leading_edge']*deg_to_rad) + wing['center_chord'] *0.5
    fuel_system_moment = fuel_system_weight*fuel_system_center_of_gravity_xposition

    # flight control
    flight_control_system_wing_center_of_gravity_xposition = wing_leading_edge_xposition - wing['mean_aerodynamic_chord_yposition']  * \
        np.tan(wing['sweep_leading_edge']*deg_to_rad) + (wing['span'] *
                                                      np.tan(wing['sweep_leading_edge']*deg_to_rad) + wing['tip_chord'])/2
    flight_control_system_wing_moment = 0.5*flight_control_weight * \
        flight_control_system_wing_center_of_gravity_xposition

    flight_control_system_tail_center_of_gravity_xposition = vertical_tail_center_of_gravity_xposition
    flight_control_tail_moment = 0.5*flight_control_weight * \
        flight_control_system_tail_center_of_gravity_xposition

    # hydraulic system
    hydraulic_system_center_of_gravity_xposition = wing_leading_edge_xposition + \
        0.6*wing['center_chord'] 
    hydraulic_system_moment = hydraulic_system_weight * \
        hydraulic_system_center_of_gravity_xposition

    # electrical system
    electrical_system_center_of_gravity_xposition = wing_leading_edge_xposition - \
        wing['mean_aerodynamic_chord_yposition']  * \
        np.tan(wing['sweep_leading_edge']*deg_to_rad) + wing['center_chord'] 
    electrical_system_moment = electrical_system_weight * \
        electrical_system_center_of_gravity_xposition

    # avionics
    avionics_system_center_of_gravity_xposition = 0.4*fuselage['cockpit_length']
    avionics_system_moment = avionics_system_weight * \
        avionics_system_center_of_gravity_xposition

    # air system
    air_system_center_of_gravity_xposition = wing_leading_edge_xposition - wing['mean_aerodynamic_chord_yposition']  * \
        np.tan(wing['sweep_leading_edge']*deg_to_rad) + \
        (wing['mean_aerodynamic_chord_yposition']  *
         np.tan(wing['sweep_leading_edge']*deg_to_rad)/2)
    air_system_moment = air_system_weight*air_system_center_of_gravity_xposition

    # oxygen system
    oxygen_system_center_of_gravity_xposition = fuselage['cockpit_length'] + \
        (wing_leading_edge_xposition - wing['mean_aerodynamic_chord_yposition']  *
         np.tan(wing['sweep_leading_edge']*deg_to_rad) - fuselage['cockpit_length'])/2
    oxygen_system_moment = oxygen_system_weight * \
        oxygen_system_center_of_gravity_xposition

    # auxiliar power unit
    apu_center_of_gravity_xposition = fuselage['length'] - 2
    apu_moment = apu_weight*apu_center_of_gravity_xposition

    # furnishing
    furnishing_center_of_gravity_xposition = fuselage['cockpit_length'] + \
        (fuselage_cabine_lenght/2)
    furnishing_moment = furnishing_weight*furnishing_center_of_gravity_xposition

    # paint
    paint_center_of_gravity_xposition = 0.51*fuselage['length']
    paint_moment = paint_weight*paint_center_of_gravity_xposition

    # wing fuel
    wing_fuel_center_of_gravity_xposition = wing_leading_edge_xposition + \
        wing_tanks_center_of_gravity_xposition
    wing_fuel_moment = fuel_weight*wing_fuel_center_of_gravity_xposition

    aircraft_empty_weight_center_of_gravity_xposition = (wing_moment+horizontal_tail_moment+vertical_tail_moment+fuselage_moment+engine_moment+engine_2_moment+propulsion_system_moment+propulsion_system_2_moment+nacelle_moment+nose_landing_gear_moment+main_landig_gear_moment +
                                                         fuel_system_moment+flight_control_system_wing_moment+flight_control_tail_moment+hydraulic_system_moment+electrical_system_moment+avionics_system_moment+air_system_moment+oxygen_system_moment+apu_moment+furnishing_moment+paint_moment+wing_fuel_moment)/aircraft_empty_weight

    aircraft_empty_weight_center_of_gravity_mean_aerodynamic_chord_xposition = aircraft_empty_weight_center_of_gravity_xposition / \
        wing['mean_aerodynamic_chord']

    # == crew ==
    # cockpit
    crew_cockpit_weight = 2*78
    crew_cockpit_center_of_gravity_xposition = fuselage['cockpit_length']/2
    crew_cockpit_moment = crew_cockpit_weight * \
        crew_cockpit_center_of_gravity_xposition

    # cabine

    crew_cabine_weight = 3*75
    crew_cabine_center_of_gravity_xposition = fuselage['cockpit_length'] + fuselage_cabine_lenght
    crew_cabine_moment = crew_cabine_weight*crew_cabine_center_of_gravity_xposition

    residual_fuel_weight = 0.005*wing['fuel_capacity']
    residual_fuel_center_of_gravity_xposition = wing_leading_edge_xposition + \
        wing_tanks_center_of_gravity_xposition
    residual_fuel_moment = residual_fuel_weight * \
        residual_fuel_center_of_gravity_xposition

    aircraft_operating_empty_weight_moment = aircraft_empty_weight*aircraft_empty_weight_center_of_gravity_xposition + \
        crew_cockpit_moment + crew_cabine_moment + residual_fuel_moment

    aircraft_operating_empty_weight = aircraft_empty_weight + \
        crew_cockpit_weight + crew_cabine_weight + residual_fuel_weight

    fuel_tanks_center_of_gravity_xposition = wing_leading_edge_xposition + \
        wing_tanks_center_of_gravity_xposition
    fuel_tanks_moment = fuel_weight*fuel_tanks_center_of_gravity_xposition

    pax_weight = pax_number*100
    pax_center_of_gravity_xposition = fuselage_cockpit_lenght + fuselage_cabine_lenght/2
    pax_moment = pax_weight*pax_center_of_gravity_xposition

    # CG shift positions
    configuration_1 = aircraft_operating_empty_weight_moment / \
        aircraft_operating_empty_weight

    configuration_2 = (aircraft_operating_empty_weight_moment +
                       fuel_tanks_moment)/(aircraft_operating_empty_weight + fuel_weight)

    configuration_3 = (aircraft_operating_empty_weight_moment + fuel_tanks_moment +
                       pax_moment)/(aircraft_operating_empty_weight + fuel_weight + pax_weight)

    configuration_4 = (aircraft_operating_empty_weight_moment +
                       pax_moment)/(aircraft_operating_empty_weight + pax_weight)

    aircraft_forward_center_of_gravity_xposition = min(
        configuration_1, configuration_2, configuration_3, configuration_4)
    aircraft_after_center_of_gravity_xposition = max(
        configuration_1, configuration_2, configuration_3, configuration_4)

    aircraft_center_of_gravity_shift_range = (
        (aircraft_forward_center_of_gravity_xposition - aircraft_after_center_of_gravity_xposition)/wing['mean_aerodynamic_chord'])*100
    return
# =============================================================================
# MAIN
# =============================================================================


# =============================================================================
# TEST
# =============================================================================
cachaça
