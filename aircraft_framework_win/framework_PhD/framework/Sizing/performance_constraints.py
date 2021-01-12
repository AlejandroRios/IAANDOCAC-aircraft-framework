"""
File name : Performance constraints
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    -
Inputs:
    -
Outputs:
    -
TODO's:
    -Add sigma effect of engine

"""
# =============================================================================
# IMPORTS
# =============================================================================
from framework.Performance.Analysis.balanced_field_length import balanced_field_length
from framework.Performance.Analysis.landing_field_length import landing_field_length
from framework.Performance.Analysis.second_segment_climb import second_segment_climb
from framework.Performance.Analysis.missed_approach_climb import missed_approach_climb_AEO, missed_approach_climb_OEI
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Performance.Analysis.cruise_performance import cruise_performance
from framework.baseline_aircraft import *
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def takeoff_field_length_check(aircraft_data, airport_data):
    takeoff_field_length_required = airport_data['takeoff_field_length']
    weight_takeoff = aircraft_data['maximum_takeoff_weight']

    flag = 0
    while flag == 0:
        aircraft_data['maximum_takeoff_weight'] = weight_takeoff
        takeoff_field_length_computed = balanced_field_length(
            aircraft_data, airport_data)

        if takeoff_field_length_computed > takeoff_field_length_required:
            weight_takeoff = weight_takeoff - (10*GRAVITY)
        else:
            flag = 1
    return weight_takeoff


def second_segment_climb_check(aircraft_data, airport_data):
    weight_takeoff = aircraft_data['maximum_takeoff_weight']
    thrust_takeoff = aircraft_data['maximum_engine_thrust']

    flag = 0
    while flag == 0:
        thrust_to_weight_takeoff_required = second_segment_climb(
            aircraft_data, airport_data)
        thrust_to_weight_takeoff = thrust_takeoff/weight_takeoff

        if thrust_to_weight_takeoff < thrust_to_weight_takeoff_required:
            weight_takeoff = weight_takeoff-(10*GRAVITY)
        else:
            flag = 2
    return weight_takeoff


def landing_field_length_check(aircraft_data, airport_data, maximum_takeoff_weight):
    landing_field_length_required = airport_data['landing_field_length']
    weight_landing = aircraft_data['maximum_landing_weight']
    wing_surface = aircraft_data['wing_surface']

    flag = 0
    while flag == 0:
        aircraft_data['maximum_landing_weight'] = weight_landing
        landing_field_length_computed = landing_field_length(
            aircraft_data, airport_data)

        maximum_takeoff_mass = maximum_takeoff_weight/GRAVITY
        maximum_landing_mass = weight_landing/GRAVITY

        maximum_takeoff_mass_to_wing_surface_requirement = (
            (maximum_landing_mass/wing_surface)/(maximum_landing_mass/maximum_takeoff_mass))
        maximum_takeoff_mass_to_wing_surface = maximum_landing_mass/wing_surface

        if (landing_field_length_computed > landing_field_length_required or maximum_takeoff_mass_to_wing_surface > maximum_takeoff_mass_to_wing_surface_requirement):
            weight_landing = weight_landing-(10*GRAVITY)
        else:
            flag = 2

    return weight_landing


def landing_climb_check(aircraft_data, airport_data, maximum_takeoff_weight):
    weight_landing = aircraft_data['maximum_landing_weight']
    thrust_landing = aircraft_data['maximum_engine_thrust'] * 0.98

    flag = 0
    while flag == 0:
        aircraft_data['maximum_landing_weight'] = weight_landing
        thrust_to_weight_landing_required = missed_approach_climb_AEO(
            aircraft_data, airport_data, maximum_takeoff_weight)
        thrust_to_weight_landing = thrust_landing/weight_landing

        if thrust_to_weight_landing < thrust_to_weight_landing_required:
            weight_landing = weight_landing-(10*GRAVITY)
        else:
            flag = 2
    return weight_landing


