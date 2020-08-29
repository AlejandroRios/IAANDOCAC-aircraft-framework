"""" 
Title     : Section Clmax
Written by: Alejandro Rios
Date      : 05/11/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
Mach
AirportElevation
PROOT
Craiz
PKINK
Cquebra
PTIP
Cponta

Outputs:
clmax_airfoil
flagsuc
"""
########################################################################################
import numpy as np
import os
from atmosphere import atmosphere
from cf_flat_plate import cf_flat_plate
########################################################################################
"""Constants declaration"""
class structtype():
    pass

pneu = structtype()
wlay = structtype()
########################################################################################
def winglaywei2018a(planffusdf,wingcrank,wingsweepLE, wingb,
    longtras, slat,Ccentro,Cquebra, Cponta,PEng, xutip, yutip,
   yltip, xukink,xlkink, yukink, ylkink, xuroot, xlroot, yuroot, ylroot ):
    # Generates wing structural layout and estimates fuel storage
    # Author: Bento Mattos
    # Version 2013R3b

    # OBS: Wing leading edge must be of constant sweep
    # Input:
    # poslongtras = Posicao da longarina traseira (fracional)
    # AR = Wing aspect ratio
    # Chord at fuselage centerline (CRaiz)
    # Chord at wingtip (Cponta)
    # Chord at kink station (Cquebra)
    # PSILE: Leading-edge sweepback angle
    # Aileron basis as semi-span fraction (posaileron)
    # If the wing has slat device (slat = 1 means yes otherwise no slat)
    # Location of the kink station as semi-span fraction (wing.ybreak)

    # Initialization
    rad            = np.pi/180
    wingfuelcapacitykg = 0
    nukink         = len(yukink)
    #
    nervspacing  = 22 # (pol) Roskam Vol III pg 220 suggests 24
    nervspacm    = nervspacing* 0.0254  #cm)
    denquerosene = 803 # jet A1 density
    # longtras     = 0.72
    angquebralongtras=0
    #
    diamfus     = planffusdf
    # Craiz       = Craiz
    # Cponta      = wingct
    # Cquebra     = wingc1
    fquebra     = wingcrank
    poslongtras = longtras
    #posaileron  = 0.75 # inicio do aileron (fracao da semienvergadura)

    # Variaveis auxiliares
    bdiv2       = 0.50*wingb
    xquebraBA   = bdiv2*fquebra*np.tan(rad*wingsweepLE)
    yquebra     = fquebra*bdiv2
    #yinfaileron = posaileron*bdiv2
    # localizacao da longarina dianteira como fracao da corda
    if slat > 0:
        fraclongdi = 0.25
    else:
        fraclongdi = 0.15

    limited = fraclongdi


    # Dados do trem de pouso:
    pneu.diam = 0.80 # diam do pneu em metros
    pneu.height = 0.25 # largura do pneu (m)
    lmunhao=1.3 # Comprimento do munhao (m)

    # Intersecao asa-fuselagem
    yfusjunc=diamfus/2

    # Vetor para Aramzernar Todas as Nervuras
    # Nerv = [x1 y1 x2 y2]
    Nerv = np.zeros((0,4))

    # Calcula a corda na intersecao

    xbainter=yfusjunc*np.tan(rad*wingsweepLE) # coord do ba na intersecao

    xbfquebra = xquebraBA + Cquebra

    if xbfquebra == Ccentro:
        xbfinter = xbfquebra
    else:
        inclinabf=(yquebra-0)/((xquebraBA + Cquebra) - Ccentro)
        xbfinter=Ccentro+(yfusjunc-0)/inclinabf # coord do bf na intersecao
    #
    Cinter = xbfinter - xbainter
    wlay.Cinter = Cinter

    #
    aux1=bdiv2*np.tan(rad*wingsweepLE)
    aux2=xquebraBA

    # *** Forma em planta da asa***
    xw=[0, xbainter, aux1, (aux1+Cponta), (aux2+Cquebra), xbfinter, Ccentro]
    yw=[0, yfusjunc, bdiv2, bdiv2, yquebra, yfusjunc, 0]

    # figure(7)
    # #
    # plot(xw,yw,'k') # Desenha forma em planta
    # hold on

    #
    xfus=[-2, Ccentro+2]
    yfus=[diamfus/2, diamfus/2]

    # plot(xfus,yfus,'--c')
    # hold on
    #


    # *** Ponta da asa ***
    xcontrolpoint2=bdiv2*np.tan(rad*wingsweepLE)
    xcontrolpoint3=bdiv2*np.tan(rad*wingsweepLE)+Cponta
    xcontrolpoint4=aux2+Cquebra
    ycontrolpoint3=bdiv2
    ycontrolpoint4=fquebra*bdiv2
    inclinabf=(ycontrolpoint4-ycontrolpoint3)/(xcontrolpoint4-xcontrolpoint3)
    xprojbfponta=xcontrolpoint3+(1.05*bdiv2-ycontrolpoint3)/inclinabf

    # projecao do BF da ponta
    xpp=[xcontrolpoint2, (xcontrolpoint2+0.15*Cponta), xprojbfponta, (xcontrolpoint2+Cponta)]
    ypp=[bdiv2, (bdiv2+0.025*bdiv2), (bdiv2+0.05*bdiv2), bdiv2]


    # plot(xpp,ypp,'-k')
    # hold on

    # *** Longarina dianteira

    xld = [(yfusjunc*np.tan(rad*wingsweepLE)+fraclongdi*Cinter), (bdiv2*np.tan(rad*wingsweepLE)+fraclongdi*Cponta)]
    yld = [yfusjunc , bdiv2]
    


    # plot(xld,yld,'-b')
    # hold on

    # *** Fim longarina dianteira ***

    # *** Longarina traseira (LT) ***
        
    # LT externa
    x1aux=(poslongtras*Cquebra+bdiv2*fquebra*np.tan(rad*wingsweepLE))
    xlte =[x1aux, (bdiv2*np.tan(rad*wingsweepLE)+poslongtras*Cponta)]
    ylte=[bdiv2*fquebra,  bdiv2]

    # plot(xlte,ylte,'-b')
    # hold on

    # LT Interna

    inclnt=x1aux-(bdiv2*np.tan(rad*wingsweepLE)+poslongtras*Cponta)
    inclnt=(bdiv2*fquebra - bdiv2)/inclnt
    anglti=np.arctan(inclnt)+angquebralongtras*np.pi/180 # adiciona angulo graus para aumentar o tamanho do caixao central
    xltintern=x1aux+((yfusjunc-bdiv2*fquebra)/np.tan(anglti))
    xlti=[xltintern, x1aux]
    ylti=[yfusjunc, bdiv2*fquebra]

    # plot(xlti,ylti,'-b')
    # hold on
    xlt = []
    xlt = xlti
    xlt[1] = xlte[1]

    ylt = []
    ylt = ylti
    ylt[1] = ylte[1]
            
    # *** Fim da longarina traseita ***

    # ************************   Nervuras ********************************
    # ++++  Na quebra
    #
    x1aux = yfusjunc*np.tan(rad*wingsweepLE) + fraclongdi*Cinter
    y1aux = yfusjunc
    x2aux = bdiv2*np.tan(rad*wingsweepLE) + fraclongdi*Cponta
    y2aux = bdiv2

    xnq = []
    ynq = []

    if x1aux == x2aux:
        xnq.append(x1aux)
    else:
        inclinald=(y2aux-y1aux)/(x2aux-x1aux)
        x0 = x1aux
        y0 = y1aux
        xnq.append((yquebra-y0)/inclinald + x0)

    #
    

    xnq.append(xquebraBA+poslongtras*Cquebra)
    ynq.append(yquebra)
    ynq.append(ynq[0])

 
    Nerv = np.hstack((xnq, ynq))
    # plot(xnq,ynq,'-b')
    # hold on


    # Coordendas da nervura na quebra
    xtnervq = xnq[1]
    ytnervq = ynq[1]
    xdnervq = xnq[0]
    ydnervq = ynq[0]

    # Nervura da asa externa com origem na quebra(eh perpendicular ah longarina
    # traseira)
    x1aux = xquebraBA + poslongtras*Cquebra
    y1aux = yquebra

    x2aux = bdiv2*np.tan(rad*wingsweepLE) + poslongtras*Cponta
    y2aux = bdiv2

    nervkinknormal =0 # a principio esta nervura nao existe
    nnervext  = 1 # Por enquanto, apenas a nervura padrao da quebra eh levada em conta
    if x2aux == x1aux:
        anglte    = np.pi/2
        angnev    =  0
    else:
        inclinalt = (y2aux-y1aux)/(x2aux-x1aux)
        if inclinalt > 0:
            anglte         = np.arctan(inclinalt)
            angnev         = np.pi/2 + anglte
            # testa se o angulo entrea nerv da quebra e esta nervura eh maior
            # que 5 graus
            if (np.pi-angnev) > 5*rad:
                nervkinknormal = 1 # nervura serah considerada
                nnervext  = 2

    x02=xnq[1]
    y02=ynq[1]
    inclinanerv=np.tan(angnev)
    x01=yfusjunc*np.tan(rad*wingsweepLE) + fraclongdi*Cinter
    y01=yfusjunc
    #

    xnqa = []
    ynqa = []

    if nervkinknormal == 1:
    # acha intersecao com a longarina dianteira
        xnqa.append(xnq[1]) # coord x do ponto da longarina traseira na quebra
        ynqa.append(ynq[1]) # coord y do ponto da longarina traseira na quebra
        #
        term1 = (y02-y01)-inclinanerv*x02+inclinald*x01
        xinerv=term1/(inclinald-inclinanerv)
        yinerv=y01+inclinald*(xinerv-x01)
        xnqa.append(xinerv)
        ynqa.append(yinerv)
        #
        Nerv = np.vstack((Nerv,np.hstack((xnqa, ynqa))))
        
        # plot(xnqa,ynqa,'-b')
        # hold on
    else:
        yinerv      = yquebra

    #
    # Restante das nervuras do caixao central externo

    #
    ytnerv = y02
    xtnerv = x02
    ydnerv = yinerv
    #
    jnervext=0
    deltay=nervspacm
    if anglte == 0:
        deltax = 0
    else:
        deltax = deltay/np.tan(anglte)

    xnervext_aux1 = []
    ynervext_aux1 = []
    xnervext_aux2 = []
    ynervext_aux2 = []
    # parte 1 ateh o flape
    while (ydnerv+deltay) < bdiv2:
        # descobre coord da nova nervura na LT
        ytnerv=ytnerv+deltay
        xtnerv=xtnerv+deltax
        jnervext=jnervext+1
        xnervext_aux1.append(xtnerv)
        ynervext_aux1.append(ytnerv)
        xnq[1]=xtnerv
        ynq[1]=ytnerv
        # Calcula intersecao com a LD
        ydnerv=ydnerv+deltay
        xdnerv=x01+(ydnerv-y01)/inclinald
        xnervext_aux2.append(xdnerv)
        ynervext_aux2.append(ydnerv)
        xnq[0]=xdnerv
        ynq[0]=ydnerv
        nnervext=nnervext+1

        Nerv = np.vstack((Nerv,np.hstack((xnq, ynq))))
        # plot(xnq,ynq,'-b')
        # hold on


    # Ultima nervura (fracionaria)

    if (ytnerv+deltay) < bdiv2:
        jnervext=jnervext+1
        ytnerv = ytnerv+deltay
        xtnerv = xtnerv+deltax
        xnq[0] = xtnerv
        ynq[0] = ytnerv
        xdnerv = (ytnerv-y01 + x01*inclinald-inclinanerv*xtnerv)/(inclinald-inclinanerv)
        ydnerv = y01 + inclinald*(xdnerv-x01)
        yinerv = ydnerv
        sinerv = xdnerv

        if ydnerv > bdiv2:
            yinerv = bdiv2
            y01p = bdiv2
            x01p = bdiv2*np.tan(rad*wingsweepLE)
            xinerv = (ytnerv-y01p + x01p*0-inclinanerv*xtnerv)/(0-inclinanerv) # inclinacao d apont eh zero

        xnervext_aux1.append(xtnerv)
        ynervext_aux1.append(ytnerv)
        xnervext_aux2.append(xinerv)
        ynervext_aux2.append(yinerv)

        #xdnerv = xtnerv + (bdiv2-ytnerv)/inclinanerv
        xnq[1] = xdnerv
        ynq[1] = yinerv
        nnervext=nnervext+1
   
        Nerv = np.vstack((Nerv,np.hstack((xnq, ynq))))
        # plot(xnq,ynq,'-b')
        # hold on

    xnervext = np.vstack((xnervext_aux1,xnervext_aux2))
    ynervext = np.vstack((ynervext_aux1,ynervext_aux2))


    print('\n Nervuras na asa externa (incluindo a da quebra): %2.0f \n' % nnervext)

    # Nervuras no caixao central interno
    xtnerv = xtnervq
    ytnerv = ytnervq
    xdnerv = xdnervq
    ydnerv = ydnervq

    nni =0
    deltay = 0.60*deltay

    xnervint_aux1 = []
    ynervint_aux1 = []
    xnervint_aux2 = []
    ynervint_aux2 = []

    while (ytnerv-yfusjunc-deltay) > (nervspacm/2):
        ytnerv = ytnerv - deltay
        xtnerv = xtnervq +(ytnerv-ytnervq)/np.tan(anglti)
        ydnerv = ytnerv
        xdnerv = x01+(ydnerv-y01)/inclinald
        xnq[0] = xdnerv
        ynq[0] = ydnerv
        nni = nni + 1
        xnervint_aux1.append(xdnerv)
        ynervint_aux1.append(ydnerv)
        xnq[1] = xtnerv
        ynq[1] = ytnerv
        xnervint_aux2.append(xtnerv)
        ynervint_aux2.append(ytnerv)

        Nerv = np.vstack((Nerv,np.hstack((xnq, ynq))))
        # plot(xnq,ynq,'-b')
        # hold on

    nni=nni+1

    

    

    # nervura na juncao asa-fuselagem

    xnq[0] = xld[0]
    ynq[0] = yld[0]
    xnervint_aux1.append(xnq[0])
    ynervint_aux1.append(ynq[0])
    xnq[1] = xlti[0]
    ynq[1] = ylti[0]
    xnervint_aux2.append(xnq[1])
    ynervint_aux2.append(ynq[1])
    #
    xnervint = np.vstack((xnervint_aux1,xnervint_aux2))
    ynervint = np.vstack((ynervint_aux1,ynervint_aux2))

  

    Nerv = np.vstack((Nerv,np.hstack((xnq, ynq))))
    # plot(xnq,ynq,'-b')
    # hold on
    print('\n Nervuras na asa interna (excluindo a da quebra): %2.0f \n' % nni)

    # *** Aileron ***
    # comprimento estimado do aileron: aprox. 25# da semi-envergadura

    xail = []
    yail = []
    xail.append(bdiv2*np.tan(rad*wingsweepLE)+poslongtras*Cponta)
    yail.append(bdiv2)
    xail.append(bdiv2*np.tan(rad*wingsweepLE)+Cponta)
    yail.append(bdiv2)
    #
    yinfaileron=0.75*bdiv2
    # Procura a nervura mais proxima de yinfaileron
    minnerv=1e06


    for j in range(jnervext):
        if abs(yinfaileron-ynervext[0,j]) < minnerv:

            minnerv=abs(yinfaileron-ynervext[0,j])

            mem=j

    ytop_tanque_externo=0.85*bdiv2
    minnerv=1e06
    for j in range(jnervext):
        if abs(ytop_tanque_externo-ynervext[0,j]) < minnerv:
            minnerv=abs(ytop_tanque_externo-ynervext[0,j])
            memtqe=j

    # calcula intesecao com BF
    tg1 = inclinabf
    tg2 = 0
    x1 = xcontrolpoint3
    y1 = ycontrolpoint3
    x2 = xnervext[0,mem]
    y2 = ynervext[0,mem]
    #
    term1 = (y2-y1)-tg2*x2+tg1*x1

    # xail = []
    # yail = []
    xail.append(term1/(tg1-tg2))
    yail.append(y1+tg1*(xail[2]-x1))
    #
    xail.append(xnervext[1,mem])
    yail.append(ynervext[1,mem])
    # fill(xail,yail,'r')
    # hold on
    xcombe=[]
    ycombe=[]
    # Tanque de combust�vel na asa externa
    if PEng == 2:
        xcombe.append(xtnervq)
        ycombe.append(ytnervq)
        xcombe.append(xdnervq)
        ycombe.append(ydnervq)
        xcombe.append(xnervext[1,memtqe])
        ycombe.append(ynervext[1,memtqe])
        xcombe.append(xnervext[1,memtqe])
        ycombe.append(ynervext[1,mem])
    else:
        xcombe.append(xnervext[0,0])
        ycombe.append(ynervext[0,0])
        xcombe.append(xnervext[1,0])
        ycombe.append(ynervext[1,0])
        xcombe.append(xnervext[1,memtqe])
        ycombe.append(ynervext[1,memtqe])
        xcombe.append(xnervext[1,memtqe])
        ycombe.append(ynervext[1,memtqe])

    # #
    # patch(xcombe,ycombe,'g','FaceAlpha',0.2)
    # hold on
    #
    xcgtqe = sum(xcombe)/4  # CG do tanque externo
    ycgtqe = sum(ycombe)/4
    #
    # Calcula capacidade dos tanques (duas semi-asas)
    limitepe =poslongtras
    #
    # estacoes da base inf e sup do tanque externo (ymed1 e ymed2)
    ymed1=0.50*(ynervext[0,0]+ynervext[1,0])
    ymed2=0.50*(ynervext[0,memtqe]+ynervext[1,memtqe])

    # estacao superior do tanque interno da asa
    if PEng == 2:
        ymed3=ytnervq
        limitepi1=poslongtras

        aux=max(xnervint[0,nni-1],xnervint[1,nni-1])
        limitepi2=(aux-yfusjunc*np.tan(rad*wingsweepLE))/Cinter
    else:
        ymed3=ynervint[1,0]  
        deltaysta=yquebra-yfusjunc
        Csupint = Cinter + ((ymed3-yfusjunc)/deltaysta)*(Cquebra-Cinter)
        xbainter = yfusjunc*np.tan(rad*wingsweepLE)
        xbaint  = xbainter + ((ymed3-yfusjunc)/deltaysta)*(xquebraBA-xbainter)
        aux=max(xnervint[0,0],xnervint[1,0])
        limitepi1=(aux-xbaint)/Csupint
        aux=max(xnervint[0,nni-1],xnervint[1,nni-1])
        limitepi2=(aux-yfusjunc*np.tan(rad*wingsweepLE))/Cinter


    #fprintf('\n cheguei aqui: volume de tanque da asa \n')

    #################################################################################
    #################################################################################
    yinterno=ymed1
    yexterno=ymed2
    #acha perfil externo
    deltay=wingb/2-yinterno


    xuperfilext=xutip
    yuperfilext=yukink + ((yexterno-yinterno)/deltay)*(yutip-yukink)
    ylperfilext=ylkink + ((yexterno-yinterno)/deltay)*(yltip-ylkink)
    Cext = Cquebra + ((yexterno-yinterno)/deltay)*(Cponta-Cquebra)
    heighte = ymed2-ymed1
    icount=0

    xpolye = []
    ypolye = []
    xpolyi = []
    ypolyi = []
    for i in range(0,nukink,1):
        if xuperfilext[i] < limitepe and xuperfilext[i] >= limited:
            icount=icount+1
            xpolye.append(xuperfilext[i])
            ypolye.append(yuperfilext[i])
            xpolyi.append(xukink[i])
            ypolyi.append(yukink[i])

    for i in range(nukink-1,0,-1):
        if xuperfilext[i] < limitepe and xuperfilext[i] >= limited:
            icount=icount+1
            xpolye.append(xuperfilext[i])
            ypolye.append(ylperfilext[i])
            xpolyi.append(xlkink[i])
            ypolyi.append(ylkink[i])

    #xistosxlkink=xlkink
    #xistosylkink=ylkink
    # a percentagem da corda na secao da raiz nao eh a memsma da long traseira
    yinterno=yfusjunc
    yexterno=ymed3
    #xistosquebra=yquebra
    #acha perfil externo
    deltay=yquebra-yinterno

    gradaux= (yexterno-yinterno)/deltay

    xuperfilint=xuroot

    yuperfilint = []
    ylperfilint = []


    for j in range(len(xuroot)):
        yuperfilint.append(yuroot[j] + gradaux*(yukink[j]-yuroot[j]))
        ylperfilint.append(ylroot[j] + gradaux*(ylkink[j]-ylroot[j]))
    
    Csupint = Cinter + ((yexterno-yinterno)/deltay)*(Cquebra-Cinter)


    limitedr = limited

    icount=0

    xpolyroot = []
    ypolyroot = []

    for i in range(0,len(xuroot),1):
        if xuperfilint[i] <= limitepi1 and xuperfilint[i] >= limitedr:
            icount=icount+1
            xpolyroot.append(xuroot[i])
            ypolyroot.append(yuperfilint[i])

    #xistosxlroot=xlroot
    #xistosylroot=ylroot
    for i in range(len(xuroot),0,-1):

        if xuperfilint[i-1] <= limitepi1 and xuperfilint[i-1] >= limitedr:
            icount=icount+1
            xpolyroot.append(xuroot[i])
            ypolyroot.append(ylperfilint[i])

    #
    # Area molhada no perfil da interseccao asa-fuselagem
    icount=0

    xpolyroot1 = []
    ypolyroot1 = []
    for i in range(0,len(xuroot),1):
        if xuroot[i] <= limitepi2 and xuroot[i] >= limitedr:
            icount=icount+1
            xpolyroot1.append(xuroot[i])
            ypolyroot1.append(yuroot[i])

    #xistosxlroot=xlroot
    #xistosylroot=ylroot

    for i in range(len(xuroot),0,-1):
        if xuroot[i-1] <= limitepi2 and xuroot[i-1] >= limitedr:
            icount=icount+1
            xpolyroot1.append(xuroot[i])
            ypolyroot1.append(ylroot[i])

    def PolyArea(x,y):
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


    areae=PolyArea(xpolye,ypolye)*Cext*Cext
    areai=PolyArea(xpolyi,ypolyi)*Cquebra*Cquebra
    arearootsup=PolyArea(xpolyroot,ypolyroot)*Csupint*Csupint
    arearootinf=PolyArea(xpolyroot1,ypolyroot1)*Cinter*Cinter
    # Calculo dos volumes
    voltanqueext=0.98*(heighte/3)*(areai + areae + np.sqrt(areai*areae)) # 2# de perdas devido a nervuras, revestimento e outros equip
    voltanqueint=0.98*(deltay/3)*(arearootinf + arearootsup + np.sqrt(arearootinf*arearootsup)) # 2# de perdas devido a nervuras, revestimento e outros equip
