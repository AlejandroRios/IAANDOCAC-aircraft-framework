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
import numpy as np
from atmosphere import atmosphere
########################################################################################
"""Constants declaration"""
########################################################################################

########################################################################################

# HTarea = 21.7200
# HTAR = 4.6400
# HTTR = 0.3900
# PHT = 2
# wS = 93.5000
# wSweep14 = 17.4500
# lf = 33.1553
# vtSweepLE = 46.0456
# vtct = 3.1621
# vtc0 = 4.2731
# vtb = 3.3086
# htac_rel = 0.2500
# Mach = 0.8000
# Ceiling = 35000

def size_ht(HTarea,HTAR,HTTR,PHT,wS,wSweep14,lf,vtSweepLE,
    vtct,vtc0,vtb,htac_rel,Mach,Ceiling):

#
    rad       = np.pi/180
    m22ft2    = (1/0.3048)**2
    kt2ms     = 1/1.943844   # [kt] para [m/s]
    
    ht = {}
    ht['S']      = HTarea
    ht['sweep']  = wSweep14 + 5
    ht['AR']     = HTAR # alongamento EH
    ht['TR']     = HTTR # Afilamento EH
    ht['tcroot'] = 0.10 # [#]espessura relativa raiz
    ht['tctip']  = 0.10 # [#]espessura relativa ponta
    ht['tcmed']  =(ht['tcroot']+ht['tctip'])/2 # [#]espessura media
    ht['Sh_SW']  = ht['S']/wS # rela�ao de areas
    ht['et']     = 0 # torcao EH    

    if PHT == 1:
        ht['sweepLE']=1/rad*(np.arctan(np.tan(rad*ht['sweep'])+1/ht['AR']*(1-ht['TR'])/(1+ht['TR']))) # [�] enflechamento bordo de ataque
        ht['sweepC2']=1/rad*(np.arctan(np.tan(rad*ht['sweep'])-1/ht['AR']*(1-ht['TR'])/(1+ht['TR']))) # [�] enflechamento C/2
        ht['sweepTE']=1/rad*(np.arctan(np.tan(rad*ht['sweep'])-3/ht['AR']*(1-ht['TR'])/(1+ht['TR']))) # [�] enflechamento bordo de fuga
        ht['b']=sqrt(ht['AR']*ht['S']) # evergadura EH
        ht['c0']=2*ht['S']/(ht['b']*(1+ht['TR'])) # corda de centro  
        ht['ct']=ht['TR']*ht['c0'] # corda na ponta
        ht['di'] = 3
    else:
        ht['c0'] = vtct
        ht['ct'] = ht['TR']*ht['c0']
        ht['b']  = 2*ht['S']/(ht['ct']+ht['c0'])
        ht['AR'] = ht['b']**2/ht['S']
        ht['di'] = -2 # if "T" config a negative dihedral angle to help relaxe  lateral stability
        ht['sweepLE']=1/rad*(np.arctan(np.tan(rad*ht['sweep'])+1/ht['AR']*(1-ht['TR'])/(1+ht['TR']))) # [�] enflechamento bordo de ataque
        ht['sweepC2']=1/rad*(np.arctan(np.tan(rad*ht['sweep'])-1/ht['AR']*(1-ht['TR'])/(1+ht['TR']))) # [�] enflechamento C/2
        ht['sweepTE']=1/rad*(np.arctan(np.tan(rad*ht['sweep'])-3/ht['AR']*(1-ht['TR'])/(1+ht['TR']))) # [�] enflechamento bordo de fuga


    # corda da ponta 
    ht['mgc']=ht['S']/ht['b'] # mgc
    ht['mac']=2/3*ht['c0']*(1+ht['TR']+ht['TR']**2)/(1+ht['TR']) # mean aerodynamic chord
    ht['ymac']=ht['b']/6*(1+2*ht['TR'])/(1+ht['TR'])
    #
    ######################### HT Wetted area ######################################
    tau=ht['tcroot']/ht['tctip']
    #ht.thicknessavg = ht['tcmed']*0.50*(ht['c0']+ht['ct'])
    ht['Swet']=2.*ht['S']*(1+0.25*ht['tcroot']*(1+(tau*ht['TR']))/(1+ht['TR'])) # [m2] 
    # HT aerodynamic center
    if PHT == 1:
        ht['xac']=(0.92*lf - ht['c0'] + ht['ymac']*np.tan(rad*ht['sweepLE'])+
        htac_rel*ht['mac'])
    else:
        ht['xac']=0.95*lf-vtc0+vtb*np.tan(rad*vtSweepLE)+htac_rel*ht['mac']+ht['ymac']*np.tan(rad*ht['sweepLE'])

    ## EMPENAGEM HORIZONTAL (HORIZONTAL TAIL)
    atm                 = atmosphere(Ceiling,0)                                 # propriedades da atmosfera
    va                  = atm.va                                          # velocidade do som [m/s]
    sigma               = atm.sigma
    vc                  = Mach*va                                              # velocidade de cruzeiro meta, verdadeira [m/s]
    vckeas              = vc*sigma**0.5/kt2ms                                   # velocidade de cruzeiro meta [KEAS]
    vdkeas              = 1.25*vckeas   
    kh                  = 1.1                                                  # empenagem horizontal movel
    prod1               = 3.81*(((ht['S']*m22ft2)**0.2)*vdkeas)                    # termo 1
    prod2               = (1000*(np.cos(ht['sweepC2']*rad))**0.5)                     # termo 2
    prodf               = prod1/prod2                                          # termo 3
    ht['weight']           = 1.25*kh*(ht['S']*m22ft2)*(prodf-0.287)

    return(ht)
