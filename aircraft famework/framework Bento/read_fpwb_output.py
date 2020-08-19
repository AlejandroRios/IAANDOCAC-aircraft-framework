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
import pandas as pd
import os
from scipy import interpolate
from area_triangle_3d import area_triangle_3d
from airfoil_preprocessing import airfoil_preprocessing
import matplotlib.pyplot as plt
import mmap
import sys
from itertools import islice
########################################################################################

def find(substr, infile):
    with open(infile) as a:
        num_line = []       
        for num, line in enumerate(a, 1):
            if substr in line:               
                num_line = num
    return(num_line)

def read(line_num, infile):
    with open(infile) as lines:
        for line in islice(lines, line_num, line_num+1):
            line_saida = line.split()
            line.split(',')
        # line_saida = [line.split() for line in islice(lines, line_num, line_num+1)]
    return(line_saida)

def read_fpwb_output(ybreaksta,diamfus,meia_env,airfoil_info):
    #   Leitura do CD, Momento Fletor e Calculo do CLMAX
    #clc
    CLMAX      = 0
    CLALFA_rad = 0
    nstat      = 21
    K_IND      = 1000
    CD0        = 1E06
    estaestol = 1 # estacao da envergadura onde ocorre o inicio do estol (fracao da enverghadura)
    #
    #ybreaksta = dist_quebra/(meia_env)
    # estacao da ponta
    #yetaponta=(env/2)/(env/2+envergadurarake) # with raked wingtip
    yetaponta=1 # with no raked wingtip
    #
    #  calcula clmax da asa-fuselagem
    # Inicialmente faz leitura da saida do BLWF para a primeira condicao
    #
    error1 = 1
    error2 = 1
    #
    arq_output = 'fpwbclm1.out'

    # with open(arq_output, 'rb', 0) as file:
    #     mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as file:
    end_file = find('The end', arq_output) 

    print(end_file)
    if end_file >= 0:
        error1 = 0

    if error1 == 1:
        return
    else:
        to_find = 'MACH'
        line_num = find(to_find, arq_output)

        data = pd.read_csv(arq_output, skiprows = line_num-1, nrows =1 , delim_whitespace=True)
        ALFA1 = data.ALPHA

        to_find = 'CHORD'
        line_num = find(to_find, arq_output)

        data = pd.read_csv(arq_output, skiprows = line_num-1, nrows = nstat, delim_whitespace=True)
        Zestacao1 = data.Z
        CLestacao1 = data.CL
        Chordestacao1 = data.CHORD

        to_find = 'CDIND'
        line_num = find(to_find, arq_output)

        data = pd.read_csv(arq_output, skiprows = line_num, nrows =1 , delim_whitespace=True, header =None)
        

        data.columns = ['CL','CDIND','CDWAVE','CDP','CMZ','CDFP','CDFU','CDFL']
        CL1  = data.CL
        CD1 = data.CDIND + data.CDWAVE + data.CDP

    #=================================================================
    # Leitura da distribuicao de cl para alpha2
    if error1 == 0:
        #
        arq_output = 'fpwbclm2.out'
        end_file = find('The end', arq_output) 

        print(end_file)
        if end_file >= 0:
            error2 = 0

        if error2 == 1:
            return
        else:
            to_find = 'MACH'
            line_num = find(to_find, arq_output)

            data = pd.read_csv(arq_output, skiprows = line_num-1, nrows =1 , delim_whitespace=True)
            ALFA2 = data.ALPHA
            to_find = 'CHORD'
            line_num = find(to_find, arq_output)

            data = pd.read_csv(arq_output, skiprows = line_num-1, nrows = nstat, delim_whitespace=True)
            Zestacao2 = data.Z
            CLestacao2 = data.CL
            Chordestacao2 = data.CHORD


            to_find = 'CDIND'
            line_num = find(to_find, arq_output)

            data = pd.read_csv(arq_output, skiprows = line_num, nrows =1 , delim_whitespace=True, header =None)
        

            data.columns = ['CL','CDIND','CDWAVE','CDP','CMZ','CDFP','CDFU','CDFL']
            CL2  = data.CL
            CD2 = data.CDIND + data.CDWAVE + data.CDP
            CLALFA_rad = ((CL2-CL1)/(ALFA2-ALFA1))*180/np.pi

            Clalfa = []
            Clzero = []
            for k in range(nstat):
                Clalfa_aux=(CLestacao2[k]-CLestacao1[k])/(ALFA2-ALFA1)
                Clalfa.append(Clalfa_aux)
                Clzero_aux=CLestacao2[k]-Clalfa_aux*ALFA2
                Clzero.append(Clzero_aux)



        # Arrassto CD0 e fator k dor arrasto induzido CD=CD0 + k*CL^2
            K_IND = (CD1-CD2)/(CL1**2-CL2**2)
            CD0   = CD1-K_IND*(CL1**2)
            # descobre o menor alfa no qual uma estacao atinge o cl maximo 2D
            alfamin=10000
            clr=airfoil_info[1]['Clmax']
            clq=airfoil_info[2]['Clmax']
            clp=airfoil_info[3]['Clmax']
            #alfacomp=zeros(1,nstat)

            for k in range(nstat):
                if Zestacao2[k] > yetaponta:
                    alfa=10000
                else:
                    if Zestacao2[k] <= ybreaksta:
                        gradcl        = (clr-clq)/(0-ybreaksta)
                        Clcomp        = clr+gradcl*(Zestacao2[k]-0)
                        #gradalfa_airf =(inc_root-inc_kink)/(0-ybreaksta)
                        #alfa0         = inc_root
                        #alfacomp(k)   = alfa0 + gradalfa_airf*(Zestacao2(k)-0)
                    else:
                        gradcl        = (clq-clp)/(ybreaksta-yetaponta)
                        Clcomp        = clq+gradcl*(Zestacao2[k]-ybreaksta)
                        #gradalfa_airf = (inc_kink-inc_tip)/(ybreaksta-1)
                        #alfa0         = inc_kink
                        #alfacomp(k)   = alfa0 + gradalfa_airf*(Zestacao2(k)-ybreaksta)

                #
                    alfa=np.asarray((Clcomp-Clzero[k])/Clalfa[k])

               
                if alfa < alfamin:
                    alfamin_aux = alfa
                    estaestol = Zestacao2[k]

        #    Extrapolacao do cl na linha de centro
            cl1 = Clzero[0]   + Clalfa[0]*alfamin
            cl2 = Clzero[1]   + Clalfa[1]*alfamin
            inclina = (cl2-cl1)/(Zestacao2[1]-Zestacao2[0])
            clcentro=cl1 + inclina*(0-Zestacao2[0])
            CLMAX=0.50*(clcentro + Clzero[0] + Clalfa[0]*alfamin)*Zestacao2[0]
            # Calculo do Cl no restante da asa
            for k in range(nstat-1):
                cl1=Clzero[k]   + Clalfa[k]*alfamin
                cl2=Clzero[k+1] + Clalfa[k+1]*alfamin
                CLMAX=CLMAX     + 0.50*(cl1+cl2)*(Zestacao2[k+1]-Zestacao2[k])


    # #
    # figure(13)
    # hold on
    # xclmax(1)=0
    # xclmax(2)=(diamfus/2)/(meia_env)
    # xclmax(3)=ybreaksta
    # xclmax(4)=1
    # yclmax(1)=clr
    # yclmax(2)=clr
    # yclmax(3)=clq
    # yclmax(4)=clp
    # #
    # xistosclmaxairfoil=clmax_airfoil
    # xistosxclmax=xclmax
    # xistosyclmax=yclmax
    # #
    # plot(xclmax,yclmax,'-gs')
    # # hold on
    # xclmax=[0 Zestacao1]
    # yclmax=[clcentro (Clzero(1:21)+Clalfa(1:21)*alfamin)]
    # plot(xclmax,yclmax,'--rs')
    # title('Wing-body CLmax Calculation with FPWB')
    # xlabel('eta')
    # ylabel('Cl')
    # clmaxstr1=num2str(CLMAX,'#4.2f')
    # clmaxstr2='CLMAX = '
    # clmaxstr=[clmaxstr2 clmaxstr1]
    # text(0.50,1.4,clmaxstr)
    # #
    # if exist('cldistribution.jpg') > 0 ##ok<EXIST>
    # delete ('cldistribution.jpg')
    # end
    # #
    # nomeclmax='cldistspan.jpg'
    # #print(hfig13,nomeclmax,'-djpeg','-r300')
    # print -djpeg -f13 -r300 '../Figures/cldistribution.jpg'
    # close(figure(13))
    # clear xclmax yclmax Clzero Clalfa Zestacao2
    # clear clmaxstr1 clmaxstr2 clmaxstr CD1 CD2
    # end # function

    return(CD0, K_IND, CLALFA_rad, CLMAX, estaestol,error1,error2)