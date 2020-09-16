import numpy as np

def breguet(type, task, E_R_or_frac, LD, SFC, V, eta_p,t):

    if V == "False":
        V = 'NaN'

    varargout = [0]*2

    if type == 'jet' and task == 'loiter':
        varargout = 1/np.exp(t/((1/SFC)*LD))
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


# Test
# type = 'jet'
# task = 'range'
# R =  0.7
# LD =  0.866*18
# SFC = 0.5
# V =  500
# eta_p = 'false'

# print(breguet(type, task, R, LD, SFC, V, eta_p))


















