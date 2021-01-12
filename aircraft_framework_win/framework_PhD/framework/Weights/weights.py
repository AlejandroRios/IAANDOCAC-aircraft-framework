"""
File name : weights function
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python 3.8 or >
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This code describe the class to obtain the aircraft weight for the following groups:
        - Wing
        - Tail
        - Body
        - Alighting gear
        - Alighting water
        - Surface controls
        - Engine
Future implementations:
    - 
Inputs:
    -
Outputs:
    - 
"""
# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================


def wing_mass(MTOW, wing_position, landing_gear_position, spoilers, AR, S_w, wing_TR, wing_Sweep_c4, V_MO, wing_tc_m):
    '''
    Methodology from Isikveren 2002
    Inputs:
        - MTOW - Max. TakeOff Weight
        - n_ultimate - ultimate load factor
        - S_w - reference area (wing)
        - AR - aspect ratio (wing)
        - wing_TR - wing taper ratio
        - wing_Sweep_c4
        - V_MO - Maximum operating speed at sea level
    '''
    # Constants definition
    FS = 1.5    # factor of safety
    YEIS = 2016    # Year of entry into service
    alpha_w = 0.0328
    phi_w = 0.656
    Beta_w = 1.5
    delta_w = 1.5
    epsilon_w = 1.5
    Chi_w = 1.1
    rho_sls_g = 0.125

    if MTOW <= 1868:
        n_limit = 3.8
    elif MTOW > 1868 and MTOW < 22680:
        n_limit = 2.1 + 24000/(2.205*MTOW+10000)
    elif MTOW >= 22680:
        n_limit = 2.5    # limit load factor

    # wing installation philosophy
    if wing_position == 'low':
        k_co = 1.17
    elif wing_position == 'high':
        k_co = 1.25

    # spoilers existence correction
    if spoilers == 'True':
        k_sp = 1.02
    else:
        k_sp = 1

    # landing gear installation philosophy
    if landing_gear_position == 'wing':
        k_lg = 1.03
    elif landing_gear_position == 'fuselage':
        k_lg = 1.015

    n_ultimate = FS*n_limit
    Pi_ATM = np.exp(2.965-0.001525*YEIS)
    Pi_Cw = k_co*k_sp*k_lg
    Pi_tc = 16.5*np.sin(2*np.pi*wing_tc_m)

    tau_s = 1 + 1.31*(((0.5*rho_sls_g*V_MO**2)/(1000))**2) * (1/n_ultimate**3)

    aux1 = Pi_ATM*alpha_w*Pi_Cw
    aux2 = MTOW*n_ultimate*S_w*(AR**Beta_w) * \
        (Chi_w + wing_TR/2)*(tau_s**delta_w)
    aux3 = Pi_tc*np.cos(wing_Sweep_c4*np.pi/180)**phi_w

    return aux1*(aux2/aux3)**phi_w


def horizontal_tail_mass(V_Dive, S_H, HT_sweep_c2):
    '''
    Methodology from Torenbeek 1982
    Inputs:
        - V_Dive - Dive speed
    '''

    fin = 'trimmable'
    if fin == 'trimmable':
        k_H = 1.1
    elif fin == 'fixed':
        k_H = 1

    C1 = (S_H**0.2)*V_Dive
    C2 = 1000*np.sqrt(np.cos(HT_sweep_c2*np.pi/180))
    return k_H*S_H*(62*(C1/C2) - 2.5)


def vertical_tail_mass(V_Dive, S_H, z_H, S_V, b_V, VT_sweep_c2):
    '''
    Methodology from Torenbeek 1982
    Inputs:
        - V_Dive - Dive speed
    '''
    k_V = 1 + 0.15*((S_H*z_H)/(S_V*b_V))
    C1 = (S_V**0.2)*V_Dive
    C2 = 1000*np.sqrt(np.cos(VT_sweep_c2*np.pi/180))
    return k_V*S_V*(62*(C1/C2) - 2.5)


