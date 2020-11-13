"""
Function  : cruise_performance.py
Title     : Cruise performance function
Written by: Alejandro Rios
Date      : November/2020
Last edit : November/2020
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
from inspect import isfunction
import numpy as np 
from scipy.optimize import fsolve

from framework.Performance.Engine.engine_performance import turbofan
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
from framework.Attributes.Airspeed.airspeed import V_cas_to_mach, mach_to_V_cas,mach_to_V_tas, crossover_altitude
from framework.baseline_aircraft import baseline_aircraft
from framework.Aerodynamics.aerodynamic_coefficients import zero_fidelity_drag_coefficient
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def cruise_performance(altitude,delta_ISA,mach,mass,distance_cruise):
    aircraft_data = baseline_aircraft()
    n = 10
    step_cruise = distance_cruise/n
    distance = 0
    time_cruise = 0
    mass_fuel_cruise = 0

    V_tas = mach_to_V_tas(mach,altitude,delta_ISA)

    for i in range(n):

        TSFC,L_over_D,fuel_flow,throttle_position = specific_fuel_consumption(aircraft_data,mach,altitude,delta_ISA,mass)

        mass_fuel,time= mission_segment(mass,step_cruise,L_over_D,TSFC,V_tas)
        
        time_cruise = time_cruise + time

        mass_fuel_cruise = mass_fuel_cruise + mass_fuel

    
    final_mass = mass - mass_fuel_cruise
    # print(final_mass)

    return time_cruise,final_mass

def specific_fuel_consumption(aircraft_data,mach,altitude,delta_ISA,mass):
    knots_to_meters_second = 0.514444
    wing_surface = aircraft_data['wing_surface']
    number_engines = aircraft_data['number_of_engines']

    V_tas = mach_to_V_tas(mach,altitude,delta_ISA)
    _,_,_,_,_,rho_ISA,_ = atmosphere_ISA_deviation(altitude,delta_ISA)
   
    CL_required = (2*mass*gravity)/(rho_ISA*((knots_to_meters_second*V_tas)**2)*wing_surface)
    phase = 'cruise'
    CD = zero_fidelity_drag_coefficient(aircraft_data,CL_required,phase)
    L_over_D = CL_required/CD
    throttle_position = 0.6

    thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]

    FnR = mass*gravity/L_over_D

    step_throttle = 0.01
    throttle_position = 0.6
    total_thrust_force = 0

    while (total_thrust_force<FnR and throttle_position<=1):
        thrust_force,fuel_flow = turbofan(altitude,mach,throttle_position) # force [N], fuel flow [kg/hr]
        TSFC = (fuel_flow*gravity)/thrust_force
        total_thrust_force = number_engines*thrust_force
        throttle_position = throttle_position+step_throttle
    
    L_over_D = CL_required/CD

    return TSFC,L_over_D,fuel_flow,throttle_position

def mission_segment(mass_0,step_cruise,L_over_D,TSFC,V_tas):
    knots_to_meters_second = 0.514444
    second_to_miniute = 0.01667
    fixedW = mass_0#  [kg]
    R = step_cruise*1852 # convert 600 nmi to m [m]


    # TSFC = TSFC*gravity*(1/3600) # 1/s
    TSFC = TSFC*(1/3600) # 1/s
    # eta_prop = 0.8 

    
    V = V_tas*knots_to_meters_second # [kt]
    segments = [breguet('jet','cruise', R, L_over_D, TSFC,V,'false')]
    fuel_safety_margin = 0.06
    FF = (1+fuel_safety_margin)*missionfuelburn(segments)

    EWfunc = lambda w0: 3.03*w0**-0.235
    mass_0 = fuelfractionsizing(EWfunc,fixedW,FF,'false','false')
    mass_fuel = FF*mass_0
    time = 1/TSFC * L_over_D * np.log(1/segments[0])
    return mass_fuel,time*second_to_miniute


def breguet(type, task, E_R_or_frac, LD, SFC, V, eta_p):

    if V == "False":
        V = 'NaN'

    varargout = [0]*2

    if type == 'jet' and task == 'loiter':
        varargout = np.exp(-E_R_or_frac*SFC/(LD))
    elif type == 'jet' and task == 'cruise':
        varargout = np.exp(-E_R_or_frac*SFC/(V*LD))
    elif type == 'prop' and task == 'loiter':
        varargout = np.exp(-E_R_or_frac*SFC*V/(LD*eta_p))
    elif type == 'prop' and task == 'cruise':
        varargout = np.exp(-E_R_or_frac*SFC/(LD*eta_p))
    elif type == 'jet' and task == 'range':
        varargout[0] = -LD*np.log(E_R_or_frac)/SFC
        varargout[1] = varargout[0]*V
    elif type == 'prop' and task == 'range':
        varargout[0] = -LD*eta_p*np.log(E_R_or_frac)/SFC
        varargout[1] = varargout[0]/V
    else:
        print('Unknown mission segment type and/or task string')

    return(varargout)


def fuelfractionsizing(sf,fixedW,FF,tol,maxW):

    if isfunction(sf) != True:
        if len(sf) == 1:
            W0 = fixedW/(1-FF-sf[0])
            return
        elif len(sf) == 2:
            sf = lambda w0: sf[0]*w0**(sf[1])
        elif len(sf) == 3:
            sf = lambda w0: sf[2]*sf[0]*w0**(sf[1])
        else:
            print('invalid empty weight function sf')
        
    

    if isinstance(sf, (np.ndarray)) == True:
         FF = missionfuelburn(FF)
    
    minW = fixedW/(1-FF)

    # # default maxW represents an aircraft with a terrible fixedW fraction
    # if (*args < 5) || isempty(maxW)
    maxW = minW*1e6
    
    tol = 1e-5*minW
    # if (nargin < 4) || isempty(tol)
    #     tol = 1e-5*minW

    f = lambda W: 1 - sf(W) - FF -fixedW/W

    bounds = np.array([minW,maxW])
    bounds = minW
    W0 = fsolve(f,bounds,xtol=tol)

    return(W0)


def missionfuelburn(varargin):
    n=len(varargin)
    fracs = [0]*(n+1)
    fracs[0] = 1
    for ii in range(n):
        fracs[ii+1] = fracs[ii]*varargin[ii]
    FF = 1 - fracs[-1]
    return(FF)

########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################
global gravity
gravity = 9.80665 


# altitude = 39000
# delta_ISA = 0
# mach = 0.97
# mass = 46120
# distance_cruise = 1476
# results = cruise_performance(altitude,delta_ISA,mach,mass,distance_cruise)
# print(results)