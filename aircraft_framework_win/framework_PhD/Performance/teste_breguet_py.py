
import numpy as np 
from breguet import breguet
from missionfuelburn import missionfuelburn
from fuelfractionsizing import fuelfractionsizing

fixedW = 400
R = 600*1852
L_over_D = 10
PSFC = 0.4*1.657e-06
eta_prop = 0.8

t = 1200 

segments = [0.98,
            0.99,
            breguet('jet','cruise', R, L_over_D, PSFC,252,eta_prop,t),
            breguet('jet','loiter', R, L_over_D, PSFC,252,eta_prop,t),
            0.99]

print(segments)
fuel_safety_margin = 0.06
FF = (1+fuel_safety_margin)*missionfuelburn(segments)

EWfunc = lambda w0: 3.03*w0**-0.235
W0 = fuelfractionsizing(EWfunc,fixedW,FF,'false','false')

print(W0)