#
    #################################################################################
    #################################################################################
    #fprintf('\n Passei por aqui: volume de tanque da asa \n')

    capacidadete=2.*voltanqueext*denquerosene
    #
    print('\n Capacidade dos tanques externos:(ambas semiasas) %4.0f kg \n' % capacidadete)
    #
    # Capacidade dos tanques da asa interna
    xcombi=[]
    ycombi=[]
    if PEng == 2:
        xcombi.append(xdnervq)
        ycombi.append(ydnervq)
        xcombi.append(xtnervq)
        ycombi.append(ytnervq)
        xcombi.append(xnervint[1,nni-1])
        ycombi.append(ynervint[1,nni-1])
        xcombi.append(xnervint[0,nni-1])
        ycombi.append(ynervint[0,nni-1])
    else:
        xcombi.append(xnervint[0,0])
        ycombi.append(ynervint[0,0])
        xcombi.append(xnervint[1,0])
        ycombi.append(ynervint[1,0])
        xcombi.append(xnervint[1,nni-1])
        ycombi.append(ynervint[1,nni-1])
        xcombi.append(xnervint[0,nni-1])
        ycombi.append(ynervint[0,nni-1])
        #fprintf('\n +++  passei por aqui xcombi \n')
 

    xcgtqi = sum(xcombi)/4  # CG do tanque interno
    ycgtqi = sum(ycombi)/4
