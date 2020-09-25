"""
Function  : engine_performance.py
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
    - Change all comments
    - Replace by function from Mattingly

"""
########################################################################################
"IMPORTS"
########################################################################################
import numpy as np
from framework.Attributes.Atmosphere.atmosphere import atmosphere
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def turbofan(h,mach,fan_compressor_ratio,compressor_pressure_ratio,bypass_ratio,throttle_position,fan_diameter,turbine_inlet_temperature):

    # ----- MOTOR DATA INPUT --------------------------------------------------
    fan_disk_area = np.pi*(fan_diameter**2)/4
    compressor_compression_rate = compressor_pressure_ratio/fan_compressor_ratio  # taxa de compressão fornecida pelo compressor
    combustor_compression_ratio = 0.99     # razão de pressão do combustor
    inlet_turbine_temperature = turbine_inlet_temperature     # temperatura na entrada da turbina
    inlet_turbine_temperature_takeoff = turbine_inlet_temperature # at takeoff 10# increase in turbine temperatute for 5 min
    thermal_energy = 43260000   # Poder calorífico (J/kg) 

    # ----- DESIGN POINT ------------------------------------------------------

    desing_mach=0
    design_altitude = 0      
    design_throttle_position = 1.0

    # ------ EFICIÊNCIAS ------------------------------------------------------

    inlet_efficiency = 0.98
    compressor_efficiency = 0.85
    combustion_chamber_efficiency = 0.99
    turbine_efficiency = 0.90
    nozzle_efficiency = 0.98
    fan_efficiency = 0.97

    # Atualizado tabela acima em setembro de 2013 de acordo com as anotacoes
    # de aula do Ney
    # ------ TEMPERATURE RATIOS -----------------------------------------------
    temperature_ratio = 1

    # #########################################################################
    # #########  G E T  T H E R M O - DESIGN MODE #############################

    # ------ PRESSURE RATIOS --------------------------------------------------

    inlet_pressure_ratio = inlet_efficiency
    compressor_pressure_ratio = compressor_compression_rate
    combustor_pressure_ratio = combustor_compression_ratio
    fan_pressure_ratio = fan_pressure_ratio


    # ------ FREE STREAM ------------------------------------------------------
    gamma = 1.4                             # gamma do programa
    R = 287.2933                           # R do programa
    [T_0,P_0] = atmosphere(design_altitude)
    T0_0 = (1 + (gamma-1)/2*design_mach^2)*T_0     # temperatura total
    P0_0 = P_0*(T0_0/T_0)^(gamma/(gamma-1))  # pressão total
    a0 = np.sqrt(gamma*R*T_0)                  # velocidade do som
    u0 = design_mach*a0                           # velocidade de vôo

    # ------ TEMPERATURE RATIOS -----------------------------------------------
        # ----- ENTRADA DE AR -----------------------------------------------------
    P0_1 = P0_0
    T0_1 = T0_0

    # ----- INLET -------------------------------------------------------------
    T0_2 = T0_1
    P0_2 = P0_1*inlet_pressure_ratio
    # ----- FAN ---------------------------------------------------------------
    gamma2 = engine_getgamma(T0_2)
    cp2 = engine_getcp(T0_2)
    del_h_fan = cp2*T0_2/eta(13)*((prat(13))^((gamma2-1)/gamma2)-1)
    del_t_fan = del_h_fan/cp2
    T0_13 = T0_2 + del_t_fan
    P0_13 = P0_2 * prat(13)
    trat(13) = T0_13 / T0_2

    # ----- COMPRESSOR --------------------------------------------------------
    gamma13 = engine_getgamma(T0_13)
    cp13 = engine_getcp(T0_13)
    del_h_c = cp13*T0_13/eta(3)*(prat(3)^((gamma13-1)/gamma13)-1)
    del_t_c = del_h_c/cp13
    T0_3 = T0_13 + del_t_c
    P0_3 = P0_13 * prat(3)
    trat(3) = T0_3 / T0_13
    cp3 = engine_getcp(T0_3)

    # ----- COMBUSTOR ---------------------------------------------------------
    T0_4 = manete * tt4takeoff    # ponto de projeto
    P0_4 = P0_3 * prat(4)
    trat(4) = T0_4 / T0_3

    # ----- HIGHT TURBINE -----------------------------------------------------
    gamma4 = engine_getgamma(T0_4)
    cp4 = engine_getcp(T0_4)
    del_h_ht = del_h_c
    del_t_ht = del_h_ht / cp4

    T0_5 = T0_4 - del_t_ht
    prat(5) = (1-del_h_ht/(cp4*T0_4*eta(5)))^(gamma4/(gamma4-1))
    P0_5 = P0_4 * prat(5)
    trat(5) = T0_5 / T0_4

    # ----- LOWER TURBINE -----------------------------------------------------
    gamma5 = engine_getgamma(T0_5)
    cp5 = engine_getcp(T0_5)
    del_h_lt = (1 + bpr)*del_h_fan
    del_t_lt = del_h_lt / cp5

    T0_15 = T0_5 - del_t_lt
    prat(15) = (1-del_h_lt/(cp5*T0_5*eta(5)))^(gamma5/(gamma5-1))
    P0_15 = P0_5 * prat(15)
    trat(15) = T0_15 / T0_5

    epr = prat(2)*prat(3)*prat(4)*prat(5)*prat(13)*prat(15)
    etr = trat(2)*trat(3)*trat(4)*trat(5)*trat(13)*trat(15)
    # #########################################################################


    # ########### G E T    G E O M E T R Y  ###################################
    acore = afan/(bpr+1)                   # área do núcleo

    #  ---- a8rat = a8 / acore ---- 
    a8rat = min(0.75*sqrt(etr/trat(2))/epr*prat(2),1.0)   
    # OBS: divide por prat(2) pois ele não é considerado no cálculo do EPR e
    # ETR acima no applet original

    a8 = a8rat * acore
    a4 = a8 * prat(5)*prat(15)/sqrt(trat(5)*trat(15))
    a4p = a8 * prat(15)/sqrt(trat(15))
    a8d = a8

    if ((Mach==Machd) && (Alt==Altd) && (manete==maneted))
        designpoint = 1
    else
        designpoint = 0
    end

    if ~designpoint
        # #########################################################################
        # #########  G E T  T H E R M O - WIND TUNNEL TEST ########################
        # disp('passei aqui designpoint')
        Mach = Machd
        manete = maneted

        # ------ FREE STREAM ------------------------------------------------------
        gamma = 1.4                             # gamma do programa
        R = 287.2933                           # R do programa
        [T_0,P_0] = atmosfera2(Altd)

        T0_0 = (1 + (gamma-1)/2*Mach^2)*T_0     # temperatura total
        P0_0 = P_0*(T0_0/T_0)^(gamma/(gamma-1))  # pressão total
        a0 = sqrt(gamma*R*T_0)                  # velocidade do som
        u0 = Mach*a0                           # velocidade de vôo

        # ----- ENTRADA DE AR -----------------------------------------------------
        P0_1 = P0_0
        T0_1 = T0_0

        # ----- INLET -------------------------------------------------------------
        T0_2 = T0_1
        P0_2 = P0_1*prat(2)

        # ----- COMBUSTOR ---------------------------------------------------------
        T0_4 = manete*tt4
        gamma4 = engine_getgamma(T0_4)
        cp4 = engine_getcp(T0_4)

        # ----- HIGHT TURBINE -----------------------------------------------------
        trat(5) = fzero(@(x) engine_achatrat(x,a4p/a4,eta(5),-gamma4/(gamma4-1)),1.0)

        T0_5 = T0_4*trat(5)
        gamma5 = engine_getgamma(T0_5)
        cp5 = engine_getcp(T0_5)
        del_t_ht = T0_5 - T0_4
        del_h_ht = del_t_ht*cp4
        prat(5) = (1-(1-trat(5))/eta(5))^(gamma4/(gamma4-1))

        # ----- LOWER TURBINE -----------------------------------------------------
        trat(15) = fzero(@(x) engine_achatrat(x,a8d/a4p,eta(5),-gamma5/(gamma5-1)),1.0)

        T0_15 = T0_5 * trat(15)
        gamma15 = engine_getgamma(T0_15)
        cp15 = engine_getcp(T0_15)
        del_t_lt = T0_15 - T0_5
        del_h_lt = del_t_lt*cp5
        prat(15) = (1-(1-trat(15))/eta(5))^(gamma5/(gamma5-1))

        # ----- FAN ---------------------------------------------------------------
        del_h_fan = del_h_lt / (1+bpr)
        del_t_fan = -del_h_fan / cp2
        T0_13 = T0_2 + del_t_fan
        gamma13 = engine_getgamma(T0_13)
        cp13 = engine_getcp(T0_13)

        trat(13) = T0_13 / T0_2
        prat(13) = (1-(1-trat(13))*eta(13))^(gamma2/(gamma2-1))

        # ----- COMPRESSOR --------------------------------------------------------
        del_h_c = del_h_ht
        del_t_c = -del_h_c / cp13

        T0_3 = T0_13 + del_t_c
        gamma3 = engine_getgamma(T0_3)
        cp3 = engine_getcp(T0_3)
        trat(3) = T0_3 / T0_13
        prat(3) = (1-(1-trat(3))*eta(3))^(gamma13/(gamma13-1))
        trat(4) = T0_4 / T0_3


        # ----- total pressures definition ----------------------------------------
        P0_13 = P0_2 * prat(13)
        P0_3 = P0_13 * prat(3)
        P0_4 = P0_3 * prat(4)
        P0_5 = P0_4 * prat(5)
        P0_15 = P0_5 * prat(15)

        # ----- overall pressure & temperature ratios -----------------------------
        epr = prat(2)*prat(3)*prat(4)*prat(5)*prat(13)*prat(15)
        etr = trat(2)*trat(3)*trat(4)*trat(5)*trat(13)*trat(15)

    end

    # ########### G E T   P E R F O R M A N C E  ##############################
    gammae = engine_getgamma(T0_5)                 # gamma de saída (T0_5 ???)
    Re = (gammae-1)/gammae*engine_getcp(T0_5)       # Constante R de saída
    g = 32.2

    P0_8 = P0_0 * epr                      
    T0_8 = T0_0 * etr

    fact2 = -0.5*(gammae+1)/(gammae-1)
    fact1 = (1 + 0.5*(gammae-1))^fact2
    mdot = a8*sqrt(gammae)*P0_8*fact1/sqrt(T0_8*Re) # fluxo mássico [kg/s]

    npr = max(P0_8 / P_0,1)

    fact1 = (gammae-1)/gammae
    uexit = sqrt(2*R/(gammae-1)*gammae*T0_8*eta(7)*(1-(1/npr)^fact1)) # ????

    if (npr<=1.893)
        pexit = P_0
    else
        pexit = 0.52828*P0_8
    end

    fgros = uexit + (pexit-P_0)*a8/mdot/g

    # ------ contribuição do fan -------------------------------------------
    snpr = P0_13 / P_0
    fact1 = (gamma-1)/gamma
    ues = sqrt(2*R/fact1*T0_13*eta(7)*(1-1/snpr^fact1))

    if (snpr<=1.893)
        pfexit = P_0
    else
        pfexit = 0.52828*P0_13
    end

    fgros = fgros + bpr*ues + (pfexit-P_0)*bpr*acore/mdot/g

    dram = u0*(1+bpr)
    fnet = fgros - dram
    fuel_air = (trat(4)-1)/(eta(4)*PC/(cp3*T0_3)-T0_4/T0_3)

    # ####### Estimativa de Peso ##############################################
    ncomp = min(15,round(1+prc/1.5))
    nturb = 2 + floor(ncomp/4)
    dfan = 293.02          # fan density
    dcomp = 293.02         # comp density
    dburn = 515.2          # burner density
    dturb = 515.2          # turbine density
    conv1 = 10.7639104167  # conversão de acore para ft^2

    weight = 4.4552*0.0932*acore*conv1*sqrt(acore*conv1/6.965)*...
        ((1+bpr)*dfan*4 + dcomp*(ncomp-3) + 3*dburn + dturb*nturb) #[N]

    # ###### SUBROUTINE OUTPUTS ###############################################
    #weightkgf = weight/9.8
    #tracaokgf = fnet*mdot/9.8  #[kgf]
    tracaonewt = fnet*mdot #[tracao em Newtons]
    FF = 1.15*fuel_air*mdot*3600  #[kg/h]   # correção de 15# baseado em dados de motores reais


    return force,fuel_flow
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################