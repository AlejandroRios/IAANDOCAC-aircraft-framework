"""" 
Title     : Fuselage cross section 
Written by: Alejandro Rios
Date      : 05/12/19
Language  : Python
Aeronautical Institute of Technology


Inputs:
hp: pressure-altitude [ft]
ISADEV: ISA temperature deviation

Outputs:
atm(1)=temperatura isa [K]
atm(2)=teta 
atm(3)=delta
atm(4)=sigma
atm(5)=pressure [KPa]
atm(6)=air density [Kg/m2]
atm(7)=sound speed [m/s]
atm(8)= air viscosity

"""
########################################################################################
"""Importing Modules"""
########################################################################################
import numpy as np
import math
########################################################################################

def fuselage_cross_section(container_type,NCorr,NSeat_i,CabHeightm,
    SEATwid,AisleWidth,widthreiratio,igraph):
    #--------------------------------------------------------------------------
    # This routine works this way : several important points describing seat arrangment, 
    # the passenger sillouette,and clearances required inside the cabin. 
    # The coordinates of these points dep# end on at least 2 parameters :
    # "delta_z_symetry," which is
    # the distance between the floor and the X axis, and "floor_thickness" that
    # describes the thickness of the floor
    # The first parameter is free whereas the seconds dep# ends on the 
    # fuselage equivalent diameter
    # This routine will find the best value of "delta_z_symetry" with a dichotomy,
    # in order to get the smallest value for
    # the equivalent diameter of the fuselage. If the equivalent diameter 
    # is the small then the drag and weight are low.
    #--------------------------------------------------------------------------
    # Conversion factors
    inch2m=0.0254 # Inch to meter
    #--------------------------------------------------------------------------
    # FUSELAGE_DZ_floor = absolute vertical (z) coordinate of the floor (a positive
    #                     input, must receive a minus sign)
    # NCorr = Number of aisles
    # NSeat =  Seating abreast (can be modified inside this routine)
    # AisleWidth = width of Aisle(s)
    # CabHeightm = Cabin height (cabin floor to ceiling)  
    # SEATwid = width of chair
    # widthreiratio = cabin height-to-width ratio
    # igraph: key to display graphs 
    #--------------------------------------------------------------------------
    # Design parameters
    armrest_top        = 22   #[inch]
    armrest_bot        = 7    # [inch]
    SEAT_t_cushion_YC  = 0.14 # (m)
    double_container   = 'no'
    PAX_d_hw           = 0.06 # [m]
    PAX_d_sw           = 0.04 # [m]
    PAX_w_shoulder     = 0.53 # [m]
    PAX_Dy_eye         = 0.87 # [m]
    PAX_Dy_midshoulder = 0.70 # [m]
    Backrest_height    = 0.59 # [m]
    floor_thickness    = 0.117# [m]
    NSeat              = NSeat_i
    iterations         = 12
    #--------------------------------------------------------------------------
    #



    if double_container is 'no':
        if container_type is 'None':
                LOWERDECK_w_ldtop = 0
                LOWERDECK_w_ldbottom = 0  
                LOWERDECK_h_ld = 0  
        elif container_type is 'none':
                LOWERDECK_w_ldtop = 0
                LOWERDECK_w_ldbottom = 0  
                LOWERDECK_h_ld = 0 
        elif container_type is 'LD1':
                LOWERDECK_w_ldbottom = 1.56   
                LOWERDECK_w_ldtop = 2.44
                LOWERDECK_h_ld = 1.68
        elif container_type is 'LD11':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 3.28
                LOWERDECK_h_ld = 1.68   
        elif container_type is  'LD2':
                LOWERDECK_w_ldbottom = 1.19   
                LOWERDECK_w_ldtop = 1.66
                LOWERDECK_h_ld = 1.68  
        elif container_type is  'LD26':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.16
                LOWERDECK_h_ld = 1.68 
        elif container_type is 'LD29':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.82
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD3':
                LOWERDECK_w_ldbottom = 1.56   
                LOWERDECK_w_ldtop = 2.11
                LOWERDECK_h_ld = 1.68
        elif container_type is 'LD3-45':
                LOWERDECK_w_ldbottom = 1.56   
                LOWERDECK_w_ldtop = 2.11
                LOWERDECK_h_ld = 1.19
        elif container_type is  'LD3-45R':
                LOWERDECK_w_ldbottom = 1.56   
                LOWERDECK_w_ldtop = 1.66
                LOWERDECK_h_ld = 1.19
        elif container_type is  'LD3-45W':
                LOWERDECK_w_ldbottom = 1.43   
                LOWERDECK_w_ldtop = 2.53
                LOWERDECK_h_ld = 1.14
        elif container_type is  'LD39':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.82
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD4':
                LOWERDECK_w_ldbottom = 2.44   
                LOWERDECK_w_ldtop = 2.54
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD6':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.16
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD8':
                LOWERDECK_w_ldbottom = 2.44   
                LOWERDECK_w_ldtop = 3.28
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD9':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 3.28
                LOWERDECK_h_ld = 1.68
    else:
        if container_type is  'None':
                LOWERDECK_w_ldtop = 0
                LOWERDECK_w_ldbottom = 0  
                LOWERDECK_h_ld = 0  
        elif container_type is  'LD1':
                LOWERDECK_w_ldbottom = 3.22   
                LOWERDECK_w_ldtop = 4.77
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD11':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 3.28
                LOWERDECK_h_ld = 1.68   
        elif container_type is  'LD2':
                LOWERDECK_w_ldbottom = 2.49   
                LOWERDECK_w_ldtop = 3.22
                LOWERDECK_h_ld = 1.68  
        elif container_type is  'LD26':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.16
                LOWERDECK_h_ld = 1.68 
        elif container_type is  'LD29':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.82
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD3':
                LOWERDECK_w_ldbottom = 3.22   
                LOWERDECK_w_ldtop = 4.11
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD3-45':
                LOWERDECK_w_ldbottom = 3.22   
                LOWERDECK_w_ldtop = 4.11
                LOWERDECK_h_ld = 1.19
        elif container_type is  'LD3-45R':
                LOWERDECK_w_ldbottom = 1.56   
                LOWERDECK_w_ldtop = 1.66
                LOWERDECK_h_ld = 1.19
        elif container_type is  'LD3-45W':
                LOWERDECK_w_ldbottom = 1.43   
                LOWERDECK_w_ldtop = 2.53
                LOWERDECK_h_ld = 1.14
        elif container_type is  'LD39':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.82
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD4':
                LOWERDECK_w_ldbottom = 2.44   
                LOWERDECK_w_ldtop = 2.54
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD6':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 4.16
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD8':
                LOWERDECK_w_ldbottom = 2.44   
                LOWERDECK_w_ldtop = 3.28
                LOWERDECK_h_ld = 1.68
        elif container_type is  'LD9':
                LOWERDECK_w_ldbottom = 3.18   
                LOWERDECK_w_ldtop = 3.28
                LOWERDECK_h_ld = 1.68





    if NCorr ==  1:
            NSeat = max(NSeat,2) # menor numero de fileiras eh 3
            NSeat = min(NSeat,6) # maior numero de fileiras eh 9
    elif NCorr ==  2:
            NSeat = max(NSeat,6) # menor numero de fileiras eh 3
            NSeat = min(NSeat,9) # maior numero de fileiras eh 9

    FUSELAGE_n_SA_YC = NSeat
    FUSELAGE_h_aisle = CabHeightm # (inch)
    FUSELAGE_n_aisles = NCorr



    if NCorr == 1:
            FUSELAGE_esq = math.ceil((FUSELAGE_n_SA_YC)/2) # seat abreasts at left
            FUSELAGE_dir = FUSELAGE_n_SA_YC - FUSELAGE_esq # seat abreasts at right
    else:
            if NSeat ==  6:
                    FUSELAGE_esq = 2
                    FUSELAGE_dir = 2
                    FUSELAGE_cen = 2
            elif NSeat == 7:
                    FUSELAGE_esq = 2
                    FUSELAGE_dir = 2
                    FUSELAGE_cen = 3
            elif NSeat ==  8:
                    FUSELAGE_esq = 3
                    FUSELAGE_dir = 3
                    FUSELAGE_cen = 2
            elif NSeat == 9:
                    FUSELAGE_esq = 3
                    FUSELAGE_dir = 3
                    FUSELAGE_cen = 3

                    
    SEAT_w_cushion_YC = SEATwid# [inch]
    FUSELAGE_w_aisle_YC = AisleWidth # [inch]
    SEAT_w_armrest_YC = 2*inch2m # [inch] Armrest width
    #SEAT_h_armrest_top = 22*inch2m # (inch) Armrest height position, top
    SEAT_h_armrest_top = armrest_top*inch2m
    #SEAT_h_armrest_bottom = 7*inch2m # (inch) Armrest height position, bottom
    SEAT_h_armrest_bottom = armrest_bot*inch2m
    #SEAT_Dy_cushion = 0.42 # (m)
    aux = ((SEAT_h_armrest_top-SEAT_h_armrest_bottom)-SEAT_t_cushion_YC)/2
    SEAT_Dy_cushion = aux + SEAT_h_armrest_bottom
    # Get the ratio of height/width
    height_witdh_ratio = widthreiratio
    # Initialize the variables
    delta_z_symetry_inf = -1
    delta_z_symetry_sup = 2
    n_points = 20
    seat_delta_width_floor = 0.025

    # Calculate the width coordinates for the various points
    w0 = 0.5*FUSELAGE_h_aisle * FUSELAGE_n_aisles
    w4 = FUSELAGE_n_SA_YC * SEAT_w_cushion_YC + FUSELAGE_n_aisles * FUSELAGE_w_aisle_YC + (FUSELAGE_n_SA_YC - FUSELAGE_n_aisles + 1) * SEAT_w_armrest_YC
    y_last_seat = 1 / 2 * (w4 - SEAT_w_cushion_YC - 2 * SEAT_w_armrest_YC)
    w1 = 2 * (y_last_seat)
    w2 = 2 * (PAX_d_hw + 0.084 + y_last_seat)
    w3 = 2 * (PAX_d_sw + PAX_w_shoulder / 2 + y_last_seat)
    w5 = w4
    w6 = w4 - 2 * seat_delta_width_floor - 2 * SEAT_w_armrest_YC
    w7 = LOWERDECK_w_ldtop
    w8 = LOWERDECK_w_ldtop
    w9 = LOWERDECK_w_ldbottom

    # ###########################################################################################################################################

    #Begin of optimization (only on height coordinates)
    while iterations > 0:

            iterations = iterations - 1
                    
            # Initialize the variables
            k = 0
            k_mini = n_points
            result_z_symetry_mini = 1000
            k_mini2 = n_points
            result_z_symetry_mini2 = 1000

            while k <= n_points:

            # Get a value for "delta_z_symetry" between "delta_z_symetry_inf" and "delta_z_symetry_sup"
            # Then calculate the results on the fuselage size, using this value
                    delta_z_symetry = k * (delta_z_symetry_sup - delta_z_symetry_inf) / n_points + delta_z_symetry_inf
                    h0 = FUSELAGE_h_aisle - delta_z_symetry
                    h1 = PAX_Dy_eye + SEAT_Dy_cushion - delta_z_symetry + 0.126 + PAX_d_hw
                    h2 = PAX_Dy_eye + SEAT_Dy_cushion - delta_z_symetry
                    h3 = PAX_Dy_midshoulder + SEAT_Dy_cushion - delta_z_symetry
                    h4 = SEAT_h_armrest_top - delta_z_symetry
                    h5 = SEAT_h_armrest_bottom - delta_z_symetry
                    h6 = -delta_z_symetry
                    h7 = -delta_z_symetry - floor_thickness
                    h8 = -delta_z_symetry - floor_thickness - LOWERDECK_h_ld + (LOWERDECK_w_ldtop - LOWERDECK_w_ldbottom) / 2
                    h9 = -delta_z_symetry - floor_thickness - LOWERDECK_h_ld
                    
                    
                    
            # Calculate the semi width of the ellipse describing the fuselage
                    a0 = np.sqrt((w0 / 2) ** 2 + h0 ** 2 / (height_witdh_ratio) ** 2)
                    a1 = np.sqrt((w1 / 2) ** 2 + h1 ** 2 / (height_witdh_ratio) ** 2)
                    a2 = np.sqrt((w2 / 2) ** 2 + h2 ** 2 / (height_witdh_ratio) ** 2)
                    a3 = np.sqrt(((w3 + 0.04) / 2) ** 2 + h3 ** 2 / (height_witdh_ratio) ** 2)
                    a4 = np.sqrt(((w4 + 0.04) / 2) ** 2 + h4 ** 2 / (height_witdh_ratio) ** 2)
                    a5 = np.sqrt((w5 / 2) ** 2 + h5 ** 2 / (height_witdh_ratio) ** 2)
                    a6 = np.sqrt((w6 / 2) ** 2 + h6 ** 2 / (height_witdh_ratio) ** 2)
                    a7 = np.sqrt((w7 / 2) ** 2 + h7 ** 2 / (height_witdh_ratio) ** 2)
                    a8 = np.sqrt((w8 / 2) ** 2 + h8 ** 2 / (height_witdh_ratio) ** 2)
                    a9 = np.sqrt((w9 / 2) ** 2 + h9 ** 2 / (height_witdh_ratio) ** 2)
                    
                    # Get the maximum value of these widths, so each point is inside the fuselage
                    arar=[a0,a1,a2,a3,a4,a5,a6,a7,a8,a9]
                    a_max = max(arar)
                    

                    
                    # If the current a_max is one of the 2 smallest, then it has to be stored
                    if a_max < result_z_symetry_mini:
                            k_mini2 = k_mini
                            result_z_symetry_mini2 = result_z_symetry_mini
                            k_mini = k
                            result_z_symetry_mini = a_max
                    elif a_max < result_z_symetry_mini2:
                            k_mini2 = k
                            result_z_symetry_mini2 = a_max
                            
            #Go to the next k
                    k = k + 1


            #  Uppdate the interval where delta_z_symetry has to be
            if k_mini < k_mini2:
                    if k_mini > 0 :
                            k = k_mini - 1
                    
                    delta_z_symetry_inf_new = k * (delta_z_symetry_sup - delta_z_symetry_inf) / n_points + delta_z_symetry_inf
                    if k_mini < n_points:
                            k = k_mini2 + 1
                    
                    delta_z_symetry_sup_new = k * (delta_z_symetry_sup - delta_z_symetry_inf) / n_points + delta_z_symetry_inf
            else:
                    if k_mini2 > 0:
                            k = k_mini2 - 1
                    
                    delta_z_symetry_inf_new = k * (delta_z_symetry_sup - delta_z_symetry_inf) / n_points + delta_z_symetry_inf

                    if k_mini < n_points:
                            k = k_mini + 1
                    
                    delta_z_symetry_sup_new = k * (delta_z_symetry_sup - delta_z_symetry_inf) / n_points + delta_z_symetry_inf
                    

            delta_z_symetry_inf = delta_z_symetry_inf_new
            delta_z_symetry_sup = delta_z_symetry_sup_new
            a_mini = result_z_symetry_mini

            # Update the fuselage equivalent diameter and fuselage and floor thicknesses
            fuselage_equivalent_diameter = 2 * a_mini * np.sqrt(height_witdh_ratio)
            fuselage_thickness = (0.084 + 0.045 * fuselage_equivalent_diameter) / 2
            floor_thickness = 0.035 * (fuselage_equivalent_diameter + fuselage_thickness)

    ###########################################################################################################################################


    # When the optimum value has been found, plot cross section

    # ###### UPDATE of floor and fuselage thicknesses ##########
    besta=[delta_z_symetry_inf,delta_z_symetry_sup]
    FUSELAGE_Dz_floor= min(besta)
    #FUSELAGE_t_floor = floor_thickness
    fuselage_outer_equivalent_diameter=fuselage_equivalent_diameter+2*fuselage_thickness

    print(' \n Fuselage equivalent inner diameter: #5.2f \n',fuselage_equivalent_diameter)
    print(' \n Fuselage equivalent outer diameter: #5.2f \n',fuselage_outer_equivalent_diameter)
    # seating rails
    # FUSELAGE_nrails_right = 2
    # FUSELAGE_nrails_left  = 2
    FUSELAGE_dseat_seat_rail = 0.20

    # Insert formulas for automatic calculation and display the cells as unmodifiable
    FUSELAGE_drails_right =(SEAT_w_armrest_YC*(FUSELAGE_dir-1)+SEAT_w_cushion_YC*FUSELAGE_dir-FUSELAGE_dseat_seat_rail*2)/(FUSELAGE_dir-1)
            
    #FUSELAGE_drails_middle =((FUSELAGE_nseats_middle_YC-1)*SEAT_w_armrest_YC+FUSELAGE_nseats_middle_YC*SEAT_w_cushion_YC-2*FUSELAGE_dseat_seat_rail)/(FUSELAGE_nrails_middle-1)
            
    FUSELAGE_drails_left = (SEAT_w_armrest_YC*(FUSELAGE_esq-1)+SEAT_w_cushion_YC*FUSELAGE_esq-FUSELAGE_dseat_seat_rail*2)/(FUSELAGE_esq-1)

    FUSELAGE_delta_yrails_right =(2-FUSELAGE_n_aisles)*FUSELAGE_w_aisle_YC/2+FUSELAGE_dseat_seat_rail

    FUSELAGE_delta_yrails_left =(2-FUSELAGE_n_aisles)*FUSELAGE_w_aisle_YC/2+FUSELAGE_dseat_seat_rail
            
    eixox=2*a_mini
    eixoy=eixox*height_witdh_ratio       
    eixoxe=eixox + 2*fuselage_thickness
    eixoye=eixoy + 2*fuselage_thickness

    return(eixoxe, eixoye,eixox,eixoy,fuselage_thickness,
    FUSELAGE_Dz_floor, a_mini, NSeat,h1)
