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
from inspect import isfunction
import numpy as np 
from scipy.optimize import fsolve
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def cruise_performance(R,mass_0,TSFC,V):

    knot_to_ms = 0.514444
    fixedW = mass_0#  [kg]
    R = R*1852 # convert 600 nmi to m [m]
    L_over_D = 13.9
    # TSFC = TSFC*gravity*(1/3600) # 1/s
    TSFC = TSFC*(1/3600) # 1/s
    eta_prop = 0.8 
    V = V*knot_to_ms # [kt]
    segments = [breguet('jet','cruise', R, L_over_D, TSFC,V,'false')]
    fuel_safety_margin = 0.06
    FF = (1+fuel_safety_margin)*missionfuelburn(segments)

    EWfunc = lambda w0: 3.03*w0**-0.235
    W0 = fuelfractionsizing(EWfunc,fixedW,FF,'false','false')
    Wf = FF*W0
    t = 1/TSFC * L_over_D * np.log(1/segments[0])



    return FF,W0,t*0.01667,Wf,segments
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

R = 400 # [nmi]
mass_0 = 50000 # [kg]
TSFC = 0.51 # [1/hr]
V = 353.65 # [kts]
result = cruise_performance(R,mass_0,TSFC,V)


print(result)