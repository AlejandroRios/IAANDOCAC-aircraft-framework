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
from framework.Performance.Analysis.climb_integration import climb_integration
from framework.Performance.Analysis.descent_integration import descent_integration
from framework.Performance.Analysis.maximum_range_cruise import maximum_range_mach
from framework.Performance.Analysis.cruise_performance import cruise_performance

from framework.Attributes.Airspeed.airspeed import V_cas_to_mach, mach_to_V_cas, crossover_altitude
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
import math

import matplotlib.pyplot as plt
import numpy as np
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
gallon_to_liter = 3.7852
feet_to_nautical_miles = 0.000164579
tolerance = 100

aircraft_data = baseline_aircraft()


heading = 2

# Operations and certification parameters:
buffet_margin = 1.3 # [g]
residual_rate_of_climb = 300 # [ft/min]
ceiling = 41000 # [ft] UPDATE INPUT!!!!!!!!!
descent_altitude = 1500
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
        max_altitude, rate_of_climb = maximum_altitude(initial_altitude,ceiling,maximum_takeoff_mass,
        climb_V_cas,climb_mach,delta_ISA)
        # Optimal altitude calculation
        optim_altitude,rate_of_climb,optimum_specific_rate = optimum_altitude(initial_altitude,ceiling,maximum_takeoff_mass,
        climb_V_cas,climb_mach,delta_ISA)
        # Maximum altitude with minimum cruise time check
        g_climb = 4/1000
        g_descent = 3/1000
        K1 = g_climb + g_descent
        minimum_cruise_time = 10*cruise_mach*minimum_cruise_time
        K2 = aircraft_data['range'] - minimum_cruise_time + g_climb*(baseline_origin_airport['elevation'] + 1500) + g_descent*(baseline_destination_airport['elevation'] + 1500)
        max_altitude_check = K2/K1

        if max_altitude_check>ceiling:
            max_altitude_check = ceiling
        if max_altitude>max_altitude_check:
            max_altitude = max_altitude_check
        if optim_altitude<max_altitude:
            final_altitude = optim_altitude
        else:
            final_altitude = max_altitude

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
        initial_altitude = initial_altitude + 1500
        _,_,total_burned_fuel0,_ = climb_integration(maximum_takeoff_mass,climb_mach,climb_V_cas,delta_ISA,final_altitude,initial_altitude)

        # Calculate best cruise mach
        mass_at_top_of_climb = maximum_takeoff_mass - total_burned_fuel0
        cruise_mach = maximum_range_mach(mass_at_top_of_climb,final_altitude,delta_ISA)
        climb_mach = cruise_mach
        descent_mach = cruise_mach

        # Recalculate climb with new mach 
        final_distance,total_climb_time,total_burned_fuel,final_altitude = climb_integration(maximum_takeoff_mass,climb_mach,climb_V_cas,delta_ISA,final_altitude,initial_altitude)

        delta = total_burned_fuel0 - total_burned_fuel

        if delta<tolerance:
            out = 1

    mass_at_top_of_climb = maximum_takeoff_mass - total_burned_fuel

    initial_cruise_altitude = final_altitude

    distance_climb = (final_distance*feet_to_nautical_miles)

    distance_cruise = aircraft_data['range'] - distance_climb
    
    altitude = initial_cruise_altitude
    flag = 1

    while flag == 1:

        transition_altitude = crossover_altitude(cruise_mach,cruise_V_cas,delta_ISA)
        _,_,_,_,_,rho_ISA,_  = atmosphere_ISA_deviation(initial_cruise_altitude,delta_ISA)

        if altitude <= 10000:
            mach = V_cas_to_mach(250,altitude,delta_ISA)
        
        if (altitude > 10000 and altitude <= transition_altitude):
            mach = V_cas_to_mach(cruise_V_cas,altitude,delta_ISA)

        if altitude > transition_altitude:
            mach = cruise_mach

        # Breguet calculation type for cruise performance
        total_cruise_time,final_cruise_mass = cruise_performance(altitude,delta_ISA,mach,mass_at_top_of_climb,distance_cruise)

        final_cruise_altitude = altitude
        
        # Type of descent: 1 = full calculation | 2 = no descent computed
        type_of_descent = 1

        if type_of_descent == 1:

             # Recalculate climb with new mach 
            final_distance,total_descent_time,total_burned_fuel,final_altitude = descent_integration(final_cruise_mass,descent_mach,descent_V_cas,delta_ISA,descent_altitude,final_cruise_altitude)
            distance_descent = (final_distance*feet_to_nautical_miles)
            distance_mission = distance_climb + distance_cruise + distance_descent
            distance_error = np.abs(aircraft_data['range']-distance_mission)

            if distance_error <= 1.0:
                flag = 0
            else:
                distance_cruise = distance_cruise - distance_error

        if type_of_descent == 2:
            flag = 0
            total_burned_fuel = 0
            final_distance = 0
            total_decent_time = 0
            total_burned_fuel = 0
            final_altitude = 0

    final_mission_mass = final_cruise_mass - total_burned_fuel
    total_mission_burned_fuel = maximum_takeoff_mass - final_mission_mass
    total_mission_flight_time = total_climb_time + total_cruise_time + total_descent_time

    
    print('========================================================================================')
    print('Cruise distance [nautical miles]:', distance_mission)
    print('----------------------------------------------------------------------------------------')
    print('Initial mission mass [Kg]:', maximum_takeoff_mass)
    print('----------------------------------------------------------------------------------------')
    print('Final mission mass [Kg]:', final_mission_mass)
    print('----------------------------------------------------------------------------------------')
    print('Fuel burned during mission [Kg]:', total_mission_burned_fuel)
    print('----------------------------------------------------------------------------------------')
    print('Flight time [min]:', total_mission_flight_time)
    print('========================================================================================')













        
        





        





        








        
    
            


        # print(total_burned_fuel)



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

