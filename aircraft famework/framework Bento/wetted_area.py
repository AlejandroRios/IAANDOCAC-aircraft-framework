"""" 
Title     : wetted_area function
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
import os
import pandas as pd
from pax_cabine_length import pax_cabine_length
from tailcone_sizing import tailcone_sizing
from wetted_area_fuselage import wetted_area_forward_fuselage,wetted_area_tailcone_fuselage
from wetted_area_wing import wetted_area_wing
from airfoil_preprocessing import airfoil_preprocessing
from size_ht import size_ht
####################


def wetted_area(Ceiling,CruiseMach,MMO,NPax,NSeat,NCorr,
    SEATwid,AisleWidth,SeatPitch,
    Kink_semispan,Swing,wAR,wTR,wSweep14,wTwist,PWing,fus_w,fus_h,
    ediam,PEng,T0,VTarea,VTAR,VTTR,VTSweep,
    HTarea,HTAR,HTTR,PHT,htac_rel,wlet_present,wlet_AR,wlet_TR,
    PROOT,PKINK,PTIP):
    ###############Dimensionamento############################################
    #
    rad             = np.pi/180
    FusDiam         = np.sqrt(fus_w*fus_h)
    #--------------------------------------------------------------------------

    fileToRead1     = PROOT
    fileToRead2     = PKINK
    fileToRead3     = PTIP


    n=max(2,PEng) # number of engines
    print('\n')
    print('\n *** Single-engine Thrust = #6.0f  lb ***\n',T0)
    print('\n')
    #

    if PWing > 2:
        PWing = 2
        print('\n *** Warning: Wing location reset to #g ***\n',PWing)
    #
    if PWing < 1:
        PWing = 1
        print('\n*** Warning: Wing location reset to #g ***\n',PWing)
    #
    if PHT > 2:
        PHT = 2
        print('\n *** Warning: EH config reset to #g ***\n',PHT)
    #
    if PHT < 1:
        PHT = 1
        print('\n *** Warning: EH config reset to #g ***\n',PHT)

    #
    if PEng == 2 or PEng == 3:
        PHT= 2


    PEngm   = PEng
    # switch PEng
    #     case 2
    #         if PWing == 2 && PHT == 1
    #             PHT = 2 # asa alta ==> HT em "T"
    #             print('\n Warning: HT config reset to #g \n',PHT)
    #             PEngm  = 1 # asa alta ==> motores na asa
    #             print('\n Warning: Engine location reset to #g \n',PEng)
    #         end       
    #     case 3
    #         PHT   = 2 # Um motor eh central na fuselagem ==> EH em "T"
    #         print('\n *** Warning: EH config reset to #g ***\n',PHT)
    #     case 4
    #         if PWing == 2
    #             PHT  = 2
    #             print('\n *** Warning: EH config reset to #g *** \n',var.ht)
    #         end
    # end


    #
    PHTout = PHT
    PEng = PEngm

    airplane = {}
    airplane['npax']   = NPax
    airplane['naisle'] = NCorr # numero de corredores
    airplane['nseat']  = NSeat # numero de assentos por fileira
    airplane['wseat']  = SEATwid # [m] largura do assento
    airplane['waisle'] = AisleWidth # [m] largura corredor 
    airplane['pitch']  = SeatPitch # [m]  

    fuselage = {}
    fuselage['df']     = FusDiam
    fuselage['wfus']   = FusDiam

    fuselage['lcab']= pax_cabine_length(NPax,NSeat,airplane['pitch'],AisleWidth,SEATwid)

    fuselage['tail']= tailcone_sizing(NPax,PEng,FusDiam,FusDiam)

    FUSELAGE_lnose_df = 1.67
    fuselage['lco']      = FUSELAGE_lnose_df*fuselage['df']
    #
    fuselage['length'] =fuselage['lcab'] + fuselage['tail'] + fuselage['lco'] # comprimento fuselagem [m]
    #fesbeltez_f      = fuselage['length']/fuselage.df

    #fuselage.Swet    = pi*FusDiam*fuselage['length']*((1-(2/fesbeltez_f))**(2/3))*(1+(1/fesbeltez_f**2)) # [m2]
    # #
    lf               = fuselage['length']
    lco              = fuselage['lco']
    ltail            = fuselage['tail']
    lcab             = lf - (ltail+lco)
    # Calculo da area molhada da fuselagem
    # --> Fuselagem dianteira
    SWET_FF= wetted_area_forward_fuselage(fus_h,fus_w,lco)
    # --> Cabina de passageiros
    # calculo da excentricidade da elipse (se��o transversal da fuselagem)
    a=max(fus_w,fus_h)/2
    b=min(fus_w,fus_h)/2
    c=np.sqrt(a**2-b**2)
    e=c/a
    p=np.pi*a*(2-(e**2/2) + (3*e**4)/16)
    SWET_PAXCAB=p*lcab
    # --> Cone de cauda
    SWET_TC=wetted_area_tailcone_fuselage(fus_h,fus_w,lf,ltail)
    # Hah ainda que se descontar a area do perfil da raiz da asa
    # Sera feito mais adiante
    fuselage['Swet']=SWET_FF+SWET_PAXCAB+SWET_TC



# "ATEEEEEE AQUIIIIIIIIIIII OKKKKKKKKKKKK"




    ###########################################################################
    ###########################################################################
    ################################WING#######################################
    ###########################################################################
    #############################TRAPEZOIDAL###################################
    wing = {}
    wingtrap = {}
    wingref = {}
    wing['ir']     = 2
    wing['iq']     = 0
    twist       = wTwist
    wing['it']     = wing['ir'] + twist
    wingtrap['S']  = Swing # [m�]area da asa 
    wing['S']      = Swing
    wingtrap['AR'] = wAR # Alongamento da asa 
    wing['b']      = np.sqrt(wingtrap['AR']*wingtrap['S']) #  envergadura
    wingtrap['TR'] = wTR # afilamento
    wingtrap['c0'] = 2*wingtrap['S']/(wing['b']*(1+wingtrap['TR']))# [m] corda no centro
    wing['sweep']  = wSweep14 #[�] enflechamento 1/4c
    wing['et']     = twist # [�] torcao
    if PWing == 1: 
        wing['di']=2.5 # [�] diedro para asa baixa
        if PEng == 2:
            wing['di']=3      
    else:
        wing['di']=-2.5 # [�] diedro para asa alta


    wing['ct']=wingtrap['TR']*wingtrap['c0'] # [m] corda na ponta
    wingtrap['mgc']=wingtrap['S']/wing['b'] # [m] corda media geometrica
    wingtrap['mac']=2/3*wingtrap['c0']*(1+wingtrap['TR']+wingtrap['TR']**2)/(1+wingtrap['TR']) # [m] corda media geometrica
    wingtrap['ymac']=wing['b']/6*(1+2*wingtrap['TR'])/(1+wingtrap['TR']) # [m] posi�ao y da mac
    wing['sweepLE']=1/rad*(np.arctan(np.tan(rad*wing['sweep'])+1/wingtrap['AR']*(1-wingtrap['TR'])/(1+wingtrap['TR']))) # [�] enflechamento bordo de ataque
    wing['sweepC2']=1/rad*(np.arctan(np.tan(rad*wing['sweep'])-1/wingtrap['AR']*(1-wingtrap['TR'])/(1+wingtrap['TR']))) # [�] enflechamento C/2
    wSweepC2    = wing['sweepC2']
    wing['sweepTE']=1/rad*(np.arctan(np.tan(rad*wing['sweep'])-3/wingtrap['AR']*(1-wingtrap['TR'])/(1+wingtrap['TR']))) # [�] enflechamento bordo de fuga

    ##############################REFERENCE####################################
    wing['crank'] = Kink_semispan # porcentagem da corda

    wing['s0']=fuselage['df']/2 # [m] y da raiz da asa
    wing['s1']=wing['crank']*wing['b']/2 # [m] y da quebra
    wing['c1']=(wing['b']/2*np.tan(rad*wing['sweepLE'])+wing['ct'])-(wing['s1']*np.tan(rad*wing['sweepLE'])+(wing['b']/2-wing['s1'])*np.tan(rad*wing['sweepTE'])) # [m] corda da quebra
    wingtrap['cr']=(wing['b']/2*np.tan(rad*wing['sweepLE'])+wing['ct'])-(wing['s0']*np.tan(rad*wing['sweepLE'])+(wing['b']/2-wing['s0'])*np.tan(rad*wing['sweepTE'])) # [m] corda da raiz fus trap
    wing['cb']=wingtrap['cr']+(wing['s1']-wing['s0'])*np.tan(rad*wing['sweepTE']) # corda da raiz fus crank 
    wing['Sexp']=(wing['cb']+wing['c1'])*(wing['s1']-wing['s0'])+(wing['c1']+wing['ct'])*(wing['b']/2-wing['s1']) # area exposta 
    wingref['cr']=wing['Sexp']/(wing['b']/2-wing['s0'])-wing['ct'] # corda na juncao com a fus da asa de ref
    wingref['c0']=(wing['b']/2*wingref['cr']-wing['s0']*wing['ct'])/(wing['b']/2-wing['s0']) # [m] corda na raiz  da asa de ref
    #
    wing['c0']=wingtrap['c0']+wing['s1']*np.tan(rad*wing['sweepTE']) #[m] chord at root
    wing['TR']=wing['ct']/wingref['c0'] # taper ratio actual wing
    #
    wingref['cponta']=wingref['c0']*wing['TR']
    wingref['mgc']=wingref['c0']*(1+wing['TR'])/2 # mgc asa de ref
    wingref['mac']=2/3*wingref['c0']*(1+wing['TR']+wing['TR']**2)/(1+wing['TR']) # mac da asa ref
    wingref['ymac']=wing['b']/6*(1+2*wing['TR'])/(1+wing['TR']) # y da mac da asa ref
    wing['AR']=wing['b']/wingref['mgc']# alongamento asa real
    wingref['S']=wing['b']*wingref['mgc']# reference area [m�]
    wing['bexp']=wing['b']-fuselage['df']/2 # envergadura asa exposta
    wing['ARexp']=(wing['bexp']**2)/(wing['Sexp']/2) # exposed wing aspect ratio
    wing['TRexp']=wing['ct']/wing['cb'] # afilamento asa exposta

    wMAC     = wingref['mac']
    wYMAC    = wingref['ymac']
    wSweepLE = wing['sweepLE']

    xle=0.4250*fuselage['length'] # inital estimative
    wing['xac']=xle+wingref['ymac']*np.tan(rad*wing['sweepLE'])+0.25*wingref['mac']
    wing['xac_rel']=wing['xac']/wingref['mac']

    wing['cail']=(wing['b']/2*np.tan(rad*wing['sweepLE'])+wing['ct'])-((0.75*wing['b']/2)*np.tan(rad*wing['sweepLE'])+(wing['b']/2-(0.75*wing['b']/2))*np.tan(rad*wing['sweepTE'])) # corda no aileron
    wing['Sail']=(wing['cb']+wing['c1'])*(wing['s1']-wing['s0'])+(wing['c1']+wing['cail'])*((0.75*wing['b']/2)-wing['s1']) # area exposta com flap

    ############################# WING WETTED AREA ############################
    engine = {}
    wingloc   = PWing
    semispan  = wing['b']/2
    sweepLE   = wing['sweepLE']
    iroot     = wing['ir']
    ikink     = wing['iq']
    itip      = wing['it']
    wingdi    = wing['di']
    wtaper    = wing['TR']
    yposeng   = Kink_semispan
    Ccentro   = wing['c0']
    Craiz     = wing['cb']
    Cquebra   = wing['c1']
    Cponta    = wing['ct']

    engine['de'] = ediam/0.98 # [m]
    ediam     = engine['de']

    [Swet, xutip, yutip, xltip, yltip,
        xubreak,yubreak,xlbreak,ylbreak, xuraiz,yuraiz,xlraiz,ylraiz]  = wetted_area_wing(ediam,wingloc,FusDiam,Ccentro,Craiz,Cquebra,
        Cponta,semispan,sweepLE,iroot,ikink,itip,xle,yposeng,wingdi,wtaper,
        fileToRead1,fileToRead2,fileToRead3)

    wing['Swet'] = Swet


    # descontar a area do perfil da raiz da asa da area molhada da fuselagem
    xproot = np.array([np.flip(xuraiz),xlraiz])
    xproot = xproot.ravel()
    yproot = np.array([np.flip(yuraiz),ylraiz])
    yproot = yproot.ravel()

    def PolyArea(x,y):
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

    ARaiz=PolyArea(Craiz*xproot,Craiz*yproot)
    fuselage['Swet']=fuselage['Swet'] - 2*ARaiz
    ################################# WINGLET #################################
    ###########################################################################
    wlet = {}
    wlet['Swet']      = 0
    if wlet_present == 1:
        wlet_CR        = 0.65*Cponta
        wlet_b         = wlet_AR*wlet_CR*(1+wlet_TR)/2
        wlet_S         = wlet_CR*(1 + wlet_TR)*wlet_b/2
        wlet_tau       = 1 # Perfil da ponta = perfil da raiz
        wlet_TC_root   = 0.09 # Assume-se 9# da espessura relativa do perfil
        Taux           = 1 + 0.25*(wlet_TC_root*((1 + wlet_tau*wlet_TR)/(1 + wlet_TR)))
        wlet['Swet']      = 2*wlet_S*Taux # [m2]

    #----------------------------------------------------------------------------------------------------
    ##############################VERTICAL TAIL################################
    ###########################################################################
    vt = {}
    # initial guess for VT area
    vt['S']=VTarea
    vt['Sv_Sw']=vt['S']/wingref['S'] # rela�ao de areas
    vt['AR']=VTAR # alongamento EV
    vt['TR']=VTTR # Afilamento EV
    vt['sweep']=VTSweep # Enfl c/4 EV
    vt['et']=0 # torcao EV
    vt['di']=90 # diedro RV
    vt['b']=np.sqrt(vt['AR']*vt['S']) # Envergadura EV (m)
    vt['c0']=2*vt['S']/(vt['b']*(1+vt['TR'])) # corda de centro 
    vt['ct']=vt['TR']*vt['c0'] # corda da ponta 
    vt['cr']=vt['ct']/vt['TR'] # corda na raiz
    vt['mgc']=vt['S']/vt['b'] # mgc
    vt['mac']=2/3*vt['c0']*(1+vt['TR']+vt['TR']**2)/(1+vt['TR']) #mac
    vt['ymac']=2*vt['b']/6*(1+2*vt['TR'])/(1+vt['TR'])
    vt['sweepLE']=1/rad*(np.arctan(np.tan(rad*vt['sweep'])+1/vt['AR']*(1-vt['TR'])/(1+vt['TR']))) # [�] enflechamento bordo de ataque
    vt['sweepC2']=1/rad*(np.arctan(np.tan(rad*vt['sweep'])-1/vt['AR']*(1-vt['TR'])/(1+vt['TR']))) # [�] enflechamento C/2
    vt['sweepTE']=1/rad*(np.arctan(np.tan(rad*vt['sweep'])-3/vt['AR']*(1-vt['TR'])/(1+vt['TR']))) # [�] enflechamento bordo de fuga
    #lv=(0.060*wingref.S*wing['b'])/vt['S'] # fisrt estimate
    #lv=lh - 0.25*ht.ct - vt['b'] * tan(rad*vt['sweepLE']) + 0.25*vt['c0'] + vt['ymac']*tan(rad*vt['sweep']) # braco da EV
    #vt.v=vt['S']*lv/(wingref.S*wing['b']) # volume de cauda   
    ############################# VT wetted area ######################################
    vt['tcroot'] = 0.11 # [#]espessura relativa raiz
    vt['tctip']  = 0.11 # [#]espessura relativa ponta
    vt['tcmed']  = (vt['tcroot']+3*vt['tctip'])/4 # [#]espessura media
    vt['tau']    = vt['tctip']/vt['tcroot']
    dorsalfinSwet = 1 # additional area due to the dorsal fin [m2]
    vt['Swet']=2*vt['S']*(1+0.25*vt['tcroot']*((1+vt['tau']*vt['TR'])/(1+vt['TR'])))+dorsalfinSwet # [m2] 
    # Read geometry of VT airfoil


    panel_number = 201
    airfoil_name = 'pvt'
    airfoil_preprocessing(airfoil_name,panel_number)
    df_pvt = pd.read_table(""+ airfoil_name +'.dat' ,header=None,skiprows=[0],sep=',')
    df_pvt.columns = ['x','y']

    # [coordinates,~]=get_airfoil_coord('pvt.dat')

    xvt=df_pvt.x
    yvt=df_pvt.y
    AVT=PolyArea(xvt*vt['cr'],yvt*vt['cr'])
    # Desconta area da intersecao VT-fuselagem da area molhada da fuselagem
    fuselage['Swet']=fuselage['Swet'] - AVT
    #----------------------------------------------------------------------------------------------------
    ##############################HORIZONTAL TAIL##############################
    ###########################################################################
    ht=size_ht(HTarea,HTAR,HTTR,PHT,Swing,wSweep14,lf,vt['sweepLE'],vt['ct'],vt['c0'],vt['b'],
        htac_rel,CruiseMach+0.05,Ceiling)
    ###########################################################################
    ###################################ENGINE##################################
    ###########################################################################

    engine['length'] = 2.22*((T0)**0.4)*(MMO**0.2)*2.54/100 # [m] Raymer pg 19

    if PEng == 1:
        # livro 6 pag 111 fig 4.41 x/l=0.6
        wing['se']     = Kink_semispan*wing['b']/2 # [m] y do motor
        wing['seout']  = wing['se'] 
        wing['ce']    = wing['c0']-wing['se'] *np.tan(rad*wing['sweepLE']) # corda da seccao do motor
    elif PEng == 2:
        wing['se']     = fuselage['df']/2+0.65*engine['de']*np.cos(15*rad)
        wing['seout']  = wing['se'] 
    elif PEng == 3:
            # livro 6 pag 111 fig 4.41 x/l=0.6
        wing['se']     = Kink_semispan*wing['b']/2 # [m] y do motor
        wing['seout']  = wing['se'] 
        wing['ce']    = wing['c0']-wing['se'] *np.tan(rad*wing['sweepLE']) # corda da seccao do motor
    elif PEng == 4:
        # livro 6 pag 111 fig 4.41 x/l=0.6
        wing['se']     = Kink_semispan*wing['b']/2 # [m] y do motor
        wing['seout']  = (var.yEng+0.3)*wing['b']/2 # [m] y do motor externo distancia entre os dois 30# de b 
        wing['ce'] = wing['c0']-wing['se'] *np.tan(rad*wing['sweepLE']) # corda da seccao do motor
        pylon['ceout']=(wing['b']/2*np.tan(rad*wing['sweepLE'])+wing['ct'])-(wing['seout'] *np.tan(rad*wing['sweepLE'])+(wing['b']/2-wing['seout'] )*np.tan(rad*wing['sweepTE']))


    #########################AREA MOLHADA######################################

    ########################## Engine #########################################
    # aux1=(1-2/auxdiv)**2/3
    # engine.Swet=pi*engine['de']*engine['length']*aux1*(1+1/((engine['length']/engine['de'])**2)) # [m2]
    ln   = 0.50*engine['length'] # Fan cowling
    ll   = 0.25*ln
    lg   = 0.40*engine['length'] # Gas generator
    lp   = 0.10*engine['length'] # Plug
    esp  = 0.12
    Dn   = (1.+esp)*ediam
    Dhl  = ediam
    Def  = (1+esp/2)*ediam
    Dg   = 0.50*Dn
    Deg  = 0.90*Dg
    Dp   = lp/2
    swet_fan_cowl = ln*Dn*(2+0.35*(ll/ln)+0.80*((ll*Dhl)/(ln*Dn)) + 1.15*(1-ll/ln)*(Def/Dn))
    swet_gas_gen  = np.pi*lg*Dg*(1- 0.333*(1-(Deg/Dg)*(1-0.18*((Dg/lg)**(5/3)))))
    swet_plug     = 0.7*np.pi*Dp*lp
    engine['Swet']=swet_fan_cowl+swet_gas_gen+swet_plug
    ESwet      = engine['Swet']
    ###########################################################################
    ####################################PYLON##################################
    ###########################################################################

    pylon = {}
    if PEng == 1:
        pylon['c0']= wing['ce']
        pylon['ct'] = engine['length']
        pylon['TR'] = pylon['ct']/pylon['c0']
        pylon['mgc']=pylon['c0']*(1+pylon['TR'])/2
        pylon['mac']=2/3*pylon['c0']*(1+pylon['TR']+pylon['TR']**2)/(1+pylon['TR']) #mac
        # x/l=-0.6 e z/d = 0.85 figure 4.41 pag 111
        pylon['b'] = 0.85*engine['de'] - 0.5*engine['de']
        pylon['x'] = 0.6*wing['ce']
        pylon['AR']=pylon['b']/pylon['mgc']
        pylon['S']=pylon['b']*pylon['mgc']
        pylon['sweepLE'] = (1/rad)*np.tan(pylon['b']/pylon['x'])
        pylon['sweep'] = (1/rad)*np.tan(pylon['sweepLE']*rad)+((1-pylon['TR'])/(pylon['AR']*(1-pylon['TR'])))
    elif PEng == 2:
        pylon['c0']= engine['length']
        pylon['ct'] = 0.80*engine['length']
        pylon['TR'] = pylon['ct']/pylon['c0']
        pylon['mgc']=pylon['c0']*(1+pylon['TR'])/2
        pylon['mac']=2/3*pylon['c0']*(1+pylon['TR']+pylon['TR']**2)/(1+pylon['TR']) #mac
        # t/d=0.65 figure 4.42 pag 113  ang=15
        pylon['b'] = 0.65*engine['de']-engine['de']/2
        pylon['AR']=pylon['b']/pylon['mgc']
        pylon['S']=pylon['b']*pylon['mgc']
        pylon['sweep'] = 0
    elif PEng == 3:
        pylon['c0']= engine['length']
        pylon['ct'] = engine['length']
        pylon['TR'] = pylon['ct']/pylon['c0']
        pylon['mgc']=pylon['c0']*(1+pylon['TR'])/2
        pylon['mac']=2/3*pylon['c0']*(1+pylon['TR']+pylon['TR']**2)/(1+pylon['TR']) #mac
        # t/d=0.65 figure 4.42 pag 113  ang=15
        pylon['b'] = 0.65*engine['de']-engine['de']/2
        pylon['AR']=pylon['b']/pylon['mgc']
        pylon['S']=pylon['b']*pylon['mgc']
        pylon['sweep'] = 0        
    elif PEng == 4:
        pylon['c0']= wing['ce']
        pylon['ct'] = engine['length']
        pylon['TR'] = pylon['ct']/pylon['c0']
        pylon['mgc']=pylon['c0']*(1+pylon['TR'])/2
        pylon['mac']=2/3*pylon['c0']*(1+pylon['TR']+pylon['TR']**2)/(1+pylon['TR']) #mac
        # x/l=-0.6 e z/d = 0.85 figure 4.41 pag 111
        pylon['b'] = 0.85*engine['de'] - 0.5*engine['de']
        pylon['x'] = 0.6*wing['ce']
        pylon['AR']=pylon['b']/pylon['mgc']
        pylon['S']=pylon['b']*pylon['mgc']
        pylon['sweepLE'] = (1/rad)*np.tan(pylon['b']/pylon['x'])
        pylon['sweep'] = (1/rad)*np.tan(pylon['sweepLE']*rad)+((1-pylon['TR'])/(pylon['AR']*(1-pylon['TR'])))
        # engine out
        pylon['c0out'] = pylon['ceout']
        pylon['ctout'] = engine['length']
        pylon['TRout'] = pylon['ctout']/pylon['c0out']
        pylon['mgcout']=pylon['c0out']*(1+pylon['TRout'])/2
        pylon['macout']=2/3*pylon['c0out']*(1+pylon['TRout']+pylon['TRout']**2)/(1+pylon['TRout']) #mac
        # x/l=-0.6 e z/d = 0.85 figure 4.41 pag 111
        pylon['bout'] = 0.85*engine['de'] - 0.5*engine['de']
        pylon['xout'] = 0.6*pylon['ceout']
        pylon['ARout']=pylon['bout']/pylon['mgcout']
        pylon['Sout']=pylon['bout']*pylon['mgcout']
        pylon['sweepLEout'] = (1/rad)*np.tan(pylon['bout']/pylon['xout'])
        pylon['sweepout'] = (1/rad)*np.tan(pylon['sweepLEout']*rad)+((1-pylon['TRout'])/(pylon['ARout']*(1-pylon['TRout'])))


    #############################WETTED AREA###################################
    pylon['tcroot']=0.10 # [#]espessura relativa raiz
    pylon['tctip']=0.10 # [#]espessura relativa ponta
    pylon['tcmed']=(pylon['tcroot']+pylon['tctip'])/2 # [#]espessura media
    if PEng == 1 or PEng == 2 or PEng == 3:
            pylon['Swet']=2*pylon['S']*(1+0.25*pylon['tcroot']*(1+(pylon['tcroot']/pylon['tctip'])*pylon['TR'])/(1+pylon['TR'])) # [m2]
    else:
            pylon['Swetin']=2*pylon['S']*(1+0.25*pylon['tcroot']*(1+(pylon['tcroot']/pylon['tctip'])*pylon['TR'])/(1+pylon['TR'])) # [m2]
            pylon['Swetout']=2*pylon['Sout']*(1+0.25*pylon['tcroot']*(1+(pylon['tcroot']/pylon['tctip'])*pylon['TRout'])/(1+pylon['TRout'])) # [m2]
            pylon['Swet'] = pylon['Swetin'] + pylon['Swetout']

    #
    #  *************** Definicoes adicionais **********************************
    #slat = logical(var.SLATDEFLEC)
    # cg dos tanques de combust�vel da asa e posicao do trem d pouso principal
    #winglaywei2013
    dorsalfin = {}
    dorsalfin['Swet']=0.1
    wingSwet=wing['Swet']
    ################################TOTAL######################################
    airplane['Swet']=fuselage['Swet']+wing['Swet']+ht['Swet']+vt['Swet']+ n*(engine['Swet'])+pylon['Swet']+dorsalfin['Swet']+wlet['Swet']
    Swet          = airplane['Swet']
    FusSwet_m2    = fuselage['Swet']
    EnginLength_m = engine['length']
    ##
    print('\n ----------------- Wetted areas [m2] ---------------------')
    print('\n        Fuselage:  ',fuselage['Swet'])
    print('\n        Fuselage lengths [m]:')
    print('\n        Front: ',lco)
    print('\n        Pax cabin: ',lcab)
    print('\n        Tailcone: ',ltail)
    print('\n        Wing:  ',wing['Swet'])
    print('\n        Winglet:  ',wlet['Swet'])
    print('\n        Engines:  ',n*engine['Swet'])
    print('\n        Pylons:  ',pylon['Swet'])
    print('\n        HT:  ',ht['Swet'])
    print('\n        VT:  ',vt['Swet'])
    print('\n ==> Grand Total:  ',airplane['Swet'])
    print('\n ---------------- End Wetted areas ----------------------\n')
    #
    ##


    return (Swet, wingSwet, FusSwet_m2,
        ESwet,lf, lco, ltail,EnginLength_m,
        wYMAC,wMAC,wSweepLE, wSweepC2,ht,vt,pylon,
        Ccentro,Craiz,Cquebra, Cponta,
        xutip, yutip, xltip, yltip,xubreak,yubreak,xlbreak,ylbreak,
        xuraiz,yuraiz,xlraiz,ylraiz, PHTout)
