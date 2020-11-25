"""
Function  : revenue.py
Title     :
Written by: 
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
import pandas as pd
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def revenue(demand,distance,pax_capacity,pax_number):
    average_ticket_price = 110
    RPM = pax_number*distance
    passenger_revenue = pax_number*average_ticket_price
    yield_ij = passenger_revenue/RPM
    return  demand*distance*yield_ij
    
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
# distance = 3000
# load_factor = 0.3
# pax_capacity = 78
# pax_number = 78
# demand = 4000
# print(revenue(demand,distance,pax_capacity,pax_number))