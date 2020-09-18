"""
Function  : NPV.py
Title     : Net present valie
Written by: Alejandro Rios
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This functions calculates the net present value. Methodology from Fregnani 2020
TODO's:
    -
Inputs:
    -
Outputs:
    - 
"""
########################################################################################
"IMPORTS"
########################################################################################
import numpy as np
import matplotlib.pyplot as plt
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def aircraft_price(MTOW, share):
    '''
    Methodology from Airbus price list (Narrow Bodies,1 aisle) 2018
    Inputs:
        - MTOW
        - share
    Outputs:
        - price
    TODO's:
        - ask for more especification of WTADJ_price
    '''
    y0 = 3.3383
    mu = 0.0013

    WTADJ_price = y0+mu*MTOW
    discount = y_ref/x_ref*share
    price = WTADJ_price*(1-discount)
    return price*1e6
    
def market_info(share):
    '''
    Methodology from 
    Inputs:
        - 
    Outputs:
        - 
    TODO's:
        - 
    '''
    share_ref = 0.6
    price = 23000000
    share_factor = share/share_ref
    price = aircraft_price(MTOW, share)
    return price

def delivery_forecast():
    '''
    Methodology from 
    Inputs:
        - 
    Outputs:
        - 
    '''
    year = list(range(1, 16))
    deliveries = [0,0,0,0,6,20,44,92,94,102,94,90,84,30,20]
    return year,deliveries

# year,deliveries = delivery_forecast()
# plt.plot(year,deliveries)
# plt.show()

def program_share():
    '''
    Methodology from 
    Inputs:
        - 
    Outputs:
        - 
    '''
    manufacturer = 0.7
    partner = 1-manufacturer
    man_power_cost_manufacturer = 41.72
    man_power_cost_partner = 83.44
    man_power_cost_average = manufacturer*man_power_cost_manufacturer + partner*man_power_cost_partner
    return man_power_cost_average 

def product_development_cost():
    '''
    Product Development Cost 
    Methodology from 
    Inputs:
        - 
    Outputs:
        - 
    '''
    # Man Power Distribution
    PDC_MPD = [0.25,0.35,0.30,0.1]
    # Infrastructure Distribution
    PDC_INFRAD = [0.55,0.25,0.15,0.05] 
    # Generic Cost Distribution
    PDC_GEND = [0.25,0.35,0.40,0.1]
    return PDC_MPD, PDC_INFRAD, PDC_GEND

def complexity_factor():
    '''
    Production Cost - Complexity factor
    Methodology from 
    Inputs:
        - 
    Outputs:
        - 
    '''
    complexity_factors = {}
    complexity_factors['landing_gear'] = 1.2
    complexity_factors['flight_controls'] = 1.4
    complexity_factors['engines'] = 1.1
    complexity_factors['nacelles'] = 1.0
    complexity_factors['interior'] = 1.0
    complexity_factors['electrical'] = 1.3
    complexity_factors['avionics'] = 0.9
    complexity_factors['structures'] = 1.5
    complexity_factors['fuel'] = 1.0
    return complexity_factors

########################################################################################
# NON-RECURRING COST
########################################################################################
def managment_houres():
    '''
    Management and Administration hours
    Methodology from 
    Inputs:
        - 
    Outputs:
        - 
    '''
    
    return complexity_factors