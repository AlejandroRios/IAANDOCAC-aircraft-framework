"""" 
Title     : Input fpwb 
Written by: Alejandro Rios
Date      : 18/11/19
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
from atmosphere import atmosphere
########################################################################################
"""Constants declaration"""
########################################################################################
def frange(x, y, jump=1.0):
    i = 0.0
    x = float(x)  # Prevent yielding integers.
    y = float(y)  # Comparison converts y to float every time otherwise.
    x0 = x
    epsilon = jump / 2.0
    yield x  # yield always first value
    while x + epsilon < y:
        i += 1.0
        x = x0 + i * jump
        yield x
    
def input_fpwb(M,AirportElevation,
    lf,lco,lcab,xle,wS,enf,wingb,diedro,wMAC,
    c0,cr,cq,ct,etabreak,FusDiam,xuroot,xlroot,ylroot,yuroot,
    xukink,xlkink,ylkink,yukink,xutip,xltip,yutip,yltip,ir,iq,it):

    ## Constantes
    rad     = np.pi/180
    ft2m    = 0.3048
    m2ft    = 1./ft2m
    ##
    nuroot = len(xuroot)
    nlroot = len(xlroot)
    nukink = len(xukink)
    nlkink = len(xlkink)
    nutip  = len(xutip)
    nltip  = len(xltip)
    ## 
    ise   = 1. # ise - Control parameter for the nonisentropic correction. # ISE=1. - the nonisentropic correction is used # ISE=0. - no correction
    order = 2. # order - order of the artificial dissipation in the supersonic zones
    #   rchord=chord at wing-fuselage intersection#
    file_path = "/home/alejandro/Documents/Github/IAANDOCAC/MDO/Bentos Framework/"
    extensions = ('.ps', '.out','.pl4','.blp','.sav','.inp')
    filelist = [ f for f in os.listdir(file_path) if f.endswith(extensions) ]
    for f in filelist:
        os.remove(os.path.join(file_path, f))

    largfus         = 1.03*FusDiam/2
    wingb2          = wingb/2
    dist_quebra     = (wingb2)*etabreak
    raio            = FusDiam/2
    YE0             = raio*0.005 # distancia verticla da asa na linha de centro da fuselagem
    #
    if dist_quebra < largfus:   
        dist_quebra    = 1.15*largfus


    # Geracao de secao circular da fuselagem
    Nupp = 20
    #Secao circular
    yc=[]
    zc=[]
    dteta = np.pi/(2*Nupp-1)

    for j in range(0,2*Nupp):
        teta= (j)*dteta
        yc1=raio*np.cos(teta)
        yc.append(yc1)
        zc1=raio*np.sin(teta)
        zc.append(zc1)

    yc = np.flip(yc)


    #
    minespintra=min(ylroot)
    distv=(FusDiam/2)*np.sin(rad*diedro)
    d1=-1.1*FusDiam/2-minespintra*c0+distv
    if (d1+minespintra*c0) < -0.95*FusDiam/2:
        ylew = -0.94*FusDiam/2 + distv - minespintra*c0
    else:
        ylew=-1.1*FusDiam/2-minespintra*c0

    # Secao comprida entre o inicio e o fim da asa
    # 
    zw = []
    yw = []

    zw.append(0.0)
    yw.append(-1.1*raio)

    zw.append(raio/4)
    yw.append(-1.1*raio)

    zw.append(raio/2)
    yw.append(-1.1*raio)

    zw.append(0.95*raio)
    yw.append(-raio)

    zw.append(+raio)
    yw.append(-0.95*raio)

    zw.append(+raio)
    yw.append(-0.90*raio)

    zw.append(+raio)
    yw.append(-0.50*raio)

    zw.append(+raio)
    yw.append(0.)
    dteta=np.pi/2/Nupp

    for j in range(Nupp):
        teta    = (j+1)*dteta
        yw1 = raio*np.sin(teta)
        yw.append(yw1)
        zw1 = raio*np.cos(teta)
        zw.append(zw1)

    # Secao 1 da fuselagem com carenagem antes da asa
    teta1=20*rad
    y1 =-raio*np.sin(teta1)
    z1 = raio*np.cos(teta1)

    zwf1 = []
    ywf1 = []
    zwf1.append(0.0)
    ywf1.append(-raio)

    zwf1.append(z1/4)
    ywf1.append(-raio)

    zwf1.append(z1/2)
    ywf1.append(-raio)

    zwf1.append(0.90*z1)
    ywf1.append(-0.95*raio)

    zwf1.append(+z1)
    ywf1.append(-0.85*raio)

    ywf1.append(0.50*(+y1-0.95*raio))
    zwf1.append(z1)

    zwf1.append(+z1)
    ywf1.append(1.1*y1)

    zwf1.append(+z1)
    ywf1.append(y1)

    jcount  = 8

    dteta        = (np.pi/2+teta1)/Nupp

    
    for j in frange((-teta1+dteta),np.pi/2,dteta):
        jcount       = jcount + 1
        ywf11= raio*np.sin(j)
        ywf1.append(ywf11)
        zwf11 = raio*np.cos(j)
        zwf1.append(zwf11)


    #plot(zwf1,ywf1,'-bo')
    #hold on

    #
    # Secao 2 da fuselagem com carenagem antes da asa
    #
    teta1=30*rad
    teta2=60*rad
    npontos=10
    dteta = teta1/(npontos-1)

    ywf = []
    zwf = []
    for j in frange(1,npontos,1):
        ang=(j-1)*dteta
        ywf_aux= -raio*np.cos(ang)
        ywf.append(ywf_aux)
        zwf_aux= +raio*np.sin(ang)
        zwf.append(zwf_aux)


    y1 = -raio*np.cos(teta1)
    y2 = -raio*np.cos(teta2)
    #z1 = raio*sin(teta1)
    z2 = raio*np.sin(teta2)
    ymed = 0.50*(y1+y2)
    #zmed = 0.50*(z1+z2)
    ywf.append(y1-0.05*ymed)
    zwf.append(0.90*z2)
    ywf.append(y1-0.150*ymed)
    zwf.append(0.97*z2)

    npi=2*npontos -(npontos+3)+1
    dteta = teta1/(npi-1)

    for j in frange((npontos+3),2*npontos,1):
        ang=teta2+(j-(npontos+3))*dteta
        #angg=ang/rad
        ywf_aux=-raio*np.cos(ang)
        ywf.append(ywf_aux)
        zwf_aux=+raio*np.sin(ang)
        zwf.append(zwf_aux)

    teta3 =np.pi/2
    dteta=teta3/npontos
    for j in frange(1,npontos,1):
        ang=j*dteta
        ywf_aux=raio*np.sin(ang)
        ywf.append(ywf_aux)
        zwf_aux=raio*np.cos(ang)
        zwf.append(zwf_aux)

    #plot(zwf,ywf,'--r+')
    #
    # Secao 2 da fuselagem com carenagem antes da asa
    #
    teta1=40*rad
    teta2=55*rad
    npontos=12
    dteta = teta1/(npontos-1)

    ywf2 = []
    zwf2 = []
    for j in frange(1,npontos,1):
        ang=(j-1)*dteta
        ywf2_aux= -raio*np.cos(ang)
        ywf2.append(ywf2_aux)
        zwf2_aux= +raio*np.sin(ang)
        zwf2.append(zwf2_aux)


    y1 = -raio*np.cos(teta1)
    y2 = -raio*np.cos(teta2)
    #z1 = raio*sin(teta1)
    z2 = raio*np.sin(teta2)
    ymed = 0.50*(y1+y2)
    #zmed = 0.50*(z1+z2)
    ywf2.append(y1-0.05*ymed)
    zwf2.append(0.90*z2)
    ywf2.append(y1-0.150*ymed)
    zwf2.append(0.97*z2)

    npi=2*npontos -(npontos+3)+1
    dteta = teta1/(npi-1)
    for j in frange((npontos+3),2*npontos,1):
        ang=teta2+(j-(npontos+3))*dteta
        #angg=ang/rad
        ywf2_aux=-raio*np.cos(ang)
        ywf2.append(ywf2_aux)
        zwf2_aux=+raio*np.sin(ang)
        zwf2.append(zwf2_aux)

    teta3 =np.pi/2
    dteta=teta3/npontos
    for j in frange(1,npontos,1):
        ang=j*dteta
        ywf2_aux=raio*np.sin(ang)
        ywf2.append(ywf2_aux)
        zwf2_aux=raio*np.cos(ang)
        zwf2.append(zwf2_aux)

    # ****** Preparacao da geracao dos dois arquivos com angulo de ataque 
    #         diferentes cada um  *********************************************
    for jj in range(1,3):
    #
        if jj == 1:
                # gera arquivo # 1 para calculo do clmax
            CL     = 0.5
            Ataque = 3
            FCONT  = 0. # start from scratch
            atm    = atmosphere(AirportElevation*m2ft,0)

            TAE    = atm.TAE # temperatura [K]
            T8     = TAE
            ro     = atm.ro # densidade [Kg/m�]
            va     = atm.va # velocidade do som [m/s]
        # ***** air viscosity (begin)******
            mi0    = 18.27E-06
            Tzero  = 291.15 # Reference temperature (15 graus celsius)
            Ceh    = 120 # C = Sutherland's constant for the gaseous material in question
            mi     = mi0*((TAE+Ceh)/(Tzero+Ceh))*((TAE/Tzero)**1.5)
            vel    = va*M
            rey    = ro*vel*wMAC/mi
            fid    = open('fpwbclm1.inp','w+')
        elif jj == 2:
            # gera arquivo # 2 para calculo do CLmax
            CL=0.75
            Ataque = 5
            FCONT =0. # =1 ==>start from previous calculation

            atm=atmosphere(AirportElevation*m2ft,0)
            TAE=atm.TAE # temperatura [K]
            T8 = TAE
            ro=atm.ro # densidade [Kg/m�]
            va=atm.va # velocidade do som [m/s]
        # ***** air viscosity (begin)******
            mi0=18.27E-06
            Tzero=291.15 # Reference temperature
            Ceh= 120 # C = Sutherland's constant for the gaseous material in question
            mi=mi0*((TAE+Ceh)/(Tzero+Ceh))*((TAE/Tzero)**1.5)
            vel=va*M
            rey=ro*vel*wMAC/mi
            fid = open('fpwbclm2.inp',"w")

        # Stations for viscous calculation
        nvisc_i=4
        nvisc_e=5
        stavi=largfus/wingb2 + 0.0125
        stabreak=dist_quebra/wingb2 
        zvisc_internal=np.linspace(stavi,stabreak,nvisc_i)
        zvisc_external=np.linspace(stabreak+0.1,1.,nvisc_e)
        zvisc = np.concatenate([zvisc_internal,zvisc_external])
        nvisc=nvisc_i+nvisc_e
        #nvisc=double(nvisc)
        
        fid.write('          AVAER FULL POTENTIAL ANALYSIS                                           \n')
        fid.write('    NX   ><   NY   ><   NZ   ><   NT   ><  FCONT >                                \n')
        fid.write('    48.        12.        10.     5.       %2.0f                                 \n' % FCONT)
        fid.write('  FPICT1 >< FPICT2 >< FPICT3 >< FPICT4 >< FPICT5 ><        ><        >< tecplot>  \n')
        fid.write('    0.         0.        0.        0.       0.0                           0.      \n')
        fid.write('   XMIN  ><  XMAX  ><  YMIN  ><  YMAX  ><  ZMIN  ><  ZMAX  >                      \n')
        fid.write('    -.1       1.7      -.9        .9       .0        2.7                          \n')
        fid.write('    EX   ><   EY   ><   EZ   >                                                    \n')
        fid.write('   -5.        5.        10.                                                       \n')
        fid.write('    NP   ><  ETAE  ><   T8   ><   PR   ><   PRT  ><   RRR  ><   VGL  ><   VGT  >  \n')
        fid.write('    21.       4.      %4.0f      .753       .90        1.      1.26      1.26     \n' % T8)
        fid.write('    NTR  ><  AL_CL ><   CL   >< DCL/DA >                                          \n')
        fid.write(' %6.1f        0.       %4.2f     0.40                                             \n' % (nvisc, CL))
        fid.write('<   Z    ><  XTRU  ><  XTRL  >                                                    \n')
        for jvisc in range(nvisc):
            fid.write(' %9.4f      0.05      0.05    \n' % zvisc[jvisc]) 
        fid.write('    NDF  ><   NVB  >< CFXMIN ><  F_LK  >                                          \n')
        fid.write('    5.        1.0       -5.      0.0                                              \n')
        fid.write('  FPRIN0 >< FPRIN1 >< FPRIN2 >< FPRINB >                                          \n')
        fid.write('    1.        -9.      -9.       -2.                                              \n')
        fid.write('  FPLOT1 >< FPLOT2 >< FPLOT3 >< FPLOT4 >< FPLOT5 >< FPLOT6 >< FPLOT7 >< FPLOT8 >  \n')
        fid.write('    1.        1.        1.        1.        1.        1.        2.        2.      \n')
        fid.write('  CPMINW >< CPMINF >                                                              \n')
        fid.write('    -2.      -1.6                                                                 \n')
        fid.write('< NZOUT  >                                                                        \n')
        fid.write('    6.                                                                            \n')
        fid.write('< ZCPOUT >                                                                        \n')
        fid.write('   0.150                                                                          \n')
        fid.write('   0.250                                                                          \n')
        fid.write('   0.415                                                                          \n')
        fid.write('   0.500                                                                          \n')
        fid.write('   0.700                                                                          \n')
        fid.write('   0.950                                                                          \n')
        fid.write('  NCPOUT >                                                                        \n')
        fid.write('    20.                                                                           \n')
        fid.write('   CPOUT >                                                                        \n')
        fid.write('   -1.4                                                                           \n')
        fid.write('   -1.3                                                                           \n')
        fid.write('   -1.2                                                                           \n')
        fid.write('   -1.1                                                                           \n')
        fid.write('   -1.0                                                                           \n')
        fid.write('   -.9                                                                            \n')
        fid.write('   -.8                                                                            \n')
        fid.write('   -.7                                                                            \n')
        fid.write('   -.6                                                                            \n')
        fid.write('   -.5                                                                            \n')
        fid.write('   -.4                                                                            \n')
        fid.write('   -.3                                                                            \n')
        fid.write('   -.2                                                                            \n')
        fid.write('   -.1                                                                            \n')
        fid.write('    .0                                                                            \n')
        fid.write('    .1                                                                            \n')
        fid.write('    .2                                                                            \n')
        fid.write('    .3                                                                            \n')
        fid.write('    .4                                                                            \n')
        fid.write('    .5                                                                            \n')
        fid.write('    NIT  ><   MIT  ><   P1   ><   P2   ><   PL   ><   PH   ><   NLH  ><  FHALF >  \n')
        fid.write('    30.       30.      1.3       1.00      .7         1.5        3.         1.  \n')
        fid.write('    NBL  >                                                                      \n')
        fid.write('     4.                                                                         \n')
        fid.write('   NITBL ><   PB   ><  PBIV  >                                                  \n')
        fid.write('     6.       .8                                                                \n')
        fid.write('    12.       .8                                                                \n')
        fid.write('    18.       .8                                                                \n')
        fid.write('    24.       .8                                                                \n')
        fid.write('    NIT  ><   MIT  ><   P1   ><   P2   ><   PL   ><   PH   ><   NLH  ><  FHALF >\n')
        fid.write('    40.       30.      1.2       1.00      .7         1.5        4.         1.  \n')
        fid.write('    NBL  >                                                                      \n')
        fid.write('     6.                                                                         \n')
        fid.write('   NITBL ><   PB   ><  PBIV  >                                                  \n')
        fid.write('     6.       .7                                                                \n')
        fid.write('    12.       .7                                                                \n')
        fid.write('    18.       .7                                                                \n')
        fid.write('    24.       .7                                                                \n')
        fid.write('    30.       .7                                                                \n')
        fid.write('    36.       .7                                                                \n')
        fid.write('    NIT  ><   MIT  ><   P1   ><   P2   ><   PL   ><   PH   ><   NLH  ><  FHALF >\n')
        fid.write('    36.       30.      1.0       1.001     .7         1.5        5.         0.  \n')
        fid.write('    NBL  >                                                                      \n')
        fid.write('     5.                                                                         \n')
        fid.write('   NITBL ><   PB   ><  PBIV  >                                                  \n')
        fid.write('     6.       .55                                                                \n')
        fid.write('    12.       .55                                                                \n')
        fid.write('    18.       .55                                                                \n')
        fid.write('    24.       .55                                                               \n')
        fid.write('    30.       .55                                                               \n')
        fid.write('<  MACH  ><  ALFA  ><   RE   ><   CAX  ><  SWING ><   SE   >< ORDER  >          \n')
        fid.write('%8.3f%10.3f%10.0f.%10.3f%10.4f%10.4f%10.4f\n'% (M ,Ataque, rey, wMAC, wS/2, ise, order))
        fid.write('<  NSEC  >< PZROOT ><  PZTIP ><   PXLE ><   PXTE ><   PYTE ><   PZA  ><   PZB  >\n')
        fid.write('  4.00000   0.15000   0.25000   0.65000   0.65000   0.80000   0.00000   0.00000 \n')

        # ROOT SIMMETRY %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        fid.write('<    Z   ><   XLE  ><   YLE  ><  CHORD ><  THICK ><  ALPHA ><  FSEC  >          \n')
        fid.write('%9.4f %10.5f%10.5f%10.5f%10.5f%10.5f%10.5f\n' % (0,0,YE0+largfus*np.tan(rad*diedro),c0,1,ir,1))
        fid.write('<  YSYM  ><   NU   ><   NL   >                                                  \n')
        fid.write('%10.5f%10.5f%10.5f\n' % (0,nuroot,nlroot))
        fid.write(' <  XSING ><  YSING ><  TRAIL ><  SLOPT >\n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (0.00921,0,7.16234,-0.05857))
        fid.write(' <   XU   ><   YU   >\n')
        for j in range(len(xuroot)):
            fid.write('%10.5f%10.5f\n' % (xuroot[j], yuroot[j])) 
        fid.write(' <   XL   ><   YL   >\n')
        for j in range(len(xlroot)):
            fid.write('%10.5f%10.5f\n' % (xlroot[j], ylroot[j]))
        
        # ROOT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        fid.write('<    Z   ><   XLE  ><   YLE  ><  CHORD ><  THICK ><  ALPHA ><  FSEC  >          \n')
        fid.write('%9.4f %10.5f%10.5f%10.5f%10.5f%10.5f%10.5f\n' % (largfus,largfus*np.tan(rad*enf),YE0+largfus*np.tan(rad*diedro),cr,1,ir,1))
        fid.write('<  YSYM  ><   NU   ><   NL   >                                                  \n')
        fid.write('%10.5f%10.5f%10.5f\n' % (0,nuroot,nlroot))
        fid.write(' <  XSING ><  YSING ><  TRAIL ><  SLOPT >\n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (0.00921,0,7.16234,-0.05857))
        fid.write('<   XU   ><   YU   >\n')
        for j in range(len(xuroot)):
            fid.write('%10.5f%10.5f\n' % (xuroot[j], yuroot[j])) 
        fid.write(' <   XL   ><   YL   >\n')
        for j in range(len(xlroot)):
            fid.write('%10.5f%10.5f\n' % (xlroot[j], ylroot[j]))

        # % BREAK %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        fid.write('<    Z   ><   XLE  ><   YLE  ><  CHORD ><  THICK ><  ALPHA ><  FSEC  >          \n')
        fid.write('%9.4f %10.5f%10.5f%10.5f%10.5f%10.5f%10.5f\n' % (dist_quebra,(np.tan(rad*enf))*dist_quebra,YE0+dist_quebra*np.tan(rad*diedro),cq,1,iq,1))
        fid.write('<  YSYM  ><   NU   ><   NL   >                                                  \n')
        fid.write('%10.5f%10.5f%10.5f\n' % (0,nukink,nlkink))
        fid.write(' <  XSING ><  YSING ><  TRAIL ><  SLOPT >\n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (0.00800,0.00300,5.14083,-0.09346))
        fid.write(' <   XU   ><   YU   >\n')
        for j in range(len(xukink)):
            fid.write('%10.5f%10.5f\n' % (xukink[j], yukink[j])) 
        fid.write(' <   XL   ><   YL   >\n')
        for j in range(len(xlkink)):
            fid.write('%10.5f%10.5f\n' % (xlkink[j], ylkink[j]))

        # % TIP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        fid.write('<    Z   ><   XLE  ><   YLE  ><  CHORD ><  THICK ><  ALPHA ><  FSEC  >          \n')
        fid.write('%9.4f %10.5f%10.5f%10.5f%10.5f%10.5f%10.5f\n' % (wingb2,(np.tan(rad*enf))*(wingb2),YE0+wingb2*np.tan(rad*diedro),ct,1,it,1))
        fid.write('<  YSYM  ><   NU   ><   NL   >                                                  \n')
        fid.write('%10.5f%10.5f%10.5f\n' % (0,nutip,nltip))
        fid.write(' <  XSING ><  YSING ><  TRAIL ><  SLOPT >\n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (0.00249,0,4.39914,-0.12401))
        fid.write('<   XU   ><   YU   >\n')
        for j in range(len(xutip)):
            fid.write('%10.5f%10.5f\n' % (xutip[j], yutip[j])) 
        fid.write(' <   XL   ><   YL   >\n')
        for j in range(len(xltip)):
            fid.write('%10.5f%10.5f\n' % (xltip[j], yltip[j]))


        # % DADOS DA FUSELAGEM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        fid.write('<  xlew  ><  ylew  >                                                            \n')
        fid.write('  %5.3f     %5.3f \n' % (xle,ylew))
        fid.write('<  XLEF  ><  YLEF  ><  XTEF  ><  YTEF  ><  XTEF0 ><  ANSF  >                    \n')
        fid.write('  0.00000  -0.91662    %5.4f   %5.4f    %5.4f    26.0\n' % (lf,FusDiam/2-0.5,lf-0.25))
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  1 -                       \n')
        fid.write(' 0.40000   -0.83153   0.43867   1.00000\n')
        fid.write('<   NT   >                                                                      \n')
        fid.write('  53.00000\n')
        fid.write('<    Y   ><    Z   >                                                            \n')
        fid.write(' -1.27021  0.00000\n')
        fid.write(' -1.27004  0.01507\n')
        fid.write(' -1.26867  0.04518\n')
        fid.write(' -1.26593  0.07519\n')
        fid.write(' -1.26183  0.10504\n')
        fid.write(' -1.25634  0.13468\n')
        fid.write(' -1.24948  0.16402\n')
        fid.write(' -1.24124  0.19301\n')
        fid.write(' -1.23160  0.22157\n')
        fid.write(' -1.22057  0.24961\n')
        fid.write(' -1.20814  0.27707\n')
        fid.write(' -1.19431  0.30384\n')
        fid.write(' -1.17908  0.32985\n')
        fid.write(' -1.16245  0.35498\n')
        fid.write(' -1.14442  0.37913\n')
        fid.write(' -1.12501  0.40218\n')
        fid.write(' -1.10425  0.42402\n')
        fid.write(' -1.08215  0.44451\n')
        fid.write(' -1.05877  0.46352\n')
        fid.write(' -1.03416  0.48091\n')
        fid.write(' -1.00840  0.49655\n')
        fid.write(' -0.98158  0.51028\n')
        fid.write(' -0.95381  0.52197\n')
        fid.write(' -0.92522  0.53150\n')
        fid.write(' -0.89598  0.53877\n')
        fid.write(' -0.86625  0.54368\n')
        fid.write(' -0.83622  0.54618\n')
        fid.write(' -0.80609  0.54619\n')
        fid.write(' -0.77608  0.54354\n')
        fid.write(' -0.74642  0.53823\n')
        fid.write(' -0.71734  0.53034\n')
        fid.write(' -0.68904  0.52001\n')
        fid.write(' -0.66168  0.50739\n')
        fid.write(' -0.63541  0.49263\n')
        fid.write(' -0.61033  0.47591\n')
        fid.write(' -0.58654  0.45742\n')
        fid.write(' -0.56409  0.43732\n')
        fid.write(' -0.54301  0.41578\n')
        fid.write(' -0.52334  0.39296\n')
        fid.write(' -0.50508  0.36898\n')
        fid.write(' -0.48823  0.34400\n')
        fid.write(' -0.47280  0.31811\n')
        fid.write(' -0.45877  0.29144\n')
        fid.write(' -0.44612  0.26409\n')
        fid.write(' -0.43486  0.23613\n')
        fid.write(' -0.42495  0.20767\n')
        fid.write(' -0.41640  0.17877\n')
        fid.write(' -0.40918  0.14951\n')
        fid.write(' -0.40330  0.11996\n')
        fid.write(' -0.39873  0.09017\n')
        fid.write(' -0.39547  0.06021\n')
        fid.write(' -0.39352  0.03013\n')
        fid.write(' -0.39287  0.00000\n')
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  2 -                       \n')
        fid.write(' 0.76000   -0.75298   0.63910   1.00000\n')
        fid.write('<   NT   >                                                                      \n')
        fid.write('  38.00000\n')
        fid.write('<    Y   ><    Z   >                                                            \n')
        fid.write(' -1.39209  0.00000\n')
        fid.write(' -1.39094  0.04512\n')
        fid.write(' -1.38586  0.10508\n')
        fid.write(' -1.37672  0.16456\n')
        fid.write(' -1.36350  0.22326\n')
        fid.write(' -1.34622  0.28090\n')
        fid.write(' -1.32488  0.33716\n')
        fid.write(' -1.29949  0.39172\n')
        fid.write(' -1.27008  0.44421\n')
        fid.write(' -1.23669  0.49427\n')
        fid.write(' -1.19940  0.54149\n')
        fid.write(' -1.15830  0.58544\n')
        fid.write(' -1.11357  0.62567\n')
        fid.write(' -1.06539  0.66172\n')
        fid.write(' -1.01407  0.69311\n')
        fid.write(' -0.95995  0.71939\n')
        fid.write(' -0.90348  0.74014\n')
        fid.write(' -0.84519  0.75499\n')
        fid.write(' -0.78566  0.76367\n')
        fid.write(' -0.72554  0.76600\n')
        fid.write(' -0.66557  0.76143\n')
        fid.write(' -0.60655  0.74979\n')
        fid.write(' -0.54928  0.73139\n')
        fid.write(' -0.49442  0.70670\n')
        fid.write(' -0.44252  0.67629\n')
        fid.write(' -0.39397  0.64076\n')
        fid.write(' -0.34906  0.60072\n')
        fid.write(' -0.30796  0.55677\n')
        fid.write(' -0.27080  0.50946\n')
        fid.write(' -0.23761  0.45927\n')
        fid.write(' -0.20841  0.40665\n')
        fid.write(' -0.18319  0.35202\n')
        fid.write(' -0.16192  0.29573\n')
        fid.write(' -0.14458  0.23811\n')
        fid.write(' -0.13112  0.17946\n')
        fid.write(' -0.12154  0.12005\n')
        fid.write(' -0.11579  0.06015\n')
        fid.write(' -0.11388  0.00000\n')
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  3 -                       \n')
        fid.write(' 1.50500   -0.60064   0.94872   1.00000\n')
        fid.write('<   NT   >                                  \n')                                    
        fid.write('  36.00000\n')
        fid.write('<    Y   ><    Z   >                                                            \n')
        fid.write(' -1.54935 0.00000\n')
        fid.write(' -1.54681 0.07505\n')
        fid.write(' -1.53706 0.16462\n')
        fid.write(' -1.52004 0.25310\n')
        fid.write(' -1.49583 0.33989\n')
        fid.write(' -1.46454 0.42438\n')
        fid.write(' -1.42631 0.50597\n')
        fid.write(' -1.38134 0.58404\n')
        fid.write(' -1.32987 0.65799\n')
        fid.write(' -1.27220 0.72721\n')
        fid.write(' -1.20867 0.79110\n')
        fid.write(' -1.13970 0.84907\n')
        fid.write(' -1.06577 0.90056\n')
        fid.write(' -0.98743 0.94505\n')
        fid.write(' -0.90529 0.98207\n')
        fid.write(' -0.82004 1.01121\n')
        fid.write(' -0.73241 1.03212\n')
        fid.write(' -0.64318 1.04456\n')
        fid.write(' -0.55317 1.04839\n')
        fid.write(' -0.46328 1.04262\n')
        fid.write(' -0.37463 1.02663\n')
        fid.write(' -0.28834 1.00079\n')
        fid.write(' -0.20540 0.96563\n')
        fid.write(' -0.12667 0.92185\n')
        fid.write(' -0.05286 0.87020\n')
        fid.write('  0.01550 0.81152\n')
        fid.write('  0.07797 0.74660\n')
        fid.write('  0.13427 0.67626\n')
        fid.write('  0.18419 0.60125\n')
        fid.write('  0.22758 0.52229\n')
        fid.write('  0.26436 0.44004\n')
        fid.write('  0.29449 0.35512\n')
        fid.write('  0.31793 0.26812\n')
        fid.write('  0.33468 0.17959\n')
        fid.write('  0.34473 0.09004\n')
        fid.write('  0.34808 0.00000\n')
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  4 -                       \n')
        fid.write('  2.31900  -0.37244   1.259513   1.00000\n')
        fid.write('<   NT   >                                                                      \n')
        fid.write('  44.00000\n')
        fid.write('<    Y   ><    Z   >                                                            \n')
        fid.write(' -1.63195 0.00000\n')
        fid.write(' -1.62595 0.08975\n')
        fid.write(' -1.61332 0.17880\n')
        fid.write(' -1.59419 0.26669\n')
        fid.write(' -1.56876 0.35296\n')
        fid.write(' -1.53719 0.43719\n')
        fid.write(' -1.49970 0.51895\n')
        fid.write(' -1.45650 0.59785\n')
        fid.write(' -1.40782 0.67349\n')
        fid.write(' -1.35392 0.74550\n')
        fid.write(' -1.29506 0.81351\n')
        fid.write(' -1.23150 0.87716\n')
        fid.write(' -1.16356 0.93610\n')
        fid.write(' -1.09154 0.98998\n')
        fid.write(' -1.01577 1.03846\n')
        fid.write(' -0.93710 1.08208\n')
        fid.write(' -0.85616 1.12132\n')
        fid.write(' -0.77315 1.15599\n')
        fid.write(' -0.68831 1.18587\n')
        fid.write(' -0.60158 1.20972\n')
        fid.write(' -0.51329 1.22687\n')
        fid.write(' -0.42393 1.23709\n')
        fid.write(' -0.33405 1.23879\n')
        fid.write(' -0.24444 1.23106\n')
        fid.write(' -0.15583 1.21567\n')
        fid.write(' -0.06879 1.19301\n')
        fid.write('  0.01618 1.16351\n')
        fid.write('  0.09866 1.12763\n')
        fid.write('  0.17829 1.08580\n')
        fid.write('  0.25478 1.03847\n')
        fid.write('  0.32785 0.98602\n')
        fid.write('  0.39729 0.92884\n')
        fid.write('  0.46249 0.86686\n')
        fid.write('  0.52448 0.80168\n')
        fid.write('  0.58315 0.73348\n')
        fid.write('  0.63825 0.66237\n')
        fid.write('  0.68947 0.58843\n')
        fid.write('  0.73643 0.51170\n')
        fid.write('  0.77864 0.43227\n')
        fid.write('  0.81542 0.35019\n')
        fid.write('  0.84589 0.26556\n')
        fid.write('  0.86890 0.17862\n')
        fid.write('  0.88307 0.08982\n')
        fid.write('  0.88707 0.00000\n')


        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  5 -                       \n')
        fid.write('%8.7f %8.7f %8.7f 1.00000\n' % (lco,0.,raio))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yc))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))  

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  6 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (lco+0.10,0.,raio,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % (len(yc)))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))  

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  7 -                       \n')
        fid.write('%8.7f 0.000000  %8.7f 1.00000\n' % (lco+0.25,raio))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n'  % len(yc))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))  

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  8 -                       \n')
        fid.write('%9.8f 0.000000  %8.7f 1.00000\n' % (lco+1.,raio))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % (len(yc)))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))  
        xpos1=max(lco+1.2,xle-1.80)
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  9 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xpos1,0.,raio,1.0))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n'   % (len(yc))) 
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))  

        xpos2=max(xpos1+0.2,xle-1.20)
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  10 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xpos2,0.,raio,1.0))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % (len(yc)))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))  

        ywf2med = 0.50*(max(ywf2)+ min(ywf2))
        radius2 = max(ywf2)-ywf2med

        ywfmed   = 0.50*(max(ywf)+min(ywf))
        radiusf  = max(ywf)-ywfmed

        xpos3=max(xpos2+0.20,xle-1.0)
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  11 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xpos3,ywfmed,radiusf,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(ywf))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(ywf)):
            fid.write('%8.7f %8.7f\n' % (ywf[j], zwf[j])) 

        ywf1med   = 0.50*(max(ywf1)+min(ywf1))
        radiusf1  = max(ywf1) - ywf1med

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  12 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle-0.50,ywf1med,radiusf1,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(ywf1))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(ywf1)):
            fid.write('%8.7f %8.7f\n' % (ywf1[j], zwf1[j]))  

        # %fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  11 -                       \n')
        # %fid.write('%8.7f 0.000000  %8.7f 1.00000\n',xle-0.12,raio)
        # %fid.write('<   NT   >                                                                      \n')
        # %fid.write('%8.7f\n',size(yw,2))
        # %fid.write('<    Y   ><    Z   >                                                            \n') 
        # %fid.write('%8.7f %8.7f\n',[ywzw]) 

        ywmed   = 0.50*(max(yw)+min(yw))
        radiusw = max(yw)-ywmed

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  13 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle-0.1,ywmed,radiusw,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yw))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yw)):
            fid.write('%8.7f %8.7f\n' % (yw[j], zw[j])) 

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  14 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle,ywmed,radiusw,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yw))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yw)):
            fid.write('%8.7f %8.7f\n' % (yw[j], zw[j])) 

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  15 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+c0/4.,ywmed,radiusw,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yw))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yw)):
            fid.write('%8.7f %8.7f\n' % (yw[j], zw[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  16 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+c0/2.,ywmed,radiusw,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yw))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yw)):
            fid.write('%8.7f %8.7f\n' % (yw[j], zw[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  17 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+3*c0/4,ywmed,radiusw,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yw))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yw)):
            fid.write('%8.7f %8.7f\n' % (yw[j], zw[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  18 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+c0+0.20,ywmed,radiusw,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yw))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yw)):
            fid.write('%8.7f %8.7f\n' % (yw[j], zw[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  19 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+c0+0.80,ywf1med,radiusf1,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(ywf1))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(ywf1)):
            fid.write('%8.7f %8.7f\n' % (ywf1[j], zwf1[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  20 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+c0+1.50,ywfmed,radiusf,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n'% len(ywf))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(ywf)):
            fid.write('%8.7f %8.7f\n' % (ywf[j], zwf[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  21 -                       \n')
        fid.write('%10.5f%10.5f%10.5f%10.5f\n' % (xle+c0+1.80,ywf2med,radius2,1.))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(ywf2))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(ywf2)):
            fid.write('%8.7f %8.7f\n' % (ywf2[j], zwf2[j]))

        xpos10=0.50*((xle+c0+1.80)+(lco+lcab))
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  22 -                       \n')
        fid.write('%8.7f 0.000000  %8.7f 1.00000\n' % (xpos10,raio))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yc))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  23 -                       \n')
        fid.write('%8.7f 0.000000  %8.7f 1.00000\n' % (lco+lcab,raio))
        fid.write('<   NT   >                                                                      \n')
        fid.write('%8.7f\n' % len(yc))
        fid.write('<    Y   ><    Z   >                                                            \n') 
        for j in range(len(yc)):
            fid.write('%8.7f %8.7f\n' % (yc[j], zc[j]))
        
        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  24 -                       \n')
        fid.write('%8.7f %8.7f %8.7f 1.00000\n' % (lf-0.90,FusDiam/2-0.25,0.25))
        fid.write('<   NT   >                                                                      \n')
        fid.write(' %8.7f\n' % 11.0)
        fid.write('<    Y   ><    Z   >                                                            \n')  
        fid.write('%8.7f 0.00000\n' % (raio-0.50))
        fid.write('%8.7f 0.05000\n' % (raio-0.50))
        fid.write('%8.7f 0.12000\n' % (raio-0.50))
        fid.write('%8.7f 0.12500\n' % (raio-0.45))
        fid.write('%8.7f 0.12500\n' % (raio-0.40))
        fid.write('%8.7f 0.12500\n' % (raio-0.30))
        fid.write('%8.7f 0.12500\n' % (raio-0.25))
        fid.write('%8.7f 0.12500\n' % (raio-0.05))
        fid.write('%8.7f 0.12000\n' % raio)
        fid.write('%8.7f 0.05000\n' % raio)
        fid.write('%8.7f 0.00000\n' % raio)

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  25 -                       \n')
        fid.write('%8.7f %8.7f %8.7f 1.00000\n' % (lf-0.75,raio-0.25,0.25))
        fid.write('<   NT   >                                                                      \n')
        fid.write(' %8.7f\n' % 11.0)
        fid.write('<    Y   ><    Z   >                                                            \n')  
        fid.write('%8.7f 0.00000\n' % (raio-0.50))
        fid.write('%8.7f 0.05000\n' % (raio-0.50))
        fid.write('%8.7f 0.12000\n' % (raio-0.50))
        fid.write('%8.7f 0.12500\n' % (raio-0.45))
        fid.write('%8.7f 0.12500\n' % (raio-0.40))
        fid.write('%8.7f 0.12500\n' % (raio-0.30))
        fid.write('%8.7f 0.12500\n' % (raio-0.25))
        fid.write('%8.7f 0.12500\n' % (raio-0.05))
        fid.write('%8.7f 0.12000\n' % raio)
        fid.write('%8.7f 0.05000\n' % raio)
        fid.write('%8.7f 0.00000\n' % raio)

        fid.write('<   XF   ><   YF   ><   RF   >< FCONT  >   - section  26 -                       \n')
        fid.write('%8.7f %8.7f %8.7f 1.00000\n' % (lf-0.5,raio-0.25,0.25))
        fid.write('<   NT   >                                                                      \n')
        fid.write(' %8.7f\n' % 11.0)
        fid.write('<    Y   ><    Z   >                                                            \n')  
        fid.write('%8.7f 0.00000\n' % (raio-0.50))
        fid.write('%8.7f 0.05000\n' % (raio-0.50))
        fid.write('%8.7f 0.12000\n' % (raio-0.50))
        fid.write('%8.7f 0.12500\n' % (raio-0.45))
        fid.write('%8.7f 0.12500\n' % (raio-0.40))
        fid.write('%8.7f 0.12500\n' % (raio-0.30))
        fid.write('%8.7f 0.12500\n' % (raio-0.25))
        fid.write('%8.7f 0.12500\n' % (raio-0.05))
        fid.write('%8.7f 0.12000\n' % raio)
        fid.write('%8.7f 0.05000\n' % raio)
        fid.write('%8.7f 0.00000\n' % raio)
        fid.close()

    return()






