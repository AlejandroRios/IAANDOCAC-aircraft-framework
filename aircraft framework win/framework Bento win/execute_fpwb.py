"""
Function  : execute_fpwb.py
Title     : Execute fpwb full potential method
Written by: Alejandro Rios
Date      : November/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module takes as input the fpwb input file and execute fpwb to obtain the output file 
        whith aerodynamic information

Future implementations:
    - 

Inputs:
    - time check
    - checks to kill
    - input file for fpwb
Outputs:
    - fpwb output files
"""

########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
import os
import subprocess
########################################################################################

def execute_fpwb(time2check,checks2kill,arq_input):

    execute  = "fpwb.exe"
    comando = execute + ' ' + arq_input
    if not time2check or not checks2kill or time2check == 0 or checks2kill == 0:
        subprocess.call(comando, shell=True)
    else:
        #Verify prior fpwb tasks
        # b = subprocess.check_output(['ps'])
        # b = b.decode("utf-8")
        # index_before = b.find('fpwb')
        comando1=execute + ' ' + arq_input + ' ' +  '&'
        #Running fpwb independently
        p = subprocess.Popen(comando1, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        #This makes the wait possible
        p_status = p.wait() 

        #Verify new tasks list
        # b = subprocess.check_output(['ps'])
        # b = b.decode("utf-8") 
        # index_later = b.find('fpwb')
    
    return

