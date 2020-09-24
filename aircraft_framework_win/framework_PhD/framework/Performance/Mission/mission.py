"""
Function  : mission.py
Title     : Mission function
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
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
###################################

########################################################################################
"IMPORTS"
########################################################################################
from framework.Economics.crew_salary import crew_salary
from framework.Sizing.performance_constraints import regulated_takeoff_weight, regulated_landing_weight
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
gallon_to_liter = 3.7852

# Operations and certification parameters:
buffet_margin = 1.3 # [g]
residual_rate_of_climb = 300 # [ft/min]
ceiling = 41000 # [ft] UPDATE INPUT!!!!!!!!!

# Network and mission parameters
holding_time = 30 # [min]
minimum_cuise_time = 3 # [min]
fuel_density = 0.81 # [kg/l]
fuel_price_per_kg = 1.0 # [per kg]
fuel_price = (fuel_price_per_kg/fuel_density)*gallon_to_liter
time_between_overhaul = 2500 # [hr]
taxi_fuel_flow_reference = 5 # [kg/min]
contingency_fuel_pct = 0.1 # pct ??????????????????
minimum_cruise_time = 3 # [min]
pax_weight = 110 # [kg]
go_around_allowance = 300

# Initial flight speed schedule
climb_CAS = 280
climb_Mach = 0.78
cruise_Mach = 0.78
cruise_CAS = 310
descent_CAS = 310
descent_Mach = 0.78

captain_salary,first_officer_salary,flight_attendant_salary = crew_salary(1000)

regulated_takeoff_weight = regulated_takeoff_weight()
regulated_landing_weight = regulated_landing_weight()

# print('========================================')
# print('Regulated takeoff weight:', regulated_takeoff_weight)
# print('========================================')


# print('========================================')
# print('Regulated landing weight:', regulated_landing_weight)
# print('========================================')


########################################################################################
"""MAIN"""
########################################################################################

