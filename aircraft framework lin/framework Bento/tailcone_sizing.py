"""" 
Title     : Tail cone sizing
Written by: Alejandro Rios
Date      : 08/11/19
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
########################################################################################


def tailcone_sizing(NPax,PEng,fuse_height,fuse_width):
    #  Provide a sizing of the tailcone
    fusext   = 0
    if NPax <= 50:
        #passenger baggage 200 kg/m3 e 20 kg por pax
        bagvol=NPax*20/200   # m3

    if PEng == 2:
        ltail_df=2.25  
    else:
        ltail_df=2.0 # relacao coni/diametro Roskam vol 2 pag 110

    ltail = ltail_df*fuse_width+fusext
    
    return(ltail)
