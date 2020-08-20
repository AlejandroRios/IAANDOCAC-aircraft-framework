"""" 
Title     : Wetted area wing
Written by: Alejandro Rios
Date      : 13/11/19
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

########################################################################################
"""Constants declaration"""
########################################################################################


def wetted_area_wing(ediam,wingloc,FusDiam,Ccentro,Craiz,Cquebra,
    Cponta,semispan,sweepLE,iroot,ikink,itip,xle,yposeng,wingdi,wtaper,
    fileToRead1,fileToRead2,fileToRead3):
    # Calcula area exposta ada asa
    rad  = np.pi/180
    #
    raio = FusDiam/2

    tanaux=np.tan(rad*sweepLE)


    airfoil_names= [fileToRead1,fileToRead2,fileToRead3]
    airfoil_chords = [Craiz,Cquebra,Cponta] 

    ########################################################################################
    """Pre-processing airfoils"""
    ########################################################################################
    airfoils = {1:{},
                    2:{},
                    3:{}}

    panel_number = 201
        
    for i in range(len(airfoils)):
            j = i+1
            airfoils[j]['name'] = airfoil_names[i]
            airfoils[j]['chord'] = airfoil_chords[i]

    for i in airfoils:
            airfoil = i
            airfoil_name = airfoils[airfoil]['name']
            airfoil_preprocessing(airfoil_name,panel_number)


    ########################################################################################
    """Importing Data"""
    ########################################################################################
    # Load airfoil coordinates
    df = pd.read_table(""+ airfoil_names[0] +'.dat' ,header=None,skiprows=[0],sep=',')
    df.columns = ['x','y']
    df_head = df.head()
    n_coordinates = len(df)

    # Compute distance between consecutive points
    dx = []
    dy = []
    ds = []
    ds_vector = []
    ds=np.zeros((n_coordinates,1))
    ds[0] = 0 

    for i in range(1,n_coordinates):
        dx = df.x[i] - df.x[i-1]
        dy = df.y[i] - df.y[i-1]
        ds[i] = ds[i-1]  + np.sqrt(dx*dx+dy*dy)

    xa = df.x[0]
    xb = df.x[1]
    ind = 0

    # Find leading edge index
    while xb < xa:
        ind = ind + 1
        xa = df.x[ind]
        xb = df.x[ind+1]

    n_panels_x = 51
    xp = np.linspace(0,1,n_panels_x)
    xp = np.flip((np.cos(xp*np.pi)/2+0.5))


    # Interpolate upper skin
    dsaux = ds[0:ind+1]
    xaux = df.x[0:ind+1]

    dsaux = np.reshape(dsaux,-1)
    ds = np.reshape(ds,-1)

    dsinterp = interpolate.interp1d(xaux,dsaux, kind='slinear',fill_value='extrapolate')(xp)
    yupp_root = interpolate.interp1d(ds,df.y, kind='slinear')(dsinterp)

    # Interpolate lower skin
    dsaux = []
    dsaux = ds[ind:n_coordinates]
    dsinterp = []
    xaux = df.x[ind:n_coordinates]

    dsinterp = interpolate.interp1d(xaux,dsaux, kind='slinear',fill_value='extrapolate')(xp)
    ylow_root= interpolate.interp1d(ds,df.y, kind='slinear')(dsinterp)

    xproot = np.array([np.flip(xp),xp])
    xproot = xproot.ravel()
    yproot = np.array([np.flip(yupp_root),ylow_root])
    yproot = yproot.ravel()
    esspraiz=max(yupp_root)-min(ylow_root);
    # plt.figure()
    # plt.plot(xproot,yproot,'bo')

    ########################################################################################
    # Load airfoil coordinates
    df = pd.read_table(""+ airfoil_names[1] +'.dat' ,header=None,skiprows=[0],sep=',')
    df.columns = ['x','y']
    df_head = df.head()
    n_coordinates = len(df)

    # Compute distance between consecutive points
    dx = []
    dy = []
    ds = []
    ds_vector = []
    ds=np.zeros((n_coordinates,1))
    ds[0] = 0 

    for i in range(1,n_coordinates):
        dx = df.x[i] - df.x[i-1]
        dy = df.y[i] - df.y[i-1]
        ds[i] = ds[i-1]  + np.sqrt(dx*dx+dy*dy)

    xa = df.x[0]
    xb = df.x[1]
    ind = 0

    # Find leading edge index
    while xb < xa:
        ind = ind + 1
        xa = df.x[ind]
        xb = df.x[ind+1]

    n_panels_x = 51
    xp = np.linspace(0,1,n_panels_x)
    xp = np.flip((np.cos(xp*np.pi)/2+0.5))


    # Interpolate upper skin
    dsaux = ds[0:ind+1]
    xaux = df.x[0:ind+1]

    dsaux = np.reshape(dsaux,-1)
    ds = np.reshape(ds,-1)

    dsinterp = interpolate.interp1d(xaux,dsaux, kind='slinear',fill_value='extrapolate')(xp)
    yupp_kink = interpolate.interp1d(ds,df.y, kind='slinear')(dsinterp)

    # Interpolate lower skin
    dsaux = []
    dsaux = ds[ind:n_coordinates]
    dsinterp = []
    xaux = df.x[ind:n_coordinates]

    dsinterp = interpolate.interp1d(xaux,dsaux, kind='slinear',fill_value='extrapolate')(xp)
    ylow_kink= interpolate.interp1d(ds,df.y, kind='slinear')(dsinterp)

    xpkink = np.array([np.flip(xp),xp])
    xpkink = xpkink.ravel()
    ypkink = np.array([np.flip(yupp_kink),ylow_kink])
    ypkink = ypkink.ravel()

    # plt.plot(xpkink,ypkink,'ro')

    ########################################################################################
    # Load airfoil coordinates
    df = pd.read_table(""+ airfoil_names[2] +'.dat' ,header=None,skiprows=[0],sep=',')
    df.columns = ['x','y']
    df_head = df.head()
    n_coordinates = len(df)

    # Compute distance between consecutive points
    dx = []
    dy = []
    ds = []
    ds_vector = []
    ds=np.zeros((n_coordinates,1))
    ds[0] = 0 

    for i in range(1,n_coordinates):
        dx = df.x[i] - df.x[i-1]
        dy = df.y[i] - df.y[i-1]
        ds[i] = ds[i-1]  + np.sqrt(dx*dx+dy*dy)

    xa = df.x[0]
    xb = df.x[1]
    ind = 0

    # Find leading edge index
    while xb < xa:
        ind = ind + 1
        xa = df.x[ind]
        xb = df.x[ind+1]

    n_panels_x = 51
    xp = np.linspace(0,1,n_panels_x)
    xp = np.flip((np.cos(xp*np.pi)/2+0.5))


    # Interpolate upper skin
    dsaux = ds[0:ind+1]
    xaux = df.x[0:ind+1]

    dsaux = np.reshape(dsaux,-1)
    ds = np.reshape(ds,-1)

    dsinterp = interpolate.interp1d(xaux,dsaux, kind='slinear',fill_value='extrapolate')(xp)
    yupp_tip = interpolate.interp1d(ds,df.y, kind='slinear')(dsinterp)

    # Interpolate lower skin
    dsaux = []
    dsaux = ds[ind:n_coordinates]
    dsinterp = []
    xaux = df.x[ind:n_coordinates]

    dsinterp = interpolate.interp1d(xaux,dsaux, kind='slinear',fill_value='extrapolate')(xp)
    ylow_tip= interpolate.interp1d(ds,df.y, kind='slinear')(dsinterp)

    xptip = np.array([np.flip(xp),xp])
    xptip = xptip.ravel()
    yptip = np.array([np.flip(yupp_tip),ylow_tip])
    yptip = yptip.ravel()

    ########################################################################################
    ########################################################################################
    #=====> Wing
    if wingloc ==1:
        wingpos=-0.48*raio
        engzpos=-0.485*raio
    else:
        wingpos=raio-Ccentro*1.15*0.12/2
        engzpos=wingpos-0.10*ediam/2

    # Rotate root section according to given incidence
    teta=-iroot # - points sky + points ground
    tetar=teta*rad
    xproot=xproot*np.cos(tetar)-yproot*np.sin(tetar)
    yproot=xproot*np.sin(tetar)+yproot*np.cos(tetar)

    # Rotates kink station airfoil
    teta  =-ikink
    tetar =teta*rad
    xpkink=xpkink*np.cos(tetar)-ypkink*np.sin(tetar)
    ypkink=xpkink*np.sin(tetar)+ypkink*np.cos(tetar)

    # Rotates tip airfoil
    teta  =-itip
    tetar =teta*rad
    xptip=xptip*np.cos(tetar)-yptip*np.sin(tetar)
    yptip=xptip*np.sin(tetar)+yptip*np.cos(tetar)
    deltax=semispan*tanaux

    maxcota=-0.48*(FusDiam/2)+1.15*Ccentro*esspraiz
    yraiz=np.sqrt((FusDiam/2)**2 - maxcota**2)


    xleraiz=xle+yraiz*tanaux
    xlequebra=xle+semispan*yposeng*tanaux


    xistosxper = np.block([[xle+Ccentro*xproot], [xleraiz+Craiz*xproot], [xlequebra+Cquebra*xpkink], [xle+deltax+Cponta*xptip]])

    xistoszper = np.block([[(wingpos+Ccentro*yproot)], [wingpos+Craiz*yproot], [(wingpos+(yposeng*semispan*np.tan(rad*wingdi))+ Cquebra*ypkink)], [(semispan*np.tan(rad*wingdi)+wingpos+Ccentro*wtaper*yptip)]])

    sizex=len(xproot)

    yper1 = np.zeros(sizex)
    yper2 = np.ones(sizex)*yraiz
    yper3 = np.ones(sizex)*(semispan*yposeng)
    #yper3(1:sizex(2))=semispan-df/2
    yper4 = np.ones(sizex)*semispan
    xistosyper=np.block([[yper1], [yper2], [yper3], [yper4]])

    # C
    #surface(xistosxper,xistosyper,xistoszper,'FaceLighting','gouraud','EdgeColor','none','FaceColor','blue')
    #surface(xistosxper,-xistosyper,xistoszper,'FaceLighting','gouraud','EdgeColor','none','FaceColor','blue')
    #
    ##=== End wing
    #axis equal

    xuroot = xp
    xlroot = xp

    xukink = xp
    xlkink = xp

    xutip = xp
    xltip = xp
    
    areawingwet= calcareawet(xistosxper,xistosyper,xistoszper)
    return(areawingwet, xutip, yupp_tip, xltip, ylow_tip,
    xukink,yupp_kink,xlkink,ylow_kink, xuroot,yupp_root,xlroot,ylow_root)

def calcareawet(xistosXper,xistosYper,xistosZper):
    # Calcula área exposta da asa (m2)
    [m, n]=(xistosXper.shape)

    areas1 = []
    areas2 = []
    areawet1 = []
    areawet2 = []
    # for j=2:(m-1):
    for j in range(1,m-1):
        # for i=1:(n-1):
        for i in range(0,n-1):
            x1=xistosXper[j,i]
            y1=xistosYper[j,i]
            z1=xistosZper[j,i]
            
            x2=xistosXper[j,i+1]
            y2=xistosYper[j,i+1]
            z2=xistosZper[j,i+1]
            
            x3=xistosXper[j+1,i+1]
            y3=xistosYper[j+1,i+1]
            z3=xistosZper[j+1,i+1]
            
            Stri1=tri3darea(x1,y1,z1,x2,y2,z2,x3,y3,z3)
        
            areawet1 = abs(Stri1)
            
            x1=xistosXper[j,i+1]
            y1=xistosYper[j,i+1]
            z1=xistosZper[j,i+1]
            
            x2=xistosXper[j+1,i]
            y2=xistosYper[j+1,i]
            z2=xistosZper[j+1,i]
            
            x3=xistosXper[j+1,i+1]
            y3=xistosYper[j+1,i+1]
            z3=xistosZper[j+1,i+1] 
            
            Stri2=tri3darea(x1,y1,z1,x2,y2,z2,x3,y3,z3)
        
            areawet2 = abs(Stri2)
            areas1.append(areawet1)
            areas2.append(areawet2)

    total_area = sum(areas1+areas2)
    total_area = total_area*2
    return(total_area)

def tri3darea(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    # Calcula area de um triangulo a partir das coordendas dos vertices

    a1=x1-x2
    a2=y1-y2
    a3=z1-z2

    b1=x3-x2
    b2=y3-y2
    b3=z3-z2

    axb1=(a2*b3-a3*b2)
    axb2=(a3*b1-a1*b3)
    axb3=(a1*b2-a2*b1)

    Stri=0.50*np.sqrt(axb1**2 +axb2**2 + axb3**2)
    return(Stri)





