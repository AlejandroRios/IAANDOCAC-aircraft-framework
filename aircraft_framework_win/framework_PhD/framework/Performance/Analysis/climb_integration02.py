"""
Function  : 
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
from framework.Attributes.Airspeed.airspeed import V_cas_to_mach, mach_to_V_cas, crossover_altitude
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Performance.Engine.engine_performance import turbofan

from framework.Performance.Analysis.climb_to_altitude import rate_of_climb_calculation
from framework.baseline_aircraft import baseline_aircraft

import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as plt
from scipy.integrate import ode
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def climb_integration(mass,climb_mach,climb_V_cas,delta_ISA,final_altitude,initial_altitude):

    rate_of_climb = 500

    time_climb1 = 0
    time_climb2 = 0
    time_climb3 = 0

    transition_altitude = crossover_altitude(climb_mach,climb_V_cas,delta_ISA)

    # time = 0
    distance = 0
    fuel1 = 0
    fuel2 = 0
    fuel3 = 0

    if final_altitude >= transition_altitude:
        flag1 = 1
        flag2 = 1
        flag3 = 1

    if (final_altitude >= 10000 and final_altitude < transition_altitude):
        flag1 = 1
        flag2 = 1
        flag3 = 0

    if final_altitude< 10000:
        flag1 = 1
        flag2 = 0
        flag3 = 0

    total_burned_fuel = []
    total_climb_time = []

    throttle_position = 0.95
    aircraft_data = baseline_aircraft()
    number_engines = aircraft_data['number_of_engines']
    
    if flag1 == 1:

        # Climb to 10000 ft with 250 KCAS

        if final_altitude <= 11000:
            block_final_altitude = final_altitude
        else:
            block_final_altitude = 11000

        initial_block_mass = mass
        initial_block_time = 0

        altitude = 0
        delta_ISA = 0

        # if climb_V_cas > 0:
        #     mach = V_cas_to_mach(climb_V_cas,altitude,delta_ISA)
        # else:
        #     mach = climb_mach
            
        # thrust_force,_ = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        # thrust_to_weight = number_engines*thrust_force/(mass*gravity)
        # rate_of_climb,_,_ = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,initial_block_mass,aircraft_data)

        # time_to_altitude = block_final_altitude/rate_of_climb
        # time_interval = np.linspace(0,time_to_altitude[0])
        # state0 = [0.0,0.0,mass]
        # solve ODE
        t0 = 0.0
        z0 = [0.0,0.0,mass]
        solver = ode(climb)
        solver.set_integrator('dopri5')
        solver.set_f_params(climb_V_cas,climb_mach,delta_ISA)
        solver.set_initial_value(z0, t0)

        t0 = 0.0
        t1 = 5
        # N = 50
        t = np.linspace(t0, t1)
        N = len(t)
        sol = np.empty((N, 3))
        sol[0] = z0
        times = np.empty((N, 1))

        # Repeatedly call the `integrate` method to advance the
        # solution to time t[k], and save the solution in sol[k].
        k = 1
        import time
        tic = time.perf_counter()

        while solver.successful() and solver.y[1] <= 10000:
            solver.integrate(t[k])
            sol[k] = solver.y
            times[k] = solver.t
            k += 1
        toc = time.perf_counter()

        print('exec time:', (toc - tic))


        # time = times[0:k]
        # distance = sol[0:k,0]
        # altitude = sol[0:k,1]
        # weight = sol[0:k,2]
        # # print(time)
        # # print(altitude[0:k])
        # # print(weight)
        # # print(k)

        # # plt.plot(time, distance, label='x')
        # plt.plot(time,altitude, label='y')
        # # plt.plot(time,weight, label='y')
        # plt.xlabel('t')
        # plt.grid(True)
        # plt.legend()
        # plt.show()




def climb(time,state,climb_V_cas,climb_mach,delta_ISA):
    distance = state[0]
    altitude = state[1] 
    mass = state[2]
    _,_,_,_,_,rho_ISA,_  = atmosphere_ISA_deviation(altitude,delta_ISA)
    throttle_position = 0.95
    aircraft_data = baseline_aircraft()
    number_engines = aircraft_data['number_of_engines']

    
    
    if climb_V_cas > 0:
        mach = V_cas_to_mach(climb_V_cas,altitude,delta_ISA)
    else:
        mach = climb_mach
    thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
    thrust_to_weight = number_engines*thrust_force/(mass*gravity)
    rate_of_climb,V_tas, climb_path_angle = rate_of_climb_calculation(thrust_to_weight,altitude,delta_ISA,mach,mass,aircraft_data)
    

    x_dot = (V_tas*101.269)*np.cos(climb_path_angle) # ft/min
    h_dot = rate_of_climb # ft/min
    W_dot = -2*fuel_flow*0.01667  # kg/min
    time_dot =  h_dot
    dout=np.array([x_dot, h_dot, W_dot])

    dout = dout.reshape(3,)

    return dout
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
global gravity
gravity = 9.8067

# mass = 43112
# climb_mach = 0.78
# climb_V_cas = 280
# delta_ISA = 0
# final_altitude = 39000
# initial_altitude = 0
# print(climb_integration(mass,climb_mach,climb_V_cas,delta_ISA,final_altitude,initial_altitude))
# print(state)

