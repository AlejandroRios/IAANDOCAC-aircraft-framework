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
import subprocess
########################################################################################

def execute_fpwb(time2check,checks2kill,arq_input):
    # 
        #This function is responsible to kill crashed Xfoil programs
    execute  = "wine fpwb.exe"

    
    comando = execute + ' ' + arq_input
    # subprocess.call("wine fpwb.exe fpwbclm1.inp", shell=True)

    if not time2check or not checks2kill or time2check == 0 or checks2kill == 0:
    #     
        #Just run FPWB
        
        subprocess.call(comando, shell=True)
    
    else:
        
        #Verify prior fpwb tasks
        b = subprocess.check_output(['ps'])
        b = b.decode("utf-8")
        index_before = b.find('fpwb')
        comando1=execute + ' ' + arq_input + ' ' +  '&'
        #Running fpwb independently
        p = subprocess.Popen(comando1, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        #This makes the wait possible
        p_status = p.wait() 

        #Verify new tasks list
        b = subprocess.check_output(['ps'])
        b = b.decode("utf-8") 
        index_later = b.find('fpwb')

