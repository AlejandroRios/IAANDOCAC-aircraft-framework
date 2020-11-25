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
from framework.baseline_aircraft import baseline_aircraft,baseline_origin_airport,baseline_destination_airport
from framework.Performance.Mission.mission import mission

from framework.Economics.revenue import revenue

import pandas as pd
import pickle
import numpy as np




########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################

########################################################################################
"""MAIN"""
########################################################################################
global gravity
gravity = 9.80665 
gallon_to_liter = 3.7852
feet_to_nautical_miles = 0.000164579

aircraft_data = baseline_aircraft()


########################################################################################
"""TEST"""
########################################################################################


df1 = pd.read_csv('distance.csv')
df1 = (df1.T)
# print(df1)
distances = df1.to_dict()

df2 = pd.read_csv('demand.csv')
df2 = (df2.T)
# print(df2)
demand = df2.to_dict()

df3 = pd.read_csv('doc.csv')
df3 = (df3.T)
print(df3)
doc = df3.to_dict()

aircraft_data = baseline_aircraft()
pax_capacity = aircraft_data['passenger_capacity']
# rev_mat = revenue(aircraft_data,distances)

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

print(revenue_ik)

# df = pd.DataFrame(data=distances)
# df = (df.T)

# DOC_ik = {}

# for i in departures:
#     for k in arrivals:
#         if i != k:
#             DOC_ik[(i,k)] = mission(distances[i][k]) * distances[i][k]
#             print(DOC_ik[(i,k)])
#         else:
#             DOC_ik[(i,k)] = 0

# df = pd.DataFrame(data=DOC_ik)
# df = (df.T)

# print (df)
# df.to_excel('doc.xlsx')

# pickle_out = open("dict.pickle","wb")
# pickle.dump(DOC_ik, pickle_out)
# pickle_out.close()


# pickle_in = open("dict.pickle","rb")
# DOC= pickle.load(pickle_in)

# DOC_ik = {}
# for i in departures:
#     for k in arrivals:
#         if i != k:
#             DOC_ik[(i,k)] = DOC[i][k]*distances[i][k]
#         else:
#             DOC_ik[(i,k)] = 0

# print(DOC_ik)
# # print(revenue_ik)