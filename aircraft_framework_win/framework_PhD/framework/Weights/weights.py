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
from framework.Attributes.Atmosphere.atmosphere_ISA_deviation import atmosphere_ISA_deviation
# =============================================================================
# CLASSES
# =============================================================================

# =============================================================================
# FUNCTIONS
# =============================================================================
global deg_to_rad, m2_to_ft2, kg_to_lb, lb_to_kg, m_to_ft, N_to_lbf
deg_to_rad = np.pi/180
m2_to_ft2 = 10.76
kg_to_lb = 2.205
lb_to_kg = 0.4536
m_to_ft = 3.281
kn_to_m_s = 0.5144


def wing_mass(maximum_takeoff_weight, landing_gear_position, spoilers, wing_aspect_ratio, wing_area, wing_taper_ratio, wing_sweep_c_4, mach, wing_mean_thickness, altitude):
    """
    Description: Methodology from Isikveren 2002, pag. 56, eq. 84
        - Calculates the wing mass in kg
    Inputs:
        - maximum takeoff weight [kg]
        - wing position
        - landing gear position
        - spoilers presence
        - wing aspect ratio
        - wing area [m2]
        - wing taper ration
        - wing sweep at c/4
        - mach number
        - wing mean thickness
        - altitude [ft]
    Outputs:
        - wing mass [kg]
    """
    # Assiciative constants definition
    safety_factor = 1.5
    YEIS = 2016  # Year of entry into service
    alpha_w = 0.0328
    phi_w = 0.656
    Beta_w = 1.5
    delta_w = 1.5
    epsilon_w = 1.5
    Chi_w = 1.1
    rho_sls_g = 0.125

    _, _, _, _, _, _, a = atmosphere_ISA_deviation(
        altitude, 0)

    V_MO = mach*a*kn_to_m_s  # Maximum operating speed [m/s]

    # limit load factor - Roskam, pag. 37, eq 4.23
    n_limit = 2.1 + 24000/((kg_to_lb*MTOW) + 10000)

    if n_limit <= 2.5:
        n_limit = 2.5

    # wing installation philosophy
    if wing['position'] == 1:
        k_co = 1.17
    else wing['position']:
        k_co = 1.25

    # spoilers existence correction
    if spoilers == 'True':
        k_sp = 1.02
    else:
        k_sp = 1

    # landing gear installation philosophy
    if wing['position'] == 1:
        k_lg = 1.03
    else:
        k_lg = 1.015

    n_ultimate = safety_factor*n_limit
    Pi_ATM = np.exp(2.965 - 0.001525*YEIS)
    Pi_Cw = k_co*k_sp*k_lg
    Pi_tc = 16.5*np.sin(2*np.pi*wing_mean_thickness)

    tau_s = 1 + 1.31*(((0.5*rho_sls_g*V_MO**2)/(1000))**2) * \
        (1/n_ultimate**3)  # structural stiffness

    aux1 = Pi_ATM*alpha_w*Pi_Cw
    aux2 = maximum_takeoff_weight*n_ultimate*wing_area*(wing_aspect_ratio**Beta_w) * \
        (Chi_w + wing_taper_ratio/2)*(tau_s**delta_w)
    aux3 = Pi_tc*np.cos(wing_sweep_c_4*deg_to_rad)**phi_w

    return aux1*(aux2/aux3)**phi_w


def horizontal_tail_mass(V_dive, horizontal_tail_sweep_c_2):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 74, eq. 5.19
        - Calculates the horizontal tail mass in lb, but the result is converted to kg
    Inputs:
        - dive speed [ktas]
        - horizontal tail area [m2]
        - horizontal tail sweep c/2 [deg]
    Outputs:
        - horizontal tail mass [kg]
    TODO's:
        - 
    """

    fin = 'trimmable'  # This should be an input in the future

    fin = 'trimmable'
    if fin == 'trimmable':
        k_h = 1.1
    elif fin == 'fixed':
        k_h = 1

    aux_1 = (3.18*(horizontal_tail['area']*m2_to_ft2)**0.2)*V_dive
    aux_2 = 1000*np.sqrt(np.cos(horizontal_tail_sweep_c_2*deg_to_rad))
    return (k_h*horizontal_tail['area']*((aux_1/aux_2) - 0.287))*lb_to_kg


def vertical_tail_mass(V_dive, z_H, vertical_tail_span, vertical_tail_sweep_c_2):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 74, eq. 5.20
        - Calculates the vertical tail mass in lb, but the result is converted to kg
    Inputs:
        - dive speed [keas]
        - horizontal tail area [m2]
        - z distance horizontal tail [m]
        - vertical tail area [m2]
        - vertical tail span [m]
        - vertical tail sweep c/2 [deg]
    Outputs:
        - vertical tail mass [kg]
    TODO's:
        - 
    """

    horizontal_tail['position']  = "fuselage"

    if horizontal_tail['position']  == "fuselage":
        k_v = 1
    if horizontal_tail['position']  == "fin":
        z_h = 0.95
        k_v = 1 + 0.15*(((horizontal_tail['area']*m2_to_ft2)*z_h) /
                        ((vertical_tail['area']*m2_to_ft2)*(vertical_tail_span*m_to_ft)))

    aux_1 = (3.81*((vertical_tail['area']*m2_to_ft2)**0.2))*V_dive
    aux_2 = 1000*np.sqrt(np.cos(vertical_tail_sweep_c_2*deg_to_rad))
    return (k_v*vertical_tail['area']*((aux_1/aux_2) - 0.287))*lb_to_kg


