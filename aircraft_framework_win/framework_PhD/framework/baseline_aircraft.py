"""
Function  : baseline_aircraft.py
Title     : Baseline aircraft
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function descrive baseline aircraft properties which are used to test other modules
Inputs:
    -
Outputs:
    - 
TODO's:
    - Definir unidades
    - Thrust per engine?

"""
########################################################################################
"IMPORTS"
########################################################################################

########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def baseline_aircraft():
    aircraft = {}
    aircraft['maximum_takeoff_weight'] = 55000 * 9.807 # [N]
    aircraft['maximum_landing_weight'] = 32000 * 9.807 # [N]
    aircraft['wing_surface'] = 100 # [m2]
    aircraft['wing_aspect_ratio'] = 11 
    aircraft['wing_taper_ratio'] = 0.4
    aircraft['wing_sweep_leading_edge'] = 23.5 # [deg]
    aircraft['incidence_root'] = 2 # [deg]
    aircraft['incidence_kink'] = 0 # [deg]
    aircraft['incidence_tip'] = -1 # [deg]
    aircraft['semi_span_kink'] = 0.32 
    # aircraft['r0'] = [0.0153, ]
    # aircraft['thickness_to_chord_ratio'] = [0.1228,0.1055,0.0982]
    # aircraft['phi']
    aircraft['thickness_to_chord_maximum_ratio'] = [0.3738,0.3585,0.3590]
    # aircraft['theta']
    # aircraft['epsilon']
    aircraft['thickness_to_chord_average_ratio'] = 0.11
    aircraft['aircraft_wet_surface'] = 485 # [m2]
    aircraft['wing_wet_surface'] = 122.5 # [m2]
    aircraft['CL_maximum_clean'] = 1.6 
    aircraft['CL_maximum_takeoff'] = 2.4
    aircraft['CL_maximum_landing'] = 2.0
    aircraft['flap_deflection_takeoff'] = 35 # [deg]
    aircraft['flap_deflection_landing'] = 30 # [deg]
    aircraft['vertical_tail_surface'] = 16.2 # [m2]
    aircraft['horizontal_tail_surface'] = 30 # [m2]
    aircraft['vertical_tail_sweep'] = 41 # [deg]
    aircraft['engine_diameter'] = 1.425 # [m]
    aircraft['engine_bypass'] = 5.0 
    aircraft['engines_number'] = 2 
    aircraft['maximum_engine_thrust'] =  0.95 * 22000 * (1**0.8) *0.453592 * 9.80665 # [N]
    aircraft['thrust_average'] = 0.75*aircraft['maximum_engine_thrust']*((5 + aircraft['engine_bypass'])/(4 + aircraft['engine_bypass'])) # [N]

    return aircraft

def baseline_airport():
    airport = {}
    airport['takeoff_field_length'] = 2500 # [m]
    airport['landing_field_length'] = 2000 # [m]
    airport['elevation'] = 2500 # [m]
    airport['delta_ISA'] = 19.95 # [deg C]

    return airport

########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################