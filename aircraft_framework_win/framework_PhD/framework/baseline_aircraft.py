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

    lbf_to_N = 4.448
    kg_to_N = 9.80665


    aircraft = {}
    aircraft['maximum_takeoff_weight'] = 60000 * kg_to_N  # [N]
    aircraft['maximum_landing_weight'] = 60000 * kg_to_N  # [N]
    aircraft['wing_surface'] = 96 # Fokker = 93.5  [m2] 
    aircraft['wing_aspect_ratio'] = 9.6 # Fokker = 8.43 
    aircraft['wing_taper_ratio'] = 0.38
    aircraft['wing_sweep_c_4'] = 22.6 # [deg]
    aircraft['incidence_root'] = 2 # [deg]
    aircraft['incidence_kink'] = 0 # [deg]
    aircraft['incidence_tip'] = -2.5 # [deg]
    aircraft['semi_span_kink'] = 0.34
    # aircraft['r0'] = [0.0153, ]
    # aircraft['thickness_to_chord_ratio'] = [0.1228,0.1055,0.0982]
    # aircraft['phi']
    aircraft['thickness_to_chord_maximum_ratio'] = [0.3738,0.3585,0.3590]
    # aircraft['theta']
    # aircraft['epsilon']
    aircraft['thickness_to_chord_average_ratio'] = 0.11
    aircraft['aircraft_wet_surface'] = 589.7500 # [m2]
    aircraft['wing_wet_surface'] = 168.6500 # [m2]
    aircraft['CL_maximum_clean'] = 1.65 
    aircraft['CL_maximum_takeoff'] = 2.20
    aircraft['CL_maximum_landing'] = 2.0
    aircraft['flap_deflection_takeoff'] = 35 # [deg]
    aircraft['flap_deflection_landing'] = 30 # [deg]
    aircraft['vertical_tail_surface'] = 16.2 # [m2]
    aircraft['horizontal_tail_surface'] = 23.35 # [m2]
    aircraft['vertical_tail_sweep'] = 41 # [deg]
    aircraft['engine_diameter'] = 1.36 # [m]
    aircraft['engine_bypass'] = 5.0 
    aircraft['engines_number'] = 2
    # aircraft['maximum_engine_thrust'] =  0.95 * 22000 * (1**0.8) *0.453592 * 9.80665 # [N]
    aircraft['maximum_engine_thrust'] = aircraft['engines_number'] *  0.95 * 16206 * (1**0.8) * lbf_to_N  # Rolls-Royce Tay 650 Thrust[N] 
    aircraft['average_thrust'] = 0.75*aircraft['maximum_engine_thrust']*((5 + aircraft['engine_bypass'])/(4 + aircraft['engine_bypass'])) # [N]

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