def fuselage_mass(V_dive,
                  vehicle,
                  wing_aerodynamic_center_xposition):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 77, eq. 5.27
        - Calculates the fuselage mass in lb, but the result is converted to kg
    Inputs:
        - V dive [keas]
        - fuselage width [m]
        - fuselage height [m]
        - fuselage length [m]
        - fuselage wetted area [m2]
        - engine position
        - horizontal_tail_center_chord [m]
        - horizontal_tail_mean_aerodynamic_chord_yposition [m]
        - horizontal_tail_sweep_leading_edge [deg]
        - horizontal_tail_mean_aerodynamic_chord [m]
        - vertical_tail_center_chord [m]
        - vertical_tail_span [m]
        - vertical_tail_sweep_leading_edge [deg]
        - wing_aerodynamic_center_xposition [m]


    Outputs:
        - fuselage mass [kg]
    TODO's:
        - 
    """

    fuselage_configuration = "pressurized"

    if fuselage_configuration == "pressurized":
        k_f = 1.08
    elif fuselage_configuration == "maing_gear_attached":
        k_f = 1.07
    elif fuselage_configuration == "cargo":
        k_f = 1.10

    if engine['position'] == 2 or engine['position'] == 3:
        k_e = 1.04
    else:
        k_e = 1.0

    if horizontal_tail['position']  == 1:
        horizontal_tail_aerodynamic_center_xposition = 0.98*fuselage['length'] - horizontal_tail_center_chord + \
            horizontal_tail_mean_aerodynamic_chord_yposition * \
            np.tan(horizontal_tail_sweep_leading_edge*deg_to_rad) + \
            0.25*horizontal_tail_mean_aerodynamic_chord
    else:
        horizontal_tail_aerodynamic_center_xposition = 0.98*fuselage['length'] - vertical_tail_center_chord + vertical_tail_span * \
            np.tan(vertical_tail_sweep_leading_edge*deg_to_rad) + 0.25*horizontal_tail_mean_aerodynamic_chord + \
            horizontal_tail_mean_aerodynamic_chord_yposition * \
            np.tan(horizontal_tail_sweep_leading_edge*deg_to_rad)

    # arm between wing aerodynamic center an hotizontal tail aerodynamic center
    l_h = horizontal_tail_aerodynamic_center_xposition - \
        wing_aerodynamic_center_xposition

    return (0.021*k_f*k_e*np.sqrt(V_dive*(l_h/(fuselage_height+fuselage['width'])))*(fuselage['wetted_area']*m2_to_ft2)**1.2)*lb_to_kg


def nacelle_mass(engine_fan_diameter, engine, engine_compressor_maximum_static_pressure):
    """
    Description: Methodology from Roskam-GD, pag. 79, eq. 5.35
        - Calculates the nacelle mass in lb, but the result is converted to kg
    Inputs:
        - engine fan diameter [m]
        - engines number
        - engine length [m]
        - engine maximum static pressure at compressor [pascal???]
    Outputs:
        - nacelle mass [kg]
    TODO's:
        - Check dimensions
    """
    engine_inlet_area = (np.pi*engine_fan_diameter**2)/4
    return (7.435*aircraft['number_of_engines'] *(((engine_inlet_area*m2_to_ft2)**0.5)*(engine['length']*m_to_ft)*engine_compressor_maximum_static_pressure)**0.731)*lb_to_kg


def main_landig_gear_mass(maximum_takeoff_weight):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 82, eq. 5.42
        - Calculates the main landing gear mass in lb, but the result is converted to kg
    Inputs:
        - maximum_takeoff_weight [kg]
    Outputs:
        - main landing gear mass [kg]
    TODO's:
        -
    """

    if wing['position'] == 1:
        k_lg = 1
    else:
        k_lg = 1.08

    A_lg = 40
    B_lg = 0.16
    C_lg = 0.019
    D_lg = 1.5E-5

    return (k_lg*(A_lg + B_lg*(maximum_takeoff_weight*kg_to_lb)**(3/4) + C_lg*(maximum_takeoff_weight*kg_to_lb) + D_lg*(maximum_takeoff_weight*kg_to_lb)**(3/2)))*lb_to_kg


