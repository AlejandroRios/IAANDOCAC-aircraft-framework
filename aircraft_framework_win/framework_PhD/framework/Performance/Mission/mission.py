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
from framework.baseline_aircraft import baseline_aircraft,baseline_origin_airport,baseline_destination_airport

from framework.Performance.Analysis.mission_altitude import maximum_altitude, optimum_altitude

import math
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
gallon_to_liter = 3.7852

aircraft_data = baseline_aircraft()


heading = 2

# Operations and certification parameters:
buffet_margin = 1.3 # [g]
residual_rate_of_climb = 300 # [ft/min]
ceiling = 41000 # [ft] UPDATE INPUT!!!!!!!!!

# Network and mission parameters
holding_time = 30 # [min]
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
climb_V_cas = 280
climb_mach = 0.78
cruise_mach = 0.78
cruise_V_cas = 310
descent_V_cas = 310
descent_mach = 0.78

delta_ISA = 0

captain_salary,first_officer_salary,flight_attendant_salary = crew_salary(1000)

regulated_takeoff_mass = regulated_takeoff_weight()
regulated_landing_mass = regulated_landing_weight()

maximum_takeoff_mass = regulated_takeoff_mass

f = 0
while f == 0:

    baseline_origin_airport = baseline_origin_airport()
    baseline_destination_airport = baseline_destination_airport()
    initial_altitude = baseline_origin_airport['elevation']
    maximum_ceiling = 41000 # [ft]
    step = 500
    out = 0

    while out == 0:

        # Maximum altitude calculation
        maximum_altitude, rate_of_climb = maximum_altitude(initial_altitude,ceiling,maximum_takeoff_mass,
        climb_V_cas,climb_mach,delta_ISA)
        # Optimal altitude calculation
        optimum_altitude,rate_of_climb,optimum_specific_rate = optimum_altitude(initial_altitude,ceiling,maximum_takeoff_mass,
        climb_V_cas,climb_mach,delta_ISA)
        # Maximum altitude with minimum cruise time check
        g_climb = 4/1000
        g_descent = 3/1000
        K1 = g_climb + g_descent
        minimum_cruise_time = 10*cruise_mach*minimum_cruise_time
        K2 = aircraft_data['range'] - minimum_cruise_time + g_climb*(baseline_origin_airport['elevation'] + 1500) + g_descent*(baseline_destination_airport['elevation'] + 1500)
        maximum_altitude_check = K2/K1

        if maximum_altitude_check>ceiling:
            maximum_altitude_check = ceiling
        if maximum_altitude>maximum_altitude_check:
            maximum_altitude = maximum_altitude_check
        if optimum_altitude<maximum_altitude:
            final_altitude = optimum_altitude
        else:
            final_altitude = maximum_altitude

        'TODO: this should be replaced for information from ADS-B ' 
        # Check for next lower feasible RVSN FK check according to present heading
        final_altitude = 1000*(math.floor(final_altitude/1000))

        flight_level = final_altitude/100
        odd_flight_level = [90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490, 510]
        even_flight_level = [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520]

        if (heading>0 and heading<=180):
            flight_level = min(odd_flight_level, key=lambda x:abs(x-flight_level))
            final_altitude = flight_level*100
        elif (heading>180 and heading<=360):
            flight_level = min(even_flight_level, key=lambda x:abs(x-flight_level))
            final_altitude = flight_level*100

        # Initial climb fuel estimation

        

            






        # Calculate max altitude

        




# print('========================================')
# print('Regulated takeoff weight:', regulated_takeoff_weight)
# print('========================================')


# print('========================================')
# print('Regulated landing weight:', regulated_landing_weight)
# print('========================================')




########################################################################################
"""MAIN"""
########################################################################################