#     # Desenha tanque da semi-asa interna
#     patch(xcombi,ycombi,'g','FaceAlpha',0.2)
#     hold on
#    # Desenha tanque da semi-asa interna
#     patch(xcombi,ycombi,'g','FaceAlpha',0.2)
#     hold on


    capacidadeti=2*voltanqueint*denquerosene

    print('\n Capacidade dos tanques internos: %4.0f kg \n' % capacidadeti)

    # Capacidade total dos tanques
    # Considera perdas devido a nervuras, longarinas, revestimento, bombas
    # etc...
    if capacidadeti > 0 and  capacidadete > 0:
        wingfuelcapacitykg=capacidadeti + capacidadete 

    print('\n Capacidade total dos tanques: %4.0f kg \n' % wingfuelcapacitykg)

    # Localizacao do CG dos tanques de combustivel
    xcgtanques = (xcgtqe*capacidadete + xcgtqi*capacidadeti)/(capacidadeti+capacidadete)
    print('\n Localizacao do CG dos tanques x = %4.2f  \n' % xcgtanques)

    # *** Flape externo ***
    xflape = []
    yflape = []
    xflape.append(xail[2]+1)
    yflape.append(yail[2] - 0.10)

    x1aux = xquebraBA + Cquebra
    y1aux = yquebra
    x2aux = bdiv2*np.tan(rad*wingsweepLE) + Cponta
    y2aux = bdiv2

    if x1aux == x2aux:
        xflape[0] = x1aux
    else:
        gradbfaux = (y2aux-y1aux)/(x2aux-x1aux)
        xflape[0] = (yflape[0]-y1aux)/gradbfaux + x1aux

    # Intersecao com a LT
    tg1 = 0
    tg2 = inclnt
    x1 = xail[2]
    y1 = yail[2]-0.10
    x2 = xnervext[0,mem]
    y2 = ynervext[0,mem]
    term1 = (y2-y1)-tg2*x2+tg1*x1
    xflape.append(term1/(tg1-tg2))
    yflape.append(y1+tg1*(xflape[1]-x1))
    xflape.append(x02)
    yflape.append(y02)
    xflape.append(fquebra*bdiv2*np.tan(rad*wingsweepLE)+Cquebra)
    yflape.append(fquebra*bdiv2)

    # fill(xflape,yflape,'m')
    # hold on

    def PolyArea(x,y):
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

    aflape=PolyArea(xflape,yflape)
    print('\n Area dos flapes externos (recolhidos): %4.0f m2 \n' % (2*aflape))
    # Insere nervura auxiliar para o flape externo

    xnervaf = []
    ynervaf = []
    xnervaf.append(xflape[1])
    ynervaf.append(yflape[1])
    # intersecao com a LD

    #tg1 = atan(inclinald) +pi/2
    #tg1=tan(tg1)
    #tg2 = inclinald
    #x1 = xflape[1]
    #y1 = yflape[1]
    #x2 = xnervext(mem,2)
    #y2 = ynervext(mem,2)
    #term1 = (y2-y1)-tg2*x2+tg1*x1
    x1aux = yfusjunc*np.tan(rad*wingsweepLE) + fraclongdi*Cinter
    y1aux = yfusjunc
    x2aux = bdiv2*np.tan(rad*wingsweepLE) + fraclongdi*Cponta
    y2aux = bdiv2


    if x1aux == x2aux:
        xnervaf.append(x1aux)
        ynervaf.append(yflape[1])
    else:
        tg1 = (y2aux-y1aux)/(x2aux-x1aux)
        tg2= np.tan(angnev)
        x1 = x1aux
        y1 = y1aux
        x2 = xflape[1]
        y2 = yflape[1]
        term1 = (y2-y1)-tg2*x2+tg1*x1
        xnervaf.append(term1/(tg1-tg2))
        ynervaf.append(y2+tg2*(xnervaf[1]-x2))  
    

    # plot(xnervaf,ynervaf,'-b')
    # hold on

    xflapi = []
    yflapi = []

    # Flape interno
    xflapi.append(xflape[3])
    yflapi.append(yflape[3])
    xflapi.append(xflape[2])
    yflapi.append(yflape[2])
    cordafi=xflape[3]-xflape[2]
    xflapi.append(yfusjunc*(np.tan(rad*wingsweepLE)) + Cinter - cordafi)
    yflapi.append(yfusjunc)
    xflapi.append(yfusjunc*(np.tan(rad*wingsweepLE)) + Cinter)
    yflapi.append(yfusjunc)
    # fill(xflapi,yflapi,'m')
    # hold on

    # posicao em x do munhao
    posxmunhao = (xflapi[2]+xltintern)/2
    print('\n Posicao do munhao do trem de pouso principal x= %4.2f \n' % posxmunhao)

    # axis equal
    # title('Wing Structural Layout')
    #fim = max(Craiz,bdiv2*tan(rad*wing.sweepLE)+Cponta)
    #fim = round(fim+1)
    #set(gca,'XTick',0:1:fim)
    #

    if os.path.exists('wlayout.jpg'):
        os.remove('wlayout.jpg')

    #print -djpeg -f7 -r300 'wlayout.jpg'

    # close(figure(7))

    # figure(11)
    # subplot(4,1,1)
    # plot(xuperfilext,yuperfilext)
    # hold on
    # plot(xuperfilext,ylperfilext)
    # title('Tip airfoil - fuel contact area')
    # hold on
    # fill(xpolye,ypolye,'r')
    # axis equal
    # subplot(4,1,2)
    # plot(xukink,yukink)
    # hold on
    # plot(xlkink,ylkink)
    # hold on
    # fill(xpolyi,ypolyi,'g')
    # hold on
    # title('Kink airfoil - fuel contact area')
    # subplot(4,1,3)
    # plot(xuroot,yuperfilint)
    # hold on
    # plot(xlroot,ylperfilint)
    # hold on
    # fill(xpolyroot,ypolyroot,'y')
    # title('Upper internal tank airfoil - fuel contact area')
    # hold on
    # subplot(4,1,4)
    # plot(xuroot,yuroot)
    # hold on
    # plot(xlroot,ylroot)
    # hold on
    # fill(xpolyroot1,ypolyroot1,'b')
    # title('Lower internal tank airfoil - fuel contact area')
    # hold on
    # axis equal

    if os.path.exists('tankprofiles.jpg'):
        os.remove('tankprofiles.jpg')
    # end
    #print -djpeg -f11 -r300 'tankprofiles.jpg'
    # Check de consistencia
    if wingfuelcapacitykg <= 0 or aflape <= 0:
        checkconsistency = 1 # fail
    else:
        checkconsistency = 0 # ok

    return(posxmunhao, xcgtanques, wingfuelcapacitykg,aflape)