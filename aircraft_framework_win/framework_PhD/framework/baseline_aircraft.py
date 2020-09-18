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
    aircraft['maximum_takeoff_weight'] = 55000 # [kg]
    aircraft['maximum_landing_weight'] = 32000 
    aircraft['wing_surface'] = 100
    aircraft['wing_aspect_ratio'] = 11
    aircraft['wing_taper_ratio'] = 0.4
    aircraft['wing_sweep_leading_edge'] = 23.5
    aircraft['incidence_root'] = 2
    aircraft['incidence_kink'] = 0
    aircraft['incidence_tip'] = -1
    aircraft['semi_span_kink'] = 0.32
    # aircraft['r0'] = [0.0153, ]
    # aircraft['thickness_to_chord_ratio'] = [0.1228,0.1055,0.0982]
    # aircraft['phi']
    aircraft['thickness_to_chord_maximum_ratio'] = [0.3738,0.3585,0.3590]
    # aircraft['theta']
    # aircraft['epsilon']
    aircraft['thickness_to_chord_average_ratio'] = 0.11
    aircraft['aircraft_wet_surface'] = 485
    aircraft['wing_wet_surface'] = 122.5
    aircraft['CL_maximum_clean'] = 1.6
    aircraft['CL_maximum_takeoff'] = 2.4
    aircraft['CL_maximum_landing'] = 2.0
    aircraft['flap_deflection_takeoff'] = 35
    aircraft['flap_deflection_landing'] = 30
    aircraft['vertical_tail_surface'] = 16.2
    aircraft['horizontal_tail_surface'] = 30
    aircraft['vertical_tail_sweep'] = 41
    aircraft['engine_diameter'] = 1.425
    aircraft['engine_bypass'] = 5.0
    aircraft['engine_number'] = 2
    aircraft['maximum_engine_thrust'] = 0.9 * 22000 * 0.4535923 # database
    aircraft['thrust_average'] = 0.75*((5 + aircraft['engine_bypass'])/(4 + aircraft['engine_bypass'])) * (2* aircraft['maximum_engine_thrust'])# [lbf]


    return aircraft

def baseline_airport():
    airport = {}
    airport['takeoff_field_length'] = 2500
    airport['landing_field_length'] = 2000
    airport['elevation'] = 2500
    airport['delta_ISA'] = 19.95

    return airport

########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################

Tmax=0.95*MAXRATE*(sigma^ne)*lb2kg  # datasheet
Tavg=0.75*((5+BPR)/(4+BPR))*(2*Tmax)  # Bentos suggestion