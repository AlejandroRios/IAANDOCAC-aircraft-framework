from framework.aircraft_dic import baseline_aircraft,baseline_origin_airport,baseline_destination_airport
import numpy as np


x = [None]*5

x[0] = 800000000000

aircraft_data = baseline_aircraft()
aircraft_data['maximum_landing_weight'] = x[0]

print(aircraft_data)
# print(baseline_aircraft())

