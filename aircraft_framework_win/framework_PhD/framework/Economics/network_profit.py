"""
Function  :main.py
Title     : main function
Written by: 
Email     : aarc.88@gmail.com
Date      : 
Last edit :
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
########################################################################################
"IMPORTS"
########################################################################################
from framework.aircraft_dic import baseline_aircraft,baseline_engine,baseline_origin_airport,baseline_destination_airport
from framework.Performance.Mission.mission import mission
from framework.Network.network_optimization import network_optimization
from framework.Economics.revenue import revenue

import pandas as pd
import pickle
import numpy as np
from datetime import datetime



########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

########################################################################################
"""MAIN"""
########################################################################################

def network_profit(x):
    aircraft_data = baseline_aircraft()
    aircraft_data['wing_surface'] = x[0]
    aircraft_data['wing_aspect_ratio'] = x[1]
    aircraft_data['wing_taper_ratio'] = x[2]
    aircraft_data['wing_sweep_c_4'] = x[3]
    aircraft_data['incidence_tip']  = x[4]
    aircraft_data['semi_span_kink'] = x[5]
    aircraft_data['engine_bypass'] = x[6]
    aircraft_data['passenger_capacity'] = x[11]
    aircraft_data['number_of_seat_abreast'] = x[12]
    aircraft_data['range'] = x[13]
    aircraft_data['winglet_presence'] = x[17]
    aircraft_data['slat_presence'] = x[18]
    aircraft_data['horizontal_tail_position'] = x[19]

    engine_data = baseline_engine()

    engine_data['engine_bypass'] = x[6]
    engine_data['fan_pressure_ratio'] = x[7]
    engine_data['compressor_pressure_ratio'] = x[8]
    engine_data['turbine_inlet_temperature'] = x[9]
    engine_data['fan_pressure_ratio'] = x[10]
    engine_data['engine_design_point_pressure'] = x[14]
    engine_data['engine_design_point_mach'] = x[15]
    engine_data['engine_position'] = x[16]
    market_share = 0.1 
    df1 = pd.read_csv('Database/distance.csv')
    df1 = (df1.T)
    distances = df1.to_dict()
    df2 = pd.read_csv('Database/demand.csv')
    df2 = round(market_share*(df2.T))
    demand = df2.to_dict()
    pax_capacity = x[11]




    departures = ['CD1','CD2','CD3','CD4','CD5','CD6','CD7','CD8','CD9','CD10']
    arrivals = ['CD1','CD2','CD3','CD4','CD5','CD6','CD7','CD8','CD9','CD10']

    pax_number = 78
    load_factor = pax_number/pax_capacity
    revenue_ik = {}
    for i in departures:
        for k in arrivals:
            if i != k:
                # revenue_ik[(i,k)] = revenue(distances[i][k],load_factor,pax_capacity,pax_number)
                revenue_ik[(i,k)] = revenue(demand[i][k],distances[i][k],pax_capacity,pax_number)
            else:
                revenue_ik[(i,k)] = 0

    # print(revenue_ik)

    DOC_ik = {}

    for i in departures:
        for k in arrivals:
            if i != k:
                DOC_ik[(i,k)] = float(mission(distances[i][k]) * distances[i][k])
                print(DOC_ik[(i,k)])
            else:
                DOC_ik[(i,k)] = 0

    profit = network_optimization(distances,demand,DOC_ik)

    return float(profit)



########################################################################################
"""TEST"""
########################################################################################
# global NN_induced,NN_wave,NN_cd0,NN_CL,num_Alejandro
# num_Alejandro = 100000000000000000000000
# global NN_induced,NN_wave,NN_cd0,NN_CL

NN_induced = np.load('Aerodynamics/NN_induced.npy',allow_pickle=True) 
NN_wave = np.load('Aerodynamics/NN_wave.npy',allow_pickle=True) 
NN_cd0 = np.load('Aerodynamics/NN_cd0.npy',allow_pickle=True)  
NN_CL = np.load('Aerodynamics/NN_CL.npy',allow_pickle=True) 
x = [72,8.6,0.44,23.5,-3,0.32,5,1.425,28,1405,1.6,78,4,1600,41000,0.78,1,1,1,1]
result = network_profit(x)
print(result)