def nose_landig_gear_mass(maximum_takeoff_weight):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 82, eq. 5.42
        - Calculates the nose landing gear mass in lb, but the result is converted to kg
    Inputs:
        - maximum_takeoff_weight [kg]
    Outputs:
        - nose landing gear mass [kg]
    TODO's:
        -
    """
    if wing['position'] == 1:
        k_lg = 1
    else:
        k_lg = 1.08

    A_lg = 20
    B_lg = 0.1
    C_lg = 0.0
    D_lg = 2E-6

    return k_lg*(A_lg + B_lg*(maximum_takeoff_weight*kg_to_lb)**(3/4) + C_lg*(maximum_takeoff_weight*kg_to_lb) + D_lg*(maximum_takeoff_weight*kg_to_lb)**(3/2))


def engine_mass(engine_static_thrust):
    '''
    Methodology from 
    Inputs:
        - engine static thrust [N]
        - engines number 
    Outputs:
        - engine mass [kg]
    TODO's:
        -
    '''
    return aircraft['number_of_engines'] *(0.084 * ((engine_static_thrust*N_to_lbf)**1.1)*np.exp(-0.045))*lb_to_kg


def fuel_system_mass(wing_fuel_capacity, range_distace):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 92, eq. 6.24
        - Calculates the fuel system mass in lb, but the result is converted to kg
    Inputs:
        - wing fuel capacity [kg]
        - engines number
        - range distace [nm]
    Outputs:
        -
    TODO's:
        -
    """
    fuel_type = 3

    if fuel_type == 1:
        k_fsp = 5.870
    elif fuel_type == 2:
        k_fsp = 6.550
    elif fuel_type == 3:
        k_fsp = 6.710

    tanks_number = 3

    if range_distance > 2000 or aircraft['number_of_engines']  > 2:
        tanks_number = 6

    return (80*(aircraft['number_of_engines']  + tanks_number - 1) + 15*(tanks_number**0.5) * ((wing_fuel_capacity*kg_to_lb)/k_fsp)**0.333)*lb_to_kg


