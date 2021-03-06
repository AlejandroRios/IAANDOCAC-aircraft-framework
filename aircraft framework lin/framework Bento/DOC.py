"""" 
Title     : DOC function
Written by: Alejandro Rios
Date      : 30/10/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
Time block
Cons_block
weitght_empty_kg
Rangenm
T0
NEng
weitght_engine_kg
MTOW

Outputs:
DOC
"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from crew_salary import crew_salary
########################################################################################
class structtype():
    pass

salary = structtype()
var = structtype()
########################################################################################
"""Constants declaration"""
########################################################################################
def DOC(TBO,Time_Block, Cons_Block, weight_empty_kg,Rangenm,
    T0,NEng,weight_engine_kg,MTOW):

    ## Constants
    kg2lb       = 2.20462262
    ##
    # ********** Example of airplane (input) data
    #Time_Block       = 120
    #Cons_Block       = 6500
    var.Range        = Rangenm
    # salary.Captain      = 85000
    # salary.FO           = 50000
    salary.Captain,salary.FO,_=crew_salary(MTOW)
    # weight_empty_kg  = 22000
    #MTOW             = 37500
    #T0               = 14200 
    TBO              = 2500
    Fuel_price       = 2.387


    ########################################################################################
    """Mission Data"""
    ########################################################################################

    tbl         = Time_Block/60 # [HRS] BLOCK TIME EQ 5.6
    Block_Range = var.Range # [NM] BLOCK RANGE
    vbl         = Block_Range / tbl # [KTS]BLOCK SPEED EQ 5.5
    Uannbl      = 1e3 * (3.4546 * tbl + 2.994 - (12.289 * (tbl**2) - 5.6626 * (tbl) + 8.964)**(1/2)) # [HRS] ANNUAL UTILIZATION

    #==============================#
    #            DOC PAG 146       #
    #==============================#

    #==============================#
    #            DOC FLT           #
    #==============================#

    #1) CREW COST -> Ccrew
    nc1     = 1 # NUMBER OF CAPTAIN
    nc2     = 1 # NUMBER OF FIRST OFFICER
    kj      = 0.26 # FACTOR WHICH ACCOUNTS FOR VACATION PAY, COST TRAINING ...
    # THESE DATA ARE ASSUMED TO BE APPLICABLE FOR 1990
    SAL1    = salary.Captain # SALARY CAPTAIN [USD/YR] 
    SAL2    = salary.FO # SALARY FIRST OFFICER [USD/YR]
    AH1     = 800 # [HRS]
    AH2     = 800 # [HRS]
    TEF1    = 7 # [USD/blhr]
    TEF2    = TEF1 #TRAVEL EXPENSE FACTOR
    Ccrew   = (nc1 *((1 + kj)/vbl) * (SAL1/AH1) + (TEF1/vbl)) + (nc2 *((1 + kj)/vbl) * (SAL2/AH2) + (TEF2/vbl)) # [USD/NM] EQ 5.21 PAG 109 

    #2) FUEL AND OIL COST -> Cpol (PAG 148)
    pfuel   = Fuel_price # PRICE [USD/GALLON]
    dfuel   = 6.74 # DENSITY [LBS/GALLON]
    Wfbl    = Cons_Block*kg2lb # [LBS] OPERATIONAL MISSION FUEL
    Cpol    = 1.05 * (Wfbl / Block_Range) * (pfuel / dfuel) # EQ 5.30 PAG 116 5# DO DOC

    #3) INSURANCE COST -> Cins (PAG 148)
    # Cins = 0.02 * (DOC) # EQ 5.32 * PAG 117
    Cins = 0

    DOCflt    = Ccrew + Cpol + Cins

    #==============================#
    #            DOC MAINT         #
    #==============================#

    fnrev       = 1.03 # NON-REVENUE FACTOR. IT ACCOUNTS FOR EXTRA MAINTENANCE COSTS INCURRED DUE FLIGHT DELAYS 

    #1) MAINTENANCE LABOR COST FOR AIRFRAME AND SYSTEMS -> Clab_ap (PAG 148)
    weight_empty_lb  = weight_empty_kg*kg2lb
    weight_engine_lb = weight_engine_kg*kg2lb
    Wa          = weight_empty_lb - NEng*weight_engine_lb # [LBS] AIRFRAME WEIGHT
    MHRmap_bl   = 3 * 0.067 * Wa /1000 # [mhrs/blhr] FIGURE 5.5 PAG 122
    Rlap        = 16 # [USD/mhr] RATE PER MANHOUR
    Clab_ap     = fnrev * MHRmap_bl * Rlap / vbl # [USD/NM] EQ 5.34 PAG 119

    #2) MAINTENANCE LABOR COST FOR ENGINES -> Clab_eng  (PAG 149)
    # BPR = razao de passagem
    #
    Tto         = NEng*T0  # lbf
    Tto_Ne      = Tto / NEng # [LBS] TAKE-OFF THRUST PER ENGINE
    Hem         = TBO # [HRS] OVERHAUL PERIOD
    Rleng       = Rlap
    MHRmeng_bl  = ((0.718 + 0.0317 * (Tto_Ne/1000)) * (1100/Hem) + 0.1) # [mhrs/blhr] FIGURE 5.6 PAG 123
    Clab_eng    = fnrev * 1.3 * NEng * MHRmeng_bl * Rleng / vbl # [USD/NM] EQ 5.36 PAG 120

    #3) MAINTANENCE MATERIALS COST FOR AIRPLANE -> Cmat_ap (PAG 150)
    # ENGINE PRICE
    CEF         = (3.10/3.02) #FATOR DE CORRECAO DO PRECO
    EP1989      = (10**(2.3044 + 0.8858 * (np.log10(Tto_Ne)))) # [USD] PAG 65 APPENDIX B4 EQ B10 PAG 351
    EP          = CEF * EP1989 #[1992]
    # AIRPLANE PRICE
    AEP1989     = (10**(3.3191 + 0.8043 * (np.log10(MTOW * kg2lb)))) # [USD] PAG 89 APPENDIX A9 EQ A12 PAG 331
    AEP         = CEF * AEP1989 #[1992]
    # AIRFRAME PRICE
    AFP         = AEP - NEng * (EP) # [USD]

    if MTOW * kg2lb >= 10000: # FIGURE 5.8 PAG 126
        ATF = 1.0
    elif MTOW * kg2lb < 10000 and MTOW * kg2lb < 5000:
        ATF = 0.5
    else:
        ATF = 0.25


    CEFy        = 1.0 # PAG 150
    Cmat_apbhr  = 30 * CEFy * ATF + 0.79*1e-5 * AFP # PAG 150 FIGURE 5.8 PAG 126 
    Cmat_ap     = fnrev * Cmat_apbhr / vbl #[USD/NM] EQ 5.37 PAG 120 

    #4) MAINTANENCE MATERIALS COST FOR ENGINE -> Cmat_eng (PAG 150)
    KHem            = 0.021 * (Hem/100) + 0.769 # FIGURE 5.11 PAG 129
    ESPPF           = 1.5 # ENGINE SPARE PARTS PRICE PAG 133
    Cmat_engblhr    = (5.43*1e-5 * EP * ESPPF - 0.47)/KHem # FIGURE 5.9 PAG 127
    Cmat_eng        = fnrev * 1.3 * NEng * Cmat_engblhr / vbl # [USD/NM] EQ 5.38 PAG 125

    #5) APPLIED MAINTENANCE BURDEN COST -> Camb (PAG 151)
    famb_lab    = 1.2  # OVERHEAD DISTRIBUTION FACTOR LABOUR COST PAG 129 -> MIDDLE VALUE
    famb_mat    = 0.55 # OVERHEAD DISTRIBUTION FACTOR MATERIAL COST PAG 129 -> MIDDLE VALUE
    Camb        = fnrev * (famb_lab * (MHRmap_bl * Rlap + NEng * MHRmeng_bl * Rleng) +
                famb_mat * (Cmat_apbhr + NEng * Cmat_engblhr)) / vbl # [USD/NM] EQ 5.39 PAG 125
            
    # TOTAL MAINTENANCE COST
    DOCmaint    = Clab_ap + Clab_eng + Cmat_ap + Cmat_eng + Camb # [USD/NM] PAG 151

    #==============================#
    #       DOC DEPRECIATION       #
    #==============================#
    # (PAG 130)
    # 1) AIRPLANE DEPRECIATION COST -> Cdap (PAG 151)
    fdap        = 0.85 # AIRFRAME DEPRECIATION FACTOR TABELA 5.7 PAG 134 
    DPap        = 10 # AIRPLANE DEPRECIATION PERIOD TABELA 5.7 PAG 134
    ASP         = 2670000 # [USD] PAG 151 AVIONICS SYSTEM PRICE APPENDIX C THE SAME VALUE WHICH WAS USED IN THE EXAMPLE
    Cdap        = fdap * (AEP - NEng * EP - ASP)/ (DPap * Uannbl * vbl) # [USD/NM] EQ 5.41 PAG 130

    #2) ENGINE DEPRECIATION FACTOR -> Cdeng (PAG 152)
    fdeng       = 0.85 # ENGINE DEPRECIATION FACTOR TABELA 5.7 PAG 134
    DPeng       = 7 # ENGINE DEPRECIATION PERIOD TABELA 5.7 PAG 134
    Cdeng       = fdeng * NEng * EP / (DPeng * Uannbl * vbl) # [USD/NM] EQ 5.42 PAG 131

    #3) AVIONICS DEPRECIATION FACTOR -> Cdav (PAG 152)
    fdav        = 1.0 # AVIONICS DEPRECIATION FACTOR TABELA 5.7 PAG 134
    DPav        = 5.0 # AVIONICS DEPRECIATION PERIOD TABELA 5.7 PAG 134
    Cdav        = fdav * ASP / (DPav * Uannbl * vbl) # [USD/NM] EQ 5.44 PAG 131

    #4) AIRPLANE SPARE PARTS DEPRECIATION FACTOR -> Cdapsp (PAG 152)
    fdapsp      = 0.85 # AIRPLANE SPARE PARTS DEPRECIATION FACTOR TABELA 5.7 PAG 134
    fapsp       = 0.1 # AIRPLANE SPARE PARTS FACTOR PAG 132
    DPapsp      = 10 # AIRPLANE SPARE PARTS DEPRECIATION PERIOD TABELA 5.7 PAG 134
    Cdapsp      = fdapsp * fapsp * (AEP - NEng * EP) / (DPapsp * Uannbl * vbl) # [USD/NM] EQ 5.45 PAG 132

    #5) ENGINE SPARE PARTS DEPRECIATION FACTOR -> Cdengsp (PAG 153)
    fdengsp     = 0.85 # ENGINE SPARE PARTS DEPRECIATION FACTOR TABELA 5.7 PAG 134
    fengsp      = 0.5 # ENGINE SPARE PARTS FACTOR PAG 133
    ESPDF       = 1.5 # ENGINE SPARE PARTS PRICE FACTOR PAG 133
    DPengsp     = 7.0 # ENGINE SPARE PARTS DEPRECIATION PERIOD TABELA 5.7 PAG 134
    Cdengsp     = fdengsp * fengsp * NEng * EP * ESPDF / (DPengsp * Uannbl * vbl) # [USD/NM] EQ 5.46 PAG 133

    # TOTAL DEPRECIATION COST
    DOCdepr     = Cdap + Cdeng + Cdav + Cdapsp + Cdengsp # [USD/NM] PAG 153

    #==============================#
    #       DOC TAXES              #
    #==============================#
    # (PAG 130)
    # 1) COST OF LANDING FEES -> Clf (PAG 154)
    Caplf       = 0.002 * MTOW * kg2lb # EQ 5.49 PAG 135 AIRPLANE LANDING FEE PER LANDING
    Clf         = Caplf / (vbl * tbl) # [USD/NM] EQ 5.48 PAG 135 LANDING FEE 

    # 2) COST OF NAVIGATION FEES -> Cnf (PAG 154)
    Capnf       = 10 # [USD/FLIGHT] PAG 136 OPERATIONS OUTSIDE THE USA
    Cnf         = Capnf / (vbl * tbl) # [USD/NM] EQ 5.52 PAG 135 

    # 3) COST OF REGISTRY FEES -> Crf (PAG 154)
    frt         = 0.001 + 1e-8 * MTOW * kg2lb
    #Crt        = frt * DOC # EQ 5.53 PAG 136

    # DOClnr    = Clf + Cnf + Crt

    #==============================#
    #           TOTAL DOC          #
    #==============================#

    DOCcalc = (DOCflt + DOCmaint + DOCdepr + Clf + Cnf) / (1 - (0.02 + frt + 0.07)) # [USD/NM] PAG 155
    print('DOC = ',DOCcalc, 'USD$/nm ')
    #==============================#
    #       DOC FINANCING          #
    #==============================#

    #DOCfin     = 0.07 * DOC # EQ 5.5 PAG 136

    #==============================#
    #       DOC TOTAL
    #==============================#
    #DOC = DOC + DOCfin
    #==============================#
    #            IOC PAG 155       #
    #==============================#

    fioc = - 0.5617 * np.log(Block_Range) + 4.5765 # FIGURE 5.12 PAG 139
    IOC = fioc * DOCcalc # [USD/NM] EQ 5.56 PAG 137

    return(DOCcalc)
