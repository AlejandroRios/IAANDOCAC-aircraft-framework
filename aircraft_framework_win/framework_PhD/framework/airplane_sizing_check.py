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


def airplane_sizing(x):

    aircraft_data = baseline_aircraft()
    aircraft_data['wing_surface'] = x[0]
    aircraft_data['wing_aspect_ratio'] = x[1]
    aircraft_data['wing_taper_ratio'] = x[2]
    aircraft_data['wing_sweep_c_4'] = x[3]
    aircraft_data['tip_incidence'] = x[4]
    aircraft_data['semi_span_kink'] = x[5]
    aircraft_data['passenger_capacity'] = x[11]
    aircraft_data['number_of_seat_abreast'] = x[12]
    aircraft_data['range'] = x[13]
    aircraft_data['winglet_presence'] = x[17]
    aircraft_data['slat_presence'] = x[18]
    aircraft_data['horizontal_tail_position'] = x[19]

    engine_data = baseline_engine()

    engine_data['engine_bypass'] = x[6]
    engine_data['engine_fan_diameter'] = x[7]
    engine_data['compressor_pressure_ratio'] = x[8]
    engine_data['turbine_inlet_temperature'] = x[9]
    engine_data['fan_pressure_ratio'] = x[10]
    engine_data['engine_design_point_pressure'] = x[14]
    engine_data['engine_design_point_mach'] = x[15]
    engine_data['engine_position'] = x[16]

    # Cabin
    aisles_number = 1
    crew_number = 5
    cabin_height = 2
    seat_width = 0.46
    aisle_width = 0.5
    seat_pitch = 0.8128
    height_to_width_ratio = 1.1

    # Aerodynamics
    dihedral_angle = 3
    Cl_max = 1.9
    flap_angle_takeoff = 35
    flap_angle_landing = 45
    flap_span = 0.75
    root_incidence = 2
    kink_incidence = 0
    tip_incidence = aircraft_data['tip_incidence']
    slat = 1

    # Winglet
    winglet_sweep_le = 35
    winglet_aspect_ratio = 2.75
    winglet_taper_ratio = 0.25
    winglet_cant_angle = 75

    # Operations
    year_technology = 2017
    takeoff_field_length = 2000
    landing_field_length = 1500
    mach_maximum_operating = 0.8
    cruise_mach = MMO - 0.02
    maximum_operating_speed = 340
    holding_time = 30  # [min]
    alternative_airport_distance = 200  # [nm]
    max_ceiling = 41000
    passenger_mass = 100  # [kg]
    payload = aircraft_data['passenger_capacity'] * passenger_mass
    proceed = 0

    # Airframe parameters
    wing_rear_spar = 0.75
    wing_span = np.sqrt(
        aircraft_data['wing_aspect_ratio']*aircraft_data['wing_surface'])
    CL_max = 0.9*Cl_max*np.cos(aircraft_data['wing_sweep_c_4']*np.pi/180)
    CL_max_clean = CL_max
    wing_position = 1

    # Vertical tail parameters
    vertical_tail_area = 16.2
    vertical_tail_aspect_ratio = 1.2
    vertical_tail_taper_ratio = 0.5
    vertical_tail_sweep = 41
    vertical_tail_volume = 0.09
    vertical_tail_aerodynamic_center = 0.25

    # Hprizontal tail parameters
    horizontal_tail_area = 23.35
    horizontal_tail_aspect_ratio = 4.35
    horizontal_tail_taper_ratio = 0.4
    horizontal_tail_position = 1
    horizontal_tail_volume = 0.9
    horizontal_tail_aerodynamic_center = 0.25

    static_margin = 0.15

    # Landing gear parameters
    main_landig_gear_pressure = 200  # [psi]
    nose_landig_gear_pressure = 190  # [psi]

    # Fuselage parameters
    number_of_pax_transitions = 3
    transition_points = [75, 95]

    # Engine paramters
    maximum_engine_thrust = 18000
    
    if engine_data['engine_position'] == 0:
        engines_number = 2
        engines_under_wing = 0
    elif engine_data['engine_position'] == 1:
        engines_number = 2
        engines_under_wing = 2
    
    if wing_position == 2 or engine_position == 2:
        horizontal_tail_position == 2
    
    



    





    classification = 0
    for i in range(len(transition_points)):
        track = aircraft_data['passenger_capacity'] - transition_points[i]
        if track < 0:
            classification = i
            break

    if classification == 0:
        classification = number_of_pax_transitions

    if classification == 1:
        container_type == 'None'
    elif classification == 2:
        container_type == 'LD3-45W'
    elif classification == 3:
        container_type == 'LD3-45'

    fuselage_width, fuselage_height, fuselage_Dz_floor, minimum_width = fuselage_cross_section(
        container_type,
        aisles_number,
        seats_number,
        cabin_height,
        seat_width,
        aisle_width,
        height_to_width_ratio
        )



    
    


    


# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# TEST
# =============================================================================