def fuselage_mass(V_Dive, l_H, w_F, h_F, S_F_wet):
    '''
    Methodology from Torenbeek
    Inputs:
        - V_Dive - Dive speed
        - l_H - lever arm of the horizontal tailplane
        - w_F - maximum fuselage width
        - h_F - maximum fuselage height
        - S_F_wet - fuselage wetted area in 
    '''
    kwf = 0.23  # Constant of proportionality
    return kwf*np.sqrt(V_Dive*(l_H/(w_F + h_F)))*S_F_wet**1.2


def main_landig_gear_mass(m_MTO):
    '''
    Methodology from Torenbeek
    Inputs:
        - m_MTO - takeoff mass in [kg]
    '''

    if wing_position == 'low':
        k_LG = 1
    elif wing_position == 'high':
        k_LG = 1.08

    A_LG = 15.0
    B_LG = 0.033
    C_LG = 0.0210
    D_LG = 0.0

    return k_LG*(A_LG + B_LG*m_MTO**(3/4) + C_LG*m_MTO + D_LG*m_MTO**(3/2))


def nose_landig_gear_mass(m_MTO):
    '''
    Methodology from Torenbeek
    Inputs:
        - m_MTO - takeoff mass in [kg]
    '''
    if wing_position == 'low':
        k_LG = 1
    elif wing_position == 'high':
        k_LG = 1.08

    A_LG = 5.4
    B_LG = 0.049
    C_LG = 0.0
    D_LG = 0.0

    return k_LG*(A_LG + B_LG*m_MTO**(3/4) + C_LG*m_MTO + D_LG*m_MTO**(3/2))


def nacelle_mass(g, T_TO):
    '''
    Methodology from Torenbeek
    Inputs:
        - g - acceleration of GRAVITY
        - T_TO - takeoff thrust of all engines combined
    '''
    return (0.065*T_TO)/g


def engine_mass():
    '''
    Methodology from Torenbeek
    Inputs:
        -
    '''
    return


def installed_engines_mass():
    '''
    Methodology from Torenbeek
    Inputs:
        -
    '''
    return


def systems_mass():
    '''
    Methodology from Torenbeek
    Inputs:
        -
    '''
    return


def OE_mass():
    '''
    Methodology from 
    Inputs:
        -
    '''
    return


def fuel_mass(R, C, V, L_D):
    '''
    Methodology from 
    Inputs:
        -

    Mission segments
    i - description
    1 - Warmup and takeoff
    2 - Climb
    3 - Cruise
    4 - Loiter
    5 - Cruise alternative
    6 - Loiter Alternative
    7 - Land
    8 - 
    '''
    W1_W0 = 0.97
    W2_W1 = 0.985

    # R =
    # C
    # V
    # L_D
    # W3_W2

    return


def MTOW_mass(MTOW_guess):
    '''
    Methodology from 
    Inputs:
        -
    '''
    return


############00############################################################################
# MAIN
# =============================================================================
'''TODO:
    - Input parameters from CPACS
    - Define input names according to only one reference
    - Improve comments
    '''


############00############################################################################
"""TEST """
# =============================================================================

# Wing
MTOW = 22680
landing_gear_position = 'wing'
wing_position = 'high'
spoilers = 'True'
AR = 20
S_w = 100
wing_TR = 0.5
wing_sweep_c4 = 20
wing_tc_m = 0.1
mach_maximum_operating = 0.8
va = 343
V_MO = mach_maximum_operating*va
print('wing weight:', wing_mass(MTOW, wing_position, landing_gear_position,
                                spoilers, AR, S_w, wing_TR, wing_sweep_c4, V_MO, wing_tc_m))


# HT

M_Dive = mach_maximum_operating + 0.05  # Acording to JAR-23.335(b) or JAR-25.335(b)
V_Dive = M_Dive*va
S_H = 30
HT_sweep_c2 = 20
z_H = 1
print('horizontal tail weight:', horizontal_tail_mass(V_Dive, S_H, HT_sweep_c2))

# VT
S_V = 25
b_V = 5
VT_sweep_c2 = 45
print('vertical tail weight:', vertical_tail_mass(
    V_Dive, S_H, z_H, S_V, b_V, VT_sweep_c2))


# Fuselage
l_H = 20
w_F = 6
h_F = 6
S_F_wet = 100

print('fuselage weight:', fuselage_mass(V_Dive, l_H, w_F, h_F, S_F_wet))
