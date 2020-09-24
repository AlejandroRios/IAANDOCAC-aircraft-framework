import inspect
import numpy as np
import scipy as sp

from inspect import isfunction
from missionfuelburn import missionfuelburn
from scipy.optimize import fsolve

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