def missed_approach_climb_check(aircraft_data, airport_data, maximum_takeoff_weight):
    weight_landing = aircraft_data['maximum_landing_weight']
    thrust_landing = aircraft_data['maximum_engine_thrust'] * 0.98

    flag = 0
    while flag == 0:
        aircraft_data['maximum_landing_weight'] = weight_landing
        thrust_to_weight_landing_required = missed_approach_climb_OEI(
            aircraft_data, airport_data, maximum_takeoff_weight)
        thrust_to_weight_landing = thrust_landing/weight_landing

        if thrust_to_weight_landing < thrust_to_weight_landing_required:
            weight_landing = weight_landing-(10*GRAVITY)

        else:
            flag = 2
    return weight_landing


def residual_rate_of_climb_check():

    return


def maximum_cruise_speed_check():

    return


def drag_divergence_check():

    return


def regulated_takeoff_weight():

    airport_data = baseline_origin_airport()
    aircraft_data = baseline_aircraft()
    takeoff_field_length_weight = takeoff_field_length_check(
        aircraft_data, airport_data)

    airport_data = baseline_origin_airport()
    aircraft_data = baseline_aircraft()
    second_segment_climb_weight = second_segment_climb_check(
        aircraft_data, airport_data)

    maximum_takeoff_weight = min(
        takeoff_field_length_weight, second_segment_climb_weight)
    return maximum_takeoff_weight/GRAVITY  # [Kg]


def regulated_landing_weight():
    maximum_takeoff_weight = regulated_takeoff_weight() * GRAVITY

    airport_data = baseline_destination_airport()
    aircraft_data = baseline_aircraft()
    landing_field_length_weight = landing_field_length_check(
        aircraft_data, airport_data, maximum_takeoff_weight)

    airport_data = baseline_destination_airport()
    aircraft_data = baseline_aircraft()
    landing_climb = landing_climb_check(
        aircraft_data, airport_data, maximum_takeoff_weight)

    airport_data = baseline_destination_airport()
    aircraft_data = baseline_aircraft()
    missed_approach = missed_approach_climb_check(
        aircraft_data, airport_data, maximum_takeoff_weight)

    maximum_landing_weight = min(
        landing_field_length_weight, landing_climb, missed_approach)
    return maximum_landing_weight/GRAVITY  # [Kg]
# =============================================================================
# MAIN
# =============================================================================


# =============================================================================
# TEST
# =============================================================================
global GRAVITY
GRAVITY = 9.80665
# airport_data = baseline_origin_airport()
# aircraft_data = baseline_aircraft()
# takeoff_field_length_weight = takeoff_field_length_check(aircraft_data, airport_data)
# print('weight BFL requirement:', takeoff_field_length_weight/GRAVITY)

# airport_data = baseline_origin_airport()
# aircraft_data = baseline_aircraft()
# second_segment_climb_weight =  second_segment_climb_check(aircraft_data, airport_data)
# print('weight second segment requirement:', second_segment_climb_weight/GRAVITY)

# maximum_takeoff_weight = min(takeoff_field_length_weight, second_segment_climb_weight)
# print('========================================================================================')
# print('MTOW [kg]:', maximum_takeoff_weight/GRAVITY)
# print('========================================================================================')

# airport_data = baseline_origin_airport()
# aircraft_data = baseline_aircraft()
# landing_field_length_weight = landing_field_length_check(aircraft_data, airport_data, maximum_takeoff_weight)
# print('weight landing field requirement:', landing_field_length_weight/GRAVITY)

# airport_data = baseline_origin_airport()
# aircraft_data = baseline_aircraft()
# landing_climb = landing_climb_check(aircraft_data, airport_data, maximum_takeoff_weight)
# print('weight landing climb:', landing_climb/GRAVITY)

# airport_data = baseline_origin_airport()
# aircraft_data = baseline_aircraft()
# missed_approach = missed_approach_climb_check(aircraft_data, airport_data, maximum_takeoff_weight)
# print('weight missed approach:', missed_approach/GRAVITY)

# maximum_landing_weight = min(landing_field_length_weight, landing_climb, missed_approach)
# print('========================================================================================')
# print('MLW [kg]:', maximum_landing_weight/GRAVITY)
# print('========================================================================================')
