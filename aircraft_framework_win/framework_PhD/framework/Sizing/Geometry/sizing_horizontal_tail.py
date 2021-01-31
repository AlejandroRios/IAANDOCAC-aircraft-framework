"""" 
Title     : Size Horizontal Tail 
Written by: Alejandro Rios
Date      : 30/10/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
MTOW

Outputs:
Cap_Sal
FO_Sal
"""

########################################################################################
"""Importing Modules"""
########################################################################################
########################################################################################
"""Constants declaration"""
########################################################################################

########################################################################################

# horizontal_tail['area'] = 21.7200
# horizontal_tail['aspect_ratio'] = 4.6400
# horizontal_tail['taper_ratio'] = 0.3900
# horizontal_tail['position']  = 2
# wing['area'] = 93.5000
# wing['sweep_c_4'] = 17.4500
# fuselage['length'] = 33.1553
# vertical_tail['sweep_leading_edge'] = 46.0456
# vertical_tail['tip_chord'] = 3.1621
# vertical_tail['center_chord'] = 4.2731
# vertical_tail['span'] = 3.3086
# horizontal_tail['aerodynamic_center'] = 0.2500
# Mach = 0.8000
# Ceiling = 35000




import numpy as np
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
def sizing_horizontal_tail(vehicle, Mach, Ceiling):

    wing = vehicle['wing']
    winglet = vehicle['winglet']
    horizontal_tail = vehicle['horizontal_tail']
    vertical_tail = vehicle['vertical_tail']
    fuselage = vehicle['fuselage']

    #
    rad = np.pi/180
    m22ft2 = (1/0.3048)**2
    kt2ms = 1/1.943844   # [kt] para [m/s]

    horizontal_tail['sweep_c_4'] = wing['sweep_c_4'] + 5
    horizontal_tail['aspect_ratio'] = horizontal_tail['aspect_ratio']  # alongamento EH
    horizontal_tail['taper_ratio'] = horizontal_tail['taper_ratio']  # Afilamento EH
    horizontal_tail['root_chord'] = 0.10  # [#]espessura relativa raiz
    horizontal_tail['tip_chord']  = 0.10  # [#]espessura relativa ponta
    horizontal_tail['mean_chord'] = (horizontal_tail['root_chord']+horizontal_tail['tip_chord'] )/2  # [#]espessura media
    horizontal_tail['tail_to_wing_area_ratio']  = horizontal_tail['area']/wing['area']  # rela�ao de areas
    horizontal_tail['twist']  = 0  # torcao EH

    if horizontal_tail['position']  == 1:
        # [�] enflechamento bordo de ataque
        horizontal_tail['sweep_leading_edge'] = 1/rad * \
            (np.arctan(np.tan(rad*horizontal_tail['sweep_c_4']) +
                       1/horizontal_tail['aspect_ratio']*(1-horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])))
        horizontal_tail['sweep_c_2'] = 1/rad*(np.arctan(np.tan(rad*horizontal_tail['sweep_c_4'])-1 /
                                         horizontal_tail['aspect_ratio']*(1-horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])))  # [�] enflechamento C/2
        # [�] enflechamento bordo de fuga
        horizontal_tail['sweep_trailing_edge'] = 1/rad * \
            (np.arctan(np.tan(rad*horizontal_tail['sweep_c_4']) -
                       3/horizontal_tail['aspect_ratio']*(1-horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])))
        horizontal_tail['span'] = np.sqrt(horizontal_tail['aspect_ratio']*horizontal_tail['area'])  # evergadura EH
        horizontal_tail['center_chord'] = 2*horizontal_tail['area']/(horizontal_tail['span']*(1+horizontal_tail['taper_ratio']))  # corda de centro
        horizontal_tail['tip_chord'] = horizontal_tail['taper_ratio']*horizontal_tail['center_chord']  # corda na ponta
        horizontal_tail['dihedral'] = 3
    else:
        horizontal_tail['center_chord'] = vertical_tail['tip_chord']
        horizontal_tail['tip_chord'] = horizontal_tail['taper_ratio']*horizontal_tail['center_chord']
        horizontal_tail['span'] = 2*horizontal_tail['area']/(horizontal_tail['tip_chord']+horizontal_tail['center_chord'])
        horizontal_tail['aspect_ratio'] = horizontal_tail['span']**2/horizontal_tail['area']
        # if "T" config a negative dihedral angle to help relaxe  lateral stability
        horizontal_tail['dihedral'] = -2
        # [�] enflechamento bordo de ataque
        horizontal_tail['sweep_leading_edge'] = 1/rad * \
            (np.arctan(np.tan(rad*horizontal_tail['sweep_c_4']) +
                       1/horizontal_tail['aspect_ratio']*(1-horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])))
        horizontal_tail['sweep_c_2'] = 1/rad*(np.arctan(np.tan(rad*horizontal_tail['sweep_c_4'])-1 /
                                         horizontal_tail['aspect_ratio']*(1-horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])))  # [�] enflechamento C/2
        # [�] enflechamento bordo de fuga
        horizontal_tail['sweep_trailing_edge'] = 1/rad * \
            (np.arctan(np.tan(rad*horizontal_tail['sweep_c_4']) -
                       3/horizontal_tail['aspect_ratio']*(1-horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])))

    # corda da ponta
    horizontal_tail['mean_geometrical_chord'] = horizontal_tail['area']/horizontal_tail['span']  # mgc
    horizontal_tail['mean_aerodynamic_chord'] = 2/3*horizontal_tail['center_chord']*(1+horizontal_tail['taper_ratio']+horizontal_tail['taper_ratio']**2) / \
        (1+horizontal_tail['taper_ratio'])  # mean aerodynamic chord
    horizontal_tail['mean_aerodynamic_chord_yposition']  = horizontal_tail['span']/6*(1+2*horizontal_tail['taper_ratio'])/(1+horizontal_tail['taper_ratio'])
    #
    ######################### HT Wetted area ######################################
    horizontal_tail['tau'] = horizontal_tail['root_chord']/horizontal_tail['tip_chord'] 
    #ht.thicknessavg = horizontal_tail['mean_chord']*0.50*(horizontal_tail['center_chord']+horizontal_tail['tip_chord'])
    horizontal_tail['wetted_area'] = 2.*horizontal_tail['area'] * \
        (1+0.25*horizontal_tail['root_chord']*(1+(horizontal_tail['tau'] * horizontal_tail['taper_ratio']))/(1+horizontal_tail['taper_ratio']))  # [m2]
    # HT aerodynamic center
    if horizontal_tail['position']  == 1:
        horizontal_tail['aerodynamic_center'] = (0.92*fuselage['length'] - horizontal_tail['center_chord'] + horizontal_tail['mean_aerodynamic_chord_yposition'] *np.tan(rad*horizontal_tail['sweep_leading_edge']) +
                     horizontal_tail['aerodynamic_center']*horizontal_tail['mean_aerodynamic_chord'])
    else:
        horizontal_tail['aerodynamic_center'] = 0.95*fuselage['length']-vertical_tail['center_chord']+vertical_tail['span'] * \
            np.tan(rad*vertical_tail['sweep_leading_edge'])+horizontal_tail['aerodynamic_center'] * \
            horizontal_tail['mean_aerodynamic_chord']+horizontal_tail['mean_aerodynamic_chord_yposition'] *np.tan(rad*horizontal_tail['sweep_leading_edge'])

    # EMPENAGEM HORIZONTAL (HORIZONTAL TAIL)
    theta, delta, sigma, T_ISA, P_ISA, rho_ISA, a = atmosphere_ISA_deviation(
        Ceiling, 0)                                 # propriedades da atmosfera
    va = a                                         # velocidade do som [m/s]
    sigma = sigma
    # velocidade de cruzeiro meta, verdadeira [m/s]
    vc = Mach*va
    # velocidade de cruzeiro meta [KEAS]
    vckeas = vc*sigma**0.5/kt2ms
    vdkeas = 1.25*vckeas
    # empenagem horizontal movel
    kh = 1.1
    prod1 = 3.81*(((horizontal_tail['area']*m22ft2)**0.2)*vdkeas)                    # termo 1
    prod2 = (1000*(np.cos(horizontal_tail['sweep_c_2']*rad)) **
             0.5)                     # termo 2
    prodf = prod1/prod2                                          # termo 3
    horizontal_tail['weight'] = 1.25*kh*(horizontal_tail['area']*m22ft2)*(prodf-0.287)

    return(vehicle)