def propulsion_system_mass(vehicle, engine_mass):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 93, eq. 6.28 - 6.41
        - Calculates the nose landing gear mass in lb, but the result is converted to kg
    Inputs:
        - engines number
        - engine position
        - fuselage length [m]
        - wing span [m]
        - engine mass [kg] 
    Outputs:
        -
    TODO's:
        - In Prof. Bento code the summatory multiplies the number of engines. Ask if that is right, 
        because engines number is considered in the equations.
    """

    engine_afterburning_presence = 0
    if engine_afterburning_presence == 1:
        k_ec = 1.080
    elif engine_afterburning_presence == 0:
        k_ec = 0.686

    if engine['position'] == 2 or engine['position'] == 3:
        engine_controls = k_ec * \
            ((fuselage['length']*m_to_ft)*aircraft['number_of_engines'] )**0.792
    else:
        engine_controls = 88.46 * \
            (((fuselage['length'] + wing['span'])*m_to_ft)*(aircraft['number_of_engines'] /100))**0.294

    engine_starting_system = 38.93*((engine_mass*kg_to_lb)/1000)**0.918

    engine_reverser_presence = 0

    if engine_reverser_presence == 0:
        engine_reverser = 0
    else:
        engine_reverser = 0.18*engine_mass*kg_to_lb

    return (engine_controls + engine_starting_system + engine_reverser)*lb_to_kg


def flight_control_system_mass(maximum_takeoff_weight):
    """
    Description: Methodology from Roskam-Torenbeek, pag. 82, eq. 5.42
        - Calculates the nose landing gear mass in lb, but the result is converted to kg
    Inputs:
        - maximum takeoff weight
    Outputs:
        - flight control syste mass
    TODO's:
        -
    """
    powered_flight_controls = 1

    if powered_flight_controls == 0:
        k_fc = 0.44
    else:
        k_fc = 0.64

    k_le = 1.2

    return (k_fc*k_le*(maximum_takeoff_weight*kg_to_lb)**(2/3))*lb_to_kg


def fixed_equipment_mass(vehicle, l_h, maximum_takeoff_weight, fuel_weight):
    """
    Description: Methodology from Raymer, pag. 459, eq. 15.25 - 15.45 and Roskam-Torenbeek, pag. 105, eq. 7.31 - 7.45
        - Calculates the fixed equipment mass in lb, but the result is converted to kg
    Inputs:
        - fuselage lenght [m]
        - fuselage_cabine_lenght [m]
        - wing span [m]
        - wing area [m2]
        - engine position
        - engines number
        - lh - distance between wing and tail ac [m]
        - pax_number
        - maximum_takeoff_weight [kg]
        - fuel weight [kg]
    Outputs:
        -
    TODO's:
        -
    """
    # Hydraulic system
    number_of_functions_performed_by_controls = 7
    hydraulic_system_mass = (0.2673*number_of_functions_performed_by_controls *
                             ((fuselage['length'] + wing['span'])*m_to_ft)**0.937)

    # Electrical system
    system_electrical_rating = 60  # [kV]

    if engine['position'] == 1 or engine['position'] == 4:
        electrical_routing_distance = fuselage['length']*m_to_ft
    else:
        electrical_routing_distance = (fuselage['length'] - l_h)*m_to_ft

    electrical_system_mass = 7.291*system_electrical_rating**0.782 * \
        electrical_routing_distance**0.346 * aircraft['number_of_engines'] **0.1

    # Avionics
    uninstalled_avionics_mass = 1200
    avionics_mass = 1.73*(uninstalled_avionics_mass**0.983)

    # Air ice pressure
    air_ice_pressure_system_mass = 6.75 * \
        ((fuselage_cabine_lenght*m_to_ft)**1.28)

    # Oxygen system
    oxygen_system_mass = 30 + 1.2*pax_number

    # APU
    APU_mass = 0.0085*maximum_takeoff_weight*kg_to_lb

    # Furnishing
    furnishing_mass = 0.211 * \
        ((maximum_takeoff_weight - fuel_weight)*kg_to_lb)**0.91

    # Paint
    paint_mass = 0.0045*maximum_takeoff_weight*kg_to_lb

    # Safety equipment - pag 141 Jenkinson
    if range_distace > 2000:
        value = 3.4
    else:
        value = 0.9

    safety_equipment_mass = 0.0003*maximum_takeoff_weight*kg_to_lb

    # Handling gear
    handling_gear_mass = 3.0E-4 * maximum_takeoff_weight*kg_to_lb

    # Slats
    aircraft['slat_presence'] = 1
    if aircraft['slat_presence'] == 1:
        if engine['position'] == 2:
            slats_span = 0.8
        else:
            slats_span = 0.7

        slats_area = slats_span*0.15*(wing_area*m2_to_ft2)
        slats_mass = 3.53*(slats_area**0.82)
    else:
        slats_mass = 0

    return (hydraulic_system_mass + electrical_system_mass + avionics_mass + air_ice_pressure_system_mass + oxygen_system_mass + APU_mass + furnishing_mass + paint_mass + safety_equipment_mass + handling_gear_mass + slats_mass)*lb_to_kg


def aircraft_empty_weight():
    """
    Description: Methodology from Raymer, pag. 459, eq. 15.25 - 15.45 and Roskam-Torenbeek, pag. 105, eq. 7.31 - 7.45
        - Calculates the fixed equipment mass in lb, but the result is converted to kg
    Inputs:
        -
    Outputs:
        -
    TODO's:
        -
    """

    # Structural weight
    wing = wing_mass(maximum_takeoff_weight, landing_gear_position, spoilers,
                     wing_aspect_ratio, wing_area, wing_taper_ratio, wing_sweep_c_4, mach, wing_mean_thickness, altitude)
    horizontal_tail = horizontal_tail_mass(
        V_dive, horizontal_tail_sweep_c_2)
    vertical_tail = vertical_tail_mass(
        V_dive, z_H, vertical_tail_span, vertical_tail_sweep_c_2)
    fuselage = fuselage_mass(V_dive,
                             vehicle,
                             wing_aerodynamic_center_xposition)
    nacelle = nacelle_mass(engine_fan_diameter,
                           engine, engine_compressor_maximum_static_pressure)
    main_landig_gear = main_landig_gear_mass(maximum_takeoff_weight)
    nose_landig_gear = nose_landig_gear_mass(maximum_takeoff_weight)

    structural_weight = wing + horizontal_tail + vertical_tail + \
        fuselage + nacelle + main_landig_gear + nose_landig_gear

    # Power plant weight
    engines = engine_mass(engine_static_thrust)
    fuel_system = fuel_system_mass(
        wing_fuel_capacity, range_distace)
    propusion_system = propulsion_system_mass(
        vehicle, engine_mass)

    power_plant_weight = engines + fuel_system + propusion_system

    # Fixed equionet weight
    flight_control_system = flight_control_system_mass(maximum_takeoff_weight)
    fixed_equipment = fixed_equipment_mass(fuselage, fuselage_cabine_lenght, wing_area, engine['position'], l_h, maximum_takeoff_weight, fuel_weight)
    fixed_equipment_weight = flight_control_system + fixed_equipment

    return structural_weight + power_plant_weight + fixed_equipment_weight


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
